# Project Report — AI-Based Autonomous Navigation System

## Abstract
This project implements a software-only proof of concept for autonomous navigation. A virtual agent moves through a two-dimensional occupancy grid from a start cell to a goal cell. A* finds a route using unit-cost four-direction movement and Manhattan distance. A finite-range simulated sensor reports nearby occupied cells. During navigation, a dynamic obstacle is injected and the controller replans to preserve collision-free movement. Outputs include plots, a trace CSV, metrics JSON, and a log.

## Objectives
1. Implement modular grid-world navigation without physical hardware.
2. Represent obstacles using an occupancy map.
3. Implement A* path planning with an admissible heuristic.
4. Demonstrate safe waypoint following and replanning after an obstacle event.
5. Evaluate behavior with reproducible outputs and automated tests.

## Methodology
The map is a 2D NumPy array where 0 indicates free space and 1 indicates occupied space. Neighbor expansion uses north, south, east, and west cells. A* prioritizes `f(n) = g(n) + h(n)` where `g(n)` is the known path cost and `h(n)` is Manhattan distance to the goal. Since each move costs one and only four-direction movement is allowed, this heuristic does not overestimate the remaining cost.

The controller advances one cell at a time. A simulated dynamic obstacle is added to a future route cell after a configured number of steps. The controller requests a new A* route from the current position. A final safety check prevents entry into occupied cells. The sensor module models a finite-range local occupancy observation; it does not perform image recognition.

## Results
Run `python main.py` to generate the current run's metrics. Report exact values from `outputs/simulation_metrics.json` rather than copying numbers from another run. Expected successful properties are `goal_reached: true` and `collision_detected: false`. Runtime values vary by machine.

## Limitations
- Discrete grid movement; no continuous kinematics or acceleration.
- Static occupancy plus one deterministic dynamic obstacle event.
- No real camera, trained YOLO model, lane detector, lidar, ultrasonic hardware, ROS, or physical motors.
- No statistical benchmark across maps; metrics are demonstration-level.

## Conclusion
The project demonstrates core robotics software concepts—environment representation, search-based planning, local sensing abstraction, navigation, safety checks, dynamic replanning, logging, visualization, and unit tests. A future iteration could integrate OpenCV or a robotics simulator behind the existing module interfaces.
