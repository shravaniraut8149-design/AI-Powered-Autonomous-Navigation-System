# AI-Based Autonomous Navigation System

> **A complete local web platform plus modular virtual robotics simulator** demonstrating occupancy-grid perception, A* path planning, simulated range sensing, safe waypoint following, dynamic obstacle handling, and reproducible evaluation — with a light-theme dashboard and no account/login required.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Simulation](https://img.shields.io/badge/Environment-2D%20simulation-purple) ![Planner](https://img.shields.io/badge/Planner-A*-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 1. Launch the visual dashboard (recommended)

The project includes a friendly, **light-theme** browser dashboard for non-technical users. It runs only on your computer, requires no login, and lets you run a simulation, enable/disable the dynamic obstacle, review the route and metrics, and open/download result files.

### Windows PowerShell

From the extracted project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python web_app.py
```

Keep that PowerShell window open and visit **http://127.0.0.1:5000** in your browser. Click **Run simulation**. To stop the server, return to PowerShell and press `Ctrl+C`.

**Easier option:** on Windows, double-click `start_dashboard.bat`. It creates the virtual environment if needed, installs missing dependencies, opens the browser, and starts the server. Keep the launcher window open while using the dashboard.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python web_app.py
```

Open `http://127.0.0.1:5000`. The server binds to `127.0.0.1` (loopback), not your public network interface. Do not change the host to `0.0.0.0` unless you deliberately intend to expose it to your local network.

### Dashboard features

- Run the simulation with a single click.
- Toggle the dynamic obstacle scenario to compare route replanning with a static run.
- Review goal status, movement steps, replans, and collision status.
- View the generated navigation map and download CSV, JSON, and log outputs.
- No login, cloud service, GPU, camera, or physical robot required.

For more details, see [`docs/WEB_DASHBOARD_GUIDE.md`](docs/WEB_DASHBOARD_GUIDE.md).

## 2. Project overview

An autonomous navigation system must perceive its environment, represent obstacles, choose a collision-free route, and control an agent toward a goal. This project demonstrates those responsibilities in a deterministic 2D grid-world simulation.

**What it does:**
- Builds a map with free cells and blocked obstacle cells.
- Simulates a range sensor with a finite sensing radius around the robot.
- Uses A* with an admissible Manhattan-distance heuristic to plan a route.
- Follows waypoints while checking the next move for safety.
- Demonstrates a dynamic obstacle event and replans when a route becomes blocked.
- Saves map/path figures, a robot trace CSV, metrics JSON, and a run log.
- Includes automated tests for path planning, collision safety, and output generation.

**Scope and honesty:** This is a virtual grid-world proof of concept, not a physical robot, camera-based lane detector, trained deep-learning detector, or road-ready autonomous vehicle. Obstacles are represented by map cells; range sensing is simulated. The modular interfaces are suitable for future OpenCV, YOLO, ROS, Webots, or CARLA integration.

## 3. Problem statement and industry relevance

Robots and autonomous vehicles need to move from a start location to a destination while avoiding obstacles. The same high-level problem appears in warehouse AMRs, delivery robots, drones, industrial material handling, and vehicle simulation. This project makes the core planning loop observable and testable without hardware costs.

### Simple workflow

1. **Perception / map input:** read a grid containing free and occupied cells.
2. **Sensor simulation:** reveal nearby occupied cells within a finite radius.
3. **Planning:** A* searches for a low-cost route from start to goal.
4. **Navigation:** the robot advances one grid cell at a time along waypoints.
5. **Safety:** occupied cells are never entered; if a new obstacle blocks the route, the robot replans.
6. **Evaluation:** save the route, movement trace, path length, planning time, replan count, and collision status.

## 4. Tech stack options

| Level | Stack | GPU | Outcome |
|---|---|---:|---|
| A — Beginner (selected) | Python, NumPy, Matplotlib, custom 2D grid | No | Reproducible planning and navigation demo |
| B — Intermediate | OpenCV camera processing + a simulator such as Webots/Gazebo | Usually no for basic CV | Image/sensor integration and richer robot dynamics |
| C — Advanced | ROS 2 + Gazebo/Webots or CARLA + PyTorch/YOLO/SLAM | Depends on models | Multi-sensor robotics or vehicle simulation |

The beginner option is selected because it runs on a typical laptop, avoids large model downloads, and provides testable core navigation behavior quickly.

## 5. Architecture

```text
Scenario configuration
        │
        ▼
Grid world / occupancy map ──► Simulated range sensor
        │                              │
        └──────────────┬───────────────┘
                       ▼
              A* global path planner
                       │
                       ▼
            Waypoint navigation controller
                       │
             safety check / replan event
                       │
                       ▼
              Robot pose + trace logger
                       │
                       ▼
          plots + CSV + metrics JSON + log
```

| Module | Responsibility |
|---|---|
| `src/navigation_sim/world.py` | Grid map, deterministic scenario, obstacle placement |
| `src/navigation_sim/planner.py` | A* search and path validation |
| `src/navigation_sim/sensors.py` | Simulated finite-range occupancy observation |
| `src/navigation_sim/controller.py` | Waypoint following, safety checks, replanning |
| `src/navigation_sim/visualization.py` | Map/path and progress visualizations |
| `src/navigation_sim/metrics.py` | Metrics, trace CSV, JSON report |
| `main.py` | Orchestrates one full terminal simulation run |
| `web_app.py` | Local Flask server and simulation API for the dashboard |
| `start_dashboard.bat` | Windows one-click setup and dashboard launcher |
| `templates/index.html` | Dashboard structure and accessible controls |
| `static/styles.css` | Responsive light-theme UI styling |
| `static/app.js` | Dashboard actions, metrics, and output refresh |

## 6. Requirements

- Windows 10/11, macOS, or Linux
- Python **3.10 or newer** (Python 3.11/3.12 recommended; Python 3.13 should also work with compatible wheels)
- Internet connection only for initial package installation
- Flask (installed automatically from `requirements.txt`) for the localhost dashboard
- No GPU, VS Code, login, camera, or robot hardware required

## 7. Install and run

### Windows PowerShell

Open PowerShell in the extracted project folder (the folder containing `main.py`):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, use the environment's interpreter directly instead:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

If `py` is not recognized, install Python from python.org and enable **Add Python to PATH**, then reopen PowerShell.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

### Expected terminal output

Exact timing varies by machine. A successful run prints a summary similar to:

```text
AI-BASED AUTONOMOUS NAVIGATION — SIMULATION COMPLETE
Scenario: demo_dynamic_obstacle
Grid: 30 columns x 22 rows
Path found: True
Dynamic obstacle introduced: True
Replans: 1
Movement steps: 46
Collision detected: False
Outputs: outputs/navigation_map.png, outputs/navigation_progress.png,
         outputs/navigation_trace.csv, outputs/simulation_metrics.json
```

The program exits normally after writing output files. Open the PNG files from `outputs/` with File Explorer.

## 7. Test the project

With the virtual environment activated:

```powershell
python -m unittest discover -s tests -v
```

A successful test run ends with `OK`. Tests cover route validity, blocked-cell avoidance, unreachable goals, and core simulation safety.

## 8. Output files

| File | Description |
|---|---|
| `outputs/navigation_map.png` | Occupancy map, start/goal, planned route, and obstacles |
| `outputs/navigation_progress.png` | Robot's visited trajectory and key event annotations |
| `outputs/navigation_trace.csv` | One row per movement step, including position and sensor observations |
| `outputs/simulation_metrics.json` | Machine-readable run summary and safety metrics |
| `outputs/run.log` | Human-readable run log |

The `outputs/` directory is created automatically. Existing files with the same names are replaced on each run.

## 9. Configure the scenario

The default scenario is in `src/navigation_sim/world.py`. You can change the grid dimensions, start, goal, obstacle blocks, sensor radius, and dynamic obstacle event there. Keep start and goal on free cells. If the goal is enclosed or no route exists, the planner reports failure rather than fabricating a path.

## 10. Virtual simulation workflow

1. Create the occupancy grid and static obstacles.
2. Place the virtual robot at the start and define the goal.
3. Simulate a local range sensor observation around the robot.
4. Compute a route with A*.
5. Move along route waypoints, checking every next cell.
6. Inject a dynamic obstacle during the demonstration.
7. If the obstacle blocks the remaining route, plan again from the current pose.
8. Record trace, safety state, and planning metrics.
9. Inspect the generated visualizations and JSON/CSV outputs.

## 11. GitHub publishing

1. Create a repository named `AI-Based-Autonomous-Navigation-System`.
2. Add a concise description: `A Python 2D robotics simulation demonstrating A* path planning, simulated range sensing, dynamic obstacle avoidance, replanning, and evaluation.`
3. From the project directory:

```bash
git init
git add README.md requirements.txt .gitignore main.py src tests docs outputs
git commit -m "Build autonomous navigation grid simulation"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AI-Based-Autonomous-Navigation-System.git
git push -u origin main
```

Replace `YOUR-USERNAME` with the GitHub username. If Git reports that `origin` already exists, use `git remote set-url origin <repository-url>`.

Suggested topics: `robotics`, `autonomous-navigation`, `path-planning`, `a-star`, `python`, `simulation`, `obstacle-avoidance`.

### Evidence to capture

Store genuine screenshots in `docs/screenshots/`:
- `01-terminal-success.png` — successful `python main.py` output
- `02-navigation-map.png` — `navigation_map.png`
- `03-navigation-progress.png` — `navigation_progress.png`
- `04-test-results.png` — unit test results
- `05-repository-readme.png` — repository README page

Optionally record a short screen video showing the run and opening both plots. Do not claim that screenshots are camera perception or physical robot tests.

## 12. Results and interpretation

The JSON report includes whether the route was found, path length, movement steps, replan count, planning duration, and collision status. A collision-free run means the simulated agent did not enter a blocked grid cell. It does not prove real-world safety, sensor accuracy, or vehicle readiness.

## 13. Resume and interview notes

Use only statements that match the implementation and outputs you personally verified. Example bullets:
- Implemented a modular Python grid-world navigation simulator with A* path planning and an admissible Manhattan heuristic.
- Added simulated finite-range obstacle sensing, dynamic obstacle injection, safe waypoint following, and route replanning.
- Produced reproducible navigation traces, metrics JSON, visual reports, and unit tests for route validity and collision avoidance.

Be ready to explain A*'s `f(n) = g(n) + h(n)`, why Manhattan distance fits four-direction grid movement, how dynamic obstacles trigger replanning, and the difference between simulated occupancy and real camera-based object detection.

## 14. Future improvements

- Add OpenCV camera input and lane/path feature extraction.
- Integrate a pre-trained YOLO detector for object classes (requires model weights and suitable compute).
- Replace the custom grid world with Webots, Gazebo/ROS 2, or CARLA.
- Add robot kinematics, velocity/turn-rate control, and realistic sensor noise.
- Explore SLAM, occupancy-grid mapping, Dijkstra comparisons, multi-agent coordination, or reinforcement learning.
- Add a web dashboard or a recorded animation after the core algorithm is validated.
- Deploy on Raspberry Pi/Jetson only after adding hardware-specific safety interlocks and testing.

## 15. Troubleshooting

| Problem | Likely cause | Fix |
|---|---|---|
| `py` not recognized | Python launcher missing | Install Python and enable PATH, or use `python`/`python3` |
| `ModuleNotFoundError: numpy` | Wrong environment or packages not installed | Activate `.venv`, then `python -m pip install -r requirements.txt` |
| `python main.py` says file not found | PowerShell is in the wrong folder | `cd` to the extracted folder containing `main.py` |
| Plot files not found | Run stopped early or wrong working directory | Check terminal output; rerun from project root |
| No path found | Goal blocked or map disconnected | Review obstacle/start/goal definitions in `world.py` |
| Test discovery finds zero tests | Wrong command or folder | Run `python -m unittest discover -s tests -v` from project root |
| Git push rejected | Remote contains an initial commit or URL is wrong | Check remote with `git remote -v`; reconcile remote history before pushing |

## 16. Limitations and safety

This educational simulator uses a discrete grid and deterministic simulated sensing. It does not contain trained object detection, real-time camera perception, lane detection, physical robot control, or validated vehicle dynamics. Never connect this software directly to motors without a separate hardware driver, emergency stop, fail-safe behavior, and controlled testing.

## 17. License and attribution

MIT License. See `LICENSE`. The project is intended for education and portfolio demonstration.
