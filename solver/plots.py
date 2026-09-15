from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

from solver.search import SearchResult
from solver.state import Model, make_state

ROOT = Path(__file__).resolve().parent.parent
FIGURE_DIR = ROOT / "report" / "figures"


def _style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 8,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def save_cost_figures(
    hc: SearchResult,
    tabu: SearchResult,
    out_dir: Path | None = None,
) -> tuple[Path, Path]:
    _style()
    out_dir = Path(out_dir) if out_dir is not None else FIGURE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    current_path = out_dir / "cost-current.pdf"
    fig, axes = plt.subplots(2, 1, figsize=(3.35, 4.2), sharex=True, layout="constrained")
    axes[0].plot(hc.trace_t, hc.trace_current, color="black", lw=0.55)
    axes[0].set_ylabel("uncovered houses")
    axes[0].text(0.02, 0.92, "naive HC", transform=axes[0].transAxes, va="top", fontsize=8)
    axes[1].plot(tabu.trace_t, tabu.trace_current, color="black", lw=0.7)
    axes[1].set_ylabel("uncovered houses")
    axes[1].text(0.02, 0.92, "tabu search", transform=axes[1].transAxes, va="top", fontsize=8)
    axes[1].set_xlabel("time (s)")
    for ax in axes:
        ax.set_xlim(0, max(hc.trace_t[-1], tabu.trace_t[-1]))
        ax.grid(True, lw=0.3, alpha=0.5)
    fig.savefig(current_path, format="pdf")
    plt.close(fig)

    best_path = out_dir / "cost-best.pdf"
    fig, ax = plt.subplots(figsize=(3.35, 2.4), layout="constrained")
    ax.plot(hc.trace_t, hc.trace_best, color="black", lw=1.1, ls="--", label="naive HC")
    ax.plot(tabu.trace_t, tabu.trace_best, color="black", lw=1.1, ls="-", label="tabu search")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("uncovered houses")
    ax.set_xlim(0, max(hc.trace_t[-1], tabu.trace_t[-1]))
    late_hc = [b for t, b in zip(hc.trace_t, hc.trace_best) if t >= 1.0]
    late_ts = [b for t, b in zip(tabu.trace_t, tabu.trace_best) if t >= 1.0]
    lo = min(hc.trace_best[-1], tabu.trace_best[-1])
    hi = max(max(late_hc), max(late_ts))
    ax.set_ylim(lo - 15, hi + 40)
    ax.grid(True, lw=0.3, alpha=0.5)
    ax.legend(frameon=False)
    fig.savefig(best_path, format="pdf")
    plt.close(fig)
    return current_path, best_path


def save_placement_figure(
    model: Model,
    chosen: np.ndarray,
    out_dir: Path | None = None,
    filename: str = "placement-tabu.pdf",
) -> Path:
    """Map of unique house cells plus the chosen unit disks."""
    _style()
    out_dir = Path(out_dir) if out_dir is not None else FIGURE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    state = make_state(model, chosen)
    xy = model.inst.xy
    weights = model.inst.weights.astype(np.float64)
    covered = state.counts > 0
    sizes = 10.0 + 55.0 * np.sqrt(weights / weights.max())
    world = float(max(10.0, np.ceil(xy.max())))

    fig, ax = plt.subplots(figsize=(3.35, 3.15), layout="constrained")
    for idx in chosen:
        cx, cy = model.centres[int(idx)]
        ax.add_patch(
            Circle(
                (cx, cy),
                1.0,
                facecolor="0.82",
                edgecolor="black",
                lw=0.7,
                alpha=0.45,
                zorder=1,
            )
        )
    ax.scatter(
        xy[covered, 0],
        xy[covered, 1],
        s=sizes[covered],
        c="black",
        linewidths=0,
        zorder=3,
        rasterized=True,
    )
    ax.scatter(
        xy[~covered, 0],
        xy[~covered, 1],
        s=sizes[~covered],
        facecolors="none",
        edgecolors="black",
        linewidths=0.65,
        zorder=4,
    )
    ax.scatter(
        model.centres[chosen, 0],
        model.centres[chosen, 1],
        s=18,
        facecolors="white",
        edgecolors="black",
        linewidths=0.6,
        zorder=5,
    )
    ax.set_xlim(0, world)
    ax.set_ylim(0, world)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ticks = range(0, int(world) + 1, 2)
    ax.set_xticks(list(ticks))
    ax.set_yticks(list(ticks))
    fig.savefig(path, format="pdf")
    plt.close(fig)
    return path


def write_trace_csv(res: SearchResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("t,current,best\n")
        for t, cur, best in zip(res.trace_t, res.trace_current, res.trace_best):
            fh.write(f"{t:.6f},{cur},{best}\n")
