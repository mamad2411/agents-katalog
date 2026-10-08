---
name: constraint-programming
description: When the user wants to model and solve combinatorial problems with constraint programming, especially OR-Tools CP-SAT: integer, boolean, and interval variables, AllDifferent, NoOverlap, Cumulative, channeling, and search strategies, plus CP-vs-MIP selection guidance. Also use when the user mentions "constraint programming," "CP-SAT," "interval variables," "AllDifferent," "no-overlap," "cumulative constraint," or when the problem is feasibility-heavy with disjunctive resources and logical conditions. For MIP modeling, see milp-modeling-gurobi; for solver alternatives, see open-source-solvers.
---

# Constraint Programming with CP-SAT

You are an expert in constraint programming (CP) for combinatorial optimization, specifically in modeling with Google OR-Tools CP-SAT. This skill covers the CP modeling vocabulary — integer, boolean, and interval variables; global constraints such as AllDifferent, NoOverlap, and Cumulative; channeling and reification — plus search strategies, solver parameters, and the judgment call of when CP beats MIP. Use the framework below to assess the problem, choose CP or MIP deliberately, build the model from global constraints rather than decomposed booleans, and report solution quality honestly.

## Initial Assessment

Before writing any model, establish the following. Each answer changes a modeling decision downstream.

- **Problem class.** Sequencing/scheduling with disjunctive resources, assignment with clash constraints, configuration/feasibility puzzles — all CP home turf. Network flows, blending, continuous costs — MIP/LP territory. See the decision table below before committing.
- **Are all quantities integer, or can they be made integer?** CP-SAT has no continuous variables. Durations, costs, and capacities must be integers; floats must be scaled (e.g., cents, milliminutes). Confirm an acceptable scaling before modeling.
- **Domain sizes.** A start-time variable with domain `[0, 10^9]` cripples propagation. Compute a tight horizon (sum of durations, or a critical-path bound) and tight per-variable bounds first.
- **Feasibility-driven or objective-driven?** Pure feasibility (timetabling with only hard constraints) and min-max objectives (makespan) favor CP. Strong economic objectives with many cost terms and a tight LP relaxation favor MIP.
- **Hard vs soft constraints.** List them separately. Hard constraints become model constraints; soft constraints become penalty terms on reified booleans. Get the user's penalty weights or a lexicographic priority order explicitly.
- **Instance size, now and at target scale.** Number of tasks/lectures, machines/rooms, time slots. Channeling booleans grow as variables × domain size — check that product before generating them.
- **Solver availability.** OR-Tools is Apache-licensed and `pip install ortools` — almost always available. If the user is locked into a Gurobi-only stack, indicator constraints there cover some of the same ground (see milp-modeling-gurobi).
- **Time budget and proof requirement.** CP-SAT is an anytime solver: it reports the best incumbent and a dual bound. Does the user need proven optimality, a certified gap, or just a good feasible solution in N seconds?
- **Symmetry.** Identical machines, identical rooms, interchangeable shifts? Plan symmetry-breaking constraints up front; CP search suffers from symmetry exactly as MIP does.
- **Dual values or sensitivity analysis needed?** CP-SAT provides neither. If the user needs shadow prices, the model must be (also) an LP/MIP.
- **Determinism and reproducibility.** Research use: fix `random_seed` and `num_workers`; prefer `max_deterministic_time` over wall-clock limits when run-to-run reproducibility matters.
- **Existing data format.** Standard benchmark formats (JSP `ft06`-style tables, ITC timetabling files) parse into the same model structures used below; do not invent a new format if a standard one exists.

## CP-SAT Anatomy and the CP-vs-MIP Decision

A constraint satisfaction/optimization problem is

$$
\min\ f(x) \quad \text{s.t.}\quad x_j \in D_j \ \ (j = 1,\dots,n), \qquad C_i(x_{S_i}) \ \text{holds} \ \ (i = 1,\dots,m),
$$

where each domain $D_j$ is a finite set of integers and each constraint $C_i$ is an arbitrary relation over the variables in its scope $S_i$. The power of CP is that constraints are not restricted to linear inequalities: a constraint is anything that comes with a *propagator* — an algorithm that removes domain values that cannot appear in any solution of that constraint.

CP-SAT is not a classical backtracking CP solver. It is a clause-learning SAT solver with integer propagators bolted on, following *lazy clause generation* (Ohrimenko, Stuckey & Codish 2009, "Propagation via lazy clause generation"): every domain reduction made by a propagator is recorded as a boolean literal with an explanation clause, so conflicts can be analyzed and turned into learned clauses exactly as in SAT. Add a simplex-based LP propagator for dual bounds, restarts, and a parallel portfolio of workers sharing learned clauses, and you get a solver that has dominated scheduling and timetabling benchmarks since roughly 2018 (it has won the MiniZinc Challenge repeatedly). Treat it as a hybrid SAT/CP/MIP machine, not as "old CP".

### Variable types

