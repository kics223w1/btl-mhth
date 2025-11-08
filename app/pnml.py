from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Dict, Set, Tuple, List

from .model import PetriNet


NS = {"pnml": "http://www.pnml.org/version-2009/grammar/pnml"}


def _text(elem: ET.Element) -> str:
    return elem.text or ""


def load_pnml(path: str) -> PetriNet:
    tree = ET.parse(path)
    root = tree.getroot()
    net = root.find("pnml:net", NS)
    if net is None:
        raise ValueError("Missing <net>")
    page = net.find("pnml:page", NS)
    if page is None:
        raise ValueError("Missing <page>")

    places: Dict[str, Dict] = {}
    transitions: Dict[str, Dict] = {}
    arcs: List[Tuple[str, str, str]] = []  # (id, source, target)

    for pl in page.findall("pnml:place", NS):
        pid = pl.get("id")
        if pid is None:
            raise ValueError("Place without id")
        if pid in places:
            raise ValueError(f"Duplicate place id: {pid}")
        init = 0
        im = pl.find("pnml:initialMarking", NS)
        if im is not None:
            txt = im.find("pnml:text", NS)
            if txt is not None:
                try:
                    init = int(_text(txt).strip())
                except ValueError:
                    init = 0
        places[pid] = {"initial": init}

    for tr in page.findall("pnml:transition", NS):
        tid = tr.get("id")
        if tid is None:
            raise ValueError("Transition without id")
        if tid in transitions:
            raise ValueError(f"Duplicate transition id: {tid}")
        transitions[tid] = {}

    for ar in page.findall("pnml:arc", NS):
        aid = ar.get("id") or ""
        src = ar.get("source")
        tgt = ar.get("target")
        if not src or not tgt:
            raise ValueError(f"Arc {aid} missing source/target")
        arcs.append((aid, src, tgt))

    # Consistency
    node_ids = set(places) | set(transitions)
    for (aid, src, tgt) in arcs:
        if src not in node_ids:
            raise ValueError(f"Arc {aid} references unknown node: {src}")
        if tgt not in node_ids:
            raise ValueError(f"Arc {aid} references unknown node: {tgt}")

    pre: Dict[str, Set[str]] = {t: set() for t in transitions}
    post: Dict[str, Set[str]] = {t: set() for t in transitions}
    for (_aid, src, tgt) in arcs:
        if src in places and tgt in transitions:
            pre[tgt].add(src)
        elif src in transitions and tgt in places:
            post[src].add(tgt)
        else:
            # Either place->place or transition->transition, which we do not support here
            raise ValueError(f"Unsupported arc direction: {src} -> {tgt}")

    initial = {p for p, meta in places.items() if meta["initial"] > 0}
    return PetriNet(
        places=list(places.keys()),
        transitions=list(transitions.keys()),
        pre=pre,
        post=post,
        initial=initial,
    )


