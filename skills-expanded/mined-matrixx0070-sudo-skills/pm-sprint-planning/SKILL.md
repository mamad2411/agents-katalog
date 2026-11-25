---
name: pm-sprint-planning
version: 1.0.0
description: Plan a sprint the team can actually commit to — one goal, honest buffered capacity, P0 commitments vs stretch, readiness-checked items, and named slip risk.
author: matrixx0070
tags: [product, sprint, planning, agile, execution, capacity]
capabilities: []
---

# Sprint Planning

## When to use
Use this when a new sprint or cycle is starting and you need a plan the team can commit to, with a single goal, honest capacity, and a clean line between must-ship and nice-to-have.

**Not for:** cross-cycle roadmap sequencing (use pm-roadmap-update), backlog grooming of undefined ideas, or a single-feature spec (use pm-write-spec). If the team has no groomed, estimated backlog, groom first, do not plan on vapor.

## Method
1. Set one sprint goal: a single sentence naming the outcome that makes the sprint a success. **Decision point:** if you cannot name one, the scope is unfocused, stop and narrow.
2. Compute real capacity: person-days minus meetings, on-call, PTO, and support load. Do not plan to 100%; leave buffer.
3. Pull candidate work in order: carryover from last sprint, then goal-aligned items, then dependencies blocking others.
4. Classify P0 (must ship to hit the goal), P1 (planned if capacity holds), Stretch (only if all else lands). **Decision point:** if P0 exceeds buffered capacity, cut scope now, do not hope.
5. Check readiness: each committed item has acceptance criteria, no unresolved blockers, and an estimate. Kick back anything not ready.
6. Name risks and the single most likely thing to slip.

## Example
Goal: "Users can reset their password without contacting support." Capacity: 5 devs x 8 working days = 40 person-days, minus ~30% overhead = 28 usable. P0 = reset flow + email service (18 pts). P1 = audit logging (6 pts). Stretch = localization. Readiness: email service blocked on SecOps sign-off, flagged as top slip risk with a Monday deadline to unblock.

## Pitfalls
- Planning to 100% capacity, so any surprise blows the sprint.
- Committing items with no acceptance criteria, guaranteeing scope arguments later.
- A vague or multi-part goal that lets everything feel "in scope."
- Treating stretch items as commitments the team is judged on.

## Output format
```
# Sprint Plan: [sprint name] — [dates]
Sprint goal: one sentence.

## Capacity
Available: X person-days | Planned: Y | Buffer: Z%

## Committed (P0)
- [item] — estimate — acceptance criteria ref

## Stretch
- [item] — estimate

## Carryover from last sprint
- [item] — reason

## Risks & dependencies
- ...
Top slip candidate: [item] — why.
If planned > capacity: proposed cuts here.
```
