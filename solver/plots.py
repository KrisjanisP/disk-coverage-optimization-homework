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


def _tick_step(world: float) -> int:
    w = int(round(world))
    if w <= 12:
        return 2
    if w <= 40:
        return 5
    if w <= 120:
        return 20
    return 50


def _world(xy: np.ndarray) -> float:
    return float(max(1.0, np.ceil(xy.max())))


def _marker_sizes(weights: np.ndarray, n_unique: int) -> np.ndarray:
    rel = np.sqrt(weights / weights.max())
    if n_unique < 200:
        return 10.0 + 55.0 * rel
    if n_unique < 1500:
        return 4.0 + 14.0 * rel
    return 2.0 + 8.0 * rel


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
    ax.plot(hc.trace_t, hc.trace_best, color="black", lw=1.1, ls="--", label="naivais algoritms")
    ax.plot(tabu.trace_t, tabu.trace_best, color="black", lw=1.1, ls="-", label="tabu meklēšana")
    ax.set_xlabel("laiks (s)")
    ax.set_ylabel("nenoklātas mājsaimniecības")
    ax.set_xlim(0, max(hc.trace_t[-1], tabu.trace_t[-1]))
    late_hc = [b for t, b in zip(hc.trace_t, hc.trace_best) if t >= 5.0]
    late_ts = [b for t, b in zip(tabu.trace_t, tabu.trace_best) if t >= 5.0]
    lo = min(hc.trace_best[-1], tabu.trace_best[-1])
    hi = max(max(late_hc), max(late_ts)) if late_hc and late_ts else max(hc.trace_best[-1], tabu.trace_best[-1])
    pad = max(15.0, 0.12 * (hi - lo + 1))
    ax.set_ylim(lo - pad, hi + pad)
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
    """Integer house locations plus the chosen disks of radius R."""
    _style()
    out_dir = Path(out_dir) if out_dir is not None else FIGURE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    state = make_state(model, chosen)
    xy = model.inst.xy
    weights = model.inst.weights.astype(np.float64)
    covered = state.counts > 0
    sizes = _marker_sizes(weights, xy.shape[0])
    world = _world(xy)
    radius = float(model.inst.radius)
    ticks = _tick_step(world)

    fig, ax = plt.subplots(figsize=(3.35, 3.15), layout="constrained")
    for idx in chosen:
        cx, cy = model.centres[int(idx)]
        ax.add_patch(
            Circle(
                (cx, cy),
                radius,
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
        linewidths=0.45,
        zorder=4,
        rasterized=True,
    )
    ax.scatter(
        model.centres[chosen, 0],
        model.centres[chosen, 1],
        s=12,
        facecolors="white",
        edgecolors="black",
        linewidths=0.55,
        zorder=5,
    )
    ax.set_xlim(0, world)
    ax.set_ylim(0, world)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xticks(list(range(0, int(world) + 1, ticks)))
    ax.set_yticks(list(range(0, int(world) + 1, ticks)))
    fig.savefig(path, format="pdf")
    plt.close(fig)
    return path


def save_placement_houses_figure(
    model: Model,
    chosen: np.ndarray,
    houses_xy: np.ndarray,
    out_dir: Path | None = None,
    filename: str = "placement-tabu-houses.pdf",
) -> Path:
    """Integer (or sampled) house points with disk outlines of radius R."""
    _style()
    out_dir = Path(out_dir) if out_dir is not None else FIGURE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    world = _world(np.vstack([model.inst.xy, houses_xy]))
    radius = float(model.inst.radius)
    ticks = _tick_step(world)
    state = make_state(model, chosen)
    cover = { (int(x), int(y)): bool(hit) for (x, y), hit in zip(model.inst.xy, state.counts > 0) }
    rounded = np.clip(np.rint(houses_xy), 0, world).astype(int)
    is_cov = np.array([cover.get((int(x), int(y)), False) for x, y in rounded])

    fig, ax = plt.subplots(figsize=(3.35, 3.15), layout="constrained")
    ax.scatter(
        houses_xy[is_cov, 0],
        houses_xy[is_cov, 1],
        s=1.4,
        c="black",
        alpha=0.22,
        linewidths=0,
        zorder=2,
        rasterized=True,
    )
    ax.scatter(
        houses_xy[~is_cov, 0],
        houses_xy[~is_cov, 1],
        s=2.2,
        c="black",
        alpha=0.55,
        linewidths=0,
        zorder=3,
        rasterized=True,
    )
    for idx in chosen:
        cx, cy = model.centres[int(idx)]
        ax.add_patch(
            Circle(
                (cx, cy),
                radius,
                fill=False,
                edgecolor="black",
                lw=0.8,
                zorder=4,
            )
        )
    ax.scatter(
        model.centres[chosen, 0],
        model.centres[chosen, 1],
        s=12,
        facecolors="white",
        edgecolors="black",
        linewidths=0.55,
        zorder=5,
    )
    ax.set_xlim(0, world)
    ax.set_ylim(0, world)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xticks(list(range(0, int(world) + 1, ticks)))
    ax.set_yticks(list(range(0, int(world) + 1, ticks)))
    fig.savefig(path, format="pdf")
    plt.close(fig)
    return path


def write_trace_csv(res: SearchResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("t,current,best\n")
        for t, cur, best in zip(res.trace_t, res.trace_current, res.trace_best):
            fh.write(f"{t:.6f},{cur},{best}\n")
