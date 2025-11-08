from __future__ import annotations

from typing import Dict, Optional, Set

import pulp
from dd.autoref import BDD

from .model import PetriNet
from .reach_bdd import cube_from_marking


def _is_reachable_marking(bdd: BDD, reach, cur_vars: Dict[str, object], marked: Set[str]) -> bool:
    cube = cube_from_marking(bdd, cur_vars, marked)
    return (cube & reach) != bdd.false


def find_reachable_deadlock(net: PetriNet, bdd: BDD, reach, cur_vars: Dict[str, object]) -> Optional[Set[str]]:
    # If any transition has empty pre-set, it is always enabled -> no dead marking exists.
    for t in net.transitions:
        if not net.pre[t]:
            return None
    prob = pulp.LpProblem("deadlock", pulp.LpMaximize)
    x = {p: pulp.LpVariable(f"x_{p}", lowBound=0, upBound=1, cat="Binary") for p in net.places}
    prob += 0  # no objective

    for t in net.transitions:
        # sum(1 - x_p for p in pre(t)) >= 1 => at least one pre-place is unmarked
        prob += pulp.lpSum(1 - x[p] for p in net.pre[t]) >= 1

    while True:
        status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
        if pulp.LpStatus[status] != "Optimal":
            return None
        sol_marked = set()
        for p in net.places:
            v = pulp.value(x[p])
            if v is None:
                v = 0.0
            if v >= 0.5:
                sol_marked.add(p)
        if _is_reachable_marking(bdd, reach, cur_vars, sol_marked):
            return sol_marked
        # nogood cut to exclude this assignment
        prob += (
            pulp.lpSum(x[p] for p in sol_marked)
            + pulp.lpSum(1 - x[p] for p in set(net.places) - sol_marked)
            <= len(net.places) - 1
        )


