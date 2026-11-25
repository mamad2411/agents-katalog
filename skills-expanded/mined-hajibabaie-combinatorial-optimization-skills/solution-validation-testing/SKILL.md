---
name: solution-validation-testing
description: When the user wants to verify optimization code: independent feasibility checkers, objective recomputation separate from the solver, unit tests for constraint builders and operators, known-optimum regression tests, and exact-vs-heuristic cross-validation on small instances. Also use when the user mentions "validate solution," "feasibility checker," "test optimization code," "verify objective," "regression test optimum," or when a heuristic appears to beat a proven optimum. For repairing infeasible solutions, see constraint-handling-techniques; for seeded test instances, see instance-generation-and-benchmarks.
---

# Solution Validation and Testing

You are an expert in validating optimization code: establishing, before anyone else asks, that reported solutions are feasible, that objectives are computed correctly, and that claimed improvements are real. This skill covers the five-layer validation stack — independent feasibility checkers, objective recomputation separate from the model, unit tests for constraint builders and operators, known-optimum regression tests, and exact-vs-heuristic cross-validation on small instances. Use the protocols below whenever optimization results will be trusted, published, or acted on. Hooker (1995, "Testing Heuristics: We Have It All Wrong") and Johnson (2002, "A Theoretician's Guide to the Experimental Analysis of Algorithms") both observed that most reported algorithm comparisons fail at exactly this layer: the code computing the numbers was never independently checked.

## Initial Assessment

Establish these facts before writing any validation code. The answers determine which layers of the stack you need and how deep each must go.

- **Map every place a solution is born or transformed.** Solver extraction (`.X` values), construction heuristics, decoders, crossover/mutation operators, repair routines, local-search moves, file deserialization. Each is a validation boundary; a checker call belongs at every one of them.
- **List the constraint families from the problem statement, not from the model code.** The checker must be derived from the written specification. If the only description of a constraint is the model code itself, write the prose statement first — that document is what the checker implements.
- **Pin down the objective convention exactly.** Minimization or maximization; units; rounding rules (TSPLIB `EUC_2D` rounds each distance to the nearest integer — Reinelt 1991, "TSPLIB — A Traveling Salesman Problem Library"); whether soft-constraint penalties are part of the reported objective or reported separately.
- **Inventory the ground-truth sources.** Brute-forceable instance sizes, published optima (OR-Library — Beasley 1990; MIPLIB; TSPLIB; QAPLIB), a second solver, a trusted prior implementation. No ground truth at any size means metamorphic testing carries more weight (see Advanced Techniques).
- **Record the solver tolerances in play.** Gurobi defaults: `IntFeasTol` 1e-5, `FeasibilityTol` 1e-6, `MIPGap` 1e-4. A solution the solver calls optimal can violate exact integrality and exact feasibility by these amounts; the checker must handle that boundary deliberately.
- **Separate hard constraints from soft ones.** Hard violations make a solution invalid; soft violations are costs. The checker must report them differently, and the objective recomputation must include penalty terms with the documented weights.
- **Check for shared code between pipelines.** If the heuristic, the exact model, and the "checker" all call the same objective function, one bug makes all three agree. Shared code is the single most common cause of false validation confidence.
- **Establish reproducibility of failures.** Are instances generated with seeds? Is every run's (instance, seed, parameters) tuple recorded? A validation failure that cannot be reproduced cannot be fixed.
- **Set the compute budget per test tier.** Per-commit suites should run in seconds without a solver license; nightly suites can afford small exact solves. Decide the budget now so the suite is actually run.
- **Determine what is already tested.** Existing pytest suites, ad-hoc assertion scripts, manual spot checks. Fold them into the stack rather than duplicating them.
- **Assess the cost of a wrong answer.** A paper result, a production planning decision, or a thesis chapter each justify the full stack; a throwaway prototype may justify only layers 1-2. Scale effort to consequence, but never skip layer 1.

## The Validation Stack

Five layers, ordered by how early they catch a bug and how much machinery they need. Build them in this order; each layer assumes the ones below it exist.

| Layer | Artifact | What it catches | Typical cost |
|---|---|---|---|
| 1. Independent feasibility checker | `check_problem(instance, solution) -> report` | missing or wrong constraints in the model, decoder bugs, broken repair operators, corrupted solution files | half a day to write; milliseconds per call |
| 2. Objective recomputation | independent objective function inside the checker | wrong coefficients, missing terms, sense errors, delta-evaluation drift, big-M leakage into the objective | comes with layer 1 |
| 3. Component unit tests | pytest suite per constraint builder, operator, decoder | sign errors, index off-by-one, operators that break representation invariants, delta evaluation that disagrees with full evaluation | minutes per component |
| 4. Known-optimum regression | pinned `(instance, optimum)` fixtures | silent behavior changes after refactors, parameter changes, dependency upgrades | brute force once; fast forever after |
| 5. Exact-vs-heuristic cross-validation | harness over a bed of seeded small instances | systematic disagreement between two whole pipelines that both look correct in isolation | small exact solves, nightly |

Formally, a checker is a function built only from the raw instance data $D$ and the written problem statement:

$$
\text{check}: (D, s) \;\mapsto\; \big(\, \text{feasible}(s) \in \{\text{true}, \text{false}\},\;\; V(s),\;\; \hat{f}(s) \,\big)
$$

where $V(s)$ is the list of specific violations (never just a boolean) and $\hat{f}(s)$ is the independently recomputed objective. The **independence rule**: the only inputs the checker shares with the solver or heuristic are $D$ and the specification. No shared functions, no shared distance matrix builder, no shared penalty code. The checker is the specification in executable form, so it should be written in the most boring style available — plain loops, no cleverness, no performance tricks. Slow and obviously correct beats fast and probably correct here, because the checker is the court of last appeal.

Objective reconciliation uses a mixed absolute/relative tolerance:

