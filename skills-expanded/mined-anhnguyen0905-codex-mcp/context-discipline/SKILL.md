---
name: context-discipline
description: Enforce large-project context discipline with no-raw-read thresholds, phase-boundary compaction, and tiered AGENTS.md guidance.
---

# Context Discipline

## Why

Protect the orchestrator's working context across long backlogs.
Repeated exploration, large diffs, and verbose logs crowd out current-task evidence.
Keep bulk evidence outside the orchestrator and bring back only anchored conclusions.
Write durable state to disk so a fresh session can resume without hidden context.

## Recitation

At every phase boundary and immediately before each `codex_execute`, re-state all three in one
concise line: the current phase, the current task ID + title, and the next pending gate. Recite the
run position from current durable state; do not re-read control files solely for this recitation.

## No-raw-read rules (orchestrator)

- For a diff over 400 lines, delegate a conformance summary to a subagent, then directly read only
  targeted critical hunks.
- For test or build logs, run them via a script and inspect only tail output or grep matches. Delegate
  full-log analysis to a subagent.
- During Phase 2 exploration, use Explore subagents. Require conclusions with paths and line anchors;
  never bulk-dump files into the orchestrator.

## Tiered read-back

- Have the orchestrator and Codex read budgeted derived slices instead of whole control files:
  `.codex-flow/CONTEXT-T<n>.md` (≤ 4000 estimated tokens using the chars/4 heuristic) for each task
  and `.codex-flow/RESUME.md` (≤ 8000 estimated tokens using the chars/4 heuristic) on resume.
- Keep full `.codex-flow/PLAN.md` as the durable source of truth on disk. Read it in full only to
  resolve a disputed finding or to follow a slice's omitted-pointer line to a needed section — the
  generated slice is never optional. If the helper is not found, STOP and tell the user to reinstall the codex-flow plugin (its scripts/ directory is required); if it is present but exits non-zero, surface the error to the user and STOP. Never edit control files by hand.
- Treat derived slice files as generated views. Regenerate them; never hand-edit them.
- Check the generation anchor recorded in each slice header. Re-check every `[verify]`-stamped
  block against the current code before relying on it.

## Safe compaction points

- Phase 2 boundary: wait until the plan is approved, PLAN.md and planning.md are written, and the
  AGENTS.md guidance commit is complete. TASKS.md does not exist yet and is not required.
- Sequential task boundary: wait until the task passes review and its Decision log schema block is
  on disk. If checkpoint commits are enabled, wait for that commit too.
- Parallel wave boundary: wait until every task commit is merged, the integration review passes,
  and the coordinator appends the per-task Decision log schema blocks.
- At an allowed boundary, verify the required durable state is on disk. Tell the user this is a
  safe compaction point and suggest running `/compact`; the orchestrator cannot run that client
  command. With state on disk, an auto-compaction landing at or after the boundary is lossless.
- NEVER compact mid-task.
- Phase 5 step 0 re-reads the task's generated context slice and TASKS.md entry from disk after
  compaction; read full PLAN.md only under the Tiered read-back rules.

| Boundary | Safe compaction point? |
|---|---|
| Phase 2 plan approval | Yes — after PLAN.md, the AGENTS.md commit, and planning.md are complete |
| Sequential task completion | Yes — after review and the Decision log block; also the checkpoint commit when enabled |
| Parallel wave completion | Yes — after merge, integration review, and per-task Decision log blocks |
| Mid-implementation | No |
| After a failed approach | Record the dead end on disk, then wait for an allowed boundary; never mid-attempt |

## Tiered AGENTS.md

- Generate AGENTS.md files in Phase 2 after plan approval and before Phase 3.
- Keep the root AGENTS.md to about 50 lines or fewer. Include the project one-liner, exact
  build/test/lint commands, and repo-wide conventions Codex cannot infer.
- Create a per-package AGENTS.md only when the approved PLAN.md **Component → files** map touches
  that package and its conventions differ from the root. Apply nearest-wins semantics.
- Make additive-only changes: create AGENTS.md if missing; if present, append or propose missing
  facts. Never delete or rewrite user lines.
- Replace every angle-bracket field in this template with repository facts:

```markdown
# AGENTS.md

<Project purpose in one line.>

## Commands
- Build: `<exact build command>`
- Test: `<exact test command>`
- Lint: `<exact lint command>`

## Conventions
- <Repo-wide or package-specific fact Codex cannot infer.>
```
