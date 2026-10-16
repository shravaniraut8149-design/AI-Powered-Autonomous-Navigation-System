"""Persist simulation trace and metrics in portable formats."""
from __future__ import annotations
import csv, json
from pathlib import Path
from datetime import datetime, timezone


def save_metrics(result: dict, planner_stats: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "navigation_trace.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["step", "row", "col", "event", "sensor_occupied_count"])
        writer.writeheader(); writer.writerows(result["trace"])
    metrics = {
        "scenario": "demo_dynamic_obstacle",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "grid_rows": int(result["grid_final"].shape[0]),
        "grid_columns": int(result["grid_final"].shape[1]),
        "start": list(result["start"]),
        "goal": list(result["goal"]),
        "goal_reached": bool(result["path_found"]),
        "dynamic_obstacle_introduced": bool(result["dynamic_obstacle_introduced"]),
        "replans": int(result["replans"]),
        "collision_detected": bool(result["collision_detected"]),
        "movement_steps": int(result["movement_steps"]),
        "final_planned_path_length_cells": int(result["path_length_cells"]),
        "planning_time_ms_total": round(float(result["planning_time_ms"]), 3),
        "initial_expanded_nodes": int(planner_stats.get("expanded_nodes", 0)),
        "sensor_model": "simulated finite-range occupancy observation",
        "perception_scope": "grid occupancy only; no camera or trained object detector",
    }
    (output_dir / "simulation_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
