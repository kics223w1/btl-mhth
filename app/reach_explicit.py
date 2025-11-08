from collections import deque
from typing import Set, FrozenSet, List, Tuple

from .model import PetriNet, Marking


def reachable_bfs(net: PetriNet) -> Set[Marking]:
    start: Marking = frozenset(net.initial)
    visited: Set[Marking] = {start}
    q: deque[Marking] = deque([start])
    while q:
        m = q.popleft()
        for t in net.enabled(m):
            m2 = net.fire(m, t)
            if m2 not in visited:
                visited.add(m2)
                q.append(m2)
    return visited


