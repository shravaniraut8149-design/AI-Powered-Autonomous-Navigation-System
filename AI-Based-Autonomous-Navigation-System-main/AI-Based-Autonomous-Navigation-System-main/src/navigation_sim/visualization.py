"""Create presentation-ready visual summaries of a simulation run."""
from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def save_visualizations(original_grid: np.ndarray, result: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    cmap = ListedColormap(["#f4f7fb", "#273449"])
    path = result["final_path"]
    fig, ax = plt.subplots(figsize=(12, 7), dpi=150)
    ax.imshow(result["grid_final"], cmap=cmap, vmin=0, vmax=1, origin="upper")
    if path:
        ax.plot([c for r, c in path], [r for r, c in path], color="#1b9e77", linewidth=2.5, label="A* route")
    visited = result["visited"]
    if visited:
        ax.plot([c for r, c in visited], [r for r, c in visited], color="#377eb8", linewidth=1.6, linestyle="--", label="Robot trajectory")
    sr, sc = result["start"]
    gr, gc = result["goal"]
    ax.scatter(sc, sr, s=120, marker="o", color="#2ca25f", edgecolors="white", linewidths=1.2, label="Start", zorder=4)
    ax.scatter(gc, gr, s=150, marker="*", color="#e6550d", edgecolors="white", linewidths=1.0, label="Goal", zorder=4)
    ax.set_title("AI-Based Autonomous Navigation | Occupancy Grid & Route", fontsize=14, weight="bold", pad=14)
    ax.set_xlabel("Grid column"); ax.set_ylabel("Grid row")
    ax.set_xticks(range(0, original_grid.shape[1], 2)); ax.set_yticks(range(0, original_grid.shape[0], 2))
    ax.grid(which="major", color="#cbd5e1", linewidth=0.35, alpha=0.7)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.10), ncol=4, frameon=False)
    fig.tight_layout()
    fig.savefig(output_dir / "navigation_map.png", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=150)
    if visited:
        ax.plot(range(len(visited)), [p[1] for p in visited], label="Column", linewidth=2, color="#377eb8")
        ax.plot(range(len(visited)), [p[0] for p in visited], label="Row", linewidth=2, color="#e6550d")
    ax.set_title("Robot Progress by Movement Step", fontsize=14, weight="bold", pad=12)
    ax.set_xlabel("Movement step"); ax.set_ylabel("Grid coordinate")
    ax.grid(True, alpha=0.25); ax.legend(frameon=False, ncol=2)
    ax.text(0.02, 0.97, f"Reached goal: {result['path_found']}  |  Replans: {result['replans']}  |  Collision: {result['collision_detected']}", transform=ax.transAxes, va="top", fontsize=10, bbox={"boxstyle":"round,pad=0.35", "facecolor":"white", "alpha":0.85, "edgecolor":"#cbd5e1"})
    fig.tight_layout()
    fig.savefig(output_dir / "navigation_progress.png", bbox_inches="tight")
    plt.close(fig)
