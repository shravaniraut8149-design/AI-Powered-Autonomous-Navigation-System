"""Run the complete autonomous navigation simulation from the repository root."""
from __future__ import annotations
import logging
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from navigation_sim.world import build_demo_world, DEMO_START, DEMO_GOAL, DYNAMIC_EVENT_STEP
from navigation_sim.sensors import observe_local_occupancy
from navigation_sim.planner import astar, validate_path
from navigation_sim.controller import run_navigation
from navigation_sim.visualization import save_visualizations
from navigation_sim.metrics import save_metrics


def main() -> int:
    output_dir = ROOT / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler(output_dir / "run.log", mode="w", encoding="utf-8"), logging.StreamHandler()],
    )
    logger = logging.getLogger("navigation")
    grid = build_demo_world()
    local_map = observe_local_occupancy(grid, DEMO_START, radius=5)
    initial_path, initial_stats = astar(grid, DEMO_START, DEMO_GOAL)
    if not initial_path:
        logger.error("No initial route exists. Check the map configuration.")
        return 2
    if not validate_path(grid, initial_path, DEMO_START, DEMO_GOAL):
        logger.error("Planner returned an invalid path.")
        return 3

    result = run_navigation(
        grid=grid,
        start=DEMO_START,
        goal=DEMO_GOAL,
        initial_path=initial_path,
        dynamic_event_step=DYNAMIC_EVENT_STEP,
        planning_time_ms=initial_stats["planning_time_ms"],
    )
    save_visualizations(grid, result, output_dir)
    save_metrics(result, initial_stats, output_dir)

    print("\nAI-BASED AUTONOMOUS NAVIGATION — SIMULATION COMPLETE")
    print("Scenario: demo_dynamic_obstacle")
    print(f"Grid: {grid.shape[1]} columns x {grid.shape[0]} rows")
    print(f"Start: {DEMO_START} | Goal: {DEMO_GOAL}")
    print(f"Path found: {result['path_found']}")
    print(f"Dynamic obstacle introduced: {result['dynamic_obstacle_introduced']}")
    print(f"Replans: {result['replans']}")
    print(f"Movement steps: {len(result['trace']) - 1}")
    print(f"Collision detected: {result['collision_detected']}")
    print("Outputs: outputs/navigation_map.png, outputs/navigation_progress.png,")
    print("         outputs/navigation_trace.csv, outputs/simulation_metrics.json, outputs/run.log")
    print("Scope: virtual grid simulation; no physical robot or camera-based detector is connected.")
    return 0 if result["path_found"] and not result["collision_detected"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
