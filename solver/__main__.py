from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from solver.candidates import candidate_centres, coverage_lists
from solver.instance import load_instance
from solver.search import naive_multistart, tabu_search
from solver.state import Model


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Cover houses with K unit disks")
    p.add_argument("--instance", type=Path, required=True)
    p.add_argument("--seconds", type=float, default=60.0, help="wall time per method")
    p.add_argument("--tenure", type=int, default=12, help="tabu tenure")
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--json-out", type=Path, default=None)
    return p.parse_args(argv)


def _result_dict(res) -> dict:
    return {
        "name": res.name,
        "covered": res.covered,
        "uncovered": res.uncovered,
        "seconds": res.seconds,
        "iterations": res.iterations,
        "restarts": res.restarts,
        "extra": res.extra,
        "chosen": [int(x) for x in res.chosen],
    }


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    inst = load_instance(args.instance)
    centres = candidate_centres(inst)
    covered = coverage_lists(centres, inst)
    model = Model(inst=inst, centres=centres, covered=covered)
    print(
        f"N={inst.n_houses} unique={inst.n_unique} K={inst.k} candidates={model.n_cand}",
        file=sys.stderr,
    )
    rng_hc = np.random.default_rng(args.seed)
    rng_ts = np.random.default_rng(args.seed + 1)
    hc = naive_multistart(model, rng_hc, args.seconds)
    print(
        f"naive HC  covered={hc.covered}/{inst.n_houses}  "
        f"restarts={hc.restarts}  iters={hc.iterations}  {hc.seconds:.1f}s",
        file=sys.stderr,
    )
    ts = tabu_search(model, rng_ts, args.seconds, args.tenure)
    print(
        f"tabu      covered={ts.covered}/{inst.n_houses}  "
        f"restarts={ts.restarts}  iters={ts.iterations}  {ts.seconds:.1f}s  tenure={args.tenure}",
        file=sys.stderr,
    )
    payload = {
        "instance": str(args.instance),
        "n_houses": inst.n_houses,
        "n_unique": inst.n_unique,
        "k": inst.k,
        "n_candidates": model.n_cand,
        "seconds": args.seconds,
        "seed": args.seed,
        "naive_hc": _result_dict(hc),
        "tabu": _result_dict(ts),
    }
    text = json.dumps(payload, indent=2)
    print(text)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
