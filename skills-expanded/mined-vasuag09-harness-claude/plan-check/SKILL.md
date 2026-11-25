---
name: plan-check
description: Adversarially review a plan against its spec before implementation — check that every acceptance criterion is covered, no scope crept in, and parallel tasks have disjoint write-sets. Use after /plan, before /implement. Read-only gate; delegates to the harness-claude:planner agent in a check pass. Non-blocking except on Critical.
---

# /plan-check — gate the plan before building

Goal: catch a broken plan **before** an executor acts on it. An ambiguous or incomplete
plan produces an executor that guesses; parallel executors guessing differently about the
same file produce conflicts. Cheaper to fix the plan now than to unwind code later.

This is the plan-phase counterpart to `/harness-claude:review` — same adversarial stance, one step
earlier. It is **read-only**: it reports, it does not edit the plan.

## Do this
1. Load the artifacts: `.claude/planning/<slug>/PLAN.md` and `SPEC.md` (slug is in
   `.claude/STATE.md`). If there's no `PLAN.md` on disk (trivial/inline work), review the
   plan from the conversation instead — the checks are the same.
2. **Delegate to the `harness-claude:planner` agent in a check pass** (read-only — pass it
   the plan, the spec, and the objective: "find why this plan fails before we build it").
   Get back a summary with severities, not a raw dump.
3. Check the plan across three dimensions:
   - **Criteria coverage** — does every `AC-n` in `SPEC.md` map to at least one task's
     `addresses:`? Name any uncovered criterion.
   - **Scope** — does any task do work no criterion asked for (scope creep), or is any
     in-scope item unplanned? Flag both directions.
   - **Task independence** — for tasks meant to run in parallel (same wave / no
     `depends_on` between them), are the **write-sets pairwise disjoint**? Are
     `depends_on` edges acyclic and complete (no task reads another's output without
     declaring it)? Overlapping write-sets or a missing edge is a correctness bug.
4. Red-team it: assume the plan already failed in execution and ask why. Attack hidden
   assumptions, not just the obvious risks.
5. If findings warrant a revision, hand them back to `/harness-claude:plan` and re-check — **loop ≤ 3
   times** (per rules/agents.md), then accept or escalate to the user.

## Output
A findings list, most-severe first, each with a severity:

| Severity | Meaning | Action |
|----------|---------|--------|
| Critical | The plan **cannot** satisfy a criterion, or parallel tasks collide on a file | BLOCK — fix the plan before `/harness-claude:implement` |
| High | Likely bug or significant gap | Fix before building |
| Medium | Maintainability / clarity concern | Fix when reasonable |
| Low | Minor suggestion | Optional |

If nothing survives, say so plainly — a clean plan is a valid result.

## State
Patch `.claude/STATE.md`: `phase: plan-check`, `status: done` (or `blocked` if a Critical
stands), `next_skill: /implement`.

## Exit criterion
No Critical finding remains (High/Medium/Low may be noted and carried). Then
`/harness-claude:implement`.
