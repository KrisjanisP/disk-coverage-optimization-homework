from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from solver.candidates import candidate_centres, coverage_lists
from solver.exact import solve_ilp
from solver.instance import load_instance
from solver.plots import save_cost_figures, save_placement_figure, save_placement_houses_figure, write_trace_csv
from solver.search import naive_multistart, tabu_search
from solver.state import Model


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Cover houses with K disks of radius R")
    p.add_argument("--instance", type=Path, required=True)
    p.add_argument("--seconds", type=float, default=120.0, help="wall time per method")
    p.add_argument("--tenure", type=int, default=12, help="tabu tenure")
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--json-out", type=Path, default=None)
    p.add_argument("--figure-dir", type=Path, default=None)
    p.add_argument("--exact", action="store_true", help="also solve the candidate ILP (comparison, not the search)")
    return p.parse_args(argv)


def _result_dict(res) -> dict:
    return {
        "name": res.name,
        "covered": res.covered,
        "uncovered": res.uncovered,
        "seconds": res.seconds,
        "iterations": res.iterations,
        "restarts": res.restarts,
        "extra": {k: v for k, v in res.extra.items() if k != "trace_points"},
        "chosen": [int(x) for x in res.chosen],
        "trace_points": len(res.trace_t),
    }


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    inst = load_instance(args.instance)
    centres = candidate_centres(inst)
    covered = coverage_lists(centres, inst)
    model = Model(inst=inst, centres=centres, covered=covered)
    print(
        f"N={inst.n_houses} unique={inst.n_unique} K={inst.k} R={inst.radius:g} candidates={model.n_cand}",
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
        "radius": inst.radius,
        "n_candidates": model.n_cand,
        "seconds": args.seconds,
        "seed": args.seed,
        "naive_hc": _result_dict(hc),
        "tabu": _result_dict(ts),
    }
    fig_dir = args.figure_dir
    if args.exact:
        opt_chosen, opt_uncovered, extra = solve_ilp(model)
        payload["ilp"] = {
            "covered": inst.n_houses - opt_uncovered,
            "uncovered": opt_uncovered,
            "chosen": [int(x) for x in opt_chosen],
            "extra": extra,
        }
        print(
            f"ILP       covered={inst.n_houses - opt_uncovered}/{inst.n_houses}  "
            f"{extra['seconds']:.2f}s  success={extra['success']}  {extra['message']}",
            file=sys.stderr,
        )
        if extra["success"] and len(opt_chosen) == inst.k:
            opt_fig = save_placement_figure(model, opt_chosen, fig_dir, filename="placement-opt.pdf")
            print(f"wrote {opt_fig}", file=sys.stderr)
            raw_path = args.instance.with_name(args.instance.stem + "_raw.npy")
            if raw_path.is_file():
                houses_xy = np.load(raw_path)
                opt_h = save_placement_houses_figure(
                    model, opt_chosen, houses_xy, fig_dir, filename="placement-opt-houses.pdf"
                )
                print(f"wrote {opt_h}", file=sys.stderr)
    text = json.dumps(payload, indent=2)
    print(text)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text + "\n", encoding="utf-8")
        write_trace_csv(hc, args.json_out.with_name("cost_trace_hc.csv"))
        write_trace_csv(ts, args.json_out.with_name("cost_trace_tabu.csv"))
    current_fig, best_fig = save_cost_figures(hc, ts, fig_dir)
    place_fig = save_placement_figure(model, ts.chosen, fig_dir)
    print(f"wrote {current_fig}", file=sys.stderr)
    print(f"wrote {best_fig}", file=sys.stderr)
    print(f"wrote {place_fig}", file=sys.stderr)
    raw_path = args.instance.with_name(args.instance.stem + "_raw.npy")
    if raw_path.is_file():
        houses_xy = np.load(raw_path)
        houses_fig = save_placement_houses_figure(model, ts.chosen, houses_xy, fig_dir)
        print(f"wrote {houses_fig}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
