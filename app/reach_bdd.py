from __future__ import annotations

from typing import Dict, Set, Tuple
from dd.autoref import BDD

from .model import PetriNet


def _eq(bdd: BDD, a, b):
    return (~a | b) & (~b | a)


def build_bdd_manager(places) -> Tuple[BDD, Dict[str, str]]:
    bdd = BDD()
    order = []
    for p in places:
        order.append(p)
        order.append(f"{p}'")
    bdd.declare(*order)
    return bdd, {p: f"{p}'" for p in places}


def encode_relation(bdd: BDD, net: PetriNet) -> Tuple[BDD, Dict[str, object], Dict[str, object]]:
    cur_vars = {p: bdd.var(p) for p in net.places}
    nxt_vars = {p: bdd.var(f"{p}'") for p in net.places}

    R = bdd.false
    for t in net.transitions:
        en = bdd.true
        for p in net.pre[t]:
            en &= cur_vars[p]
        rel = en
        for p in net.places:
            if p in net.post[t] and p not in net.pre[t]:
                rel &= nxt_vars[p]
            elif p in net.pre[t] and p not in net.post[t]:
                rel &= ~nxt_vars[p]
            elif p in net.pre[t] and p in net.post[t]:
                rel &= nxt_vars[p]
            else:
                rel &= _eq(bdd, cur_vars[p], nxt_vars[p])
        R |= rel
    return R, cur_vars, nxt_vars


def cube_from_marking(bdd: BDD, cur_vars: Dict[str, object], marked: Set[str]):
    node = bdd.true
    for p, var in cur_vars.items():
        node &= var if p in marked else ~var
    return node


def reachability_bdd(net: PetriNet):
    bdd, primed = build_bdd_manager(net.places)
    R, cur, nxt = encode_relation(bdd, net)
    # Quantify over current-state variable NAMES (strings), not BDD nodes
    cur_space = set(cur.keys())

    reach = cube_from_marking(bdd, cur, net.initial)
    while True:
        img = bdd.exist(cur_space, reach & R)
        # Rename primed variable NAMES to current-state nodes
        ren = {f"{p}'": cur[p] for p in net.places}
        img_cur = bdd.let(ren, img)
        nxt_reach = reach | img_cur
        if nxt_reach == reach:
            break
        reach = nxt_reach
    return bdd, reach, cur, nxt


def count_reachable(bdd: BDD, reach) -> int:
    n = 0
    for _ in bdd.pick_iter(reach):
        n += 1
    return n


