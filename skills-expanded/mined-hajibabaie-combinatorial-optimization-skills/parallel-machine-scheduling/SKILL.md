---
name: parallel-machine-scheduling
description: When the user wants to schedule jobs on one machine or on identical, uniform, or unrelated parallel machines: dispatching rules (SPT, WSPT, EDD, Moore-Hodgson), LPT and list scheduling with worst-case bounds, exact MIP models for makespan and due-date objectives, and LNS for large instances. Also use when the user mentions "parallel machines," "single machine scheduling," "minimize tardiness," "LPT," "weighted completion time," or "machine assignment." For jobs that visit several machines in a routing, see job-shop-scheduling; for MIP construction idioms, see milp-modeling-gurobi.
---

# Parallel Machine Scheduling

You are an expert in deterministic machine scheduling on a single machine and on identical (P),
uniform (Q), and unrelated (R) parallel machines. This skill covers the polynomial single-machine
dispatching rules (SPT, WSPT, EDD, Moore-Hodgson) with their optimality arguments, list scheduling
and LPT with worst-case bounds, exact MIP models for makespan and due-date objectives, and an LNS
heuristic for large instances. Use the framework below to classify the problem in three-field
notation, pick the cheapest method that actually solves it, and validate every schedule independently.

## Initial Assessment

Establish the following before proposing any model or algorithm.

- **Machine environment.** One machine, identical machines (same speed), uniform machines
  (speed factors `s_k`, so `p_jk = p_j / s_k`), or unrelated machines (a full `n x m` matrix
  `p_jk` with no structure)? This is the single biggest complexity driver.
- **Objective.** Makespan `Cmax`, total completion `sum C_j`, weighted completion `sum w_j C_j`,
  maximum lateness `Lmax`, number of tardy jobs `sum U_j`, or (weighted) total tardiness
  `sum (w_j) T_j`? Several of these are solved by a sorting rule; do not build a MIP for those.
- **Regularity check.** Is the objective non-decreasing in every completion time? All objectives
  above are regular, which means an optimal schedule exists with no inserted idle time. Earliness
  or just-in-time costs break this and require idle-time variables.
- **Beta-field complications.** Release dates `r_j`? Preemption allowed? Sequence-dependent setup
  times? Precedence constraints? Machine eligibility (job j may only run on a subset of machines)?
  Each one changes the complexity class. Confirm their absence explicitly; users forget to mention them.
- **Instance size.** Get `n` (jobs) and `m` (machines). The disjunctive MIP for tardiness has
  `O(n^2 m)` big-M rows and stalls beyond roughly 20-30 jobs; assignment-only models scale much further.
- **Data type and horizon.** Integer or fractional processing times? Time-indexed formulations
  need integer data and a horizon `T ~ sum p_j`; estimate `n * m * T` variables before suggesting one.
- **Due-date data.** Are due dates and weights given, or must they be generated? If generated for
  experiments, control tightness and range (TF/RDD parameters, see the instance generator below).
- **Exactness need.** Is a provable optimum required, or a good schedule with a reported gap
  against a lower bound? LPT plus the trivial bounds often certifies near-optimality without a solver.
- **Time budget and solver access.** Seconds or hours? Gurobi license available, or should the
  model target an open-source solver / CP-SAT?
- **Usage pattern.** One offline instance, or a dispatching decision repeated every few minutes
  inside a production system? The latter favors O(n log n) rules over any solver.
- **Deliverable.** Machine assignment only (enough for `Cmax`), or a fully timed schedule with
  per-machine sequences and start times (required for any due-date objective and for Gantt charts)?

## Problem Classes and Formulation

