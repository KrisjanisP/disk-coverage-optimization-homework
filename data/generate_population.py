#!/usr/bin/env python3
"""Build a clustered house instance from C city impulses plus a Gaussian blur."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

SEED = 2026
N_CITIES = 8
N_HOUSES = 10_000
K_TOWERS = 12
GRID = 512
SIGMA_PX = 20.0
MIN_SEP_PX = 80.0
WORLD = 100
RADIUS = 10.0
RURAL_MIX = 0.12

ROOT = Path(__file__).resolve().parent.parent
FIGURE_DIR = ROOT / "report" / "figures"
INSTANCE_DIR = ROOT / "data" / "instances"


def place_cities(rng: np.random.Generator) -> np.ndarray:
    """Return (C, 2) integer pixel centres with a minimum separation."""
    margin = int(3 * SIGMA_PX)
    lo, hi = margin, GRID - margin
    centres: list[tuple[int, int]] = []
    for _ in range(20_000):
        if len(centres) == N_CITIES:
            break
        y = int(rng.integers(lo, hi))
        x = int(rng.integers(lo, hi))
        if any((y - cy) ** 2 + (x - cx) ** 2 < MIN_SEP_PX**2 for cy, cx in centres):
            continue
        centres.append((y, x))
    if len(centres) != N_CITIES:
        raise RuntimeError(f"could not place {N_CITIES} cities; relax MIN_SEP_PX")
    return np.asarray(centres, dtype=int)


def density_map(centres: np.ndarray, weights: np.ndarray) -> np.ndarray:
    impulses = np.zeros((GRID, GRID), dtype=np.float64)
    for (y, x), w in zip(centres, weights):
        impulses[y, x] = w
    blurred = gaussian_filter(impulses, sigma=SIGMA_PX, mode="nearest")
    if RURAL_MIX:
        blurred = (1.0 - RURAL_MIX) * blurred + RURAL_MIX * blurred.mean()
    total = blurred.sum()
    if total <= 0:
        raise RuntimeError("density map is zero")
    return blurred / total


def sample_houses(density: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Sample N points in world coordinates, with subpixel jitter inside pixels."""
    idx = rng.choice(GRID * GRID, size=N_HOUSES, replace=True, p=density.ravel())
    rows, cols = np.unravel_index(idx, (GRID, GRID))
    jitter = rng.random((N_HOUSES, 2))
    px = cols + jitter[:, 0]
    py = rows + jitter[:, 1]
    scale = WORLD / GRID
    xy = np.column_stack((px * scale, py * scale))
    return xy


def save_instance(xy: np.ndarray, meta: dict) -> Path:
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    xy_int = np.clip(np.rint(xy), 0, WORLD).astype(int)
    path = INSTANCE_DIR / f"houses_n{N_HOUSES}_k{K_TOWERS}_r{int(RADIUS)}.txt"
    header = [
        f"# houses from C={N_CITIES} blurred city impulses",
        f"# seed={SEED} grid={GRID} sigma_px={SIGMA_PX} world={WORLD} radius={RADIUS}",
        f"# unique_integer_locations={len(np.unique(xy_int, axis=0))}",
    ]
    with path.open("w", encoding="utf-8") as fh:
        fh.write("\n".join(header) + "\n")
        fh.write(f"{N_HOUSES} {K_TOWERS} {RADIUS:g}\n")
        np.savetxt(fh, xy_int, fmt="%d %d")
    meta_path = path.with_suffix(".json")
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    np.save(INSTANCE_DIR / f"houses_n{N_HOUSES}_k{K_TOWERS}_r{int(RADIUS)}_raw.npy", xy)
    return path


def _tick_step(world: int) -> int:
    if world <= 12:
        return 2
    if world <= 40:
        return 5
    if world <= 120:
        return 20
    return 50


def style_axes(ax: plt.Axes) -> None:
    ax.set_xlim(0, WORLD)
    ax.set_ylim(0, WORLD)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    step = _tick_step(WORLD)
    ax.set_xticks(range(0, WORLD + 1, step))
    ax.set_yticks(range(0, WORLD + 1, step))


def save_density_figure(density: np.ndarray) -> Path:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURE_DIR / "density-map.pdf"
    fig, ax = plt.subplots(figsize=(3.35, 3.15), layout="constrained")
    ax.imshow(
        density,
        origin="lower",
        cmap="gray_r",
        extent=(0, WORLD, 0, WORLD),
        interpolation="nearest",
        rasterized=True,
    )
    style_axes(ax)
    fig.savefig(path, format="pdf")
    plt.close(fig)
    return path


def save_points_figure(xy: np.ndarray) -> Path:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURE_DIR / "sampled-houses.pdf"
    fig, ax = plt.subplots(figsize=(3.35, 3.15), layout="constrained")
    ax.scatter(xy[:, 0], xy[:, 1], s=1.2, c="black", alpha=0.25, linewidths=0, rasterized=True)
    style_axes(ax)
    fig.savefig(path, format="pdf")
    plt.close(fig)
    return path


def main() -> None:
    rng = np.random.default_rng(SEED)
    centres = place_cities(rng)
    weights = rng.uniform(0.45, 1.0, size=N_CITIES)
    density = density_map(centres, weights)
    xy = sample_houses(density, rng)
    xy_int = np.clip(np.rint(xy), 0, WORLD).astype(int)
    unique = int(len(np.unique(xy_int, axis=0)))
    meta = {
        "seed": SEED,
        "n_cities": N_CITIES,
        "n_houses": N_HOUSES,
        "k_towers": K_TOWERS,
        "grid": GRID,
        "sigma_px": SIGMA_PX,
        "min_sep_px": MIN_SEP_PX,
        "world": WORLD,
        "radius": RADIUS,
        "rural_mix": RURAL_MIX,
        "city_centres_px": centres.tolist(),
        "city_weights": weights.tolist(),
        "unique_integer_locations": unique,
        "bbox": [int(xy_int[:, 0].min()), int(xy_int[:, 1].min()), int(xy_int[:, 0].max()), int(xy_int[:, 1].max())],
    }
    inst = save_instance(xy, meta)
    dens_fig = save_density_figure(density)
    pts_fig = save_points_figure(xy_int)
    print(f"instance {inst} unique_cells={unique}")
    print(f"wrote {dens_fig}")
    print(f"wrote {pts_fig}")


if __name__ == "__main__":
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 8,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    main()
