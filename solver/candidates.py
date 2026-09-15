from __future__ import annotations

import numpy as np
from scipy.spatial import KDTree

from solver.instance import Instance

RADIUS = 1.0
RADIUS_SQ = RADIUS * RADIUS
PAIR_LIMIT = 2.0
CENTER_DECIMALS = 9


def _pair_centres(p: np.ndarray, q: np.ndarray) -> list[np.ndarray]:
    """Unit-disk centres whose boundary passes through p and q."""
    dvec = q - p
    d2 = float(dvec @ dvec)
    if d2 <= 1e-18 or d2 > 4.0 + 1e-9:
        return []
    d = np.sqrt(d2)
    a = 0.5 * d
    h2 = RADIUS_SQ - a * a
    mid = 0.5 * (p + q)
    if h2 <= 1e-18:
        return [mid]
    h = np.sqrt(max(h2, 0.0))
    perp = np.array((-dvec[1], dvec[0]), dtype=np.float64) * (h / d)
    return [mid + perp, mid - perp]


def candidate_centres(inst: Instance) -> np.ndarray:
    """O(U^2) equivalent set: input points plus at most two unit centres per close pair."""
    xy = inst.xy
    raw: list[np.ndarray] = [xy[i] for i in range(xy.shape[0])]
    tree = KDTree(xy)
    for i, j in tree.query_pairs(PAIR_LIMIT + 1e-12):
        raw.extend(_pair_centres(xy[i], xy[j]))
    if not raw:
        raise RuntimeError("no candidate centres")
    stacked = np.vstack(raw)
    rounded = np.round(stacked, decimals=CENTER_DECIMALS)
    unique = np.unique(rounded, axis=0)
    return unique


def coverage_lists(centres: np.ndarray, inst: Instance) -> list[np.ndarray]:
    """For each centre, unique-location indices at distance <= 1."""
    xy = inst.xy
    covered: list[np.ndarray] = []
    chunk = 4096
    for start in range(0, centres.shape[0], chunk):
        block = centres[start : start + chunk]
        delta = block[:, None, :] - xy[None, :, :]
        d2 = np.einsum("cui,cui->cu", delta, delta)
        for row in d2:
            covered.append(np.flatnonzero(row <= RADIUS_SQ + 1e-9).astype(np.int32))
    return covered
