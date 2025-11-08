Mathematical Modeling – CO2011
Symbolic and Algebraic Reasoning in Petri Nets (Toolkit)

Overview
- Parse PNML 1-safe P/T nets
- Explicit reachability (BFS)
- Symbolic reachability with BDD
- Deadlock detection via ILP + BDD
- Linear optimization over reachable markings

Quick start
1) Create a virtual environment (optional)
2) Install deps:
   pip install -r requirements.txt
3) Try explicit reachability:
   python -m app.cli explicit --pnml pnml/mutual_exclusion.pnml
4) Try BDD reachability:
   python -m app.cli bdd --pnml pnml/mutual_exclusion.pnml
5) Deadlock detection:
   python -m app.cli deadlock --pnml pnml/deadlock_reachable.pnml
6) Optimization example:
   python -m app.cli optimize --pnml pnml/choice_conflict.pnml --weights p1=1,p2=2

Structure
- app/: source code
- docs/: short readmes for each task
- pnml/: example models (provided)

Notes
- Models are assumed 1-safe as per assignment.
- If CBC solver is missing, PuLP will try to use the default solver. See docs if needed.

# btl-mhth