$$
|f_{\text{solver}}(s) - \hat{f}(s)| \;\le\; \varepsilon_{\text{abs}} + \varepsilon_{\text{rel}} \cdot |\hat{f}(s)|
$$

with $\varepsilon_{\text{abs}} = \varepsilon_{\text{rel}} = 10^{-6}$ as a sane default for well-scaled data. Anything looser hides bugs; anything tighter generates false alarms from solver tolerances.

One asymmetry deserves emphasis because it drives the cross-validation protocol: **a heuristic that beats a proven optimum has not found a better solution — it has found a bug.** Either the heuristic's solution is infeasible (heuristic bug), or the exact model solves a different problem than the heuristic does (model bug). The independent checker is the arbiter: validate both solutions against the raw data and the side whose solution fails is the side that is wrong.

### Decision tree

```text
START: do you trust this optimization result?
|
+-- New project, no validation yet?
|     -> Build layer 1 (checker) and layer 2 (recomputation) BEFORE the first
|        real experiment. Add layer 3 alongside the first constraint builder
|        or operator. Add layers 4-5 as soon as a tiny instance solves.
|
+-- One solution looks suspicious?
|     -> Run layers 1+2 on it.
|        Infeasible        -> trace the violated family to the builder,
|                             decoder, or operator that owns it (layer 3).
|        Objective mismatch-> diff the objective term by term; check sense,
|                             rounding convention, penalty weights.
|
+-- Heuristic reports a better objective than the exact method?
|     -> Validate BOTH solutions with layers 1+2 against raw data.
|        Heuristic solution infeasible -> heuristic bug: missing constraint
|                                         check, incomplete repair.
|        Heuristic solution feasible   -> the exact model is wrong or solves
|                                         a different problem: audit each
|                                         constraint builder against the spec.
|
+-- Refactor, dependency upgrade, or parameter change planned?
|     -> Layer 4 regression suite green before AND after. Pin objective
|        values, never solution vectors (ties and symmetry break the latter).
|
+-- Results headed into a paper or a production decision?
      -> Full layer 5 sweep on small instances, layers 1+2 on every reported
         solution, and archive the validation table next to the result table.
```

### Symptom-to-layer diagnosis

| Symptom | Layer that catches it | Usual root cause |
|---|---|---|
| Solver says optimal, answer is operationally nonsense | 1 | a constraint family missing from the model |
| Reported objective differs from a hand calculation | 2 | sense error, missing term, wrong rounding convention |
| Metaheuristic results degrade after an "equivalent" refactor | 4 | delta evaluation drifted from full evaluation |
| Heuristic "beats" the exact optimum | 5 (then 1 arbitrates) | the two pipelines solve different problems |
| Crash or garbage only on some instances | 3 | operator violates a representation invariant on edge cases |
| Two formulations of the same model disagree | 5 / differential testing | one formulation's builder is wrong |

## Layers 1 and 2 — Independent Feasibility Checking and Objective Recomputation

Design rules for checkers, in order of importance:

1. **Read only raw instance data.** Coordinates, demands, capacities — not the model's preprocessed arrays, not the heuristic's distance matrix. If preprocessing has a bug, a checker that consumes preprocessed data inherits it.
2. **Collect every violation with a specific message.** A boolean checker tells you that something is wrong; a violation list tells you what to fix and which component owns the bug. Do not stop at the first violation.
3. **Recompute the objective even when infeasible.** The objective of an infeasible solution is still diagnostic — a heuristic that is 2% better and slightly infeasible is a constraint-handling problem, not an objective problem.
4. **Keep it deliberately simple.** Plain Python loops over the specification. The checker for a problem with an $O(n)$ evaluation may be $O(n^2)$; it runs on demand, not in the inner loop.
5. **Return a structured report**, so harnesses (layer 5) and CI can consume it without parsing strings.

The end-to-end example below is a CVRP checker — a good template because the CVRP has several independent constraint families (vehicle count, visit-exactly-once, capacity) plus a distance objective with an explicit convention.

```python
"""Independent feasibility checker and objective recomputation for the CVRP.

The checker reads only raw instance data (coordinates, demands, capacity).
It never imports the model or heuristic code, so a bug there cannot hide here.
"""
from dataclasses import dataclass, field
import math


@dataclass(frozen=True)
class CVRPInstance:
    """Raw CVRP data. Node 0 is the depot."""
    coords: tuple[tuple[float, float], ...]   # (x, y) per node, depot first
    demands: tuple[int, ...]                  # demand per node, demands[0] == 0
    capacity: int
    n_vehicles: int


@dataclass
class ValidationReport:
    """Outcome of one validation pass."""
    feasible: bool
    objective: float
    violations: list[str] = field(default_factory=list)

    def add(self, message: str) -> None:
        """Record a violation and mark the report infeasible."""
        self.feasible = False
        self.violations.append(message)


def euclid(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Plain Euclidean distance — the documented objective convention."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def check_cvrp(instance: CVRPInstance, routes: list[list[int]]) -> ValidationReport:
    """Validate routes against raw data and recompute the objective.

    Each route is a customer sequence without the depot, e.g. [3, 1, 4].
    Checks: vehicle count, valid node ids, capacity, visit-exactly-once.
    """
    report = ValidationReport(feasible=True, objective=0.0)
    n = len(instance.coords)

    if len(routes) > instance.n_vehicles:
        report.add(f"{len(routes)} routes used, only "
                   f"{instance.n_vehicles} vehicles available")

    seen: dict[int, int] = {}
    for r_idx, route in enumerate(routes):
        load = 0
        for node in route:
            if not 1 <= node < n:
                report.add(f"route {r_idx}: invalid node id {node}")
                continue
            seen[node] = seen.get(node, 0) + 1
            load += instance.demands[node]
        if load > instance.capacity:
            report.add(f"route {r_idx}: load {load} exceeds "
                       f"capacity {instance.capacity}")
        path = [0, *route, 0]
        report.objective += sum(
            euclid(instance.coords[u], instance.coords[v])
            for u, v in zip(path, path[1:])
        )

    for customer in range(1, n):
        count = seen.get(customer, 0)
        if count != 1:
            report.add(f"customer {customer} visited {count} times, expected 1")
    return report


def reconcile_objective(model_obj: float, checker_obj: float,
                        abs_tol: float = 1e-6, rel_tol: float = 1e-6) -> bool:
    """True when the solver objective matches the recomputation within tolerance."""
    return abs(model_obj - checker_obj) <= abs_tol + rel_tol * abs(checker_obj)


# Tiny synthetic instance: depot at the origin, 4 customers.
inst = CVRPInstance(
    coords=((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (2.0, 0.0)),
    demands=(0, 3, 3, 3, 3),
    capacity=6,
    n_vehicles=2,
)
good = check_cvrp(inst, [[1, 2], [3, 4]])
bad = check_cvrp(inst, [[1, 2, 3], [4]])     # route 0 carries 9 > 6
print(good.feasible, round(good.objective, 4), bad.feasible, bad.violations[0])
# Expected: True 7.4142 False route 0: load 9 exceeds capacity 6
```

