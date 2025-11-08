Task 1 – PNML parsing

Goal
- Load a 1-safe P/T net from a PNML file and check consistency.

How to run
Use it indirectly via other tasks. As a smoke test:

```bash
python -m app.cli explicit --pnml pnml/mutual_exclusion.pnml
```

Expected
- Prints the number of reachable states. If the PNML is malformed, an error is raised.


