# Viva, Resume, and Presentation Notes

## 60-second explanation for HR
I built a software simulation of a robot that navigates a map from a start point to a destination. The program represents obstacles in a grid, uses A* search to find a route, simulates nearby obstacle sensing, and replans if an obstacle appears in the route. It records the movement and creates plots and metrics so the result can be checked. It is a virtual prototype, not a physical robot.

## Technical explanation
The environment is an occupancy grid. A* uses `f(n)=g(n)+h(n)` with Manhattan distance because movement is restricted to four neighboring cells with unit cost. The controller follows the route one cell at a time and performs a safety check before each move. A deterministic dynamic obstacle event demonstrates replanning. Unit tests validate route adjacency, blocked-cell avoidance, unreachable targets, and safe completion.

## Resume bullet examples
- Built a modular Python occupancy-grid navigation simulation using A* path planning and Manhattan-distance heuristics.
- Implemented finite-range simulated obstacle sensing, waypoint following, dynamic obstacle insertion, and route replanning.
- Added automated unit tests and reproducible CSV/JSON/plot outputs to evaluate route validity and collision-free behavior.

## Interview questions and short answers
1. **What problem does the project solve?** It demonstrates how a robot can plan and follow a route around obstacles in a virtual map.
2. **Why A*?** It combines the cost already traveled with a heuristic estimate to prioritize promising nodes.
3. **What is the heuristic?** Manhattan distance, appropriate for four-connected unit-cost grid movement.
4. **What is an occupancy grid?** A discretized map in which each cell is represented as free or occupied.
5. **How are obstacles sensed?** In this version, a simulated finite-range sensor reads occupied cells near the current grid position.
6. **How does dynamic replanning work?** A new obstacle is inserted into the future route; the controller runs A* again from its current position.
7. **How do you prevent collisions?** The controller checks that the next cell is free before moving and stops if it cannot find a safe route.
8. **What are the limitations?** It does not include real camera perception, trained object detection, continuous vehicle dynamics, or hardware.
9. **How could it be improved?** Integrate OpenCV, lidar/camera data, ROS 2, or Webots/Gazebo after defining sensor and movement adapters.
10. **Why simulate?** It is repeatable, low-cost, and lets the planning algorithm be tested before hardware is available.

## LinkedIn project description
Built an educational AI-based autonomous navigation simulation in Python. The project includes occupancy-grid mapping, A* path planning, a finite-range simulated sensing abstraction, dynamic obstacle replanning, visualization, trace logging, and unit tests. The implementation is simulation-only and is designed as a foundation for future OpenCV/ROS integration.