The second half of layers 1-2 is the boundary where solutions leave a MIP solver. Two rules: never read `.X` without checking `Status` and `SolCount` first, and never trust raw `.X` values of integer variables — they can sit `IntFeasTol` away from an integer. Round, measure the drift, and refuse to round when drift is large (large drift signals a numerically unstable model, not a rounding problem — see Klotz & Newman 2013, "Practical Guidelines for Solving Difficult Mixed Integer Linear Programs").

```python
"""Extract a rounded solution from a solved Gurobi model, then re-verify it
from raw data. Never trust raw .X values of integer variables."""
import gurobipy as gp
from gurobipy import GRB


def extract_binary_solution(model: gp.Model, x: gp.tupledict) -> dict:
    """Round binary variables to {0,1} after checking solution availability."""
    if model.Status not in (GRB.OPTIMAL, GRB.TIME_LIMIT) or model.SolCount == 0:
        raise RuntimeError(f"no solution to extract (status {model.Status})")
    solution = {key: int(round(var.X)) for key, var in x.items()}
    drift = max(abs(var.X - round(var.X)) for var in x.values())
    if drift > 1e-4:  # far beyond default IntFeasTol=1e-5: investigate scaling
        raise RuntimeError(f"integrality drift {drift:.2e} too large to round")
    return solution


# Tiny demonstration: 0-1 knapsack, extract, then recheck from raw data.
values = [10, 13, 7]
weights = [4, 5, 3]
cap = 8
m = gp.Model("knapsack")
m.Params.OutputFlag = 0
y = m.addVars(3, vtype=GRB.BINARY, name="y")
m.addConstr(gp.quicksum(weights[i] * y[i] for i in range(3)) <= cap,
            name="capacity")
m.setObjective(gp.quicksum(values[i] * y[i] for i in range(3)), GRB.MAXIMIZE)
m.optimize()
sol = extract_binary_solution(m, y)
chosen = [i for i in range(3) if sol[i] == 1]
recomputed = sum(values[i] for i in chosen)        # independent of the model
weight_ok = sum(weights[i] for i in chosen) <= cap
print(chosen, recomputed, weight_ok, abs(m.ObjVal - recomputed) < 1e-6)
# Expected: [1, 2] 20 True True
```

## Layer 3 — Unit Tests for Constraint Builders and Operators

Constraint builders (the `add_<family>_constraints` functions a well-structured model is made of — see **milp-modeling-gurobi**) are ordinary functions and deserve ordinary unit tests. The most effective strategy is **probing**: fix the variables to a hand-built solution with known feasibility status, then ask the solver whether the fixed model is feasible. This tests the builder against the problem statement, not against itself. Complement probing with structural assertions: constraint counts, constraint names, and objective coefficients read back from the model.

The running example is the generalized assignment problem (GAP): assign each job to exactly one machine at minimum cost, subject to machine capacities. Save this block as `gap_model.py`; the test and harness blocks import it — the tests must import the code under test, never re-implement it.

```python
"""Generalized assignment model in gurobipy, built from named constraint
builders. Save as gap_model.py. Builders are separate functions so unit
tests can exercise each constraint family in isolation."""
import gurobipy as gp
from gurobipy import GRB
import numpy as np


def add_assignment_constraints(model: gp.Model, x: gp.tupledict,
                               n_machines: int, n_jobs: int) -> None:
    """Each job goes to exactly one machine."""
    for j in range(n_jobs):
        model.addConstr(
            gp.quicksum(x[i, j] for i in range(n_machines)) == 1,
            name=f"assign[{j}]",
        )


def add_capacity_constraints(model: gp.Model, x: gp.tupledict,
                             a: np.ndarray, b: np.ndarray) -> None:
    """Total resource use on each machine stays within its capacity."""
    n_machines, n_jobs = a.shape
    for i in range(n_machines):
        model.addConstr(
            gp.quicksum(a[i, j] * x[i, j] for j in range(n_jobs)) <= b[i],
            name=f"capacity[{i}]",
        )


def build_gap_model(c: np.ndarray, a: np.ndarray,
                    b: np.ndarray) -> tuple[gp.Model, gp.tupledict]:
    """Minimize assignment cost s.t. one-machine-per-job and capacities."""
    n_machines, n_jobs = c.shape
    model = gp.Model("gap")
    model.Params.OutputFlag = 0
    x = model.addVars(n_machines, n_jobs, vtype=GRB.BINARY, name="x")
    add_assignment_constraints(model, x, n_machines, n_jobs)
    add_capacity_constraints(model, x, a, b)
    model.setObjective(
        gp.quicksum(c[i, j] * x[i, j]
                    for i in range(n_machines) for j in range(n_jobs)),
        GRB.MINIMIZE,
    )
    return model, x


if __name__ == "__main__":
    # Tiny synthetic instance: 2 machines, 3 jobs.
    c = np.array([[4.0, 2.0, 5.0], [3.0, 6.0, 1.0]])
    a = np.array([[3.0, 2.0, 4.0], [2.0, 4.0, 2.0]])
    b = np.array([5.0, 5.0])
    model, x = build_gap_model(c, a, b)
    model.optimize()
    assignment = dict(sorted((j, i) for (i, j) in x if x[i, j].X > 0.5))
    print(model.Status == GRB.OPTIMAL, round(model.ObjVal, 1), assignment)
# Expected: True 6.0 {0: 1, 1: 0, 2: 1}
```

