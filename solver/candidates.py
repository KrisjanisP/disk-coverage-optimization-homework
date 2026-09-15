from __future__ import annotations

import numpy as np
from scipy.spatial import KDTree

from solver.instance import Instance

CENTER_DECIMALS = 9
# Pair-derived centres are snapped onto this lattice so the O(U^2) set stays searchable.
# With R=10, a 1-unit snap is 10% of the radius.
CANDIDATE_SNAP = 1.0


def _pair_centres(p: np.ndarray, q: np.ndarray, radius: float) -> list[np.ndarray]:
    """Radius-R disk centres whose boundary passes through p and q."""
    r2 = radius * radius
    dvec = q - p
    d2 = float(dvec @ dvec)
    if d2 <= 1e-18 or d2 > 4.0 * r2 + 1e-9:
        return []
    d = np.sqrt(d2)
    a = 0.5 * d
    h2 = r2 - a * a
    mid = 0.5 * (p + q)
    if h2 <= 1e-18:
        return [mid]
    h = np.sqrt(max(h2, 0.0))
    perp = np.array((-dvec[1], dvec[0]), dtype=np.float64) * (h / d)
    return [mid + perp, mid - perp]


def candidate_centres(inst: Instance) -> np.ndarray:
    """O(U^2) equivalent set: input points plus at most two radius-R centres per close pair."""
    xy = inst.xy
    radius = inst.radius
    raw: list[np.ndarray] = [xy[i] for i in range(xy.shape[0])]
    tree = KDTree(xy)
    for i, j in tree.query_pairs(2.0 * radius + 1e-12):
        raw.extend(_pair_centres(xy[i], xy[j], radius))
    if not raw:
        raise RuntimeError("no candidate centres")
    stacked = np.vstack(raw)
    if CANDIDATE_SNAP and CANDIDATE_SNAP > 0:
        stacked = np.round(stacked / CANDIDATE_SNAP) * CANDIDATE_SNAP
    rounded = np.round(stacked, decimals=CENTER_DECIMALS)
    unique = np.unique(rounded, axis=0)
    return unique


def coverage_lists(centres: np.ndarray, inst: Instance) -> list[np.ndarray]:
    """For each centre, unique-location indices at distance <= R."""
    xy = inst.xy
    r2 = inst.radius * inst.radius
    covered: list[np.ndarray] = []
    chunk = 4096
    for start in range(0, centres.shape[0], chunk):
        block = centres[start : start + chunk]
        delta = block[:, None, :] - xy[None, :, :]
        d2 = np.einsum("cui,cui->cu", delta, delta)
        for row in d2:
            covered.append(np.flatnonzero(row <= r2 + 1e-9).astype(np.int32))
    return covered