**Three-field notation** (Graham, Lawler, Lenstra & Rinnooy Kan 1979, "Optimization and
approximation in deterministic sequencing and scheduling"): `alpha | beta | gamma` where `alpha`
is the machine environment (`1`, `P`, `Pm`, `Q`, `R`), `beta` lists constraints (`r_j`, `pmtn`,
`prec`, `s_jk`), and `gamma` is the objective. Examples: `1 || sum w_j C_j`, `P || Cmax`,
`R || Cmax`, `P | r_j | Lmax`.

**Formal setting.** Jobs `j in J = {1, ..., n}`, machines `k in M = {1, ..., m}`. Job j has
processing time `p_jk` on machine k (identical: `p_jk = p_j`; uniform: `p_jk = p_j / s_k`),
optionally a due date `d_j` and weight `w_j > 0`. A schedule assigns each job to one machine and
sequences the jobs on each machine; `C_j` is the completion time of job j. Derived quantities:
lateness `L_j = C_j - d_j`, tardiness `T_j = max(L_j, 0)`, tardy indicator `U_j = 1 if C_j > d_j`.

Two structural facts drive every method choice below:

1. For regular objectives, a schedule is fully described by the pair (assignment, per-machine
   sequence) with jobs run back-to-back from time 0. No start-time decisions are needed beyond that.
2. For `Cmax` the per-machine sequence is irrelevant (only machine loads matter), so
   parallel-machine makespan is a pure assignment problem. For completion-time and due-date
   objectives the sequence matters; given an assignment, WSPT within each machine is optimal for
   `sum w_j C_j`, and EDD within each machine is optimal for `Lmax`.

**Complexity landscape.**

| Problem | Complexity | Method of choice |
|---|---|---|
| 1 \|\| sum C_j | polynomial | SPT sort (Smith 1956) |
| 1 \|\| sum w_j C_j | polynomial | WSPT sort, exchange argument (Smith 1956) |
| 1 \|\| Lmax | polynomial | EDD sort (Jackson 1955) |
| 1 \|\| sum U_j | O(n log n) | Moore-Hodgson algorithm (Moore 1968) |
| 1 \|\| sum T_j | NP-hard, ordinary (Du & Leung 1990) | Lawler (1977) decomposition DP, pseudo-polynomial |
| 1 \|\| sum w_j T_j | strongly NP-hard (Lawler 1977) | B&B with Emmons dominance; local search at scale |
| P2 \|\| Cmax | NP-hard via PARTITION | DP over loads, or MIP |
| P \|\| Cmax | strongly NP-hard via 3-PARTITION | LPT + bounds; MIP or LNS; PTAS exists |
| P \| pmtn \| Cmax | polynomial | McNaughton (1959) wrap-around rule |
| P \|\| sum C_j | polynomial | SPT list scheduling |
| R \|\| sum C_j | polynomial | assignment over (machine, position) slots (Horn 1973; Bruno, Coffman & Sethi 1974) |
| R \|\| Cmax | strongly NP-hard; no rho < 3/2 unless P = NP | assignment MIP; LP-rounding 2-approx (Lenstra, Shmoys & Tardos 1990); LNS |
| 1 \| r_j \| sum C_j | strongly NP-hard | do not apply SPT; B&B or heuristics |

**Preemptive lower bound.** `P | pmtn | Cmax` has optimum `max(max_j p_j, sum_j p_j / m)`
(McNaughton 1959). This value is also the standard lower bound for the non-preemptive `P || Cmax`.

The unrelated-machine makespan problem, the workhorse exact model of this skill, reads:

$$
\min \; C_{\max}
\quad \text{s.t.} \quad
\sum_{k=1}^{m} x_{jk} = 1 \;\; \forall j \in J, \qquad
\sum_{j=1}^{n} p_{jk}\, x_{jk} \le C_{\max} \;\; \forall k \in M, \qquad
x_{jk} \in \{0, 1\}.
$$

**Method selection.**

| Situation | Recommended approach |
|---|---|
| One machine, objective in the polynomial rows above | Apply the rule; report objective; done — no solver |
| One machine, total (weighted) tardiness | Small n or small `sum p_j`: DP / time-indexed MIP; large: local search with dominance rules |
| Identical machines, makespan | LPT + lower bound first; if the gap is not closed, MIP with symmetry breaking, or LNS |
| Unrelated machines, makespan | Assignment MIP (no sequencing variables needed); LNS when n*m is large |
| Parallel machines, due-date objective | Disjunctive MIP up to ~20-30 jobs; CP-SAT intervals mid-size; LNS at scale |
| Jobs visit several machines in a fixed routing | Different problem — see job-shop-scheduling |
| Repeated dispatching inside a live system | Dispatching rules (WSPT/EDD variants), never a solver in the loop |

## Single-Machine Sequencing Rules

**The WSPT exchange argument** (Smith 1956, "Various optimizers for single-stage production").
Take any sequence in which job i immediately precedes job j with `p_i / w_i > p_j / w_j`, and let
t be the start time of the pair. The pair contributes `w_i (t + p_i) + w_j (t + p_i + p_j)`.
After swapping, it contributes `w_j (t + p_j) + w_i (t + p_j + p_i)`. The difference
(before minus after) is `w_j p_i - w_i p_j > 0`, and no other job's completion time changes. So
any sequence not ordered by non-decreasing `p_j / w_j` can be strictly improved by an adjacent
swap, which proves WSPT optimal for `1 || sum w_j C_j`. The same adjacent-interchange template
proves SPT optimal for `sum C_j` (set `w_j = 1`) and EDD optimal for `Lmax` (Jackson 1955). This
argument style transfers: given a fixed machine assignment on parallel machines, it applies
machine by machine.

```python
import numpy as np


def spt_order(p: np.ndarray) -> np.ndarray:
    """SPT: non-decreasing p_j. Optimal for 1 || sum C_j (Smith 1956 with unit weights)."""
    return np.argsort(p, kind="stable")


def wspt_order(p: np.ndarray, w: np.ndarray) -> np.ndarray:
    """WSPT: non-decreasing p_j / w_j. Optimal for 1 || sum w_j C_j (Smith 1956)."""
    return np.argsort(p / w, kind="stable")


def edd_order(d: np.ndarray) -> np.ndarray:
    """EDD: non-decreasing d_j. Optimal for 1 || Lmax (Jackson 1955)."""
    return np.argsort(d, kind="stable")


def sequence_stats(order: np.ndarray, p: np.ndarray, d: np.ndarray, w: np.ndarray) -> dict:
    """Recompute all standard objectives of a single-machine sequence (no inserted idle time)."""
    completion_in_seq = np.cumsum(p[order])
    c = np.empty_like(completion_in_seq)
    c[order] = completion_in_seq
    lateness = c - d
    tardiness = np.maximum(lateness, 0.0)
    return {
        "total_completion": float(c.sum()),
        "weighted_completion": float((w * c).sum()),
        "lmax": float(lateness.max()),
        "total_tardiness": float(tardiness.sum()),
        "num_tardy": int((tardiness > 0).sum()),
    }


p = np.array([3.0, 1.0, 4.0, 2.0])
w = np.array([1.0, 1.0, 4.0, 1.0])
d = np.array([4.0, 2.0, 9.0, 12.0])
order = wspt_order(p, w)
print(order, sequence_stats(order, p, d, w)["weighted_completion"])
# Expected: order [1, 2, 3, 0] (ratios p/w = [3, 1, 1, 2]; the stable sort puts job 1
# before job 2) and weighted completion 1*1 + 4*5 + 1*7 + 1*10 = 38.0.
```

**Moore-Hodgson for `1 || sum U_j`** (Moore 1968, "An n job, one machine sequencing algorithm
for minimizing the number of late jobs"). Scan jobs in EDD order, keeping a running completion
time. The moment the current job would finish late, remove the *longest* job scheduled so far —
removing the longest job restores the most slack, and an exchange argument shows this greedy
choice is never wrong. Removed jobs are appended at the end in any order; only they are tardy.

```python
import heapq

import numpy as np


def moore_hodgson(p: np.ndarray, d: np.ndarray) -> tuple[list[int], list[int]]:
    """1 || sum U_j in O(n log n) (Moore 1968). Returns (on_time_sequence, late_jobs)."""
    order = np.argsort(d, kind="stable")
    heap: list[tuple[float, int]] = []          # max-heap on p_j via negated keys
    t = 0.0
    late: list[int] = []
    for j in order.tolist():
        heapq.heappush(heap, (-float(p[j]), j))
        t += float(p[j])
        if t > d[j]:
            neg_p, k = heapq.heappop(heap)      # drop the longest job scheduled so far
            t += neg_p
            late.append(k)
    late_set = set(late)
    on_time = [j for j in order.tolist() if j not in late_set]
    return on_time, late


p = np.array([4.0, 3.0, 2.0, 5.0])
d = np.array([4.0, 5.0, 6.0, 10.0])
print(moore_hodgson(p, d))
# Expected: ([1, 2, 3], [0]) -- dropping job 0 leaves jobs 1, 2, 3 all on time; exactly
# one tardy job, which is optimal for this instance.
```

For `1 || sum T_j`, no sorting rule is optimal. The problem is NP-hard in the ordinary sense
(Du & Leung 1990), and the classic exact approach is Lawler's (1977) decomposition: in EDD order,
the longest job's final position can be restricted to a small candidate set, splitting the
instance into independent subproblems — a pseudo-polynomial DP. For `1 || sum w_j T_j` (strongly
NP-hard), use branch-and-bound with Emmons (1969) dominance rules on small instances and local
search beyond that.

## Identical Machines: List Scheduling, LPT, and Bounds

**List scheduling** assigns the next job in a given list to the machine that becomes free first.
Graham's (1966) bound: if job l determines the makespan, it started at `Cmax - p_l` when all
machines were busy, so `m (Cmax - p_l) <= sum_{j != l} p_j`, giving
`Cmax <= sum_j p_j / m + (1 - 1/m) p_l <= (2 - 1/m) OPT`. This holds for *any* list order — a
useful guarantee for online arrival.

**LPT** (Longest Processing Time first) sorts the list by non-increasing `p_j` and achieves
`Cmax(LPT) <= (4/3 - 1/(3m)) OPT` (Graham 1969). Proof idea: if the critical job satisfies
`p_l <= OPT / 3`, the list-scheduling inequality already gives the bound; otherwise every machine
holds at most two jobs, and LPT is optimal for such instances.

**Lower bounds for `P || Cmax`:** the longest job `max_j p_j`; the average load
`ceil(sum_j p_j / m)` (equal to the preemptive optimum of McNaughton 1959 for integer data); and
the pairing bound: among the `m + 1` longest jobs, two must share a machine, so the sum of the
two smallest of them is a valid bound. Report `LB = max` of the three next to any heuristic value.

**PTAS note.** `P || Cmax` admits a PTAS (Hochbaum & Shmoys 1987, dual approximation): binary
search a target makespan T, round the "big" jobs (those above `eps * T`) to few size classes,
enumerate machine configurations by DP, and fill small jobs greedily. Polynomial for fixed `eps`
but rarely competitive in practice; use it as a theory reference, not as an implementation plan.

```python
import heapq

import numpy as np


def lpt_schedule(p: np.ndarray, m: int) -> tuple[np.ndarray, float]:
    """LPT for P || Cmax: longest job first onto the least-loaded machine.

    Guarantee: Cmax(LPT) <= (4/3 - 1/(3m)) * OPT (Graham 1969). Runs in O(n log n).
    """
    assign = np.empty(p.shape[0], dtype=np.int64)
    loads: list[tuple[float, int]] = [(0.0, k) for k in range(m)]
    heapq.heapify(loads)
    for j in np.argsort(-p, kind="stable").tolist():
        load, k = heapq.heappop(loads)
        assign[j] = k
        heapq.heappush(loads, (load + float(p[j]), k))
    return assign, max(load for load, _ in loads)


def cmax_lower_bound(p: np.ndarray, m: int) -> float:
    """Max of: longest job, average machine load, and the (m+1)-longest-jobs pairing bound."""
    lb = max(float(p.max()), float(np.ceil(p.sum() / m)))
    if p.shape[0] > m:
        top = np.sort(p)[::-1][: m + 1]         # two of these m+1 jobs must share a machine
        lb = max(lb, float(top[-2] + top[-1]))
    return lb


p = np.array([3.0, 3.0, 2.0, 2.0, 2.0])
assign, cmax = lpt_schedule(p, m=2)
print(assign, cmax, cmax_lower_bound(p, m=2))
# Expected: Cmax(LPT) = 7.0 against lower bound 6.0 -- the classic tight instance for
# Graham's 4/3 - 1/(3m) = 7/6 ratio at m = 2 (OPT = 6 with {3,3} and {2,2,2}).
```

When LPT matches the lower bound, optimality is certified without any solver. When it does not
(as above), decide between the exact MIP below and LNS based on instance size and time budget.
On uniform machines (`Q`), the same template works with completion-time-aware insertion (put the
next longest job where it would *finish* earliest); the worst-case ratio degrades but the
heuristic stays strong in practice.

## Exact MIP Models in gurobipy

### Assignment model for R || Cmax

Sequencing is irrelevant for makespan, so the model needs only assignment variables `x_jk` and
the makespan variable — the formulation displayed in the framework section. The LP relaxation is
weak (it splits jobs fractionally), but modern solvers handle thousands of jobs. Each constraint
family lives in its own builder function so it can be unit-tested and reused.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_assignment_constraints(model: gp.Model, x: gp.tupledict, data: dict) -> None:
    """Every job is assigned to exactly one machine."""
    for j in range(data["n"]):
        model.addConstr(x.sum(j, "*") == 1, name=f"assign[{j}]")


def add_makespan_constraints(model: gp.Model, x: gp.tupledict, cmax: gp.Var, data: dict) -> None:
    """The load of every machine is at most the makespan."""
    p = data["p"]
    for k in range(data["m"]):
        load = gp.quicksum(float(p[j, k]) * x[j, k] for j in range(data["n"]))
        model.addConstr(load <= cmax, name=f"load[{k}]")


def solve_r_cmax(data: dict, time_limit: float = 60.0) -> dict:
    """Exact MIP for R || Cmax. data holds n, m, and p as an (n, m) numpy array."""
    model = gp.Model("r_cmax")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    x = model.addVars(data["n"], data["m"], vtype=GRB.BINARY, name="x")
    cmax = model.addVar(lb=0.0, vtype=GRB.CONTINUOUS, name="cmax")
    add_assignment_constraints(model, x, data)
    add_makespan_constraints(model, x, cmax, data)
    model.setObjective(cmax, GRB.MINIMIZE)
    model.optimize()
    usable = model.Status == GRB.OPTIMAL or (model.Status == GRB.TIME_LIMIT and model.SolCount > 0)
    if not usable:
        return {"status": int(model.Status)}
    x_val = np.array([[x[j, k].X for k in range(data["m"])] for j in range(data["n"])])
    return {
        "status": int(model.Status),
        "cmax": float(cmax.X),
        "assign": x_val.argmax(axis=1),
        "gap": float(model.MIPGap),
    }


data = {"n": 4, "m": 2, "p": np.array([[2, 3], [4, 1], [3, 3], [2, 5]], dtype=float)}
print(solve_r_cmax(data))
# Expected: cmax = 4.0 -- e.g. jobs 0 and 3 on machine 0 (load 2+2) and jobs 1 and 2 on
# machine 1 (load 1+3). The bound sum_j min_k p_jk / m = 8/2 = 4 proves optimality.
```

### Disjunctive model for R | d_j | sum w_j T_j

Due-date objectives need per-machine sequences, hence start times `s_j`, completion times `C_j`,
tardiness `T_j`, and ordering binaries `y_ij` (i < j; `y_ij = 1` means i precedes j when they
share a machine). The big-M disjunction is only active when both jobs sit on the same machine:

```text
min  sum_j w_j T_j
s.t. sum_k x_jk = 1                                      for all j         (assignment)
     C_j  = s_j + sum_k p_jk x_jk                        for all j         (completion)
     s_j >= C_i - M (1 - y_ij) - M (2 - x_ik - x_jk)     for all i<j, k    (i before j on k)
     s_i >= C_j - M y_ij       - M (2 - x_ik - x_jk)     for all i<j, k    (j before i on k)
     T_j >= C_j - d_j                                    for all j         (tardiness)
     s_j, T_j >= 0;  x_jk, y_ij in {0, 1}
```

A safe and explainable big-M is `M = sum_j max_k p_jk`: no active schedule for a regular
objective finishes later than that. The model has `m * n * (n - 1)` big-M rows and a weak LP
relaxation; expect it to be practical up to roughly 20-30 jobs. Beyond that, switch to CP-SAT
interval models (the pattern is covered in job-shop-scheduling) or to the LNS below.

```python
import gurobipy as gp
import numpy as np
from gurobipy import GRB


def add_assignment_constraints(model: gp.Model, x: gp.tupledict, data: dict) -> None:
    """Every job is assigned to exactly one machine (same builder as the makespan model)."""
    for j in range(data["n"]):
        model.addConstr(x.sum(j, "*") == 1, name=f"assign[{j}]")


def add_completion_constraints(model: gp.Model, x: gp.tupledict, s: gp.tupledict,
                               c: gp.tupledict, data: dict) -> None:
    """C_j = s_j + processing time of j on its chosen machine."""
    p = data["p"]
    for j in range(data["n"]):
        proc = gp.quicksum(float(p[j, k]) * x[j, k] for k in range(data["m"]))
        model.addConstr(c[j] == s[j] + proc, name=f"complete[{j}]")


def add_disjunctive_constraints(model: gp.Model, x: gp.tupledict, s: gp.tupledict,
                                c: gp.tupledict, y: gp.tupledict, data: dict) -> None:
    """Jobs sharing a machine must not overlap; y[i, j] = 1 means i precedes j."""
    n, m, big_m = data["n"], data["m"], data["big_m"]
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(m):
                shared = 2 - x[i, k] - x[j, k]
                model.addConstr(s[j] >= c[i] - big_m * (1 - y[i, j]) - big_m * shared,
                                name=f"prec[{i},{j},{k}]")
                model.addConstr(s[i] >= c[j] - big_m * y[i, j] - big_m * shared,
                                name=f"prec[{j},{i},{k}]")


def add_tardiness_constraints(model: gp.Model, c: gp.tupledict, t: gp.tupledict,
                              data: dict) -> None:
    """T_j >= C_j - d_j; T_j >= 0 comes from the variable lower bound."""
    for j in range(data["n"]):
        model.addConstr(t[j] >= c[j] - float(data["d"][j]), name=f"tardy[{j}]")


def solve_weighted_tardiness(data: dict, time_limit: float = 120.0) -> dict:
    """Exact MIP for R | d_j | sum w_j T_j: machine assignment plus big-M sequencing."""
    model = gp.Model("r_sum_wt")
    model.Params.OutputFlag = 0
    model.Params.TimeLimit = time_limit
    n, m = data["n"], data["m"]
    data = {**data, "big_m": float(np.asarray(data["p"]).max(axis=1).sum())}
    x = model.addVars(n, m, vtype=GRB.BINARY, name="x")
    y = model.addVars([(i, j) for i in range(n) for j in range(i + 1, n)],
                      vtype=GRB.BINARY, name="y")
    s = model.addVars(n, lb=0.0, name="s")
    c = model.addVars(n, lb=0.0, name="c")
    t = model.addVars(n, lb=0.0, name="t")
    add_assignment_constraints(model, x, data)
    add_completion_constraints(model, x, s, c, data)
    add_disjunctive_constraints(model, x, s, c, y, data)
    add_tardiness_constraints(model, c, t, data)
    model.setObjective(gp.quicksum(float(data["w"][j]) * t[j] for j in range(n)), GRB.MINIMIZE)
    model.optimize()
    usable = model.Status == GRB.OPTIMAL or (model.Status == GRB.TIME_LIMIT and model.SolCount > 0)
    if not usable:
        return {"status": int(model.Status)}
    assign = [max(range(m), key=lambda k: x[j, k].X) for j in range(n)]
    return {
        "status": int(model.Status),
        "objective": float(model.ObjVal),
        "assign": assign,
        "start": [float(s[j].X) for j in range(n)],
        "gap": float(model.MIPGap),
    }


data = {
    "n": 3, "m": 2,
    "p": np.array([[3, 3], [2, 2], [2, 2]], dtype=float),
    "d": np.array([3.0, 2.0, 3.0]),
    "w": np.array([2.0, 1.0, 1.0]),
}
print(solve_weighted_tardiness(data))
# Expected: objective = 1.0 -- job 0 alone on one machine (on time), jobs 1 then 2 on the
# other machine (C_1 = 2 on time; C_2 = 4 is one unit late with weight 1).
```

Modeling notes: drop the `y` variables for pairs that can never share a machine (machine
eligibility), and tighten the second big-M occurrence to pair-specific values
`M_ij = max_k p_ik + max upstream load` when the generic horizon proves too loose. For identical
machines, add symmetry breaking (see Advanced Techniques) before anything else.

## LNS, Instance Generation, and Validation

### LNS for R || Cmax

Large Neighborhood Search is the natural metaheuristic here: the destroy/repair pattern maps
directly onto "free some jobs, reinsert them greedily," and for makespan no sequencing state
needs repair. The implementation below keeps the loads vectorized (`np.bincount` with weights and
broadcast `ld + p[j]` for the repair scan). It is a deliberately small fixed-operator LNS; for
adaptive operator weights, regret-based insertion, and simulated-annealing acceptance, use the
full machinery in the large-neighborhood-search skill.

```python
import numpy as np


def lns_r_cmax(p: np.ndarray, iters: int = 2000, q: int = 4, seed: int = 0) -> tuple[np.ndarray, float]:
    """LNS for R || Cmax. p has shape (n, m) with p[j, k] = time of job j on machine k.

    Destroy: remove q jobs, half from the busiest machine, half uniformly at random.
    Repair: greedy minimum-resulting-load reinsertion in random order.
    Acceptance: accept ties or improvements (drifts across the flat makespan plateaus).
    See the large-neighborhood-search skill for the full adaptive (ALNS) version.
    """
    rng = np.random.default_rng(seed)
    n, m = p.shape
    jobs = np.arange(n)

    def loads(a: np.ndarray) -> np.ndarray:
        return np.bincount(a, weights=p[jobs, a], minlength=m)

    cur = p.argmin(axis=1).astype(np.int64)             # cheapest-machine start
    cur_val = float(loads(cur).max())
    best, best_val = cur.copy(), cur_val
    for _ in range(iters):
        a = cur.copy()
        ld = loads(a)
        busy = np.flatnonzero(a == int(ld.argmax()))
        k1 = min(q // 2, busy.size)
        rem1 = rng.choice(busy, size=k1, replace=False)
        rest = np.setdiff1d(jobs, rem1)
        rem2 = rng.choice(rest, size=min(q - k1, rest.size), replace=False)
        removed = np.concatenate([rem1, rem2]).astype(np.int64)
        ld = ld - np.bincount(a[removed], weights=p[removed, a[removed]], minlength=m)
        for j in rng.permutation(removed).tolist():
            k = int(np.argmin(ld + p[j]))               # vectorized repair scan over machines
            a[j] = k
            ld[k] += p[j, k]
        val = float(ld.max())
        if val <= cur_val:
            cur, cur_val = a, val
            if val < best_val:
                best, best_val = a.copy(), val
    return best, best_val


p = np.array([[2, 3], [4, 1], [3, 3], [2, 5]], dtype=float)
assign, cmax = lns_r_cmax(p, iters=200, q=2, seed=7)
print(assign, cmax)
# Expected: cmax = 4.0, matching the MIP optimum for the same instance in the exact-model
# section (the cheapest-machine start gives 7.0; LNS closes the gap within a few iterations).
```

Parameter guidance: set `q` to roughly 10-20% of `n` (minimum 2); larger `q` diversifies more
per iteration but slows the repair. For due-date objectives, keep the same destroy logic but
repair by best-position insertion into the per-machine EDD/WSPT sequences and evaluate
incrementally; the acceptance rule then needs a real annealing or record-to-record criterion
because tardiness landscapes have wide plateaus.

### Instance generator

The hardness of unrelated-machine instances depends on the correlation structure of `p_jk`
(machine-correlated and job-correlated classes are systematically harder for assignment-based
bounds than uncorrelated ones). Due dates use the standard tardiness-factor / due-date-range
scheme (TF/RDD, as in Potts & Van Wassenhove 1982): TF controls how tight due dates are on
average, RDD how spread out they are.

```python
import numpy as np


def gen_unrelated(n: int, m: int, corr: str = "uncorrelated", seed: int = 0) -> dict:
    """Unrelated-machine instance; corr in {'uncorrelated', 'machine', 'job'}."""
    rng = np.random.default_rng(seed)
    if corr == "uncorrelated":
        p = rng.integers(10, 101, size=(n, m))
    elif corr == "machine":
        speed = rng.integers(1, 11, size=m)
        p = rng.integers(10, 21, size=(n, m)) * speed       # slow/fast machines
    elif corr == "job":
        base = rng.integers(10, 101, size=(n, 1))
        p = base + rng.integers(0, 21, size=(n, m))         # intrinsically long/short jobs
    else:
        raise ValueError(f"unknown correlation class: {corr!r}")
    return {"n": n, "m": m, "p": p.astype(np.int64)}


def add_due_dates(data: dict, tf: float = 0.4, rdd: float = 0.8, seed: int = 1) -> dict:
    """Attach due dates and weights using the TF/RDD scheme (Potts & Van Wassenhove 1982).

    Due dates are uniform on [H(1 - TF - RDD/2), H(1 - TF + RDD/2)] where H estimates the
    average machine load. Larger TF = tighter dates; larger RDD = more spread.
    """
    rng = np.random.default_rng(seed)
    horizon = float(data["p"].mean(axis=1).sum()) / data["m"]
    lo = max(horizon * (1.0 - tf - rdd / 2.0), 0.0)
    hi = max(horizon * (1.0 - tf + rdd / 2.0), 1.0)
    d = rng.uniform(lo, hi, size=data["n"])
    w = rng.integers(1, 11, size=data["n"]).astype(np.int64)
    return {**data, "d": d, "w": w}


inst = add_due_dates(gen_unrelated(n=6, m=2, corr="uncorrelated", seed=42), tf=0.4, rdd=0.8, seed=42)
print(inst["p"].shape, inst["p"].min(), inst["p"].max(), inst["d"].round(1))
# Expected: p has shape (6, 2) with entries in [10, 100]; due dates fall inside
# [0.2 * H, 1.0 * H] where H is the average machine load. Same seeds reproduce the instance.
```

Hold the generator fixed (seeds recorded) across every experiment; tune algorithm parameters on
one seed range and report results on a disjoint one.

### Independent validator

Never trust the objective value an algorithm reports about itself. The validator recomputes
feasibility and all objectives from the raw solution artifact, sharing no code with the model or
the heuristic. Run it after every solver call and inside every experiment script.

```python
import numpy as np


def validate_assignment(assign: np.ndarray, p: np.ndarray) -> tuple[list[str], float]:
    """Check an assignment-only schedule (R || Cmax) and recompute its makespan."""
    errors: list[str] = []
    n, m = p.shape
    a = np.asarray(assign)
    if a.shape != (n,):
        errors.append(f"assignment has shape {a.shape}, expected ({n},)")
        return errors, float("inf")
    if a.min() < 0 or a.max() >= m:
        errors.append("machine index out of range")
        return errors, float("inf")
    loads = np.bincount(a, weights=p[np.arange(n), a], minlength=m)
    return errors, float(loads.max())


def validate_sequences(seqs: list[list[int]], p: np.ndarray, d: np.ndarray,
                       w: np.ndarray) -> tuple[list[str], dict]:
    """Check a sequenced schedule (one job list per machine); recompute Cmax, Lmax, sum w_j T_j."""
    errors: list[str] = []
    n, m = p.shape
    if len(seqs) != m:
        errors.append(f"{len(seqs)} machine sequences given for {m} machines")
        return errors, {}
    flat = [j for seq in seqs for j in seq]
    if sorted(flat) != list(range(n)):
        errors.append("jobs are not partitioned exactly once across machines")
        return errors, {}
    c = np.zeros(n)
    for k, seq in enumerate(seqs):
        t = 0.0
        for j in seq:                                   # back-to-back: regular objectives
            t += float(p[j, k])
            c[j] = t
    tard = np.maximum(c - d, 0.0)
    objectives = {
        "cmax": float(c.max()),
        "lmax": float((c - d).max()),
        "total_weighted_tardiness": float((w * tard).sum()),
    }
    return errors, objectives


p = np.array([[3, 3], [2, 2], [2, 2]], dtype=float)
d = np.array([3.0, 2.0, 3.0])
w = np.array([2.0, 1.0, 1.0])
print(validate_sequences([[0], [1, 2]], p, d, w))
# Expected: ([], {'cmax': 4.0, 'lmax': 1.0, 'total_weighted_tardiness': 1.0}) -- the same
# value the disjunctive MIP reported, confirmed by code that shares nothing with the model.
```

A disagreement between the validator and the solver almost always means the *model* is wrong
(big-M too small, a missing disjunction, or an objective that ignores idle time), not the
validator. Debug the model first.

## Advanced Techniques

### PTAS for P || Cmax via dual approximation

Hochbaum & Shmoys (1987, "Using dual approximation algorithms for scheduling problems") binary
search a target makespan T in `[LB, 2 LB]`. For each T they answer "can all jobs finish by
`(1 + eps) T`?": jobs longer than `eps * T` are rounded down to the nearest multiple of
`eps^2 * T`, leaving at most `1 / eps^2` distinct big-job sizes and at most `1 / eps` big jobs
per machine, so feasible machine configurations can be enumerated and counted by dynamic
programming; small jobs are then poured greedily into the leftover capacity. The scheme is the
canonical example of dual approximation (approximate the *decision* version, then search), and
the same template extends to `Q || Cmax`. Use it to justify "near-optimal is cheap for identical
machines" — but implement LPT + MIP, not the PTAS.

### LP rounding for R || Cmax

Lenstra, Shmoys & Tardos (1990) solve a parametric LP in which `x_jk` is fixed to 0 whenever
`p_jk > T`, then exploit the structure of extreme points: at most `n + m` variables are positive,
so the bipartite support graph is a forest in which fractional jobs can be matched one-per-machine.
Rounding along that matching yields a schedule of makespan at most `2T`. They also prove no
polynomial algorithm achieves a ratio below 3/2 unless P = NP. Practical takeaway: the parametric
LP (or just the assignment LP) is a strong, cheap lower bound — report LNS gaps against it.

### Time-indexed formulations for due-date objectives

With integer data and horizon `T = max big_m`, binaries `x_jkt` ("job j starts at time t on
machine k") give the constraint set `sum_{k,t} x_jkt = 1` per job plus, for each machine and time
slot, "at most one job covers slot t." Any additively separable objective in completion times —
weighted tardiness included — becomes linear. The LP relaxation dominates the big-M disjunctive
relaxation (Dyer & Wolsey 1990; Sousa & Wolsey 1992) and often yields gaps an order of magnitude
smaller; the price is `O(n m T)` variables, so scale processing times down first and consider
solving the LP only as a bounding device, or pricing the columns out lazily.

### Symmetry breaking on identical machines

Every solution on identical machines has `m!` mirror images obtained by permuting machine
indices, which branch-and-bound explores separately unless told otherwise. Standard remedies:
restrict job j to machines `0..min(j, m-1)` (the first j+1 machines); or order machines by
non-increasing load with named constraints `load[k] >= load[k+1]`; or fix the longest job on
machine 0. Load-ordering interacts badly with machine eligibility constraints — prefer the
job-index scheme when eligibility is present. On unrelated machines the symmetry vanishes by
itself, which is one reason the R model often solves *faster* than a naive P model of equal size.

### Warm starts from list schedules

The MIP never has to start cold: LPT (makespan) or per-machine WSPT/EDD after a greedy
assignment (due-date objectives) produce a feasible incumbent in milliseconds. Set `x[j,k].Start`
from the construction, derive the `y_ij` ordering binaries from the per-machine sequences, and
the solver begins with an upper bound that prunes most of the weak big-M relaxation's tree. The
same constructions seed the LNS (replace the cheapest-machine start) and the comparison baseline
in experiments. Mechanics and pitfalls of MIP starts are covered in warm-starts-and-initial-solutions.

## Practical Challenges

**The disjunctive tardiness MIP stalls beyond ~20-30 jobs.** This is expected: `O(n^2 m)` big-M
rows with a near-vacuous LP relaxation. In order of preference: tighten big-M values per pair,
add symmetry breaking, warm-start with a list schedule, switch to a CP-SAT interval model (see
job-shop-scheduling for the pattern), or accept the LNS plus a time-indexed LP bound.

**Identical machines blow up the branch-and-bound tree.** Machine-permutation symmetry makes the
solver re-prove the same subtree `m!` times. Add one symmetry-breaking family before touching any
other parameter; on a P||Cmax model with m = 8 this alone can turn hours into seconds.

**Due dates bolted onto an assignment-only model give wrong answers.** For `Cmax` the per-machine
sequence is irrelevant, so people reuse the assignment model for tardiness and compute completion
times as machine loads. That assigns every job on a machine the same completion time. The
validator's sequenced check exists precisely to catch this class of bug.

**Release dates silently break the dispatching rules.** SPT is optimal for `1 || sum C_j` but
`1 | r_j | sum C_j` is strongly NP-hard, and EDD loses optimality for `1 | r_j | Lmax` as well.
Whenever `r_j` appears, re-derive the method; do not patch the rule with "skip unavailable jobs"
and assume optimality survived.

**Ties make runs irreproducible.** Equal `p_j / w_j` ratios or equal due dates produce alternative
optima, and an unstable sort picks among them by memory layout. Use stable sorts with a documented
tie-break (the code above uses `kind="stable"` everywhere) and record seeds; otherwise two "identical"
runs report different schedules and your regression tests flap.

**Tardiness landscapes are flat.** Once most jobs are on time, large neighborhoods of schedules
share the same objective and a hill-climber stalls. Use a lexicographic surrogate (total weighted
tardiness, then total completion time) for move evaluation, or an acceptance rule that tolerates
sideways moves — the LNS above accepts ties for exactly this reason.

**LPT's gap will not close on "few large jobs" instances.** When two or three long jobs dominate,
LPT's early commitments cannot be undone. Try MULTIFIT (Coffman, Garey & Johnson 1978), which
binary-searches a bin capacity and packs by FFD, or run pairwise-swap local search on the LPT
solution; if `n` is moderate, the assignment MIP settles the question outright.

**The heuristic "beats" the exact optimum.** A heuristic objective below the MIP optimum always
means the two codes evaluate different problems — a too-small big-M cutting off true optima, a
transposed `p` matrix, or due dates scaled differently. Run both solutions through the independent
validator; whichever code disagrees with it is the broken one.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| gurobipy | Exact assignment and disjunctive MIPs | Commercial license; see milp-modeling-gurobi |
| OR-Tools CP-SAT | Due-date objectives at 30-200 jobs | Interval variables + NoOverlap usually beat big-M MIPs |
| HiGHS (highspy / PuLP) | No commercial license available | Handles the assignment models well; weaker on big-M sequencing |
| numpy | Dispatching rules, LNS, validators | Stable argsort, bincount loads, broadcast repair scans |
| heapq (stdlib) | LPT and Moore-Hodgson | O(log m) machine selection, O(log n) longest-job removal |
| scipy.optimize | `R \|\| sum C_j` via linear_sum_assignment | Polynomial (machine, position)-slot assignment |
| pandas | Experiment result tables | One row per (instance, seed, algorithm) run |
| matplotlib | Gantt charts and convergence curves | Gantt = horizontal bars per machine, jobs as segments |

## Output Format

A complete answer to a parallel-machine scheduling task contains:

1. **Problem classification.** One line of three-field notation with the complexity status, e.g.
   "`R | d_j | sum w_j T_j` — strongly NP-hard; exact up to ~25 jobs, LNS beyond." If a
   polynomial rule applies, say so and skip the solver entirely.
2. **Model summary** (when a MIP is built):

   | Item | Value |
   |---|---|
   | Variables | x: n*m binary; y: n(n-1)/2 binary; s, c, t: n continuous |
   | Constraints | n assignment, n completion, m*n*(n-1) disjunctive, n tardiness |
   | Big-M | sum_j max_k p_jk, with per-pair tightening if applied |
   | Symmetry breaking | scheme used, or "none needed (unrelated machines)" |

3. **Solution-quality report.** Best objective, lower bound and its source (LP value, preemptive
   bound, pairing bound), relative gap, runtime, solver status, and — for stochastic methods —
   the seed list with best/median/worst over seeds.
4. **Schedule artifact.** Per machine, the ordered job list with start and completion times
   (CSV columns: `machine, position, job, start, completion, due, tardiness`). Assignment-only
   output is acceptable solely for makespan objectives, and the answer must say why.
5. **Validation line.** Explicit confirmation that the independent validator reproduced the
   reported objective, e.g. "validator: feasible, total weighted tardiness 1431.0 = reported."
6. **Convergence summary** (heuristics): iterations run, iteration of last improvement, and
   initial-vs-final objective, so the reader can judge whether more time would help.

## Questions to Ask

- One machine or several? If several: identical speeds, speed factors, or a full per-job
  per-machine time matrix?
- Which single objective — makespan, total (weighted) completion time, max lateness, number of
  tardy jobs, or (weighted) total tardiness? Or several, and in what priority?
- Are there release dates, sequence-dependent setup times, precedence constraints, or machine
  eligibility restrictions? Is preemption allowed?
- How large is the instance (n jobs, m machines), and is it solved once or repeatedly?
- Are processing times integer (or scalable to integers), and how large is the horizon?
- Is a provable optimum required, or is a certified gap against a lower bound acceptable?
- What is the time budget per solve, and is a Gurobi license available?
- What artifact does the downstream consumer need — machine assignment, a timed Gantt schedule,
  or just the objective value?

## Related Skills

- **milp-modeling-gurobi** — when building, debugging, or extending the assignment and
  disjunctive MIPs: constraint-builder patterns, parameter setting, and status handling.
- **large-neighborhood-search** — when instances outgrow the exact models; full ALNS machinery
  (adaptive operator weights, regret insertion, acceptance criteria) for machine scheduling.
- **job-shop-scheduling** — when each job visits several machines in a routing; disjunctive
  models and the CP-SAT interval formulation that dominates there.
- **warm-starts-and-initial-solutions** — when feeding LPT/WSPT constructions into the MIP as
  starts or seeding the LNS population of starting points.
