from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np

from solver.state import Model, State, apply_swap, covered_houses, make_state


@dataclass
class SearchResult:
    name: str
    uncovered: int
    covered: int
    chosen: np.ndarray
    seconds: float
    iterations: int
    restarts: int = 0
    extra: dict = field(default_factory=dict)


def random_start(model: Model, rng: np.random.Generator) -> np.ndarray:
    if model.n_cand < model.k:
        raise ValueError(f"need at least K={model.k} candidates, have {model.n_cand}")
    return rng.choice(model.n_cand, size=model.k, replace=False).astype(np.int32)


def _random_neighbour(model: Model, state: State, rng: np.random.Generator) -> tuple[int, int]:
    slot = int(rng.integers(0, model.k))
    occupied = set(int(x) for x in state.chosen)
    new_idx = int(rng.integers(0, model.n_cand))
    while new_idx in occupied:
        new_idx = int(rng.integers(0, model.n_cand))
    return slot, new_idx


def hill_climb_until_stuck(
    model: Model,
    state: State,
    rng: np.random.Generator,
    deadline: float,
) -> int:
    """First-improvement walk. Stops when a full neighbourhood pass finds no improving swap."""
    steps = 0
    while time.perf_counter() < deadline:
        improved = False
        occupied = set(int(x) for x in state.chosen)
        for slot in rng.permutation(model.k):
            if time.perf_counter() >= deadline:
                return steps
            slot = int(slot)
            old = int(state.chosen[slot])
            current = state.uncovered
            for new_idx in rng.permutation(model.n_cand):
                if time.perf_counter() >= deadline:
                    return steps
                new_idx = int(new_idx)
                if new_idx in occupied:
                    continue
                apply_swap(model, state, slot, new_idx)
                steps += 1
                if state.uncovered < current:
                    occupied.remove(old)
                    occupied.add(new_idx)
                    improved = True
                    break
                apply_swap(model, state, slot, old)
            if improved:
                break
        if not improved:
            return steps
    return steps


def naive_multistart(
    model: Model,
    rng: np.random.Generator,
    seconds: float,
) -> SearchResult:
    t0 = time.perf_counter()
    deadline = t0 + seconds
    best: State | None = None
    iterations = 0
    restarts = 0
    while time.perf_counter() < deadline:
        state = make_state(model, random_start(model, rng))
        restarts += 1
        iterations += hill_climb_until_stuck(model, state, rng, deadline)
        if best is None or state.uncovered < best.uncovered:
            best = State(
                chosen=state.chosen.copy(),
                counts=state.counts.copy(),
                uncovered=state.uncovered,
            )
    assert best is not None
    return SearchResult(
        name="naive_hc_multistart",
        uncovered=best.uncovered,
        covered=covered_houses(model, best),
        chosen=best.chosen.copy(),
        seconds=time.perf_counter() - t0,
        iterations=iterations,
        restarts=restarts,
    )


def greedy_start(model: Model) -> np.ndarray:
    """K times, pick the unused candidate covering the most still-uncovered weight."""
    chosen: list[int] = []
    counts = np.zeros(model.inst.n_unique, dtype=np.int32)
    weights = model.inst.weights
    for _ in range(model.k):
        occupied = set(chosen)
        best_c = -1
        best_gain = -1
        for c in range(model.n_cand):
            if c in occupied:
                continue
            pts = model.covered[c]
            if pts.size == 0:
                gain = 0
            else:
                gain = int(weights[pts][counts[pts] == 0].sum())
            if gain > best_gain:
                best_gain = gain
                best_c = c
        if best_c < 0:
            raise RuntimeError("greedy could not pick a centre")
        chosen.append(best_c)
        counts[model.covered[best_c]] += 1
    return np.asarray(chosen, dtype=np.int32)


