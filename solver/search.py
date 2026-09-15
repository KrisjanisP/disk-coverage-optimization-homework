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
    trace_t: list[float] = field(default_factory=list)
    trace_current: list[int] = field(default_factory=list)
    trace_best: list[int] = field(default_factory=list)


class CostTrace:
    """Wall-clock samples of current cost and best-so-far cost."""

    def __init__(self, t0: float, min_dt: float = 0.02) -> None:
        self.t0 = t0
        self.min_dt = min_dt
        self.t: list[float] = []
        self.current: list[int] = []
        self.best: list[int] = []
        self._best = 10**18
        self._last_t = -1.0

    def record(self, current: int, force: bool = False) -> None:
        now = time.perf_counter() - self.t0
        if current < self._best:
            self._best = current
            force = True
        if not force and now - self._last_t < self.min_dt:
            return
        self.t.append(now)
        self.current.append(int(current))
        self.best.append(int(self._best))
        self._last_t = now


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
    trace: CostTrace | None = None,
) -> int:
    """First-improvement walk. Stops when a full neighbourhood pass finds no improving swap."""
    steps = 0
    if trace is not None:
        trace.record(state.uncovered, force=True)
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
                    if trace is not None:
                        trace.record(state.uncovered, force=True)
                    break
                apply_swap(model, state, slot, old)
            if improved:
                break
        if not improved:
            if trace is not None:
                trace.record(state.uncovered, force=True)
            return steps
    return steps


def naive_multistart(
    model: Model,
    rng: np.random.Generator,
    seconds: float,
) -> SearchResult:
    t0 = time.perf_counter()
    deadline = t0 + seconds
    trace = CostTrace(t0)
    best: State | None = None
    iterations = 0
    restarts = 0
    while time.perf_counter() < deadline:
        state = make_state(model, random_start(model, rng))
        restarts += 1
        trace.record(state.uncovered, force=True)
        iterations += hill_climb_until_stuck(model, state, rng, deadline, trace=trace)
        if best is None or state.uncovered < best.uncovered:
            best = State(
                chosen=state.chosen.copy(),
                counts=state.counts.copy(),
                uncovered=state.uncovered,
            )
    assert best is not None
    trace.record(best.uncovered, force=True)
    return SearchResult(
        name="naive_hc_multistart",
        uncovered=best.uncovered,
        covered=covered_houses(model, best),
        chosen=best.chosen.copy(),
        seconds=time.perf_counter() - t0,
        iterations=iterations,
        restarts=restarts,
        extra={"trace_points": len(trace.t)},
        trace_t=trace.t,
        trace_current=trace.current,
        trace_best=trace.best,
    )


def greedy_start(model: Model, rng: np.random.Generator | None = None, rcl: int = 1) -> np.ndarray:
    """K times, pick among the ``rcl`` unused candidates with highest residual cover."""
    chosen: list[int] = []
    counts = np.zeros(model.inst.n_unique, dtype=np.int32)
    weights = model.inst.weights.astype(np.float64, copy=False)
    occ = np.zeros(model.n_cand, dtype=bool)
    for _ in range(model.k):
        residual = np.where(counts == 0, weights, 0.0)
        gain = model.cover_mat.dot(residual)
        gain[occ] = -1.0
        if rng is None or rcl <= 1:
            best_c = int(np.argmax(gain))
        else:
            pool_n = min(max(1, rcl), model.n_cand - int(occ.sum()))
            top = np.argpartition(gain, -pool_n)[-pool_n:]
            top = top[np.argsort(gain[top])[::-1]]
            w = gain[top] + 1.0
            w = np.maximum(w, 1e-12)
            w /= w.sum()
            best_c = int(rng.choice(top, p=w))
        chosen.append(best_c)
        occ[best_c] = True
        counts[model.covered[best_c]] += 1
    return np.asarray(chosen, dtype=np.int32)


def _swap_costs(
    model: Model,
    state: State,
    slot: int,
    skip: np.ndarray,
) -> tuple[int, np.ndarray]:
    """Uncovered counts after replacing ``chosen[slot]``. Restores ``state.counts``."""
    weights = model.inst.weights.astype(np.float64, copy=False)
    counts = state.counts
    old = int(state.chosen[slot])
    drop = model.covered[old]
    loss = float(weights[drop][counts[drop] == 1].sum())
    counts[drop] -= 1
    residual = np.where(counts == 0, weights, 0.0)
    cost = (state.uncovered + loss) - model.cover_mat.dot(residual)
    cost[skip] = np.inf
    counts[drop] += 1
    return old, cost


def first_improving_swap(
    model: Model,
    state: State,
    rng: np.random.Generator,
) -> tuple[int, int, int, int] | None:
    """First slot (random order) with an improving 1-swap; best swap on that slot."""
    skip = np.zeros(model.n_cand, dtype=bool)
    skip[state.chosen] = True
    current = state.uncovered
    for slot in rng.permutation(model.k):
        slot = int(slot)
        old, cost = _swap_costs(model, state, slot, skip)
        new_idx = int(np.argmin(cost))
        cand = float(cost[new_idx])
        if not np.isfinite(cand):
            continue
        ival = int(np.rint(cand))
        if ival < current:
            return slot, new_idx, old, ival
    return None


def _record_best(state: State, best_uncovered: int, best_chosen: np.ndarray | None) -> tuple[int, np.ndarray]:
    if state.uncovered < best_uncovered:
        return state.uncovered, state.chosen.copy()
    assert best_chosen is not None
    return best_uncovered, best_chosen


