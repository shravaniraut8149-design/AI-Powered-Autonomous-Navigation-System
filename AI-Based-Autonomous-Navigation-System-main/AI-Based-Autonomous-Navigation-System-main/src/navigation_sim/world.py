"""World map and deterministic demo scenario."""
from __future__ import annotations
import numpy as np

# Grid coordinates are (row, column). A value of 1 denotes an occupied cell.
ROWS, COLS = 22, 30
DEMO_START = (1, 1)
DEMO_GOAL = (20, 28)
DYNAMIC_EVENT_STEP = 18


def build_demo_world() -> np.ndarray:
    """Create a reproducible map with walls and gaps for meaningful route planning."""
    grid = np.zeros((ROWS, COLS), dtype=np.uint8)
    # Vertical wall with two openings. Start and goal remain in free space.
    grid[2:18, 7] = 1
    grid[5:8, 7] = 0
    grid[14:17, 7] = 0
    grid[0:14, 14] = 1
    grid[3:6, 14] = 0
    grid[17:22, 14] = 1
    grid[17:22, 14] = 0
    grid[3:20, 21] = 1
    grid[9:12, 21] = 0
    # Small obstacle clusters create local detours without enclosing the goal.
    grid[3:5, 3:5] = 1
    grid[10:12, 10:13] = 1
    grid[3:6, 25:27] = 1
    grid[16:18, 24:27] = 1
    grid[DEMO_START] = 0
    grid[DEMO_GOAL] = 0
    return grid
