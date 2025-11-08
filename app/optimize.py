from __future__ import annotations

from typing import Dict, Optional, Set, Tuple

import pulp
from dd.autoref import BDD

from .model import PetriNet
from .reach_bdd import cube_from_marking


def _is_reachable_marking(bdd: BDD, reach, cur_vars: Dict[str, object], marked: Set[str]) -> bool:
    cube = cube_from_marking(bdd, cur_vars, marked)
    return (cube & reach) != bdd.false


def maximize_over_reach(
    net: PetriNet,
    bdd: BDD,
    reach,
    cur_vars: Dict[str, object],
    weights: Dict[str, int],
) -> Optional[Tuple[Set[str], int]]:
    prob = pulp.LpProblem("optimize", pulp.LpMaximize)
    x = {p: pulp.LpVariable(f"x_{p}", lowBound=0, upBound=1, cat="Binary") for p in net.places}
    prob += pulp.lpSum(weights.get(p, 0) * x[p] for p in net.places)

    # No extra constraints; feasible region is {0,1}^{|P|}. BDD filters reachability.
    best_marking: Optional[Set[str]] = None
    best_val: Optional[int] = None

    while True:
        status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
        if pulp.LpStatus[status] != "Optimal":
            return None
        sol_marked: Set[str] = set()
        for p in net.places:
            v = pulp.value(x[p])
            if v is None:
                v = 0.0
            if v >= 0.5:
                sol_marked.add(p)
        if _is_reachable_marking(bdd, reach, cur_vars, sol_marked):
            val = int(round(sum(weights.get(p, 0) for p in sol_marked)))
            return sol_marking_or_update(best_marking, best_val, sol_marked, val)
        # exclude current assignment and continue
        prob += (
            pulp.lpSum(x[p] for p in sol_marked)
            + pulp.lpSum(1 - x[p] for p in set(net.places) - sol_marked)
            <= len(net.places) - 1
        )


def sol_marking_or_update(
    best_marking: Optional[Set[str]],
    best_val: Optional[int],
    cand_marking: Set[str],
    cand_val: int,
):
    return cand_marking, cand_val


