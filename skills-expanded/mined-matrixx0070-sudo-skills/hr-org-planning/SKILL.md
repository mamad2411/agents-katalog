---
name: hr-org-planning
version: 1.0.0
description: Plan headcount, design org structure, and shape team topology against goals and budget — every role tied to an outcome and a cost.
author: matrixx0070
tags: [org-design, headcount, workforce-planning, team-structure, budget, spans-layers]
capabilities: []
---

## When to use

Reach for this when building a hiring plan for a quarter or year, restructuring a team, or pressure-testing whether the org can deliver its roadmap. Tie every proposed role to a business outcome and a fully-loaded cost.

**Not for:** benchmarking a single role's pay (use hr-comp-analysis), reporting current workforce metrics (use hr-people-report), or managing live candidates (use hr-recruiting-pipeline).

## Method

1. **Anchor to goals** — list the objectives the org must deliver and the capabilities each requires. Gaps between required and current capability drive the plan.
2. **Baseline current state** — map existing roles, levels, reporting lines, and spans of control; flag over/under-loaded managers and single points of failure.
3. **Size headcount** — for each capability gap specify role, level, count, quarter of hire, and rationale. Decision point: separate backfills from net-new growth; they compete differently for budget.
4. **Design structure** — propose reporting lines and team boundaries; target healthy spans (~5-8 reports) and clear ownership with minimal cross-team dependency.
5. **Sequence and budget** — order hires by priority and dependency, estimate fully-loaded cost per role, and total against budget. Account for ramp lag before productivity.
6. **Stress-test** — check attrition assumptions, key-person risk, funnel diversity, and what breaks if budget is cut 20%. Decision point: if the plan can't survive the cut scenario, re-sequence to protect the highest-leverage hires.

## Example

Goal: ship a self-serve billing product in H2. Capability gaps: payments backend (none today), billing PM, and support coverage. Plan — 2× Backend Eng (L4/L5, Q3, net-new, ~$260k loaded each), 1× PM (L4, Q3, net-new, ~$230k), 1× Support (L2, Q4, net-new, ~$110k). Total ~$860k loaded. Current billing team span = 9 under one EM → split into two pods. Cut-20% scenario: drop the L4 backer and slip the L2 to next year; PM + one senior eng are the irreducible core.

## Pitfalls

- Proposing roles without a named outcome — headcount that can't be defended when budget tightens.
- Ignoring ramp lag and booking a Q3 hire as fully productive in Q3.
- Spans that balloon past ~8 (manager overload) or shrink below ~3 (too many layers).
- Costing salary only, omitting benefits, tax, equipment, and overhead in the "fully-loaded" figure.

## Output format

```
Goals → capabilities → gaps table
Current-state snapshot: role | level | reports-to | span
Headcount plan: role | level | count | quarter | backfill/new | rationale | loaded cost
Proposed org chart: reporting lines + team boundaries
Sequenced roadmap: priority order + budget total
Risks & trade-offs (incl. -20% cut scenario)
```

## Reference

### Spans and layers — healthy ranges

**Span of control** = direct reports per manager. **Layers** = management levels from IC to CEO.

| Span | Reading |
|---|---|
| < 3 | Too narrow — likely an unnecessary layer, or a manager who should be an IC/player-coach |
| 4–6 | Good for complex, high-judgment work (senior eng, research) |
| 6–8 | **Healthy default** for most professional teams |
| 8–10 | Good for well-defined, repeatable work (support, sales, ops) |
| > 10 | Overloaded — manager can't coach; either add structure or the role is really "coordinator" not "manager" |

**Layers** should stay minimal — most companies under ~500 people need only 4–5 layers (IC → manager → director → VP → exec). Extra layers slow decisions and dilute accountability. A useful diagnostic: if the org has many managers with spans <4, you have a layering problem; flatten before you hire.

### Fully-loaded cost

Never budget salary alone. Fully-loaded cost ≈ base × a multiplier that captures the true cost of employment:

```
fully-loaded cost ≈ base salary × 1.25 to 1.4   (US professional roles)
```

Components rolled in: employer payroll taxes (~7.65% US FICA + unemployment), benefits (health, retirement match — often 20–30% of base), equipment/software/seat, recruiting amortization, and overhead. For quick planning, **1.3× base** is a reasonable default; state the multiplier as an assumption. Add target bonus and annualized equity separately if your budget tracks total comp rather than base.

### Ramp lag — don't book a hire as productive on day one

A Q3 hire is not Q3 capacity. Apply a ramp discount:

| Role type | Time to full productivity |
|---|---|
| Junior/operational | 1–2 months |
| Professional IC | 3–4 months |
| Senior/specialist | 4–6 months |
| Manager | 3–6 months |
| Executive | 6–12 months |

Add a **time-to-fill** lag before ramp even starts (see below). A role you approve today typically delivers meaningful output one to two quarters later. Model effective capacity, not headcount count.

### Time-to-fill for sequencing

Back-date the requisition open date from when you need the capacity:

- Junior/high-volume: ~30 days
- Professional/technical: 45–60 days
- Senior/executive/scarce: 60–120+ days

Sequence hires so recruiting for a Q3-productive senior role starts in Q1. A plan that opens all reqs the quarter capacity is needed is already late.

### Backfill vs. net-new

Separate them explicitly — they compete for budget differently and signal different things:

- **Backfill** — replacing an exit; usually pre-approved against existing budget; the work already exists. Track backfill rate as a proxy for attrition load.
- **Net-new / growth** — expanding capacity for new scope; must be justified by a business outcome and defended when budget tightens.

Never blend them in one total; leadership will want the growth number isolated.

### Team topology patterns

Design for low cross-team dependency and clear ownership:

- **Stream-aligned** — owns a product/value stream end-to-end; the default, most teams should be this.
- **Platform** — provides internal services/tools that reduce cognitive load for stream teams.
- **Enabling** — helps other teams adopt a capability, then disbands/moves on.
- **Complicated-subsystem** — a specialist team for a genuinely deep area (e.g., a pricing engine).

Aim for teams that can deliver value with minimal hand-offs. If two teams must constantly coordinate to ship, the boundary is wrong — re-cut it. Conway's Law: your architecture will mirror your org chart, so design the org to match the system you want.

### Headcount-sizing method (capability-gap driven)

1. List objectives → the capabilities each requires.
2. Score current capability (have / partial / none) per objective.
3. For each gap: role, level, count, quarter-of-hire, backfill-or-new, one-line rationale tying it to the objective.
4. Attach fully-loaded cost per role; total against budget.
5. Order by priority × dependency (a role that unblocks others ranks higher).

Every role must trace to an outcome. A role with no named outcome is the first thing cut when budget tightens — and rightly so.

### Stress tests to run

- **−20% budget** — which hires survive? Name the irreducible core; re-sequence the rest.
- **Key-person risk** — what breaks if a single senior person leaves? Any single point of failure is a hiring or documentation priority.
- **Attrition assumption** — model expected exits (see people-report); backfill load competes with growth.
- **Ramp-adjusted capacity** — does the roadmap still land once ramp lag and time-to-fill are applied?
- **Funnel realism** — can you actually source the scarce roles in the quarter you need them?

### Quick reference numbers

```
fully-loaded cost   ≈ base × 1.3            (default; 1.25–1.4 range)
healthy span         = 6–8 reports          (4–6 complex, 8–10 defined)
layers (<500 ppl)    = 4–5                   (flatten if managers span <4)
effective capacity   = headcount × (1 − ramp_fraction_this_period)
open req lead time   = time-to-fill + ramp   (start recruiting this far ahead)
```