The probing tests. Note `DualReductions = 0` so an infeasible fixed model reports `INFEASIBLE` rather than the ambiguous `INF_OR_UNBD`.

```python
"""Unit tests for the GAP constraint builders. Save as test_gap_builders.py
and run with: pytest test_gap_builders.py -q

Strategy: probe each constraint family with hand-built assignments whose
feasibility is known from the problem statement; add structural assertions
on counts, names, and objective coefficients."""
import gurobipy as gp
from gurobipy import GRB
import numpy as np

from gap_model import build_gap_model


def fix_and_solve(model: gp.Model, x: gp.tupledict,
                  assignment: dict[int, int]) -> int:
    """Fix x to the given job->machine map and return the Gurobi status."""
    model.Params.DualReductions = 0   # report INFEASIBLE, not INF_OR_UNBD
    for (i, j), var in x.items():
        value = 1.0 if assignment.get(j) == i else 0.0
        var.LB = value
        var.UB = value
    model.optimize()
    return model.Status


def small_instance() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """2 machines x 3 jobs; capacities chosen so some assignments overload."""
    c = np.array([[4.0, 2.0, 5.0], [3.0, 6.0, 1.0]])
    a = np.array([[3.0, 2.0, 4.0], [2.0, 4.0, 2.0]])
    b = np.array([5.0, 5.0])
    return c, a, b


def test_feasible_assignment_accepted() -> None:
    """A hand-checked feasible assignment must keep the model feasible."""
    model, x = build_gap_model(*small_instance())
    status = fix_and_solve(model, x, {0: 1, 1: 0, 2: 1})  # loads: m0=2, m1=4
    assert status == GRB.OPTIMAL


def test_overload_rejected() -> None:
    """Assigning all jobs to machine 0 overloads it (3+2+4 = 9 > 5)."""
    model, x = build_gap_model(*small_instance())
    status = fix_and_solve(model, x, {0: 0, 1: 0, 2: 0})
    assert status == GRB.INFEASIBLE


def test_constraint_counts_and_names() -> None:
    """One assignment row per job, one capacity row per machine, all named."""
    model, _ = build_gap_model(*small_instance())
    model.update()
    names = {constr.ConstrName for constr in model.getConstrs()}
    assert {"assign[0]", "assign[1]", "assign[2]"} <= names
    assert {"capacity[0]", "capacity[1]"} <= names
    assert model.NumConstrs == 5


def test_objective_coefficients_match_data() -> None:
    """Every x[i,j] must carry cost c[i,j] in the objective."""
    c, a, b = small_instance()
    model, x = build_gap_model(c, a, b)
    model.update()
    for (i, j), var in x.items():
        assert var.Obj == c[i, j]
# Expected: 4 passed when run under pytest with gap_model.py importable.
```

Metaheuristic components need a different test style: **seeded random property tests**. Instead of one hand-picked case, generate hundreds of random inputs from `np.random.default_rng(seed)` and assert an invariant that must hold for every one of them — the approach popularized by QuickCheck (Claessen & Hughes 2000, "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs"; the `hypothesis` library brings it to Python with automatic shrinking of failing cases). The two invariants below catch the two most damaging metaheuristic bugs in practice: operators that silently corrupt the representation, and delta evaluation that drifts away from full evaluation.

```python
"""Property tests for metaheuristic components: a permutation crossover and
2-opt delta evaluation. Seeded random cases, fully reproducible."""
import numpy as np


def order_crossover(p1: np.ndarray, p2: np.ndarray,
                    rng: np.random.Generator) -> np.ndarray:
    """OX: copy a random slice of p1, fill the rest in p2's order."""
    n = p1.size
    lo, hi = np.sort(rng.choice(n + 1, size=2, replace=False))
    child = -np.ones(n, dtype=int)
    child[lo:hi] = p1[lo:hi]
    fill = p2[~np.isin(p2, child[lo:hi])]
    child[np.flatnonzero(child < 0)] = fill
    return child


def tour_length(tour: np.ndarray, dist: np.ndarray) -> float:
    """Full O(n) recomputation — the trusted reference."""
    return float(dist[tour, np.roll(tour, -1)].sum())


def two_opt_delta(tour: np.ndarray, dist: np.ndarray, i: int, k: int) -> float:
    """O(1) length change of reversing tour[i+1..k] (requires i < k)."""
    n = tour.size
    a, b = tour[i], tour[(i + 1) % n]
    c, d = tour[k], tour[(k + 1) % n]
    return float(dist[a, c] + dist[b, d] - dist[a, b] - dist[c, d])


def test_ox_always_yields_permutation() -> None:
    """Invariant: OX output is a permutation of 0..n-1 for ANY parents."""
    rng = np.random.default_rng(42)
    for _ in range(500):
        n = int(rng.integers(2, 30))
        p1, p2 = rng.permutation(n), rng.permutation(n)
        child = order_crossover(p1, p2, rng)
        assert np.array_equal(np.sort(child), np.arange(n))


def test_delta_matches_full_recomputation() -> None:
    """Invariant: delta == new length - old length, within float tolerance."""
    rng = np.random.default_rng(7)
    for _ in range(500):
        n = int(rng.integers(4, 40))
        pts = rng.random((n, 2))
        dist = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)
        tour = rng.permutation(n)
        i, k = np.sort(rng.choice(n, size=2, replace=False))
        delta = two_opt_delta(tour, dist, int(i), int(k))
        new_tour = tour.copy()
        new_tour[i + 1:k + 1] = new_tour[i + 1:k + 1][::-1]
        full = tour_length(new_tour, dist) - tour_length(tour, dist)
        assert abs(delta - full) <= 1e-9 * (1.0 + abs(full)), (i, k, delta, full)


test_ox_always_yields_permutation()
test_delta_matches_full_recomputation()
print("operator property tests passed")
# Expected: operator property tests passed
```

