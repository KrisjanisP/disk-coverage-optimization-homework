from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.sparse import csr_matrix

from solver.instance import Instance


def coverage_csr(covered: list[np.ndarray], n_unique: int) -> csr_matrix:
    """Candidate-by-location incidence matrix; row i is the houses disk i covers."""
    n_cand = len(covered)
    indptr = np.empty(n_cand + 1, dtype=np.int32)
    indptr[0] = 0
    nnz = 0
    for i, pts in enumerate(covered):
        nnz += int(pts.size)
        indptr[i + 1] = nnz
    indices = np.empty(nnz, dtype=np.int32)
    pos = 0
    for pts in covered:
        n = int(pts.size)
        if n:
            indices[pos : pos + n] = pts
            pos += n
    data = np.ones(nnz, dtype=np.float64)
    return csr_matrix((data, indices, indptr), shape=(n_cand, n_unique))


@dataclass
class Model:
    inst: Instance
    centres: np.ndarray
    covered: list[np.ndarray]
    cover_mat: csr_matrix = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.cover_mat = coverage_csr(self.covered, self.inst.n_unique)

    @property
    def n_cand(self) -> int:
        return int(self.centres.shape[0])

    @property
    def k(self) -> int:
        return self.inst.k


@dataclass
class State:
    chosen: np.ndarray
    counts: np.ndarray
    uncovered: int


def make_state(model: Model, chosen: np.ndarray) -> State:
    counts = np.zeros(model.inst.n_unique, dtype=np.int32)
    for idx in chosen:
        counts[model.covered[int(idx)]] += 1
    uncovered = int(model.inst.weights[counts == 0].sum())
    return State(chosen=np.asarray(chosen, dtype=np.int32).copy(), counts=counts, uncovered=uncovered)


def covered_houses(model: Model, state: State) -> int:
    return model.inst.n_houses - state.uncovered


def apply_swap(model: Model, state: State, slot: int, new_idx: int) -> int:
    """Replace chosen[slot] with new_idx. Returns previous candidate index."""
    old = int(state.chosen[slot])
    weights = model.inst.weights
    drop = model.covered[old]
    state.counts[drop] -= 1
    state.uncovered += int(weights[drop][state.counts[drop] == 0].sum())
    add = model.covered[int(new_idx)]
    born = state.counts[add] == 0
    state.uncovered -= int(weights[add][born].sum())
    state.counts[add] += 1
    state.chosen[slot] = new_idx
    return old


def revert_swap(model: Model, state: State, slot: int, old_idx: int) -> None:
    apply_swap(model, state, slot, old_idx)
