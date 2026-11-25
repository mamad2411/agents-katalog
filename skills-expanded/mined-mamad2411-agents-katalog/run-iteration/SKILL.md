---
name: run-iteration
description: Use when executing the next pending iteration from an iterate roadmap — picks the iteration, decomposes into code and evidence tasks, runs sentinel corpus baseline, dispatches implement-tasks, runs impacted + sentinel scenarios, and updates artifacts.
---

# Running an Iteration

## Overview

Drives one iteration: picks the next pending, runs sentinel corpus baseline, runs pre-iteration scope review via PAR, decomposes into code and evidence tasks, dispatches `implement-tasks`, runs impacted + sentinel scenarios at wrap-up, and updates the roadmap and iteration log.

## When to Use

Invoked by `iterate` inside the main loop. Each invocation runs exactly one iteration. After return, the orchestrator invokes `audit-progress`.

## Script Location

All scripts referenced below live in this skill's `scripts/` directory, next to this SKILL.md file.

## Iteration Process

### 1. Pick next iteration

Read `docs/moe/iterations/roadmap.md`, find the first iteration with status `pending`.

### 2. Load scope context

Read the per-epic files in `docs/moe/iterations/requirements/` to load the full story cards for each committed story ID. Only read the epic files that contain stories for this iteration — not all of them. Also:
- Load the next 3 pending iterations from the roadmap for look-ahead
- Read `docs/moe/iterations/behavior-scenarios.md` to identify impacted scenarios
- Read `docs/moe/iterations/behavior-corpus.md` to identify sentinel scenarios

### 3. Run sentinel corpus baseline

Before any code changes, run every scenario in the behavior corpus with run cadence `sentinel`:

- If all sentinels pass: record baseline as clean, proceed
- If any sentinel fails: the failure predates this iteration. Record it, create a gap story for it, but proceed with the iteration (the gap will be addressed in a follow-up)

This establishes whether regressions exist before the current iteration starts.

### 4. Pre-iteration consistency audit

Before planning any work, verify that artifact state is consistent:

1. **Citation check:** Resolve {resource:skills/run-iteration/scripts/check_citations.mjs} relative to this loaded document, then invoke it as `node "<resolved-check_citations.mjs>" docs/moe/iterations/roadmap.md docs/moe/iterations/requirements/`. If citations fail, stop and fix the roadmap.
2. **Status reconciliation:** For each story in this iteration's scope, verify:
   - Stories listed in the roadmap iteration are not already marked `done:ITER-XXXX` in the requirements index (unless code/tests actually exist for them)
   - Stories marked `done` in the requirements index actually have corresponding code and tests
   - No story appears in multiple pending iterations
3. **Epic counter validation:** Spot-check that epic progress counters match the actual count of `done` stories.

If any inconsistencies are found, reconcile before proceeding. Do not trust any single artifact blindly — cross-check.

### 5. Pre-iteration scope review (PAR)

Following {resource:skills/_shared/parallel-adversarial-review.md}, resolved relative to this loaded document:

1. Build the scope reviewer prompt using `scope-reviewer-prompt.md`
2. Resolve {resource:skills/_shared/par-reviewer-wrapper.md} relative to this loaded document and wrap in its competitive framing
3. Dispatch TWO scope reviewers in parallel
4. Aggregate findings: same issue from both = high confidence, unique = still actionable, severity disagreement = take worst
5. If REVISE recommended: adjust iteration scope and re-review. Loop until APPROVE.

### 6. Decompose into code tasks AND evidence tasks

Break the iteration scope into TDD-sized tasks. Each task = failing test → implementation → passing test → commit.

**Evidence tasks:** In addition to code tasks, identify:
- Which existing scenarios are impacted by this iteration's changes
- Which new scenarios must be added (from the story proof obligations)
- Which scenario harnesses need to be extended
- Which behavior corpus entries need updated execution commands

