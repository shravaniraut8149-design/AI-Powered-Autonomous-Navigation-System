# Implementation and Extension Guide

## A* in this project
- `g(n)`: exact number of grid moves from start to node `n`.
- `h(n)`: Manhattan distance from `n` to the goal.
- `f(n) = g(n) + h(n)`: priority used by the min-heap.
- The planner records predecessors and reconstructs the path after reaching the goal.
- If the start or goal is blocked, or no route exists, it returns an empty path.

## Sensor abstraction
`observe_local_occupancy()` returns occupied cells inside a configurable square radius around the robot. This is deliberately labelled a simulated sensor abstraction. It does not infer objects from pixels and does not replace camera/lidar perception.

## Dynamic obstacle handling
The controller adds one obstacle to a future route cell during the demo. It then plans from the current cell to the goal on the updated map. If no route exists, the controller stops rather than moving into an obstacle.

## Add camera perception later
1. Add OpenCV to `requirements.txt`.
2. Create a separate `camera_perception.py` module to acquire frames and expose detections as obstacle candidates.
3. Define a mapping step from detections to a grid/coordinate system.
4. Keep A* independent of OpenCV so it can be tested without a camera.
5. Record camera source, confidence thresholds, calibration, and failure behavior in the report.

## Replace the grid world with a simulator
A simulator adapter should provide the planner with an occupancy map or free/occupied query, current pose, goal pose, and safe movement commands. Webots, Gazebo/ROS 2, and CARLA require separate installation and adapter work; they are not included as runtime dependencies here.
