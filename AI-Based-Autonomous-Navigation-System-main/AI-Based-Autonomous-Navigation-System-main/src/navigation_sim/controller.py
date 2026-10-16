"""Waypoint following with a dynamic obstacle event and safety-first replanning."""
from __future__ import annotations
import logging
import numpy as np
from .planner import astar, Cell
from .sensors import observe_local_occupancy


def run_navigation(grid: np.ndarray, start: Cell, goal: Cell, initial_path: list[Cell], dynamic_event_step: int = 18, planning_time_ms: float = 0.0) -> dict:
    logger = logging.getLogger("navigation")
    working = grid.copy()
    path = list(initial_path)
    pose = start
    trace = [{"step": 0, "row": pose[0], "col": pose[1], "event": "start", "sensor_occupied_count": observe_local_occupancy(working, pose)["occupied_count"]}]
    visited = [pose]
    dynamic_added = False
    collision = False
    replans = 0
    total_plan_ms = planning_time_ms
    step = 0
    # The event is placed on the current route ahead of the robot, but never on goal.
    max_iterations = working.size * 3
    while pose != goal and step < max_iterations:
        # Inject an obstacle on a future waypoint after enough movement has happened.
        if not dynamic_added and step >= dynamic_event_step and len(path) > 4:
            current_index_for_event = path.index(pose) if pose in path else 0
            future_index = min(current_index_for_event + 4, len(path) - 2)
            candidate = path[future_index]
            if candidate not in (pose, start, goal):
                working[candidate] = 1
                dynamic_added = True
                logger.info("Dynamic obstacle introduced at cell %s", candidate)
                # If it blocks the current route, replan from the current pose.
                if candidate in path[path.index(pose) + 1:]:
                    new_path, stats = astar(working, pose, goal)
                    total_plan_ms += stats["planning_time_ms"]
                    replans += 1
                    if not new_path:
                        logger.error("No route remains after dynamic obstacle event")
                        break
                    path = new_path
                    logger.info("Replanned around dynamic obstacle")
        # Replan whenever the immediate next waypoint is occupied.
        try:
            current_index = path.index(pose)
        except ValueError:
            new_path, stats = astar(working, pose, goal)
            total_plan_ms += stats["planning_time_ms"]
            replans += 1
            if not new_path:
                break
            path, current_index = new_path, 0
        if current_index + 1 >= len(path):
            break
        nxt = path[current_index + 1]
        if working[nxt] != 0:
            new_path, stats = astar(working, pose, goal)
            total_plan_ms += stats["planning_time_ms"]
            replans += 1
            if not new_path:
                break
            path = new_path
            nxt = path[1]
        if working[nxt] != 0:
            collision = True
            logger.error("Safety stop: next cell is occupied")
            break
        pose = nxt
        step += 1
        visited.append(pose)
        sensing = observe_local_occupancy(working, pose, radius=5)
        event = "dynamic_obstacle" if dynamic_added and step == dynamic_event_step else "move"
        trace.append({"step": step, "row": pose[0], "col": pose[1], "event": event, "sensor_occupied_count": sensing["occupied_count"]})
    reached = pose == goal
    return {
        "path_found": reached,
        "start": start,
        "goal": goal,
        "final_path": path,
        "visited": visited,
        "trace": trace,
        "grid_final": working,
        "dynamic_obstacle_introduced": dynamic_added,
        "replans": replans,
        "collision_detected": collision,
        "planning_time_ms": total_plan_ms,
        "path_length_cells": max(0, len(path) - 1),
        "movement_steps": max(0, len(visited) - 1),
    }
