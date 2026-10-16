"""Unit tests for planner and navigation safety."""
import sys, unittest
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from navigation_sim.planner import astar, validate_path
from navigation_sim.world import build_demo_world, DEMO_START, DEMO_GOAL
from navigation_sim.controller import run_navigation

class PlannerTests(unittest.TestCase):
    def test_astar_returns_valid_route(self):
        grid = build_demo_world()
        path, stats = astar(grid, DEMO_START, DEMO_GOAL)
        self.assertTrue(validate_path(grid, path, DEMO_START, DEMO_GOAL))
        self.assertGreater(stats["expanded_nodes"], 0)

    def test_unreachable_goal_returns_empty_path(self):
        grid = np.zeros((5, 5), dtype=np.uint8)
        grid[:, 2] = 1
        path, _ = astar(grid, (2, 0), (2, 4))
        self.assertEqual(path, [])

    def test_blocked_start_is_rejected(self):
        grid = np.zeros((3, 3), dtype=np.uint8)
        grid[0, 0] = 1
        path, _ = astar(grid, (0, 0), (2, 2))
        self.assertEqual(path, [])

    def test_simulation_reaches_goal_without_collision(self):
        grid = build_demo_world()
        path, stats = astar(grid, DEMO_START, DEMO_GOAL)
        result = run_navigation(grid, DEMO_START, DEMO_GOAL, path, dynamic_event_step=18, planning_time_ms=stats["planning_time_ms"])
        self.assertTrue(result["path_found"])
        self.assertFalse(result["collision_detected"])
        for cell in result["visited"]:
            self.assertEqual(result["grid_final"][cell], 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
