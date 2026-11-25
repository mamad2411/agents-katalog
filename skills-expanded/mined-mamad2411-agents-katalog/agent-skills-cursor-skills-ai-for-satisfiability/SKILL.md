# AI for Satisfiability

## Description

Guide CDCL SAT solver branching and resets with offline neural predictions to solve more competition instances without GPU overhead.

## When to use

You want to solve Boolean satisfiability, MaxSAT, QSAT, or SMT problems faster by using machine learning for branching, restarts, or end-to-end search.

## Usage

- Improve CDCL and local-search SAT solvers with learned branching and restart policies.
- Build end-to-end neural SAT solvers to predict satisfiability and assignments.
- Combine neural guidance with CDCL variable activity in hybrid solvers.
- Learn heuristics for quantified and theory-laden satisfiability problems.

## Steps

1. Curate SAT/SMT/QSAT training instances close to the target problem distribution.
2. Train a neural model or learned heuristic to predict satisfiability, assignments, or variable activity.
3. Integrate the learned guidance into a CDCL or local-search solver.
4. Benchmark the hybrid, pure neural, and classical solvers on the target instance family.
5. Train on a distribution close to the target and test generalization across domains.
6. Compare runtimes and solution quality on SAT-COMP or SMT-LIB benchmarks.

## Code pattern

```python
import torch
import torch.nn as nn

# Simplified message-passing module for a graph neural SAT solver
class MessagePassingSAT(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.L_init = nn.Linear(1, dim)
        self.C_init = nn.Linear(1, dim)
        self.L_update = nn.GRUCell(dim, dim)
        self.C_update = nn.GRUCell(dim, dim)

    def forward(self, L, C, var_to_clauses, clause_to_vars):
        # Message passing between literals and clauses
        return self.L_update(C[clause_to_vars].mean(dim=1), L)
```

## Tuning notes

- Hybrid solvers usually outperform pure neural SAT solvers on industrial instances.
- Train on a distribution close to the target problem; generalization across domains is hard.
- Use unsat-core prediction for CDCL guidance rather than full assignment prediction.

## Verification

1. Train NeuroSAT on random 3-SAT and evaluate on graph-coloring encodings.
2. Integrate a learned branching heuristic into a CDCL solver and run SAT-COMP benchmarks.
3. Compare pure neural, hybrid, and classical solvers on a family of problem instances.

## References

- https://github.com/dselsam/neurosat
- https://arxiv.org/pdf/1802.03685
- https://doi.org/10.48550/arxiv.2203.04755
- https://doi.org/10.1561/2200000081
- https://doi.org/10.1609/socs.v18i1.35997
