Mathematical Modeling – CO2011
Symbolic and Algebraic Reasoning in Petri Nets (Toolkit)

Overview

- Parse PNML 1-safe P/T nets
- Explicit reachability (BFS)
- Symbolic reachability with BDD
- Deadlock detection via ILP + BDD
- Linear optimization over reachable markings

Quick start

1. Create a virtual environment (recommended)
   python3 -m venv .venv
2. Activate the environment
   macOS/Linux (bash/zsh):
   . .venv/bin/activate
   fish:
   . .venv/bin/activate.fish
   Windows PowerShell:
   .venv\Scripts\Activate.ps1
3. Install dependencies
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
4. Run commands (after activation)
   Explicit reachability:
   python -m app.cli explicit --pnml pnml/mutual_exclusion.pnml
   BDD reachability:
   python -m app.cli bdd --pnml pnml/mutual_exclusion.pnml
   Deadlock detection:
   python -m app.cli deadlock --pnml pnml/deadlock_reachable.pnml
   Optimization example:
   python -m app.cli optimize --pnml pnml/choice_conflict.pnml --weights p1=1,p2=2

Structure

- app/: source code
- docs/: short readmes for each task
- pnml/: example models (provided)

Notes

- Models are assumed 1-safe as per assignment.
- If CBC solver is missing, PuLP will try to use the default solver. See docs if needed.

# Commands cheat sheet

- explicit: enumerate reachable markings with BFS
  python -m app.cli explicit --pnml <path-to-pnml>
- bdd: symbolic reachability with BDD, reports count
  python -m app.cli bdd --pnml <path-to-pnml>
- deadlock: ILP+BDD search for a reachable dead marking
  python -m app.cli deadlock --pnml <path-to-pnml>
- optimize: maximize linear objective over reachable markings
  python -m app.cli optimize --pnml <path> --weights p1=2,p2=-1

# Troubleshooting

- ModuleNotFoundError (dd or pulp): ensure the venv is activated and run:
  python -m pip install -r requirements.txt
- Slow or timed-out installs: rerun the install; optionally:
  python -m pip install --upgrade pip setuptools wheel
- CBC not found (rare): install COIN-OR CBC, e.g. on macOS:
  brew install coin-or-tools/coinor/cbc
  or via conda:
  conda install -c conda-forge coincbc
- PowerShell activation policy (Windows):
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