def tabu_search(
    model: Model,
    rng: np.random.Generator,
    seconds: float,
    tenure: int,
) -> SearchResult:
    """Best-admissible-move tabu search (Glover). Evicted centres may not return for ``tenure`` steps."""
    if tenure < 1:
        raise ValueError("tabu tenure must be >= 1")
    t0 = time.perf_counter()
    deadline = t0 + seconds
    state = make_state(model, greedy_start(model))
    best_chosen = state.chosen.copy()
    best_uncovered = state.uncovered
    tabu_until = np.full(model.n_cand, -1, dtype=np.int32)
    iteration = 0
    steps = 0
    while time.perf_counter() < deadline:
        occupied = set(int(x) for x in state.chosen)
        best_slot = -1
        best_new = -1
        best_old = -1
        best_cost = 10**18
        found = False
        for slot in rng.permutation(model.k):
            if time.perf_counter() >= deadline:
                break
            slot = int(slot)
            old = int(state.chosen[slot])
            for new_idx in range(model.n_cand):
                if new_idx in occupied:
                    continue
                apply_swap(model, state, slot, new_idx)
                steps += 1
                cost = state.uncovered
                apply_swap(model, state, slot, old)
                forbidden = int(tabu_until[new_idx]) > iteration
                if forbidden and cost >= best_uncovered:
                    continue
                if not found or cost < best_cost:
                    found = True
                    best_cost = cost
                    best_slot = slot
                    best_new = new_idx
                    best_old = old
        if not found:
            break
        apply_swap(model, state, best_slot, best_new)
        tabu_until[best_old] = iteration + tenure
        iteration += 1
        if state.uncovered < best_uncovered:
            best_uncovered = state.uncovered
            best_chosen = state.chosen.copy()
    best_state = make_state(model, best_chosen)
    return SearchResult(
        name="tabu_search",
        uncovered=best_state.uncovered,
        covered=covered_houses(model, best_state),
        chosen=best_chosen,
        seconds=time.perf_counter() - t0,
        iterations=steps,
        extra={"tenure": tenure, "tabu_steps": iteration, "init": "greedy"},
    )


def lahc(
    model: Model,
    rng: np.random.Generator,
    seconds: float,
    history: int,
    idle_restart: int | None = None,
) -> SearchResult:
    """Late-acceptance hill-climbing, Burke and Bykov (2017).

    A trajectory is restarted from a new random K-subset after ``idle_restart``
    consecutive rejected neighbours. Without that, a short history fills with the
    local-minimum cost and the remaining time is spent rejecting every move.
    """
    if history < 1:
        raise ValueError("history length must be >= 1")
    if idle_restart is None:
        idle_restart = max(history, 1)
    t0 = time.perf_counter()
    deadline = t0 + seconds
    best_chosen: np.ndarray | None = None
    best_uncovered = 10**18
    iterations = 0
    restarts = 0
    while time.perf_counter() < deadline:
        state = make_state(model, random_start(model, rng))
        restarts += 1
        current_cost = state.uncovered
        if current_cost < best_uncovered:
            best_uncovered = current_cost
            best_chosen = state.chosen.copy()
        history_list = [current_cost] * history
        index = 0
        rejected = 0
        while time.perf_counter() < deadline:
            slot, new_idx = _random_neighbour(model, state, rng)
            old = apply_swap(model, state, slot, new_idx)
            cand_cost = state.uncovered
            iterations += 1
            if cand_cost <= current_cost or cand_cost < history_list[index]:
                current_cost = cand_cost
                rejected = 0
                if cand_cost < best_uncovered:
                    best_uncovered = cand_cost
                    best_chosen = state.chosen.copy()
            else:
                apply_swap(model, state, slot, old)
                rejected += 1
            if current_cost < history_list[index]:
                history_list[index] = current_cost
            index += 1
            if index == history:
                index = 0
            if rejected >= idle_restart:
                break
    assert best_chosen is not None
    best_state = make_state(model, best_chosen)
    return SearchResult(
        name="lahc",
        uncovered=best_state.uncovered,
        covered=covered_houses(model, best_state),
        chosen=best_chosen,
        seconds=time.perf_counter() - t0,
        iterations=iterations,
        restarts=restarts,
        extra={"history": history, "idle_restart": idle_restart},
    )
