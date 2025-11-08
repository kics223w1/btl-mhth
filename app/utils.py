from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Dict


@contextmanager
def timer():
    t0 = time.perf_counter()
    yield lambda: time.perf_counter() - t0


def parse_weights(raw: str) -> Dict[str, int]:
    if not raw:
        return {}
    out: Dict[str, int] = {}
    parts = [p for p in raw.split(",") if p]
    for part in parts:
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        try:
            out[k.strip()] = int(v.strip())
        except ValueError:
            pass
    return out


