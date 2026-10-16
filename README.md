# AI-Based Autonomous Navigation System

An educational, browser-based virtual navigation prototype inspired by the supplied project brief. It demonstrates grid-based obstacle representation, A* path planning, route visualization, and virtual agent animation without physical robot hardware.

## Features
- Interactive 20 × 14 grid map with editable obstacles
- Warehouse maze, narrow corridor, open field, and random obstacle presets
- A* path planner using Manhattan-distance heuristic
- Route animation and mission telemetry
- Ten-phase project workflow and architecture documentation
- Responsive dashboard UI; runs locally without a build step

## Tech stack
- HTML5, CSS3, vanilla JavaScript, Canvas API
- A* graph search, grid-world simulation
- No package installation required for the website

> **Scope note:** This is a virtual grid simulation. It does not currently implement a trained YOLO model, camera/lane detection, ROS, physical GPIO, ultrasonic sensing, or real vehicle control. These are possible future extensions from the project brief.

## Run locally
1. Extract the ZIP file.
2. Open the `AI-Based-Autonomous-Navigation-System` folder in VS Code.
3. Open `index.html` in a browser, or use the VS Code **Live Server** extension and choose **Open with Live Server**.
4. Scroll to **Test the navigation brain**.
5. Choose a preset and click **Find optimal path**.
6. Click **Animate navigation**. Click free grid cells to add/remove obstacles and re-plan.

No terminal command is required for the static website. Optional Python local server:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Architecture
`Environment input → World representation → A* path planner → Navigation output`

- **Environment input:** preset grid, start, goal, and user-edited obstacles.
- **World representation:** each blocked cell is treated as an obstacle.
- **Planner:** A* prioritizes nodes by `f(n) = g(n) + h(n)`, where `g` is route cost and `h` is Manhattan distance.
- **Navigation output:** the found path is drawn and the agent is animated over it.
- **Telemetry:** path length, explored cells, distance to goal, and mission state.

## Folder structure
```text
AI-Based-Autonomous-Navigation-System/
├── index.html       # Page sections and simulator controls
├── style.css        # Responsive visual design
├── script.js        # Grid world, A* planner, rendering and animation
├── README.md        # Setup and project overview
└── REPORT.md        # Project report and step-by-step work record
```

## Step-by-step workflow
1. Environment setup — use VS Code and a modern browser.
2. Project structure — keep markup, styling, and behavior separate.
3. Virtual simulation — create the grid, start, goal, and obstacles.
4. Perception concept — use blocked cells as simplified known environmental input.
5. Path planning — run A* to search for a route around obstacles.
6. Navigation — animate the virtual agent along the planned path.
7. Visualization — monitor path length, explored cells, and mission state.
8. Testing — test each preset, edit obstacles, and test a blocked route.
9. GitHub publishing — commit source and evidence.
10. Presentation — explain the algorithm and be transparent about simulation limits.

## Suggested tests
- Plan a route in each preset.
- Add an obstacle on the route, then re-plan.
- Add a barrier across a narrow passage and verify a no-path result if all routes are blocked.
- Verify the agent ends at the goal and the distance metric reaches zero.

## Screenshots and demo
Save your own captured evidence in `docs/screenshots/`:
- `01-home-dashboard.png`
- `02-warehouse-map.png`
- `03-planned-route.png`
- `04-agent-arrived.png`
- `05-no-path-test.png`
- `06-github-repository.png`

Record a 30–60 second screen capture showing preset selection, path planning, and animation. Only include screenshots of actual local runs.

## GitHub publishing
Create a repository named `AI-Based-Autonomous-Navigation-System`, then run in this folder:

```bash
git init
git add .
git commit -m "Build autonomous navigation simulation website"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AI-Based-Autonomous-Navigation-System.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Future commit examples:
- `Add interactive grid simulation`
- `Implement A-star path planner`
- `Add navigation telemetry and animation`
- `Document testing and project limitations`

Suggested GitHub topics: `robotics`, `autonomous-navigation`, `astar`, `path-planning`, `simulation`, `javascript`, `student-project`.

## Future improvements
- OpenCV camera input and lane detection
- YOLO object detection using a compatible pretrained model
- Sensor model for simulated distance measurements
- ROS integration and Gazebo/Webots simulation
- CARLA integration for autonomous driving scenarios
- SLAM, dynamic obstacles, multiple agents, and real hardware testing

## Resume description
Developed a browser-based autonomous navigation prototype using A* path planning in a virtual grid environment; implemented obstacle editing, route visualization, agent animation, and mission telemetry. Documented a roadmap for perception and robotics integration.

## Safety and honesty
This prototype is for learning and portfolio demonstration only. It is not validated for real-world driving or safety-critical robotic use. Do not connect it to motors or a vehicle without appropriate engineering, hardware safeguards, and testing.
