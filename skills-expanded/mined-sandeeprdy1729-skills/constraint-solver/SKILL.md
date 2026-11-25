---
name: constraint-solver
description: >
  Constraint-based problem solving skill. Finds elegant solutions when the design
  space is heavily restricted — budget caps, time limits, technology mandates, team
  size, ethical bounds, regulatory requirements. Treats constraints as the design
  material, not the obstacle. Surfaces constraint violations early, ranks constraints
  by hardness, and finds solutions that satisfy all hard constraints while optimizing
  within soft ones. The tighter the constraints, the sharper the solution.
  Use when user says: very limited budget, we can't use X, strict deadline, only
  N people, regulatory constraint, tech stack is fixed, solve with these restrictions,
  must work within these limits, strong constraints, can't change the requirements,
  work within the box, solve this but we can only, tiny budget, no budget, works
  with these limitations, solve under constraint.
  Do NOT activate for: open-ended problems with no constraints, problems where
  the first step is to challenge the constraints themselves (use pre-mortem instead).
  First response: "Constraint Solver active. State your goal and every constraint
  you know about — budget, time, team, tech, ethics, regulatory. I'll rank them
  and find the solution space."
license: Apache 2.0
---

# Constraint-Based Problem Solving

Constraints are not the enemy of good solutions. They are often the reason for them.
The iPod had a 1GB storage constraint that forced the click wheel. Twitter had a
160-character constraint that created a new writing form. The Apollo 13 CO2 scrubber
was built from duct tape and a sock because that's what was on the ship.

Unconstrained design produces mediocre solutions: bloated, over-engineered, and
slow. Constrained design forces clarity about what actually matters. This skill
treats every constraint as a design dimension and finds the solution that satisfies
all of them simultaneously.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/solve <problem>` | Full constraint-based solution for a described problem |
| `/constraints` | Extract and rank all constraints from the problem statement |
| `/rank` | Rank constraints by hardness: immovable → hard → soft → preference |
| `/feasibility` | Check whether the constraint set is satisfiable at all |
| `/relax <constraint>` | Show what becomes possible if one constraint is relaxed |
| `/tighten <constraint>` | Show what happens if a constraint is made stricter |
| `/creative` | Find a solution that violates no hard constraints but is unconventional |
| `/minimum-viable` | Find the simplest solution that satisfies only the hard constraints |
| `/tradeoffs` | Show the tradeoff frontier across soft constraints |
| `/conflict` | Identify constraints that directly conflict with each other |
| `/assumptions` | List assumptions embedded in the constraints themselves |
| `/reframe` | Restate the problem to surface a constraint as the solution |

---

## HIGH-LEVEL WORKFLOW

```text
User states goal and constraints
    │
    ├─ Phase 1: Constraint Extraction
    │     Extract all constraints; identify implicit ones
    │
    ├─ Phase 2: Constraint Classification
    │     Rank by hardness; identify conflicts
    │
    ├─ Phase 3: Feasibility Check
    │     Is there a solution space? If not, which constraints must relax?
    │
    ├─ Phase 4: Solution Search
    │     Find solutions within the feasible space
    │
    ├─ Phase 5: Solution Ranking
    │     Rank solutions by constraint satisfaction + objective quality
    │
    └─ Phase 6: Constraint Insight
          Surface what the constraint set reveals about the real problem
```

---

## PHASE 1 — CONSTRAINT EXTRACTION

### Constraint sources

Not all constraints are stated. Extract from:
- **Explicit:** "Budget is $5k." "Must ship by Q3."
- **Implicit from context:** "Solo founder" → no team available → no parallel execution
- **Domain defaults:** Building a mobile app → must work on iOS and Android
- **Ethical:** Not stated but applies (GDPR, safety requirements, fairness)
- **Second-order:** "We need it fast" → "We can't refactor later" → tech debt is a constraint

### Constraint extraction format

```text
CONSTRAINT EXTRACTION

Explicit constraints:
  C1: [constraint] — Source: [where stated]
  C2: [constraint] — Source: [where stated]

Implicit constraints (inferred):
  C3: [constraint] — Inferred from: [what implies it]
  C4: [constraint] — Inferred from: [what implies it]

Domain default constraints:
  C5: [constraint] — Domain: [field]

Second-order constraints:
  C6: [constraint] — Derived from: [C1 + C2 implies C6 because...]
```

---

## PHASE 2 — CONSTRAINT CLASSIFICATION

### Hardness taxonomy

| Class | Definition | Behavior in solving |
| --- | --- | --- |
| **Immovable** | Cannot be violated under any circumstances | Eliminate solutions that violate these first |
| **Hard** | Cannot be violated without a significant process to change it | Treat as immovable unless user explicitly opens renegotiation |
| **Soft** | Preferred but negotiable if there's a strong reason | Optimize within; allow violations with explicit cost |
| **Preference** | Nice to have; easily traded | Use as tiebreaker between otherwise equivalent solutions |

### Common constraint misclassifications

The most valuable analytical move in constraint solving is catching constraints
that are stated as immovable but are actually soft.

| Stated as | Actually | Signal |
| --- | --- | --- |
| "We can't change the tech stack" | Soft | Cost of change is high, not infinite |
| "Deadline is fixed" | Hard | Most deadlines flex when the cost of bad shipping is shown |
| "Budget is $X, not a penny more" | Soft if ROI > 2× | Budgets expand for provably high-return investment |
| "Regulatory requirement" | Truly immovable | Never challenge without legal review |
| "The team won't accept it" | Preference | Team resistance is a real constraint but not a veto |

### Constraint ranking output

```text
CONSTRAINT RANKING

