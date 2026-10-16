"""A* path planner for a four-connected occupancy grid."""
from __future__ import annotations
import heapq
import time
from typing import Iterable
import numpy as np
Cell = tuple[int, int]


def manhattan(a: Cell, b: Cell) -> int:
    """Admissible heuristic for four-direction unit-cost movement."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(grid: np.ndarray, cell: Cell) -> Iterable[Cell]:
    rows, cols = grid.shape
    r, c = cell
    for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0:
            yield (nr, nc)


def astar(grid: np.ndarray, start: Cell, goal: Cell) -> tuple[list[Cell], dict]:
    """Return a shortest collision-free path and basic planner metrics.

    Returns an empty path if start/goal is invalid or no route exists.
    """
    started = time.perf_counter()
    rows, cols = grid.shape
    for cell in (start, goal):
        if not (0 <= cell[0] < rows and 0 <= cell[1] < cols) or grid[cell] != 0:
            return [], {"planning_time_ms": (time.perf_counter() - started) * 1000, "expanded_nodes": 0}
    frontier: list[tuple[int, int, Cell]] = [(manhattan(start, goal), 0, start)]
    came_from: dict[Cell, Cell | None] = {start: None}
    cost: dict[Cell, int] = {start: 0}
    expanded = 0
    while frontier:
        _, g_score, current = heapq.heappop(frontier)
        if g_score != cost.get(current):
            continue
        expanded += 1
        if current == goal:
            path = []
            node: Cell | None = goal
            while node is not None:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return path, {"planning_time_ms": (time.perf_counter() - started) * 1000, "expanded_nodes": expanded}
        for nxt in neighbors(grid, current):
            candidate = cost[current] + 1
            if candidate < cost.get(nxt, 10**12):
                cost[nxt] = candidate
                came_from[nxt] = current
                heapq.heappush(frontier, (candidate + manhattan(nxt, goal), candidate, nxt))
    return [], {"planning_time_ms": (time.perf_counter() - started) * 1000, "expanded_nodes": expanded}


def validate_path(grid: np.ndarray, path: list[Cell], start: Cell, goal: Cell) -> bool:
    if not path or path[0] != start or path[-1] != goal:
        return False
    for cell in path:
        if not (0 <= cell[0] < grid.shape[0] and 0 <= cell[1] < grid.shape[1]) or grid[cell] != 0:
            return False
    return all(manhattan(a, b) == 1 for a, b in zip(path, path[1:]))