The same pattern covers the other component types: a repair operator's output must always pass the layer-1 checker; a decoder must map every random-key vector to a valid phenotype; a neighborhood move applied and then undone must restore the original solution bit for bit. Write one invariant test per component, 200-500 random cases each, all seeded.

## Layers 4 and 5 — Known-Optimum Regression and Exact-vs-Heuristic Cross-Validation

Layer 4 needs ground truth. Three sources, in order of preference:

1. **Brute force on tiny instances.** Enumerate the full solution space. The reference solver must be more trustworthy than the code it judges, so it is written in the most naive style possible — no pruning, no cleverness. Sizes: permutations up to $n \approx 9$ ($9! \approx 3.6 \times 10^5$), machine assignments up to $m^n \approx 10^6$, subsets up to $n \approx 20$.
2. **Published optima** for standard benchmarks (OR-Library, TSPLIB, QAPLIB, MIPLIB). These also validate your instance *parser* — but only after you confirm the objective convention matches (see Practical Challenges).
3. **A previous trusted version** of your own pipeline, pinned by commit hash.

Pin the values as data in the test file. A pinned value is a contract: a failing regression test means behavior changed, and the change must be explained before the pin is updated.

```python
"""Brute-force GAP reference solver, seeded generator, and pinned regression
tests. Save as gap_reference.py; run the test with: pytest gap_reference.py -q

The brute force enumerates every machine choice per job: m^n combinations.
Keep n_jobs <= 8. It is deliberately naive — the reference must be more
trustworthy than the code it judges."""
import itertools

import numpy as np


def make_gap_instance(seed: int, n_machines: int,
                      n_jobs: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Seeded random GAP instance; capacities sized to keep most feasible."""
    rng = np.random.default_rng(seed)
    c = rng.integers(1, 20, size=(n_machines, n_jobs)).astype(float)
    a = rng.integers(1, 10, size=(n_machines, n_jobs)).astype(float)
    b = np.full(n_machines, np.ceil(1.3 * a.mean() * n_jobs / n_machines))
    return c, a, b


def brute_force_gap(c: np.ndarray, a: np.ndarray,
                    b: np.ndarray) -> tuple[float, tuple[int, ...]]:
    """Exact optimum by full enumeration: (cost, machine-per-job tuple)."""
    n_machines, n_jobs = c.shape
    best_cost, best_assign = float("inf"), ()
    for assign in itertools.product(range(n_machines), repeat=n_jobs):
        load = np.zeros(n_machines)
        for j, i in enumerate(assign):
            load[i] += a[i, j]
        if np.any(load > b + 1e-9):
            continue
        cost = float(sum(c[i, j] for j, i in enumerate(assign)))
        if cost < best_cost:
            best_cost, best_assign = cost, assign
    return best_cost, best_assign


# Pinned fixtures: (seed, n_machines, n_jobs) -> optimum, computed once by
# the brute force above and frozen. A red test means the generator or the
# reference changed behavior; explain the change before updating a pin.
KNOWN_OPTIMA: dict[tuple[int, int, int], float] = {
    (0, 3, 6): 33.0,
    (7, 3, 6): 45.0,
    (11, 3, 6): 38.0,
    (23, 3, 6): 18.0,
}


def test_known_optima_still_reproduced() -> None:
    """Regression: the (generator, reference) pair reproduces pinned optima."""
    for (seed, n_machines, n_jobs), pinned in KNOWN_OPTIMA.items():
        c, a, b = make_gap_instance(seed, n_machines, n_jobs)
        cost, _ = brute_force_gap(c, a, b)
        assert cost == pinned, f"seed {seed}: got {cost}, pinned {pinned}"


if __name__ == "__main__":
    test_known_optima_still_reproduced()
    best, arg = brute_force_gap(*make_gap_instance(0, 3, 6))
    print(best, arg)
# Expected: 33.0 (1, 1, 0, 0, 2, 0)
```

Layer 5 closes the loop: run the exact model and the heuristic over a bed of seeded small instances and assert five invariants per instance. Each invariant, when it fails, points at a specific component:

| Invariant | Statement (minimization) | A failure means |
|---|---|---|
| I1 | exact solution passes the independent checker | the model omits or mis-states a constraint, or the checker is stricter than the spec |
| I2 | exact objective reconciles with the checker's recomputation | objective coefficient bug, missing term, or big-M leakage into the objective |
| I3 | heuristic solution passes the independent checker | operator/decoder/repair violates a constraint family |
| I4 | heuristic objective $\ge$ optimum $-\,\varepsilon$ | the two pipelines solve different problems; the checker arbitrates which one is wrong |
| I5 | solver optimum equals brute-force optimum | the MIP formulation is wrong (or, rarely, the brute force is) |

The complete harness:

```python
"""Cross-validation harness: exact (Gurobi, MIPGap=0) versus a greedy +
first-improvement heuristic on a bed of seeded small GAP instances.

Invariants per instance:
  I1 exact solution passes the independent checker
  I2 exact objective reconciles with the recomputation
  I3 heuristic solution passes the independent checker
  I4 heuristic objective >= optimum - tol   (minimization)
  I5 Gurobi optimum == brute-force optimum
"""
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd

from gap_model import build_gap_model
from gap_reference import brute_force_gap, make_gap_instance


def check_gap(assign: dict[int, int], c: np.ndarray, a: np.ndarray,
              b: np.ndarray) -> tuple[bool, float, list[str]]:
    """Independent GAP checker: each job assigned once, capacities respected."""
    n_machines, n_jobs = c.shape
    violations: list[str] = []
    if sorted(assign) != list(range(n_jobs)):
        violations.append("not every job assigned exactly once")
    load = np.zeros(n_machines)
    cost = 0.0
    for j, i in assign.items():
        load[i] += a[i, j]
        cost += c[i, j]
    for i in np.flatnonzero(load > b + 1e-9):
        violations.append(f"machine {i}: load {load[i]:.1f} > "
                          f"capacity {b[i]:.1f}")
    return (not violations), cost, violations


def solve_exact(c: np.ndarray, a: np.ndarray, b: np.ndarray,
                time_limit: float = 30.0) -> tuple[float, dict[int, int]]:
    """Proven optimum via the gurobipy model."""
    model, x = build_gap_model(c, a, b)
    model.Params.MIPGap = 0.0
    model.Params.TimeLimit = time_limit
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"exact solve failed: status {model.Status}")
    assign = dict(sorted((j, i) for (i, j) in x if x[i, j].X > 0.5))
    return model.ObjVal, assign


def greedy_heuristic(c: np.ndarray, a: np.ndarray,
                     b: np.ndarray) -> dict[int, int]:
    """Cheapest-feasible-machine construction + first-improvement moves."""
    n_machines, n_jobs = c.shape
    load = np.zeros(n_machines)
    assign: dict[int, int] = {}
    for j in np.argsort(a.min(axis=0))[::-1]:        # biggest jobs first
        feasible = [i for i in range(n_machines)
                    if load[i] + a[i, j] <= b[i] + 1e-9]
        if not feasible:
            feasible = list(range(n_machines))       # overload: I3 will flag it
        i = min(feasible, key=lambda m: c[m, j])
        assign[int(j)] = i
        load[i] += a[i, j]
    improved = True
    while improved:
        improved = False
        for j in range(n_jobs):
            i_old = assign[j]
            for i_new in range(n_machines):
                if (c[i_new, j] < c[i_old, j]
                        and load[i_new] + a[i_new, j] <= b[i_new] + 1e-9):
                    load[i_old] -= a[i_old, j]
                    load[i_new] += a[i_new, j]
                    assign[j] = i_new
                    improved = True
                    break
    return assign


def cross_validate(seeds: list[int], n_machines: int,
                   n_jobs: int) -> pd.DataFrame:
    """Assert invariants I1-I5 on every seeded instance; one row per instance."""
    rows = []
    for seed in seeds:
        c, a, b = make_gap_instance(seed, n_machines, n_jobs)
        bf_cost, _ = brute_force_gap(c, a, b)
        if bf_cost == float("inf"):
            continue                                  # infeasible instance
        exact_obj, exact_assign = solve_exact(c, a, b)
        ok_e, cost_e, viol_e = check_gap(exact_assign, c, a, b)
        assert ok_e, f"seed {seed}: exact solution fails checker: {viol_e}"
        assert abs(exact_obj - cost_e) <= 1e-6 * (1 + abs(cost_e)), \
            f"seed {seed}: objective mismatch {exact_obj} vs {cost_e}"
        assert abs(exact_obj - bf_cost) <= 1e-6 * (1 + abs(bf_cost)), \
            f"seed {seed}: Gurobi {exact_obj} != brute force {bf_cost}"
        heur_assign = greedy_heuristic(c, a, b)
        ok_h, cost_h, viol_h = check_gap(heur_assign, c, a, b)
        assert ok_h, f"seed {seed}: heuristic infeasible: {viol_h}"
        assert cost_h >= exact_obj - 1e-6, \
            f"seed {seed}: heuristic {cost_h} beats proven optimum {exact_obj}"
        rows.append({"seed": seed, "optimum": bf_cost, "heuristic": cost_h,
                     "gap_pct": 100.0 * (cost_h - bf_cost) / bf_cost})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    table = cross_validate(seeds=list(range(20)), n_machines=3, n_jobs=7)
    print(table[["gap_pct"]].describe().loc[["mean", "max"]].round(1))
    print(f"validated {len(table)} instances, all invariants hold")
# Expected: gap_pct mean 8.2 and max 53.5 on these seeds, then
# "validated 20 instances, all invariants hold".
```

Two reading notes on the harness. First, I4 is an *invariant*, not a quality target — it must hold always; the heuristic's average gap (here 8.2%) is a benchmark observation that belongs in a monitored experiment table, never in an assert. Second, when I4 fires, resist the urge to "fix" the heuristic: run the checker on both solutions first. In practice the exact model is the guilty party about as often as the heuristic.

## Advanced Techniques

### Metamorphic testing of whole pipelines

When no ground truth exists at realistic sizes, test *relations between runs* instead of absolute values (Chen, Cheung & Yiu 1998, "Metamorphic Testing: A New Approach for Generating Next Test Cases"; Segura et al. 2016, "A Survey on Metamorphic Testing"). Useful relations for optimization pipelines: scaling all costs by $k > 0$ scales a minimum by exactly $k$; permuting entity labels leaves the optimum unchanged; relaxing a constraint (more capacity, longer deadline) never worsens a minimum; adding a dominated option (a machine worse in every cost and resource) leaves the optimum unchanged. These relations hold at *any* instance size, so they also validate the pipeline where brute force cannot reach.

