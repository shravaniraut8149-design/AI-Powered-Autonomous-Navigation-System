"""Lightweight local web dashboard for the autonomous navigation simulator."""
from __future__ import annotations
import json
import logging
import sys
from pathlib import Path
from threading import Lock

from flask import Flask, jsonify, render_template, send_from_directory

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from navigation_sim.world import build_demo_world, DEMO_START, DEMO_GOAL, DYNAMIC_EVENT_STEP
from navigation_sim.sensors import observe_local_occupancy
from navigation_sim.planner import astar, validate_path
from navigation_sim.controller import run_navigation
from navigation_sim.visualization import save_visualizations
from navigation_sim.metrics import save_metrics

app = Flask(__name__)
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
run_lock = Lock()


def execute_simulation(dynamic_obstacle: bool = True) -> dict:
    """Run the existing simulation and persist its standard outputs."""
    with run_lock:
        grid = build_demo_world()
        observe_local_occupancy(grid, DEMO_START, radius=5)
        initial_path, planner_stats = astar(grid, DEMO_START, DEMO_GOAL)
        if not initial_path:
            raise RuntimeError("No route was found. Please check the simulation map.")
        if not validate_path(grid, initial_path, DEMO_START, DEMO_GOAL):
            raise RuntimeError("The planner returned an invalid route.")

        logger = logging.getLogger("navigation")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        handler = logging.FileHandler(OUTPUT_DIR / "run.log", mode="w", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(handler)
        result = run_navigation(
            grid=grid,
            start=DEMO_START,
            goal=DEMO_GOAL,
            initial_path=initial_path,
            dynamic_event_step=DYNAMIC_EVENT_STEP if dynamic_obstacle else grid.size * 4,
            planning_time_ms=planner_stats["planning_time_ms"],
        )
        save_visualizations(grid, result, OUTPUT_DIR)
        save_metrics(result, planner_stats, OUTPUT_DIR)
        logger.removeHandler(handler)
        handler.close()
        return json.loads((OUTPUT_DIR / "simulation_metrics.json").read_text(encoding="utf-8"))


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/run")
def run_simulation():
    from flask import request
    payload = request.get_json(silent=True) or {}
    dynamic_obstacle = bool(payload.get("dynamic_obstacle", True))
    try:
        metrics = execute_simulation(dynamic_obstacle)
        return jsonify({"ok": True, "metrics": metrics, "images": {
            "map": "/outputs/navigation_map.png",
            "progress": "/outputs/navigation_progress.png",
        }})
    except Exception as exc:  # return a friendly UI error; details remain in server console
        app.logger.exception("Simulation failed")
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.get("/api/status")
def status():
    metrics_path = OUTPUT_DIR / "simulation_metrics.json"
    if not metrics_path.exists():
        return jsonify({"ready": False})
    try:
        return jsonify({"ready": True, "metrics": json.loads(metrics_path.read_text(encoding="utf-8"))})
    except (OSError, json.JSONDecodeError):
        return jsonify({"ready": False})


@app.get("/outputs/<path:filename>")
def output_file(filename: str):
    allowed = {"navigation_map.png", "navigation_progress.png", "navigation_trace.csv", "simulation_metrics.json", "run.log"}
    if filename not in allowed:
        return jsonify({"error": "File not available."}), 404
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=filename.endswith((".csv", ".json", ".log")))


if __name__ == "__main__":
    print("\nAI-Based Autonomous Navigation Dashboard")
    print("Open http://127.0.0.1:5000 in your browser.")
    print("Local-only demo; no login required. Press Ctrl+C to stop.\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
