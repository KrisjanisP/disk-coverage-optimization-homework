from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np

from solver.candidates import candidate_centres, coverage_lists
from solver.instance import Instance
from solver.plots import save_placement_figure, save_placement_houses_figure
from solver.search import greedy_start, hill_climb_until_stuck, lahc, naive_multistart, tabu_search
from solver.state import Model, make_state


def _tiny() -> tuple[Model, Instance]:
    xy = np.array([[0.0, 0.0], [0.0, 1.0], [10.0, 0.0]])
    inst = Instance(xy=xy, weights=np.array([1, 1, 1], dtype=np.int64), k=1, n_houses=3)
    centres = candidate_centres(inst)
    model = Model(inst=inst, centres=centres, covered=coverage_lists(centres, inst))
    return model, inst


def test_unit_disk_covers_adjacent_pair():
    model, inst = _tiny()
    best = 0
    for i in range(model.n_cand):
        st = make_state(model, np.array([i], dtype=np.int32))
        best = max(best, inst.n_houses - st.uncovered)
    assert best == 2


def test_hill_climb_finds_pair():
    model, inst = _tiny()
    rng = np.random.default_rng(0)
    state = make_state(model, rng.choice(model.n_cand, size=1, replace=False).astype(np.int32))
    hill_climb_until_stuck(model, state, rng, deadline=1e18)
    assert inst.n_houses - state.uncovered == 2


def test_lahc_covers_the_pair():
    model, _inst = _tiny()
    rng = np.random.default_rng(1)
    res = lahc(model, rng, seconds=0.2, history=10)
    assert res.covered == 2


def test_multistart_covers_the_pair():
    model, _inst = _tiny()
    rng = np.random.default_rng(2)
    res = naive_multistart(model, rng, seconds=0.2)
    assert res.covered == 2
    assert res.restarts >= 1


def test_tabu_covers_the_pair():
    model, _inst = _tiny()
    rng = np.random.default_rng(3)
    res = tabu_search(model, rng, seconds=0.2, tenure=3)
    assert res.covered == 2


def test_greedy_covers_the_pair():
    model, inst = _tiny()
    st = make_state(model, greedy_start(model))
    assert inst.n_houses - st.uncovered == 2


def test_hc_trace_is_nonempty():
    model, _inst = _tiny()
    rng = np.random.default_rng(4)
    res = naive_multistart(model, rng, seconds=0.05)
    assert len(res.trace_t) >= 1
    assert res.trace_best[-1] == res.uncovered
    assert all(a >= b for a, b in zip(res.trace_best, res.trace_best[1:]))


def test_placement_figure_writes():
    model, _inst = _tiny()
    rng = np.random.default_rng(3)
    res = tabu_search(model, rng, seconds=0.2, tenure=3)
    with tempfile.TemporaryDirectory() as td:
        path = save_placement_figure(model, res.chosen, Path(td))
        assert path.is_file()
        assert path.stat().st_size > 0


def test_placement_houses_figure_writes():
    model, inst = _tiny()
    rng = np.random.default_rng(3)
    res = tabu_search(model, rng, seconds=0.2, tenure=3)
    with tempfile.TemporaryDirectory() as td:
        path = save_placement_houses_figure(model, res.chosen, inst.xy, Path(td))
        assert path.is_file()
        assert path.stat().st_size > 0


def test_ilp_covers_the_pair():
    from solver.exact import solve_ilp

    model, inst = _tiny()
    chosen, uncovered, extra = solve_ilp(model, time_limit=5.0)
    assert extra["success"]
    assert inst.n_houses - uncovered == 2
    assert len(chosen) == inst.k
