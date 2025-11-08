Task 3 – BDD-based reachability

Goal
- Symbolically construct the reachable set using a transition relation and relational product.

Run
```bash
python -m app.cli bdd --pnml pnml/simple_fork_join.pnml
```

Notes
- Boolean variable per place (current and primed).
- Image: ∃M. X(M) ∧ R(M,M'), then rename M'→M.


