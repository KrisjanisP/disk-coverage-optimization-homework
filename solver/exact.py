from __future__ import annotations

import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

from solver.state import Model, make_state


def solve_ilp(model: Model, time_limit: float = 60.0) -> tuple[np.ndarray, int, dict]:
    """Maximum coverage ILP on the discrete candidate set. Comparison only, not the homework solver."""
    n_c = model.n_cand
    n_u = model.inst.n_unique
    k = model.k
    weights = model.inst.weights.astype(np.float64)
    n = n_c + n_u
    c = np.zeros(n)
    c[n_c:] = -weights
    a = lil_matrix((n_u + 1, n))
    lb = np.zeros(n_u + 1)
    ub = np.zeros(n_u + 1)
    for i, pts in enumerate(model.covered):
        for j in pts:
            a[int(j), i] = 1.0
    for j in range(n_u):
        a[j, n_c + j] = -1.0
        lb[j] = 0.0
        ub[j] = np.inf
    a[n_u, :n_c] = 1.0
    lb[n_u] = k
    ub[n_u] = k
    t0 = time.perf_counter()
    res = milp(
        c=c,
        integrality=np.ones(n, dtype=int),
        bounds=Bounds(0, 1),
        constraints=LinearConstraint(a.tocsr(), lb, ub),
        options={"disp": False, "time_limit": time_limit, "mip_rel_gap": 0.0},
    )
    elapsed = time.perf_counter() - t0
    if res.x is None:
        extra = {
            "success": False,
            "status": int(res.status),
            "message": str(res.message),
            "seconds": elapsed,
            "obj": None if res.fun is None else float(-res.fun),
        }
        return np.zeros(0, dtype=np.int32), model.inst.n_houses, extra
    chosen = np.flatnonzero(res.x[:n_c] > 0.5).astype(np.int32)
    state = make_state(model, chosen)
    extra = {
        "success": bool(res.success),
        "status": int(res.status),
        "message": str(res.message),
        "seconds": elapsed,
        "obj": None if res.fun is None else float(-res.fun),
    }
    return chosen, state.uncovered, extra
