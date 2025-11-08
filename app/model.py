from dataclasses import dataclass
from typing import Dict, List, Set, FrozenSet


Marking = FrozenSet[str]


@dataclass
class PetriNet:
    places: List[str]
    transitions: List[str]
    pre: Dict[str, Set[str]]       # transition -> set(place)
    post: Dict[str, Set[str]]      # transition -> set(place)
    initial: Set[str]

    def place_index(self) -> Dict[str, int]:
        return {p: i for i, p in enumerate(self.places)}

    def enabled(self, marking: Marking) -> List[str]:
        enabled_ts: List[str] = []
        for t in self.transitions:
            if self.pre[t].issubset(marking):
                enabled_ts.append(t)
        return enabled_ts

    def fire(self, marking: Marking, transition: str) -> Marking:
        # 1-safe semantics: remove pre, add post
        after = set(marking)
        after.difference_update(self.pre[transition])
        after.update(self.post[transition])
        return frozenset(after)


