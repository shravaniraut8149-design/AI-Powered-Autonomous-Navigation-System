"""Simulated finite-range occupancy sensing; not camera perception."""
from __future__ import annotations
import numpy as np
from .planner import Cell


def observe_local_occupancy(grid: np.ndarray, pose: Cell, radius: int = 5) -> dict:
    """Return occupied cells within a Chebyshev-radius window around pose."""
    r, c = pose
    observed = []
    for rr in range(max(0, r - radius), min(grid.shape[0], r + radius + 1)):
        for cc in range(max(0, c - radius), min(grid.shape[1], c + radius + 1)):
            if grid[rr, cc] == 1 and max(abs(rr - r), abs(cc - c)) <= radius:
                observed.append((rr, cc))
    return {"pose": pose, "radius_cells": radius, "occupied_cells": observed, "occupied_count": len(observed)}
