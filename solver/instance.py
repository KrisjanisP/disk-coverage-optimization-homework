from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class Instance:
    """Houses as unique integer locations with multiplicity weights."""

    xy: np.ndarray
    weights: np.ndarray
    k: int
    n_houses: int

    @property
    def n_unique(self) -> int:
        return int(self.xy.shape[0])


def load_instance(path: Path | str) -> Instance:
    path = Path(path)
    xs: list[int] = []
    ys: list[int] = []
    n_declared: int | None = None
    k = 1
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if n_declared is None:
                if len(parts) < 2:
                    raise ValueError(f"{path}: first data line must be 'N K'")
                n_declared = int(parts[0])
                k = int(parts[1])
                continue
            xs.append(int(parts[0]))
            ys.append(int(parts[1]))
    if n_declared is None:
        raise ValueError(f"{path}: empty instance")
    if len(xs) != n_declared:
        raise ValueError(f"{path}: declared N={n_declared} but found {len(xs)} points")
    pts = np.column_stack((np.asarray(xs, dtype=np.int32), np.asarray(ys, dtype=np.int32)))
    unique, weights = np.unique(pts, axis=0, return_counts=True)
    return Instance(
        xy=unique.astype(np.float64),
        weights=weights.astype(np.int64),
        k=k,
        n_houses=int(n_declared),
    )
