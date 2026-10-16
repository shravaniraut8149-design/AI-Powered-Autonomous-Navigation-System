# Web Dashboard Guide

## Overview

`web_app.py` adds a browser-based, light-theme user interface around the existing autonomous-navigation simulation. It does not replace `main.py`; both entry points use the same planning/controller modules and write to the same `outputs/` directory.

## Start on Windows

### Easiest: double-click the launcher

Double-click `start_dashboard.bat` in File Explorer. It creates `.venv` if needed, checks/installs dependencies, opens your browser, and starts the dashboard. Keep its terminal window open. Press `Ctrl+C` in that window to stop. The first launch requires internet access to install Python packages.

### Manual PowerShell method

1. Open PowerShell.
2. Change to the extracted folder containing `web_app.py`:
   ```powershell
   cd "$HOME\Desktop\Navi\AI-Autonomous-Navigation-System"
   ```
3. Create and activate the environment if not already done:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Install packages:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Start the dashboard:
   ```powershell
   python web_app.py
   ```
6. Open `http://127.0.0.1:5000` in Edge, Chrome, or another browser.
7. Click **Run simulation**. Leave the PowerShell window running while using the dashboard.
8. Press `Ctrl+C` in PowerShell when finished.

If PowerShell activation is blocked, run the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe web_app.py
```

## Dashboard controls

- **Run simulation:** executes the selected scenario and refreshes metrics and the navigation map.
- **Introduce a new obstacle:** checked by default. A dynamic obstacle is added during navigation and the controller replans. Uncheck it to run the static scenario without the injected event.
- **View results:** scrolls to the results panel.
- **Run outputs:** opens the PNG visualizations and downloads CSV movement trace, JSON metrics, and the execution log.

## Metrics

- **Goal status:** whether the simulated agent reached the configured destination.
- **Movement steps:** number of cell-to-cell moves made by the agent.
- **Route replans:** number of times the planner calculated a new route.
- **Collision status:** whether the simulation detected an attempted move into an occupied cell.

## Output files

The dashboard writes the same files as the command-line application:

- `outputs/navigation_map.png`
- `outputs/navigation_progress.png`
- `outputs/navigation_trace.csv`
- `outputs/simulation_metrics.json`
- `outputs/run.log`

Running the dashboard or terminal pipeline again replaces the previous run's output files. Copy any run you want to preserve before starting another run.

## Troubleshooting

### Browser says it cannot connect

Confirm that `python web_app.py` is still running and displays `http://127.0.0.1:5000`. Use that exact URL. If the port is occupied, close the other local application using port 5000 before retrying.

### `ModuleNotFoundError: No module named 'flask'`

Activate `.venv` and run `pip install -r requirements.txt` again. Confirm the prompt begins with `(.venv)`.

### Dashboard loads but the map is blank

Click **Run simulation** and wait for the success message. If an error appears, check the PowerShell window and `outputs/run.log`. Refresh the page after a successful run.

### Port 5000 is already in use

Stop the other process using that port, then restart the app. The default port is intentionally fixed so the README URL stays simple.

## Local-only and scope notes

The server binds to `127.0.0.1`, does not include accounts or login, and is intended for a single user on their own computer. Do not expose it to a public network. This remains a grid-world simulation: no real camera, YOLO detector, physical sensor, motor driver, or robot is connected.
