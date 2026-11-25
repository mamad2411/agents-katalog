---
name: plan-architecture
description: Architecture design for the Planning phase — codebase convention discovery, 2-3 option trade-off analysis, and the PLAN.md structure that Codex executes against.
---

# Architecture Planning

**Helpers**: required — context-slice.mjs (helper rule).

## Step 1 — Discover conventions before designing

Read `.codex-flow/PROJECT.md` first when it exists — it is the durable project context. Then read the codebase until you can answer: How are modules organized (by feature or by layer)? How do errors propagate? Where does validation live? How is the existing code tested? What naming style rules? Your design must read like the codebase's current author wrote it — deviations are review findings waiting to happen.

## Step 2 — Compare options before choosing

For any non-trivial design decision, write 2–3 realistic options with trade-offs:

```markdown
### Decision: <what>
- Option A: … | + simple, matches existing pattern X | − doesn't scale past Y
- Option B: … | + handles Y | − new dependency, more moving parts
→ Chosen: A, because Y is out of scope (see requirements).
```

Never present only one option — the first idea is rarely the best, and the comparison is what makes the plan reviewable. Tie every "chosen because" back to a confirmed requirement.

## Step 3 — Define the contracts, then the component→files map

This is the step that makes the backlog sliceable and the review deterministic. Before writing tasks:

- **Contract-first**: pin down the seams *between* components — function/method signatures, data
  shapes (types/schemas), API request/response contracts, event/DB record shapes. Write them in
  PLAN.md concretely, not "a service that returns users". Once a boundary's contract is fixed, work
  on either side of it becomes independent and each task reviews against a stable contract instead
  of a moving target. Shared contracts (types, interfaces, schema/migration) become the FIRST tasks
  so everything downstream can build — and be reviewed — against them.
- **Component → files map**: for each component the change touches, list the exact files to create
  or modify. This is what the backlog slices along; keeping the per-component file sets disjoint is
  what later lets `task-waves` run tasks in parallel. Overlapping file sets = tasks that must
  serialize — call that out here.
- **Codex is repo-blind**: it sees only the prompt + files it opens. Name the exact existing files
  it should read for patterns (`follow the shape of src/api/orders.ts`), and spell out any
  repo-wide convention it can't infer from the task's files alone.

## Step 4 — Write PLAN.md

Use the full structure the flow executes against (all sections — the reviewer reads these back in Phase 5):

```markdown
# Plan: <feature>
## Context             — what the project is; conventions Codex MUST follow (list them explicitly)
## Objective           — confirmed goal from the interview
## Architecture        — components touched, data flow, decisions + why (from step 2)
## Contracts           — the fixed seams from step 3: signatures, data shapes, API/event contracts
## Component → files    — each component mapped to the exact files it creates/modifies (feeds the backlog)
## Risk & blast radius  — sensitive areas touched (auth, data, migrations, config), what could
                          break beyond the target files, and the rollback point (Phase 0 baseline ref)
## Skills plan
- *Verdict per facet* — `LOAD` / `VET` / `AUTHOR` for every facet the plan depends on; no empty state (a facet with no match resolves to `AUTHOR`, never to `—`)
- *Skills to use*     — domain skills selected via skill-selection (name, path, what each informs), plus any authored in this flow
- *Skills to create*  — outstanding `AUTHOR` verdicts (working name, gap filled, rules inline); write `—` only when every facet resolved to `LOAD` or `VET`
## Known-red baseline   — pre-existing test failures recorded in Phase 0 (so review blames only new ones)
## Out of scope        — things Codex must NOT do or touch
## Acceptance criteria — verifiable checks for the whole feature
## Decision log        — empty, append-only; after each task passes, append one block:
### T<n> — <title>
- Decision: <what was decided or deviated from the plan>
- Why: <reason tied to a requirement/finding>
- Constraint for later tasks: <what future tasks must respect> | —
- Contracts touched: <signatures/shapes changed or confirmed> | —
- Anchor: <git HEAD sha at append time>
- Applies to: <task IDs, files, or contract labels — 'all' for run-wide constraints>
```

Keep `## Context` to one paragraph followed by a bullet list of conventions. Duplicate those
conventions into the nearest applicable AGENTS.md (their durable per-package home) instead of
growing Context with more prose.

After each task passes, append exactly one block using this schema. The log must let a FRESH Claude
session resume from disk without the original conversation. Decisions without their constraints
are not a handoff.

The ONLY per-task writer is the post-review step: Phase 4 step 6 in sequential mode, or the
coordinator after the wave merge in parallel mode. Review steps and worktree subagents provide
their outcomes to that writer and never append a second task block.
After appending, run `node "${CLAUDE_PLUGIN_ROOT}/scripts/context-slice.mjs"
--check-plan`; fix failures before the next task.

When appending either schema, have that single writer run `git rev-parse HEAD` and record the
result in `Anchor`. Reference code only as `path:line` plus the enclosing symbol; never paste code
snippets into a Decision-log block.

Writers SHOULD fill `Applies to`; run-wide constraints use `all`.

For wave integrations, the final review, and declined improvements, append one non-task event block
using the same schema with `T<n>` replaced by the event name:

```markdown
### <event> — <label>
- Decision: <what was decided or what happened>
- Why: <reason tied to a requirement/finding>
- Constraint for later tasks: <what future tasks must respect> | —
- Contracts touched: <signatures/shapes changed or confirmed> | —
- Anchor: <git HEAD sha at append time>
- Applies to: <task IDs, files, or contract labels — 'all' for run-wide constraints>
```

A non-task event block must carry the first four fields; `Anchor` and `Applies to` are required
only in task blocks.

## Design principles

- Smallest architecture that satisfies the confirmed requirements — no speculative extension points (YAGNI).
- Respect existing boundaries; don't introduce a new layer/pattern unless an option-analysis justifies it.
- Design for testability: seams (injected dependencies) where Codex will need to fake I/O.
- **Design for the diff**: prefer changes that stay localized and additive over invasive rewrites,
  so each task produces a small diff a reviewer can fully verify in one pass (and stays under the
  64 KB diff cap). A change that forces edits sprawling across many files is a design smell — revisit.
- **Design for independence**: minimize cross-task coupling by fixing contracts up front (step 3);
  the fewer files two tasks share, the better they slice, parallelize, and review.
- Flag risky areas (migrations, shared state, public API changes) so the backlog isolates them into their own tasks.