```python
"""Metamorphic tests: transform the instance, predict the optimum's response.
No ground truth needed — the relation between two runs IS the oracle."""
import numpy as np

from gap_reference import brute_force_gap, make_gap_instance


def optimum(c: np.ndarray, a: np.ndarray, b: np.ndarray) -> float:
    """Reference optimum for small instances."""
    cost, _ = brute_force_gap(c, a, b)
    return cost


def test_cost_scaling() -> None:
    """Scaling all costs by k > 0 must scale the optimum by exactly k."""
    c, a, b = make_gap_instance(seed=5, n_machines=3, n_jobs=6)
    base = optimum(c, a, b)
    assert abs(optimum(3.0 * c, a, b) - 3.0 * base) <= 1e-9 * (1.0 + base)


def test_machine_relabeling() -> None:
    """Permuting machine indices (rows of c, a, b) leaves the optimum fixed."""
    c, a, b = make_gap_instance(seed=5, n_machines=3, n_jobs=6)
    perm = np.array([2, 0, 1])
    assert optimum(c[perm], a[perm], b[perm]) == optimum(c, a, b)


def test_capacity_relaxation_never_hurts() -> None:
    """Adding capacity can only keep or improve a minimization optimum."""
    c, a, b = make_gap_instance(seed=5, n_machines=3, n_jobs=6)
    assert optimum(c, a, b + 5.0) <= optimum(c, a, b) + 1e-9


test_cost_scaling()
test_machine_relabeling()
test_capacity_relaxation_never_hurts()
print("metamorphic tests passed")
# Expected: metamorphic tests passed
```

To apply the same relations at large scale, replace `brute_force_gap` with the heuristic plus a fixed seed: relabeling invariance then additionally certifies that the heuristic has no hidden index-order dependence.

### Fault injection: testing the tests

A checker that has never reported a violation is itself untested. After writing the validation stack, deliberately break the system one fault at a time and confirm the stack goes red: drop one constraint family from the model, flip an inequality direction, perturb a single objective coefficient by 1%, make the repair operator skip its last item, off-by-one a loop bound in the decoder. Every injected fault that survives all five layers marks a real gap in the stack — usually a constraint family the checker forgot or a tolerance set too loose. This is manual mutation testing; `mutmut` and `cosmic-ray` automate the mutation step for Python. Run a fault-injection pass when the checker is first written and after every change to the checker itself.

### Tolerance engineering at the solver boundary

Solver tolerances are the main source of false alarms — and of falsely silent checkers. Three rules. First, **round-then-verify**: convert integer variables to exact integers (asserting drift below 1e-4) before checking, then perform all feasibility arithmetic on the rounded values; with integral data the capacity check then becomes exact integer arithmetic with no epsilon at all. Second, **mind big-M leakage**: with `FeasibilityTol` $= 10^{-6}$ and $M = 10^6$, a "satisfied" constraint $y \le M z$ admits $y = 1$ while $z = 0$ rounds to zero — the checker must test the *logical* condition ("no flow unless open"), not the linear surrogate. Third, **scale the data**: keep coefficient magnitudes within a range of about $10^6$ between smallest and largest, or tighten `IntFeasTol` and `FeasibilityTol` and accept the slowdown (Klotz & Newman 2013). When a checker disagrees with the solver by amounts near the tolerance, the model is numerically fragile; fix scaling rather than loosening the checker.

### Differential testing across formulations and solvers

Two independent implementations of the same problem must agree on the optimal *value* — never require agreement on the solution, which is generally non-unique. Useful pairs: weak vs strong MIP formulations of the same problem; a MIP and a CP-SAT model; gurobipy and HiGHS on identical LP files; a compact and a pattern-based formulation (cutting stock). The disagreement protocol mirrors I4: validate both incumbents with the layer-1 checker against raw data; the side whose incumbent fails is wrong; if both pass, compare the proven bounds — the side whose bound excludes the other's feasible incumbent has the broken formulation. Differential testing earns its cost when a model is refactored: keep the old formulation alive in the test suite for one release as the comparison partner, then delete it.

### Test tiers and CI budgets

Validation only works if it runs, so budget it explicitly:

| Tier | Trigger | Contents | Budget |
|---|---|---|---|
| Unit | every commit | layer 3 + layer 4 pinned fixtures (brute-force based, no license needed) | < 30 s |
| Smoke | every merge | layers 1+2 on one medium instance per problem class | < 5 min |
| Full | nightly | layer 5 sweep, metamorphic suite, differential pairs | < 1 h |

Mark solver-dependent tests with `pytest.mark.skipif` on import failure so the unit tier passes on machines without a Gurobi license. Print the seed of every randomized test in its failure message; a failure that cannot be replayed is a failure wasted.

## Practical Challenges

**The checker quietly reuses model code.** A distance matrix builder, a penalty function, or a shared "utils" module imported by both the model and the checker makes them agree by construction — including on every bug. Audit imports: the checker module may import the standard library, numpy, and the raw instance loader, nothing else. If avoiding reuse forces you to re-derive a nontrivial computation (a piecewise tariff, a duty-time rule), that re-derivation is exactly the point.

**The solver reports optimal but the checker reports infeasible.** Almost always tolerances: the solver satisfied $\sum a_i x_i \le b$ within `FeasibilityTol` while the checker tests it exactly, or an integer variable sat at 0.99999 and the checker read it raw. Apply the round-then-verify rule, and give the checker an explicit epsilon equal to what the *application* tolerates (a vehicle physically cannot carry 100.000001 units only if units are indivisible — otherwise the constraint itself was a modeling approximation). If violations exceed solver tolerances, the model is numerically unstable: check coefficient ranges and big-M values before touching the checker.

**The heuristic beats the proven optimum.** The most information-rich failure in optimization development. Run the checker on the heuristic's solution: infeasible means the heuristic skips a constraint (typical culprits: a repair operator that fixes one violation while creating another, a decoder that ignores an edge case); feasible means the exact model is wrong — a constraint too tight, a wrong coefficient, or the model silently solving a restricted variant. Never celebrate, never average it away; one such instance, minimized to its smallest reproducing size, is the best debugging artifact you will get.

**Published optima do not match your recomputed values.** Convention drift. TSPLIB `EUC_2D` rounds each edge length to the nearest integer, so summing floating-point distances gives a different tour length than the published optimum; scheduling benchmarks differ on whether release times shift the makespan origin; some QAP results report flow$\times$distance counted once vs twice. Validate the parser and the convention together: take the smallest published instance, compute the objective of the published optimal solution by hand, and only then trust the rest of the set. Treat a benchmark set whose convention you have not reproduced as unvalidated input.