| Constructor | What it is | Notes |
|---|---|---|
| `new_int_var(lb, ub, name)` | Integer variable with finite domain | Tight bounds matter; domains can also be unions of intervals via `new_int_var_from_domain` |
| `new_bool_var(name)` | Boolean (0/1) literal | Usable in linear expressions and as a reification literal; `~b` is its negation |
| `new_interval_var(start, size, end, name)` | Interval = (start, size, end) with `start + size == end` built in | The arguments are affine expressions; consumed by NoOverlap/Cumulative |
| `new_optional_interval_var(start, size, end, presence, name)` | Interval that exists only if literal `presence` is true | The core tool for optional tasks and machine-assignment alternatives |
| `new_constant(v)` | Fixed integer | Useful to keep code uniform |

### Global constraint vocabulary

| Constraint | Meaning | Typical use |
|---|---|---|
| `add_all_different(exprs)` | All expressions take pairwise distinct values | Assignments, permutations, clash-freeness, graph coloring |
| `add_no_overlap(intervals)` | Intervals are pairwise disjoint in time | Disjunctive (unary) machines, room occupancy |
| `add_no_overlap_2d(x_ivs, y_ivs)` | Rectangles do not overlap | Packing, berth allocation |
| `add_cumulative(intervals, demands, capacity)` | Resource usage stays below capacity at all times | Renewable resources, workforce, RCPSP |
| `add_circuit(arcs)` | Selected arcs form one Hamiltonian circuit | Routing/sequencing inside CP |
| `add_element(index, exprs, target)` | `target == exprs[index]` with a variable index | Variable-dependent costs and lookups |
| `add_inverse(forward, backward)` | `forward[i] == j ⇔ backward[j] == i` | Channeling position ↔ item views of a permutation |
| `add_min_equality / add_max_equality` | `target == min/max(exprs)` | Makespan, bottleneck objectives |
| `add_multiplication_equality / add_division_equality / add_modulo_equality` | Integer products, quotients, remainders | Derived quantities (day = slot // periods) |
| `add_bool_or / add_bool_and / add_implication / add_exactly_one / add_at_most_one` | Clausal logic on literals | Logical structure, set-partitioning rows |
| `constraint.only_enforce_if(lits)` | Constraint holds when all literals are true (half-reification) | Reification, conditional constraints, soft constraints |

### What propagation buys you

Each global constraint runs a dedicated filtering algorithm at every node of the search. Three results worth knowing:

- **AllDifferent.** Domain consistency is achievable in polynomial time via bipartite matching (Régin 1994, "A filtering algorithm for constraints of difference in CSPs"). Bounds consistency follows Hall's theorem: for every value interval $[a,b]$, the variables whose domains fit inside it must satisfy $|\{i : D_i \subseteq [a,b]\}| \le b - a + 1$, and when equality holds, the interval is removed from all other domains. A clique of pairwise `!=` constraints detects none of this.
- **Disjunctive (NoOverlap) edge finding.** With $est$ the earliest start, $lct$ the latest completion, and $p(\Omega) = \sum_{j \in \Omega} p_j$: if for a task $i$ and a set $\Omega$ on the same machine $\min(est_\Omega, est_i) + p(\Omega) + p_i > lct_\Omega$, then $i$ must execute after every task in $\Omega$, so $est_i \ge \max_{\emptyset \neq \Omega' \subseteq \Omega} \big(est_{\Omega'} + p(\Omega')\big)$. This reasoning (Carlier & Pinson 1989, "An algorithm for solving the job-shop problem" — the paper that closed the famous ft10 instance) runs in $O(n \log n)$ per machine (Vilím 2009) and is the engine behind CP's dominance on shop scheduling.
- **Cumulative.** The constraint enforces $\sum_{i:\ s_i \le t < s_i + p_i} r_i \le C$ for all $t$; propagators use timetabling, energetic reasoning, and edge finding (Baptiste, Le Pape & Nuijten 2001, "Constraint-Based Scheduling"). The energy bound $\lceil \sum_i r_i p_i / C \rceil$ is the cheap lower bound on the makespan you should always report.

The modeling consequence: **always prefer one global constraint over its decomposition.** `add_all_different` beats $O(n^2)$ pairwise `!=`; `add_no_overlap` beats big-M disjunctions; `add_cumulative` beats time-indexed booleans — both in propagation strength and in model size.

### CP-SAT vs MIP: decision guidance

| Signal in the problem | Prefer CP-SAT | Prefer MIP (Gurobi/HiGHS) |
|---|---|---|
| Disjunctive scheduling, sequencing, NoOverlap structure | Yes — interval variables + edge finding | Big-M disjunctions give weak LP relaxations |
| Continuous variables (flows, prices, fractional blends) | Not supported — scaling may distort | Native |
| Logical conditions, implications, table constraints | Native (reification is cheap) | Indicator/big-M constraints, clumsier |
| Tight LP relaxation, objective is a large sum of costs | LP propagator helps but bound often weaker | Yes — decades of cutting-plane machinery |
| Pure feasibility with many clash constraints (timetabling, rostering) | Yes — clause learning excels | Possible but slower to first solution |
| Need dual values, sensitivity, shadow prices | Not available | Yes (LP duals) |
| Min-max / bottleneck objectives (makespan) | Propagates well | Weak LP bounds without extra work |
| Very large numeric coefficients or wide domains | Risky — integer overflow checks, slow encoding | Standard double-precision LP handles it |
| Column generation / decomposition planned | Use CP as a pricing or repair subroutine | Master problem must be LP-based |

Default rule: scheduling and timetabling → write CP-SAT first; flows, location, lot-sizing, blending → write MIP first; when in doubt and the model is small, write both — each is a correctness check on the other, and the loser still validates the winner.

### Complexity and integrality notes

Finite-domain CSP is NP-complete; everything here is exponential worst case. Practical performance depends on (a) propagation strength per node, (b) clause learning reusing refutations across the tree, and (c) domain sizes. Model-size accounting: interval-based scheduling models grow with the number of tasks (not the horizon), while time-indexed channeling grows with tasks × horizon — this is why interval variables are the default for scheduling and channeling booleans are generated only where soft costs need them.

## A Generic CP-SAT Workflow

The reusable skeleton: how the solver behaves, then a harness you can keep across projects. Every worked example below follows this anatomy and is self-contained.

```text
CP-SAT SOLVE LOOP (lazy clause generation, simplified)
------------------------------------------------------
input:  variables with finite integer domains, constraints, objective
state:  domain store, trail of literals with explanations, learned clauses

1. encode integer domains lazily as boolean order literals [x <= v]
   and value literals [x == v]
2. repeat:
3.    PROPAGATE: run all propagators (linear, AllDifferent, NoOverlap,
      Cumulative, element, ...) to a fixpoint; every domain reduction
      is pushed on the trail together with an explanation clause
4.    on conflict: analyze explanations -> learn a 1-UIP clause,
      backjump; conflict at decision level 0 -> INFEASIBLE
      (or: current objective bound proven)
5.    if all variables fixed: record incumbent z*, add the constraint
      objective < z*, restart the search (anytime behavior)
6.    else DECIDE: fix a literal chosen by activity scores (VSIDS-like)
      or by the user-supplied decision strategy
7. portfolio: parallel workers run different configurations (more LP,
   more restarts, LNS workers repairing the incumbent) and share
   learned clauses, bounds, and solutions
```

```python
"""Reusable CP-SAT solve harness: parameters, progress trace, status handling."""
from __future__ import annotations

from ortools.sat.python import cp_model


class ProgressLogger(cp_model.CpSolverSolutionCallback):
    """Record (wall_time, objective, best_bound) for every improving solution."""

    def __init__(self) -> None:
        super().__init__()
        self.trace: list[tuple[float, float, float]] = []

    def on_solution_callback(self) -> None:
        self.trace.append(
            (self.wall_time, self.objective_value, self.best_objective_bound)
        )


def solve_cp(
    model: cp_model.CpModel,
    time_limit_s: float = 60.0,
    workers: int = 8,
    log: bool = False,
    seed: int = 0,
) -> tuple[cp_model.CpSolver, int, ProgressLogger]:
    """Solve `model` with explicit parameters; raise only on proven failure."""
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_workers = workers
    solver.parameters.log_search_progress = log
    solver.parameters.random_seed = seed
    logger = ProgressLogger()
    status = solver.solve(model, logger)
    if status == cp_model.MODEL_INVALID:
        raise ValueError(model.validate())  # exact reason, e.g. overflow
    if status == cp_model.INFEASIBLE:
        raise ValueError("model proven infeasible: check data, then use assumptions")
    if status == cp_model.UNKNOWN:
        raise TimeoutError("no feasible solution within the limit")
    # OPTIMAL or FEASIBLE: solver.value(...) is now safe to read.
    return solver, status, logger


def quality_report(solver: cp_model.CpSolver, status: int) -> str:
    """One-line solution-quality summary: objective, dual bound, gap, effort."""
    obj = solver.objective_value
    bound = solver.best_objective_bound
    gap = abs(obj - bound) / max(1.0, abs(obj))
    return (
        f"{solver.status_name(status)}: obj={obj:.0f} bound={bound:.0f} "
        f"gap={gap:.2%} time={solver.wall_time:.1f}s "
        f"conflicts={solver.num_conflicts} branches={solver.num_branches}"
    )
```

Status handling is non-negotiable: `FEASIBLE` means "incumbent exists, optimality not proven" — report the gap, never present it as optimal. `MODEL_INVALID` is almost always an overflow or a malformed expression; `model.validate()` returns the exact reason.

### Modeling vocabulary in code

One compact model exercising reification, logic, element, products, min/max, channeling, and cumulative — the idioms every CP-SAT model is built from.

```python
"""CP-SAT modeling idioms in one toy model."""
from ortools.sat.python import cp_model

model = cp_model.CpModel()

x = model.new_int_var(0, 10, "x")
y = model.new_int_var(0, 10, "y")
b = model.new_bool_var("b")

# Reification: b <=> (x > y). Encode BOTH directions or b is only half-linked.
model.add(x > y).only_enforce_if(b)
model.add(x <= y).only_enforce_if(~b)

# Clausal logic on literals.
c = model.new_bool_var("c")
model.add_bool_or([b, c])        # b or c
model.add_implication(c, b)      # c -> b

# Element: variable-index lookup, cost == costs[x].
costs = [4, 7, 1, 3, 9, 2, 8, 5, 6, 0, 4]
cost = model.new_int_var(0, 9, "cost")
model.add_element(x, costs, cost)

# Nonlinear terms need intermediate variables; expressions stay linear.
z = model.new_int_var(0, 100, "z")
model.add_max_equality(z, [x, y, 3 * cost])
prod = model.new_int_var(0, 100, "prod")
model.add_multiplication_equality(prod, [x, y])

# Channeling two views of a permutation: pos[i] == j  <=>  item[j] == i.
pos = [model.new_int_var(0, 2, f"pos_{i}") for i in range(3)]
item = [model.new_int_var(0, 2, f"item_{j}") for j in range(3)]
model.add_inverse(pos, item)

# Cumulative: three tasks share a resource of capacity 3.
starts = [model.new_int_var(0, 10, f"st_{i}") for i in range(3)]
durs, demands = [3, 4, 2], [2, 1, 2]
ivs = [
    model.new_interval_var(starts[i], durs[i], starts[i] + durs[i], f"task_{i}")
    for i in range(3)
]
model.add_cumulative(ivs, demands, 3)

model.maximize(z - prod)
solver = cp_model.CpSolver()
status = solver.solve(model)
print(solver.status_name(status), solver.value(x), solver.value(z))
# Expected: OPTIMAL, objective 27 (x=4 -> cost=9, z=27; y=0 -> prod=0)
```

## Worked Example 1: Job-Shop Scheduling with Interval Variables

The job-shop problem (JSP): jobs $j \in J$, each an *ordered* sequence of operations; operation $k$ of job $j$ needs machine $\mu_{jk}$ exclusively for $p_{jk}$ time units. Minimize the makespan. With start variables $s_{jk} \in [0, H]$, $H = \sum_{j,k} p_{jk}$:

$$
\min\ C_{\max} \quad \text{s.t.} \quad
s_{j,k+1} \ge s_{j,k} + p_{j,k}, \qquad
C_{\max} \ge s_{j,m_j} + p_{j,m_j},
$$

plus, for every pair of operations $(o, o')$ sharing a machine, the disjunction $s_o + p_o \le s_{o'}\ \lor\ s_{o'} + p_{o'} \le s_o$. A MIP linearizes each disjunction with a binary and a big-M (Manne 1960, "On the job-shop scheduling problem"), and its LP relaxation collapses to near-trivial bounds. CP keeps the disjunction intact inside one `add_no_overlap` per machine, where edge finding (previous section) tightens the operation time windows directly — this is why CP-SAT is the practical winner on JSP and why this model is the canonical interval-variable example.

```python
"""Job-shop scheduling: interval variables, no_overlap, makespan objective."""
from __future__ import annotations

import collections

from ortools.sat.python import cp_model

Job = list[tuple[int, int]]  # ordered operations as (machine, duration)


def solve_jobshop(
    jobs: list[Job], time_limit_s: float = 30.0
) -> tuple[int, dict[tuple[int, int], int]]:
    """Minimize makespan; return (makespan, start times keyed by (job, op))."""
    horizon = sum(d for job in jobs for _, d in job)  # trivial upper bound
    model = cp_model.CpModel()

    starts: dict[tuple[int, int], cp_model.IntVar] = {}
    ends: dict[tuple[int, int], cp_model.IntVar] = {}
    on_machine: dict[int, list[cp_model.IntervalVar]] = collections.defaultdict(list)

    for j, job in enumerate(jobs):
        for k, (machine, dur) in enumerate(job):
            s = model.new_int_var(0, horizon, f"s_{j}_{k}")
            e = model.new_int_var(0, horizon, f"e_{j}_{k}")
            on_machine[machine].append(model.new_interval_var(s, dur, e, f"iv_{j}_{k}"))
            starts[j, k], ends[j, k] = s, e
        for k in range(1, len(job)):
            model.add(starts[j, k] >= ends[j, k - 1])  # precedence inside the job

    for intervals in on_machine.values():
        model.add_no_overlap(intervals)  # one disjunctive resource per machine

    makespan = model.new_int_var(0, horizon, "makespan")
    model.add_max_equality(makespan, [ends[j, len(job) - 1] for j, job in enumerate(jobs)])
    model.minimize(makespan)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    solver.parameters.num_workers = 8
    status = solver.solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE), solver.status_name(status)
    return int(solver.value(makespan)), {k: solver.value(v) for k, v in starts.items()}


def validate_schedule(jobs: list[Job], sched: dict[tuple[int, int], int]) -> int:
    """Independent feasibility check; returns the recomputed makespan."""
    busy: dict[int, list[tuple[int, int]]] = collections.defaultdict(list)
    cmax = 0
    for j, job in enumerate(jobs):
        prev_end = 0
        for k, (machine, dur) in enumerate(job):
            s = sched[j, k]
            assert s >= prev_end, f"precedence violated: job {j}, op {k}"
            busy[machine].append((s, s + dur))
            prev_end = s + dur
        cmax = max(cmax, prev_end)
    for machine, tasks in busy.items():
        tasks.sort()
        for (_, e1), (s2, _) in zip(tasks, tasks[1:]):
            assert e1 <= s2, f"overlap on machine {machine}"
    return cmax


if __name__ == "__main__":
    jobs: list[Job] = [
        [(0, 3), (1, 2), (2, 2)],
        [(0, 2), (2, 1), (1, 4)],
        [(1, 4), (2, 3)],
    ]
    cmax, sched = solve_jobshop(jobs)
    assert validate_schedule(jobs, sched) == cmax
    print(f"makespan = {cmax}")
    # Expected: makespan = 11, proven OPTIMAL in well under a second
```

Two structural points. First, the model size is independent of the horizon: 8 operations give 8 intervals regardless of whether $H$ is 21 or 21,000 — compare a time-indexed MIP with $O(\text{ops} \times H)$ binaries. Second, the independent validator costs twenty lines and has caught more modeling bugs than any solver log; never skip it (precedence read from the wrong index, duration applied to the wrong machine, and off-by-one horizon errors all surface here).

When machines can process several operations at once (capacity $> 1$), or operations consume a shared renewable resource, replace NoOverlap with Cumulative — the same intervals, plus a demand per task:

```python
"""Cumulative resource: parallel capacity instead of a disjunctive machine."""
from ortools.sat.python import cp_model

durations = [3, 4, 2, 5, 3]
demands = [2, 3, 1, 2, 2]
capacity = 4
horizon = sum(durations)

model = cp_model.CpModel()
starts = [model.new_int_var(0, horizon, f"s_{i}") for i in range(5)]
intervals = [
    model.new_interval_var(starts[i], durations[i], starts[i] + durations[i], f"iv_{i}")
    for i in range(5)
]
model.add_cumulative(intervals, demands, capacity)

makespan = model.new_int_var(0, horizon, "makespan")
model.add_max_equality(makespan, [starts[i] + durations[i] for i in range(5)])
model.minimize(makespan)

solver = cp_model.CpSolver()
status = solver.solve(model)
print(solver.status_name(status), solver.value(makespan))
# Expected: OPTIMAL 10. Energy bound: ceil(36/4) = 9 is unreachable because
# the demand-3 task leaves capacity 1, which only the single demand-1 task fits.
```

## Worked Example 2: Course Timetabling with AllDifferent and Channeling

Educational timetabling: lectures $l \in L$ (each a meeting of a course, taught by a teacher, attended by a curriculum group) must each receive a timeslot $t_l \in \{0,\dots,|T|-1\}$ (with $|T| = D$ days $\times$ $P$ periods) and a room $r_l \in \{0,\dots,|R|-1\}$. The hard constraints are clash constraints, and each is one AllDifferent:

$$
\text{AllDifferent}\big(\{t_l : l \in G\}\big) \ \ \text{for each clash group } G \ (\text{same teacher, same curriculum}),
$$

$$
\text{AllDifferent}\big(\{\,t_l \cdot |R| + r_l : l \in L\,\}\big) \ \ (\text{at most one lecture per room and slot}),
$$

$$
\text{AllDifferent}\big(\{\lfloor t_l / P \rfloor : l \in \text{course } c\}\big) \ \ (\text{lectures of one course spread over distinct days}).
$$

The combined index $t_l \cdot |R| + r_l$ is itself a channeling device: it folds a pair of variables into one so a single AllDifferent can propagate across both dimensions. Soft constraints need a second view of the same decision: booleans $x_{l,t}$ *channeled* to the integer variables by

$$
x_{l,t} = 1 \iff t_l = t, \qquad \sum_{t \in T} x_{l,t} = 1,
$$

so that slot penalties become the linear objective $\min \sum_l \sum_t w_t\, x_{l,t}$. This integer-view-for-propagation, boolean-view-for-costs pattern is the standard CP timetabling architecture: AllDifferent reasons on the integers, the objective and any soft constraint reason on the booleans, and the channeling keeps the two views consistent.

```python
"""Course timetabling: AllDifferent clash groups + integer/boolean channeling."""
from __future__ import annotations

import collections

from ortools.sat.python import cp_model

Lecture = tuple[str, str, str]  # (course, teacher, curriculum)


def solve_timetable(
    lectures: list[Lecture],
    n_days: int,
    periods_per_day: int,
    n_rooms: int,
    slot_penalty: list[int],
    time_limit_s: float = 30.0,
) -> tuple[int, dict[int, tuple[int, int]]]:
    """Assign (slot, room) per lecture; minimize total slot penalties."""
    n_slots = n_days * periods_per_day
    n_lec = len(lectures)
    model = cp_model.CpModel()

    slot = [model.new_int_var(0, n_slots - 1, f"slot_{l}") for l in range(n_lec)]
    room = [model.new_int_var(0, n_rooms - 1, f"room_{l}") for l in range(n_lec)]
    day = [model.new_int_var(0, n_days - 1, f"day_{l}") for l in range(n_lec)]
    for l in range(n_lec):
        model.add_division_equality(day[l], slot[l], periods_per_day)

    # Clash groups: same teacher or same curriculum -> distinct slots.
    by_teacher: dict[str, list[int]] = collections.defaultdict(list)
    by_curric: dict[str, list[int]] = collections.defaultdict(list)
    by_course: dict[str, list[int]] = collections.defaultdict(list)
    for l, (course, teacher, curric) in enumerate(lectures):
        by_teacher[teacher].append(l)
        by_curric[curric].append(l)
        by_course[course].append(l)
    for members in list(by_teacher.values()) + list(by_curric.values()):
        if len(members) > 1:
            model.add_all_different(slot[l] for l in members)
    # Lectures of one course go on distinct days (spread).
    for members in by_course.values():
        if len(members) > 1:
            model.add_all_different(day[l] for l in members)

    # One lecture per (slot, room): AllDifferent on the folded pair index.
    model.add_all_different(slot[l] * n_rooms + room[l] for l in range(n_lec))

    # Channeling to booleans; soft slot penalties live on this view.
    x: dict[tuple[int, int], cp_model.IntVar] = {}
    for l in range(n_lec):
        for t in range(n_slots):
            x[l, t] = model.new_bool_var(f"x_{l}_{t}")
            model.add(slot[l] == t).only_enforce_if(x[l, t])
            model.add(slot[l] != t).only_enforce_if(~x[l, t])
        model.add_exactly_one([x[l, t] for t in range(n_slots)])

    model.minimize(
        sum(slot_penalty[t] * x[l, t] for l in range(n_lec) for t in range(n_slots))
    )

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_s
    status = solver.solve(model)
    assert status in (cp_model.OPTIMAL, cp_model.FEASIBLE), solver.status_name(status)
    plan = {l: (solver.value(slot[l]), solver.value(room[l])) for l in range(n_lec)}
    return int(solver.objective_value), plan


if __name__ == "__main__":
    lectures: list[Lecture] = [
        ("calc1", "ada", "eng1"), ("calc1", "ada", "eng1"),
        ("phys1", "max", "eng1"), ("phys1", "max", "eng1"),
        ("prog1", "ada", "cs1"), ("stat1", "eva", "cs1"),
    ]
    # 2 days x 3 periods; the last period of each day is penalized.
    penalty = [0, 0, 3, 0, 0, 3]
    cost, plan = solve_timetable(
        lectures, n_days=2, periods_per_day=3, n_rooms=2, slot_penalty=penalty
    )
    print(cost, plan)
    # Expected: OPTIMAL with objective 0 -- the 6 lectures fit into the
    # 8 cheap (slot, room) pairs while respecting all clash groups.
```

Scaling notes. The channeling booleans are the expensive part ($|L| \times |T|$ of them); generate them only when soft costs or per-slot side constraints need them — the hard model alone (integers + AllDifferent) is far lighter. For room *capacity* classes (any of $k$ identical rooms), drop the room variable and post `add_cumulative` (or a per-slot count $\sum_l x_{l,t} \le k$) instead; for distinguishable rooms with per-room eligibility, keep `room[l]` and restrict its domain. Real instances (ITC-2007 curriculum-based timetabling) add minimum-working-days and room-stability soft terms — all expressible on the same two channeled views. See timetabling-and-rostering for the full benchmark treatment.

## Advanced Techniques

### Decision strategies and fixed search

CP-SAT's default portfolio is almost always the right choice. Override it only for structured feasibility problems where you know a good variable order, or when you need deterministic, explainable search behavior. `add_decision_strategy` fixes variable and value selection; it takes effect when `search_branching = FIXED_SEARCH` (otherwise it only seeds the default search).

```python
"""Fixed search with a decision strategy (8-queens)."""
from ortools.sat.python import cp_model

n = 8
model = cp_model.CpModel()
queens = [model.new_int_var(0, n - 1, f"q_{i}") for i in range(n)]
model.add_all_different(queens)
model.add_all_different(queens[i] + i for i in range(n))  # diagonals
model.add_all_different(queens[i] - i for i in range(n))

model.add_decision_strategy(queens, cp_model.CHOOSE_FIRST, cp_model.SELECT_MIN_VALUE)

solver = cp_model.CpSolver()
solver.parameters.search_branching = cp_model.FIXED_SEARCH
solver.parameters.num_workers = 1  # fixed search is a single-worker tool
status = solver.solve(model)
print(solver.status_name(status), [solver.value(q) for q in queens])
# Expected: OPTIMAL with a valid placement, found deterministically
```

Useful pairs: `CHOOSE_MIN_DOMAIN_SIZE` + `SELECT_MIN_VALUE` (fail-first), `CHOOSE_FIRST` over a hand-ordered list (schedule-critical tasks first). For scheduling, ordering interval starts by earliest start time mimics classical CP scheduling search.

### Warm starts with solution hints

`add_hint` feeds a (possibly partial, possibly infeasible) solution that the solver repairs and improves — the CP analogue of a MIP start. Hint from any cheap heuristic; on large models this routinely cuts the time-to-first-good-solution by orders of magnitude.

```python
"""Warm-starting CP-SAT: greedy solution as hints on a 0-1 knapsack."""
from ortools.sat.python import cp_model

values = [10, 13, 7, 8, 9, 4]
weights = [4, 6, 3, 4, 5, 2]
cap = 12

model = cp_model.CpModel()
take = [model.new_bool_var(f"take_{i}") for i in range(len(values))]
model.add(sum(weights[i] * take[i] for i in range(len(values))) <= cap)
model.maximize(sum(values[i] * take[i] for i in range(len(values))))

order = sorted(range(len(values)), key=lambda i: values[i] / weights[i], reverse=True)
load = 0
for i in order:  # density greedy -> hint values (gives 25 here)
    fits = load + weights[i] <= cap
    model.add_hint(take[i], int(fits))
    load += weights[i] if fits else 0

solver = cp_model.CpSolver()
status = solver.solve(model)
print(solver.status_name(status), int(solver.objective_value))
# Expected: OPTIMAL 27 (items 0, 1, 5) -- solver improves on the hinted 25
```

Set `solver.parameters.fix_variables_to_their_hinted_value = True` to *debug* a hint: the solver then tells you whether the hinted assignment is even feasible, and `model.clear_hints()` resets between experiments.

### Explaining infeasibility with assumptions

CP-SAT has no IIS tool, but assumption literals give the equivalent: guard each constraint family with a boolean, assume all guards true, and on INFEASIBLE read back a sufficient conflicting subset. This is the fastest path from "the roster is impossible" to "these two rules collide".

```python
"""Infeasibility diagnosis with assumption literals."""
from ortools.sat.python import cp_model

model = cp_model.CpModel()
x = model.new_int_var(0, 10, "x")
y = model.new_int_var(0, 10, "y")

guards = {name: model.new_bool_var(name) for name in ("sum_low", "x_big", "y_ge_x")}
model.add(x + y <= 6).only_enforce_if(guards["sum_low"])
model.add(x >= 5).only_enforce_if(guards["x_big"])
model.add(y >= x).only_enforce_if(guards["y_ge_x"])

model.add_assumptions(list(guards.values()))
solver = cp_model.CpSolver()
status = solver.solve(model)
if status == cp_model.INFEASIBLE:
    core = solver.sufficient_assumptions_for_infeasibility()
    print([model.get_bool_var_from_proto_index(i).name for i in core])
# Expected: ['sum_low', 'x_big', 'y_ge_x'] -- x>=5 and y>=x force x+y >= 10 > 6
```

The returned core is sufficient, not minimal; shrink it by deletion (re-solve with one member dropped at a time). The same guards then double as soft-constraint switches: minimize the number of relaxed guards to find a least-violating roster.

### Parameters that matter

Beyond `max_time_in_seconds`, `num_workers`, `random_seed`, and `log_search_progress` (read the log — it names which worker found each bound), the high-leverage parameters are: `max_deterministic_time` for reproducible budgets across machines; `relative_gap_limit` to stop at a proven gap (e.g., 0.01); `cp_model_presolve = False` only when debugging what presolve removed; `linearization_level = 2` to push more of the model into the LP propagator when the objective bound stalls; and `stop_after_first_solution = True` for pure feasibility checks inside a heuristic loop. Resist the urge to tune more than these — the portfolio adapts internally, and parameter-tuning effort is better spent tightening domains and adding redundant global constraints.

### Redundant constraints and symmetry breaking

Two model-side accelerators. (1) *Redundant globals*: adding an implied `add_cumulative` over all machines of a job shop (capacity = number of machines), or an energy bound $\sum p_{jk} \le |M| \cdot C_{\max}$, gives propagators extra grip without changing the solution set. (2) *Symmetry breaking*: identical rooms, machines, or vehicles admit value symmetry — break it by ordering, e.g., room indices used in nondecreasing order of first use, or `model.add(slot[a] < slot[b])` between the first two lectures of interchangeable courses. CP-SAT detects some symmetry in presolve, but explicit ordering constraints on obviously interchangeable objects remain among the highest-payoff lines you can add.

## Practical Challenges

**The data has floating-point durations or costs.** CP-SAT accepts only integers. Pick one scale per quantity family (minutes, cents, grams), apply it everywhere, and record the factor next to the model code. Watch the objective: summing $10^6$-scaled costs over $10^5$ booleans approaches the int64 overflow guard, and `MODEL_INVALID` with an overflow message is the symptom. Rescale or tighten variable bounds, do not silently truncate.

**The model is correct but slow, and the culprit is decomposed structure.** Pairwise `!=` instead of AllDifferent, big-M-style reified orderings instead of NoOverlap, time-indexed booleans instead of intervals — each loses propagation and bloats the clause database. Rebuild around globals; this is the single most common CP performance fix, worth checking before any parameter is touched.

**Channeling booleans explode the model.** $|L| \times |T|$ literals is fine at 6 × 6 and fatal at 5,000 × 600. Generate `x[l, t]` only for the (lecture, slot) pairs that carry a penalty or appear in a soft constraint; keep all hard reasoning on the integer view. If most slots are penalized, invert: use `add_element(slot[l], slot_penalty, pen_l)` and sum the `pen_l` integers instead of building any booleans.

**The solver returns FEASIBLE and the gap will not close.** CP-SAT's dual bound comes from the LP propagator and clause learning; on loosely constrained min-sum objectives it can lag far behind MIP bounds. First report the gap honestly. Then either accept the incumbent (validate it independently), raise `linearization_level`, add redundant bounding constraints, or solve the same model in a MIP solely to obtain a bound — the hybrid is legitimate and common.

**INFEASIBLE with forty constraint families and no clue.** Do not bisect by commenting code out. Guard each family with an assumption literal as shown above, read the conflicting core, and shrink it by deletion. Keep the guards in the production model behind a flag; infeasible instances will arrive again, and rosters that cannot be satisfied need an explanation a planner can act on.

**Results differ between runs of the "same" experiment.** Wall-clock limits make the portfolio nondeterministic: a busy machine means fewer restarts before timeout. Fix `random_seed`, fix `num_workers`, and switch to `max_deterministic_time` for paper experiments; record all three in the result table together with the ortools version, which changes solver behavior release to release.

**Optional tasks and machine alternatives are modeled with big-M arithmetic.** The CP-native pattern is `new_optional_interval_var` with one presence literal per (task, machine) alternative, `add_exactly_one` over the presences, and each optional interval in its machine's NoOverlap. Costs attach to presence literals. No big-M, no degenerate relaxation, and propagation still sees the alternatives.

**The objective mixes incomparable goals.** Weighted sums of makespan and tardiness and preference penalties invite weight archaeology later. Prefer lexicographic solving: optimize goal 1, fix it with `model.add(obj1 <= best1)` (or a small tolerance), re-solve for goal 2. Two short solves usually beat one long solve on a distorted weighted objective, and the result is explainable.

## Tools & Libraries

| Library | When to use | Note |
|---|---|---|
| OR-Tools CP-SAT (`ortools`) | Default CP solver: scheduling, timetabling, feasibility, sequencing | Apache license; integers only; anytime with dual bounds |
| CPMpy | Numpy-style CP modeling layer over CP-SAT and other solvers | Good for research pipelines that swap solvers |
| MiniZinc (+ Chuffed, Gecode) | Solver-independent CP language; model once, run many solvers | The CP community's lingua franca; FlatZinc backends vary widely |
| IBM ILOG CP Optimizer (`docplex.cp`) | Commercial CP, strongest native interval/sequence algebra | License required; state functions and sequence variables beyond CP-SAT |
| `python-constraint` | Teaching-scale CSPs only | Pure Python; orders of magnitude slower; avoid for real instances |
| Choco / JaCoP | JVM-stack projects needing embedded CP | Mature; relevant when Python is not an option |
| gurobipy indicator constraints | Logical conditions inside an otherwise-MIP model | Middle ground when only a few implications exist; see milp-modeling-gurobi |

## Output Format

A complete CP deliverable contains:

1. **Model summary table** — one row per constraint family:

| Element | Type | Count | Purpose |
|---|---|---|---|
| `slot[l]`, `room[l]` | IntVar | 2·\|L\| | time/room assignment |
| teacher/curriculum clash | AllDifferent | per group | hard clash-freeness |
| `x[l,t]` channeling | BoolVar + reified eq | \|L\|·\|T\| | soft-cost view |
| slot penalties | linear objective | 1 | soft constraints |

2. **Solution-quality report** — status (`OPTIMAL` / `FEASIBLE`), objective, best bound, relative gap, wall time, deterministic time, conflicts, branches; the `quality_report` helper above prints exactly this line. Never report a `FEASIBLE` incumbent without its bound.
3. **Independent validation** — feasibility checker output (every hard constraint re-verified outside the solver) and the objective recomputed from raw data; both must match the solver's values.
4. **Reproducibility block** — ortools version, `random_seed`, `num_workers`, time limit (prefer deterministic time), and the instance/seed used.
5. **Artifacts** — the solution in domain terms (schedule table, timetable grid) as CSV/JSON, plus the solver log when the run is part of a benchmark; convergence traces (`ProgressLogger.trace`) if anytime behavior is being compared.
6. **CP-vs-MIP statement** — one paragraph saying why CP was (or was not) the right tool for this instance class, with the observed evidence (time-to-first-solution, gap trajectory).

## Questions to Ask

- Are all data integer, or what scaling (time granularity, money units) is acceptable?
- Is the goal a feasible solution, a good solution under a time budget, or proven optimality?
- Which constraints are truly hard, and what are the penalty weights or priorities of the soft ones?
- What are realistic instance sizes now, and what must the model scale to next year?
- Are there optional/alternative activities (task may be skipped, machine may vary) that need optional intervals?
- Which resources are disjunctive (capacity 1) and which cumulative (capacity > 1)?
- Are there interchangeable resources (identical rooms/machines) we should symmetry-break?
- Do you need duals or sensitivity information (which CP cannot provide)?
- Is a baseline solution available to hint the solver, or a MIP model to cross-validate against?
- Does the experiment need run-to-run determinism for a paper?

## Related Skills

- **job-shop-scheduling** — when the focus is the JSP itself: disjunctive MIP comparison, critical-path neighborhoods, and benchmark instances beyond the interval model shown here.
- **timetabling-and-rostering** — when timetabling/rostering needs the full treatment: ITC/INRC benchmark formats, soft-constraint catalogs, and LNS/hyper-heuristic solution methods.
- **milp-modeling-gurobi** — when the decision table points to MIP, or a Gurobi model is needed as bound provider or cross-check for a CP model.
- **graph-coloring** — when the clash structure is a pure coloring problem; CP with AllDifferent is one of its standard exact approaches.
- **open-source-solvers** — when choosing among CP-SAT, HiGHS, SCIP, and modeling layers under license or deployment constraints.
