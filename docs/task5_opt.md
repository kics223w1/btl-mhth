Task 5 – Optimization over reachable markings

Goal
- Maximize a linear objective c^T M over the reachable set.

Run
```bash
python -m app.cli optimize --pnml pnml/choice_conflict.pnml --weights p1=1,p2=2
```

Notes
- ILP searches for an optimal marking; BDD filters for reachability.
- Adds nogood cuts until a reachable optimum is found or infeasible.