Evidence tasks are first-class — they produce scenario updates, test harness extensions, and corpus index entries. They are NOT afterthoughts. Interleave evidence tasks with code tasks: after implementing a feature, the next task should be extending or adding the scenario that proves it.

**Cross-iteration dependencies:** Some stories reference subsystems that don't exist yet. For these, implement the thinnest abstraction boundary that satisfies the story's ACs without coupling to the future implementation. Prefer a single clean interface over a decomposed hierarchy — the real implementation will define its own internal structure when it arrives. Document the dependency with a TODO comment citing the future iteration. Do NOT defer the story silently or force premature integration.

### 7. Dispatch implement-tasks

Pass the task list (code + evidence tasks) and iteration context to `implement-tasks`. Wait for completion.

### 8. Post-iteration scenario runs

After all tasks complete, run:

1. **Impacted scenarios:** every scenario in the behavior corpus whose owning stories were touched by this iteration
2. **Sentinel scenarios:** every scenario with run cadence `sentinel`

If any impacted or sentinel scenario fails that passed at baseline (step 3), this iteration introduced a regression. Create a fix task and re-dispatch to `implement-tasks`.

### 9. Resolve cross-iteration TODOs

Grep the codebase for `TODO(ITER-<current>)` markers — these are interface stubs that earlier iterations created expecting THIS iteration to provide the real implementation.

For each marker found:
1. Verify the real implementation now exists (not still a stub/NoOp)
2. If resolved: remove the TODO comment
3. If NOT resolved: the iteration is incomplete — add a fix task and re-dispatch

This step is a hard gate. An iteration that leaves its own TODO markers in the code is not done.

### 10. Wrap up

- Verify all iteration stories' ACs pass (sanity check before audit)
- Verify all proof obligations for observable ACs have corresponding scenario evidence
- Verify no `TODO(ITER-<current>)` markers remain in the codebase (step 9)
- Mark stories `done:ITER-NNNN` in the relevant epic files under `requirements/`
- Update scenario automation status and execution commands in `behavior-scenarios.md`
- Update the behavior corpus index in `behavior-corpus.md`
- Update iteration status in `roadmap.md` to `done`
- Append entry to `docs/moe/iterations/iteration-log.md` — include:
  - Stories delivered
  - Scenarios added or updated
  - Sentinel corpus results
- Validate: resolve {resource:skills/run-iteration/scripts/validate_iteration_log.mjs} relative to this loaded document, then invoke it as `node "<resolved-validate_iteration_log.mjs>" docs/moe/iterations/iteration-log.md`
- After each task commit, update the progress snapshot with `moe jig progress update --phase ... --task ... --iterations ... --event ...`. If `moe-jig` is not on PATH, overwrite `docs/moe/iterations/progress.md` manually.
- Return control to orchestrator (do NOT invoke `audit-progress` — that's the orchestrator's job)

## Quick Reference

| Step | Tool/Skill | Purpose |
|---|---|---|
| Sentinel baseline | Run sentinel scenarios | Establish pre-iteration regression state |
| Citation check | `scripts/check_citations.mjs` | Mechanical: cited stories exist |
| Scope review | PAR + `scope-reviewer-prompt.md` | Semantic: scope, scenarios, splitting, boxing-in |
| Task execution | `implement-tasks` | TDD code + evidence implementation |
| Post-iteration runs | Run impacted + sentinel scenarios | Catch regressions |
| TODO resolution | `grep -rn 'TODO(ITER-<current>)'` | Cross-iteration stubs resolved |
| Wrap up | `scripts/validate_iteration_log.mjs` | Artifact validation |

## References

- {resource:skills/_shared/parallel-adversarial-review.md} — PAR methodology; resolve relative to this loaded document
- {resource:skills/_shared/behavior-evidence-formats.md} — scenario and proof obligation formats; resolve relative to this loaded document
- `scope-reviewer-prompt.md` — scope reviewer prompt template
- [check_citations.mjs](./scripts/check_citations.mjs) — mechanical citation check
