from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from solver.instance import Instance


@dataclass
class Model:
    inst: Instance
    centres: np.ndarray
    covered: list[np.ndarray]

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