IMMOVABLE
  C3: [constraint] — Why: [reason this cannot be violated]
  C5: [constraint] — Why: [...]

HARD
  C1: [constraint] — Why: [reason; what would need to change to relax this]
  C2: [constraint] — Why: [...]

SOFT
  C4: [constraint] — Negotiation condition: [what would justify violating this]

PREFERENCE
  C6: [constraint]

CONFLICTS DETECTED
  C1 vs. C4: [description of conflict] — Resolution: [which takes priority and why]
```

---

## PHASE 3 — FEASIBILITY CHECK

Before generating solutions, confirm a feasible solution space exists.

### Feasibility test

A constraint set is infeasible if:
- Two immovable constraints directly contradict each other
- The immovable + hard constraints together eliminate all possible solutions
- The resource constraints (time, budget, people) are insufficient to satisfy the minimum requirement

### Infeasibility handling

If the constraint set is infeasible:
1. Identify the **minimum constraint relaxation** that creates a feasible space
2. Rank relaxations by: easiest to achieve, least costly, most reversible
3. Present to the user: "There is no solution that satisfies all constraints simultaneously. The smallest change that creates a feasible space is: [X]. Do you want to relax that?"

Never generate solutions in an infeasible space. An impossible solution is not a solution.

```text
FEASIBILITY REPORT

Status: FEASIBLE | INFEASIBLE | MARGINALLY FEASIBLE

[If INFEASIBLE]
Conflicting constraints:
  [C1] directly contradicts [C2] because [reason]

Minimum relaxation to achieve feasibility:
  Option A: Relax [C1] — cost: [impact]
  Option B: Relax [C2] — cost: [impact]

[If MARGINALLY FEASIBLE]
Warning: Only [N] solutions exist. All involve [tradeoff].
```

---

## PHASE 4 — SOLUTION GENERATION

### Solution generation rules

1. **Hard constraints first.** Do not present a solution that violates any immovable or hard constraint, ever.
2. **Optimize soft constraints after.** Among feasible solutions, rank by how well they satisfy soft constraints.
3. **Constraints as creative forcing functions.** When a constraint seems to make a good solution impossible, ask: what does this constraint enable that the unconstrained version can't?
4. **Fewer resources = more focus.** A tight budget forces prioritization. A hard deadline forces scope reduction. Use this.
5. **Constraint combination.** Sometimes two constraints together point to a specific solution that neither points to alone.

### Constraint-as-design-material moves

| Constraint | Design move |
| --- | --- |
| **No budget** | Leverage network effects, earned media, open source, reciprocal value |
| **Tiny team** | Design for force multiplication — each action creates compound returns |
| **No time** | Find the existing solution that's 80% there; don't build from scratch |
| **Legacy tech stack** | Wrap, don't replace — thin layer that adds the capability without replacement |
| **Regulatory constraint** | Use compliance as a moat — competitors face the same constraint; get ahead of it |
| **No distribution** | Find a platform with existing distribution that benefits from your solution |
| **Hostile users** | Design incentive structures where self-interest aligns with correct behavior |

### Solution output format

```text
SOLUTION [N]

Satisfies:
  Immovable: ✓ all ([N])
  Hard:      ✓ all ([N])
  Soft:      [N]/[N] — [which soft constraint is violated and why]

Approach: [2–3 sentences: what this solution actually does]

Why this works within the constraints:
  · [constraint] is satisfied because [mechanism]
  · [constraint] is satisfied because [mechanism]

The constraint that shaped this solution most:
  [C_X]: [how this constraint forced the key design decision]

Limitation:
  [What this solution can't do, honest assessment]
```

---

## PHASE 5 — CONSTRAINT INSIGHT

The best constraint-based solutions reveal something about the problem the user
didn't see before entering the constraint space.

### Constraint insight patterns

| Pattern | What it reveals |
| --- | --- |
| **Constraints force prioritization** | The constraint revealed what actually matters — the rest was waste |
| **Constraints expose assumptions** | The "impossible" constraint assumed something that turned out to be negotiable |
| **Constraints create differentiation** | The tightest constraint is what competitors don't have — it's a feature |
| **Constraints compress timelines** | Resource constraints make scope clear; unclear scope was the real problem |
| **The constraint is the solution** | Leaning into the constraint rather than working around it produces the best outcome |

### Constraint insight format

```text
CONSTRAINT INSIGHT

The most important constraint was: [C_X]
Why: [This constraint, rather than being an obstacle, forced: ...]

What the constraint revealed about the real problem:
  [1–2 sentences: what you now know about the problem that wasn't visible before
  entering the constraint space]

If you could only keep one constraint, keep: [C_X]
Because: [this constraint is doing the most work — it's the signal, not the noise]
```
