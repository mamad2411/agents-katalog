---
name: plan
description: Produce a phased, risk-assessed implementation plan from a spec. Use after /spec and /research, before writing code. Delegates to the harness-claude:planner agent for non-trivial work.
---

# /plan — phased implementation plan

Goal: a plan an executor (you or a subagent) can follow without re-deriving context.

## Do this
1. For non-trivial work, **delegate to the `harness-claude:planner` agent**, passing it the spec
   (read `.claude/planning/<slug>/SPEC.md` if present — the slug is in `.claude/STATE.md`),
   the reuse decision, and the objective/purpose (not just a one-line query).
2. For small/linear work, plan inline using the same shape.
3. Break work into **phases/tasks**: each small, independently verifiable, with an exit check.
   Give each task an ID (`T1`, `T2`, …), its **write-set** (files it will create/edit), a
   `depends_on` list of prior task IDs, and the `AC-n` criteria it **addresses** — the
   format `/harness-claude:orchestrate` and `/harness-claude:verify` consume (schema: `docs/state-and-artifacts.md`).
4. Surface risks, dependencies, and ordering explicitly. **Red-team the plan before
   handing it off** — assume it already failed and ask why; attack your own draft for
   hidden assumptions and missing edge cases, not just the obvious risks. Note where
   you'll need an architecture decision (`/harness-claude:architect`) vs. where the path
   is obvious.
5. **Flag parallelizable phases.** From the per-phase file lists, mark any phase that writes
   **3+ independent files with disjoint write-sets and no cross-dependency** as an
   `/harness-claude:orchestrate` candidate. This is what makes `/implement` surface the parallel
   fan-out offer instead of silently editing serially — if you don't flag it here, it's usually
   missed there. Flag only genuine cases; if none qualify, say so.

## Output
For non-trivial work, **write `.claude/planning/<slug>/PLAN.md`** (present a summary in the
reply too); for trivial work, the plan in the reply is enough (say so). Format:

```
## Plan: <title>
## Tasks
### Task T1: <goal>
- files: <write-set>
- depends_on: []
- addresses: AC-1, AC-2
- exit check: <test/build/behavior>
### Task T2: ...
## Risks & dependencies
## Parallelizable phases (if any) — tasks with 3+ independent files, disjoint write-sets → /orchestrate candidates
## Where /architect is needed (if any)
```

## State
When you wrote a `PLAN.md`, patch `.claude/STATE.md`: `phase: plan`, `status: done`,
`next_skill: /plan-check`.

## Orchestration note
This is the canonical **sequential-phase** flow (see rules/agents.md). Compact context
before heavy implementation.

## Exit criterion
Every task has a write-set, `depends_on`, the `AC-n` it addresses, and a concrete exit
check. Then `/harness-claude:plan-check` (gate the plan before building) — or
`/harness-claude:architect` first if flagged.
