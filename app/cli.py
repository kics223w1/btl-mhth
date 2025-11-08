from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .pnml import load_pnml
from .reach_explicit import reachable_bfs
from .reach_bdd import reachability_bdd, count_reachable
from .deadlock_ilp import find_reachable_deadlock
from .optimize import maximize_over_reach
from .utils import timer, parse_weights


def cmd_explicit(args: argparse.Namespace):
    net = load_pnml(args.pnml)
    with timer() as elapsed:
        reach = reachable_bfs(net)
    print(json.dumps({"states": len(reach), "time_s": elapsed()}, indent=2))


def cmd_bdd(args: argparse.Namespace):
    net = load_pnml(args.pnml)
    with timer() as elapsed:
        bdd, reach, cur, nxt = reachability_bdd(net)
        n = count_reachable(bdd, reach)
    print(json.dumps({"states": n, "time_s": elapsed()}, indent=2))


def cmd_deadlock(args: argparse.Namespace):
    net = load_pnml(args.pnml)
    bdd, reach, cur, _ = reachability_bdd(net)
    with timer() as elapsed:
        mark = find_reachable_deadlock(net, bdd, reach, cur)
    out: dict[str, Any] = {"time_s": elapsed()}
    if mark is None:
        out["deadlock"] = None
    else:
        out["deadlock"] = sorted(list(mark))
    print(json.dumps(out, indent=2))


def cmd_optimize(args: argparse.Namespace):
    net = load_pnml(args.pnml)
    weights = parse_weights(args.weights or "")
    bdd, reach, cur, _ = reachability_bdd(net)
    with timer() as elapsed:
        res = maximize_over_reach(net, bdd, reach, cur, weights)
    out: dict[str, Any] = {"time_s": elapsed()}
    if res is None:
        out["optimum"] = None
    else:
        mark, val = res
        out["optimum"] = {"value": val, "marking": sorted(list(mark))}
    print(json.dumps(out, indent=2))


def main(argv=None):
    p = argparse.ArgumentParser(prog="pn-solver")
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("explicit", help="explicit BFS reachability")
    pe.add_argument("--pnml", required=True)
    pe.set_defaults(func=cmd_explicit)

    pb = sub.add_parser("bdd", help="symbolic reachability via BDD")
    pb.add_argument("--pnml", required=True)
    pb.set_defaults(func=cmd_bdd)

    pd = sub.add_parser("deadlock", help="deadlock detection via ILP+BDD")
    pd.add_argument("--pnml", required=True)
    pd.set_defaults(func=cmd_deadlock)

    po = sub.add_parser("optimize", help="linear optimization over Reach")
    po.add_argument("--pnml", required=True)
    po.add_argument("--weights", help="p1=2,p2=-1,...")
    po.set_defaults(func=cmd_optimize)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()


