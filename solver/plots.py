from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from solver.search import SearchResult

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


def write_trace_csv(res: SearchResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("t,current,best\n")
        for t, cur, best in zip(res.trace_t, res.trace_current, res.trace_best):
            fh.write(f"{t:.6f},{cur},{best}\n")
