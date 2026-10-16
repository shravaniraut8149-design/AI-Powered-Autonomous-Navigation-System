# GitHub Proof-Building Plan

Use this as an honest staged development log; do not backdate commits or claim that stages were completed on days when they were not.

| Stage | Work to commit | Example commit | Evidence |
|---|---|---|---|
| 1. Project skeleton | Requirements, ignore file, package layout | `chore: create project structure` | Folder tree screenshot |
| 2. World map | Grid map and scenario | `feat: add deterministic occupancy grid` | Map screenshot |
| 3. A* planner | Search and path validation | `feat: implement A-star path planning` | Route plot and tests |
| 4. Sensing abstraction | Finite-range occupancy observations | `feat: simulate local obstacle sensing` | Trace sample |
| 5. Controller | Waypoint movement and dynamic replanning | `feat: replan around dynamic obstacle` | Successful run screenshot |
| 6. Evaluation | CSV, JSON, plots, tests | `test: verify collision-free navigation` | Test output and metrics |
| 7. Documentation | README and report | `docs: document setup and limitations` | README preview |

## Git setup commands
```bash
git init
git add .
git commit -m "Build autonomous navigation simulation"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/AI-Based-Autonomous-Navigation-System.git
git push -u origin main
```

## Assets checklist
- Terminal run: `01-terminal-success.png`
- Occupancy map/path: `02-navigation-map.png`
- Progress plot: `03-navigation-progress.png`
- Unit tests: `04-test-results.png`
- GitHub README: `05-repository-readme.png`

Put screenshots under `docs/screenshots/`. Capture them yourself after running the project; no screenshots are fabricated or included by default.
