Task 4 – Deadlock detection (ILP + BDD)

Goal
- Find a reachable dead marking (no enabled transitions).

Method
- ILP proposes a dead marking; BDD checks reachability.
- If unreachable, add a nogood cut and repeat.

Run
```bash
python -m app.cli deadlock --pnml pnml/deadlock_reachable.pnml
```