def climb_first_improvement(
    model: Model,
    state: State,
    rng: np.random.Generator,
    deadline: float,
    trace: CostTrace | None = None,
) -> int:
    """Apply first-improving 1-swaps until a local minimum or the deadline."""
    applied = 0
    while time.perf_counter() < deadline:
        move = first_improving_swap(model, state, rng)
        if move is None:
            if trace is not None:
                trace.record(state.uncovered, force=True)
            return applied
        slot, new_idx, _old, _cost = move
        apply_swap(model, state, slot, new_idx)
        applied += 1
        if trace is not None:
            trace.record(state.uncovered, force=True)
    return applied


def best_admissible_swap(
    model: Model,
    state: State,
    tabu_until: np.ndarray,
    iteration: int,
    best_uncovered: int,
    trial: np.ndarray | None = None,
) -> tuple[int, int, int, int] | None:
    """Cheapest admissible 1-swap via one drop per slot and a sparse matvec."""
    skip = np.zeros(model.n_cand, dtype=bool)
    skip[state.chosen] = True
    if trial is not None:
        allow = np.zeros(model.n_cand, dtype=bool)
        allow[trial] = True
        skip |= ~allow
    tabu = tabu_until > iteration
    found = False
    best_slot = -1
    best_new = -1
    best_old = -1
    best_cost = 10**18
    for slot in range(model.k):
        old, cost = _swap_costs(model, state, slot, skip)
        banned = tabu & (cost >= best_uncovered)
        cost = np.where(banned, np.inf, cost)
        new_idx = int(np.argmin(cost))
        cand_cost = float(cost[new_idx])
        if not np.isfinite(cand_cost):
            continue
        ival = int(np.rint(cand_cost))
        if not found or ival < best_cost:
            found = True
            best_cost = ival
            best_slot = slot
            best_new = new_idx
            best_old = old
    if not found:
        return None
    return best_slot, best_new, best_old, best_cost


def tabu_search(
    model: Model,
    rng: np.random.Generator,
    seconds: float,
    tenure: int,
    idle_restart: int = 80,
    sample: int | None = None,
) -> SearchResult:
    """First-improvement climb, then best-admissible tabu kicks, random restarts.

    After the climb, idle counts tabu steps without a new global best so cycling
    cannot stall a restart. ``sample`` is unused-candidate sample size per tabu
    step; ``None`` scans the full neighbourhood.
    """
    if tenure < 1:
        raise ValueError("tabu tenure must be >= 1")
    if sample is not None and sample < 1:
        raise ValueError("neighbourhood sample must be >= 1")
    t0 = time.perf_counter()
    deadline = t0 + seconds
    trace = CostTrace(t0)
    best_chosen: np.ndarray | None = None
    best_uncovered = 10**18
    tabu_until = np.full(model.n_cand, -1, dtype=np.int32)
    steps = 0
    restarts = 0
    tabu_steps = 0
    climb_steps = 0
    while time.perf_counter() < deadline:
        state = make_state(model, random_start(model, rng))
        restarts += 1
        trace.record(state.uncovered, force=True)
        if state.uncovered < best_uncovered:
            best_uncovered = state.uncovered
            best_chosen = state.chosen.copy()
        n_climb = climb_first_improvement(model, state, rng, deadline, trace)
        climb_steps += n_climb
        steps += n_climb * model.k * (model.n_cand - model.k)
        best_uncovered, best_chosen = _record_best(state, best_uncovered, best_chosen)
        tabu_until.fill(-1)
        iteration = 0
        idle = 0
        while time.perf_counter() < deadline:
            trial: np.ndarray | None
            if sample is None:
                trial = None
                steps += model.k * (model.n_cand - model.k)
            else:
                occupied = set(int(x) for x in state.chosen)
                free = [i for i in range(model.n_cand) if i not in occupied]
                if len(free) > sample:
                    trial = rng.choice(np.asarray(free, dtype=np.int32), size=sample, replace=False)
                else:
                    trial = np.asarray(free, dtype=np.int32)
                steps += model.k * int(trial.shape[0])
            move = best_admissible_swap(model, state, tabu_until, iteration, best_uncovered, trial)
            if move is None:
                break
            best_slot, best_new, best_old, _cost = move
            apply_swap(model, state, best_slot, best_new)
            tabu_until[best_old] = iteration + tenure
            iteration += 1
            tabu_steps += 1
            trace.record(state.uncovered, force=True)
            if state.uncovered < best_uncovered:
                best_uncovered = state.uncovered
                best_chosen = state.chosen.copy()
                idle = 0
                n_climb = climb_first_improvement(model, state, rng, deadline, trace)
                climb_steps += n_climb
                steps += n_climb * model.k * (model.n_cand - model.k)
                best_uncovered, best_chosen = _record_best(state, best_uncovered, best_chosen)
            else:
                idle += 1
                if idle >= idle_restart:
                    break
    assert best_chosen is not None
    trace.record(best_uncovered, force=True)
    best_state = make_state(model, best_chosen)
    return SearchResult(
        name="tabu_search",
        uncovered=best_state.uncovered,
        covered=covered_houses(model, best_state),
        chosen=best_chosen,
        seconds=time.perf_counter() - t0,
        iterations=steps,
        restarts=restarts,
        extra={
            "tenure": tenure,
            "tabu_steps": tabu_steps,
            "climb_steps": climb_steps,
            "init": "random_then_first_improvement",
            "idle_restart": idle_restart,
            "sample": sample,
            "trace_points": len(trace.t),
        },
        trace_t=trace.t,
        trace_current=trace.current,
        trace_best=trace.best,
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