**Stochastic tests fail once a week.** Flaky tests train people to ignore red. Two fixes. Seed every random component and derive per-case seeds deterministically (`default_rng(seed)` per test, never global state). And keep assertions to invariants that hold with probability one — representation validity, delta-equals-full, checker feasibility — never "the heuristic finds a solution within 5% on this instance," which is a benchmark observation, not a test. Quality numbers go into the nightly experiment table where a regression triggers investigation, not a CI failure.

**Brute force cannot even handle the "tiny" instances.** Shrink harder — 5 jobs and 2 machines already kill most formulation bugs, because most bugs are index, sign, and convention errors that any nontrivial instance exposes. If structure prevents shrinking (a constraint only activates at size 30), use a second exact path instead: the MIP with `MIPGap=0` checked against a CP-SAT model, i.e., differential testing replaces enumeration as layer-4 ground truth. Dynamic programming, where available, is an excellent middle reference: exact, independent of the MIP, and fast at medium size.

**Regression tests pin solution vectors and break on ties.** Optimal solutions are rarely unique; solver version upgrades, machine differences, and even thread counts change which optimum is returned. Pin the objective value plus checker-feasibility of the returned solution, never the solution itself. Where the solution must be stable for downstream reasons, add explicit lexicographic tie-breaking to the model — and test *that* separately.

**Everything passes on small instances yet production results are wrong.** The validation bed never activated some constraint family — capacities so loose they never bind, time windows so wide they never cut. Track *violation coverage*: across the fault-injection runs and the instance bed, every violation branch of the checker must have fired at least once (coverage.py over the checker module makes this measurable). Add generator parameters that force each family to bind (see **instance-generation-and-benchmarks**) and one stress tier of medium instances where all families are simultaneously tight.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| pytest | all of layers 3-4; harness entry points | `parametrize` over (instance, seed); `skipif` guards for solver-licensed tests |
| hypothesis | property tests for operators/decoders | generates and *shrinks* failing inputs automatically; strategy `permutations` fits encodings |
| numpy | reference recomputation, property tests | `default_rng(seed)` everywhere; exact integer dtypes for integral data |
| gurobipy | exact reference on small instances; probing fixed solutions | `MIPGap=0`, `DualReductions=0` for clean INFEASIBLE; the model under test must never be its own oracle |
| OR-Tools CP-SAT / HiGHS | differential-testing partner | independent codebase, independent failure modes |
| pandas | validation and cross-validation report tables | one row per instance; archive next to result tables |
| coverage.py | violation-branch coverage of the checker | an unfired violation branch marks an untested constraint family |
| mutmut / cosmic-ray | automated fault injection | mutates source, expects the suite to go red; run on checker and builders |

## Output Format

A complete validation deliverable for an optimization project contains four artifacts.

**1. The validator module.** One `check_<problem>(instance, solution) -> ValidationReport` per problem class, with `feasible: bool`, `objective: float`, `violations: list[str]`; plus `reconcile_objective`. Independent imports only. Lives beside the instance loader, never beside the model.

**2. The reconciliation table** — produced for every experiment whose numbers leave the repo, one row per reported solution:

| instance | solver obj | recomputed | abs diff | feasible | violations |
|---|---|---|---|---|---|
| gap-s3-3x7 | 41.0 | 41.0 | 0.0 | yes | — |
| gap-s9-3x7 | 56.0 | 56.0 | 0.0 | yes | — |

**3. The cross-validation summary** from the layer-5 harness: instance bed description (sizes, seeds, generator version), invariant pass counts (must be 100%), and the heuristic gap distribution (mean/median/max) as a benchmark observation.

**4. The sign-off checklist**, answered in writing before results are used:

- [ ] Checker imports audited: no shared code with model or heuristic.
- [ ] Every violation branch of the checker has fired at least once (fault injection or instance bed).
- [ ] All integer variables rounded with drift below 1e-4 before checking.
- [ ] Layer-4 pins green at the current commit; any pin update has a written reason.
- [ ] Layer-5 invariants I1-I5 hold on the full instance bed.
- [ ] Objective convention validated against one hand-computed instance (and against the benchmark's published optimum where applicable).
- [ ] Seeds and generator versions recorded for every instance in the bed.

When reporting a validation failure, always include: the smallest reproducing instance (seed and size), the violated invariant or constraint family, both objective values where relevant, and the component the diagnosis table points at.

## Questions to Ask

- Which document defines the constraints — is there a written problem statement independent of the model code, or must we write one first?
- What exactly is the objective convention: sense, units, rounding, and are penalty terms inside or outside the reported number?
- What ground truth exists: brute-forceable sizes, published optima, a second solver, a trusted previous version?
- Where do solutions enter and leave the system — solver extraction, decoders, operators, repair, files — and which of these boundaries currently have no checker call?
- Do the heuristic and the exact model share any evaluation code?
- What solver tolerances are in effect, and what violation magnitude does the application itself tolerate?
- Are all instances and algorithms seeded so that any failure can be replayed exactly?
- How much CI time is available per commit versus nightly?
- Has the checker ever actually failed — has anyone fault-injected it?
- What is the cost of a wrong published number, and who reviews the sign-off checklist?

## Related Skills

- **optimization-project-structure** — when the validators, test tiers, and pinned fixtures need a home: package layout, config and seed management, and atomic result writing that make validation failures reproducible.
- **constraint-handling-techniques** — when the checker keeps flagging heuristic solutions and the fix is on the construction side: repair operators, penalty schemes, and feasibility-preserving operators rather than better detection.
- **milp-modeling-gurobi** — when a failed invariant traces back to the model itself: constraint-builder structure, status handling, and solution-extraction idioms the probing tests rely on.
- **instance-generation-and-benchmarks** — when the regression and cross-validation beds need seeded generators with controlled hardness, or standard benchmark sets with published optima and their parsing conventions.
