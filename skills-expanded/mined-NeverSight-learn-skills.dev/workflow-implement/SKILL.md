---
name: workflow-implement
description: >-
  Implementation phase for GitHub-issue workflows. Reads handoff from the work
  branch, merges language into PROJECT.md, implements with TDD red-green cycles,
  commits handoff updates on branch, and sets workflow:review. Use when a routine
  fires on workflow:implement or for issue $0.
disable-model-invocation: true
metadata:
  internal: true
---

# Workflow: Implement

Build per approved `requirements.md`. **Bugfix mode** (`state.mode: bugfix`) follows bugfix process below.

Triggered by **`workflow:implement`**. Reads handoff from **`workflow/issue-{n}`** / `workflow/issues/{n}/`. See [handoff-format.md](../workflow-routines/handoff-format.md), [state-schema.md](../workflow-routines/state-schema.md), [label-rules.md](../workflow-routines/label-rules.md).

## Preconditions

1. Label **`workflow:implement`** (only one workflow label).
2. Branch **`workflow/issue-{n}`** exists with `workflow/issues/{n}/state.json`.
3. `requirements_approved: true`; `requirements.md` approval checked.
4. If `implement-handoff.md` exists and phase past implement — stop; review should run.

If preconditions fail, post short issue comment. **Do not create a new branch.**

## Start sequence

1. Read issue.
2. **Checkout `workflow/issue-{n}`**; pull latest.
3. Read `workflow/issues/{n}/` per handoff-format.
4. Verify `workflow/PROJECT.md` on branch.
5. Post session comment — **vary phrasing** (handoff-format implement example bank). Must link session; branch link optional.
6. **Commit handoff (start)** — update `state.json`: `phase: implement`, `status: ai_running`, history `started`; push.
7. Merge language → PROJECT.md; commit ADRs if present.
8. Feature or bugfix process.
9. Complete sequence.

## Prepare repo

Branch already exists — **do not create a new one**.

1. Merge `language.md` → `workflow/PROJECT.md` `## Language`.
2. Commit `adrs.md` → `docs/adr/` if present.
3. Commit workflow merge if changed; push.

## Feature / bugfix process

TDD red-green per PROJECT.md; push branch.

## implement-handoff.md

Write to `workflow/issues/{n}/implement-handoff.md` at complete. (Use feature template with Summary, Branch, Changes, TDD cycles, Test results, Acceptance criteria, Suggested review scenarios.)

## Complete sequence

1. Write `implement-handoff.md`.
2. Update `state.json` — `status: done`, `workflow_label: workflow:review`, history.
3. Commit + push handoff files.
4. `gh pr create --draft --head workflow/issue-{n} --base {base_branch} …`
5. Short issue comment — **vary phrasing** (handoff-format implement complete bank). Must link draft PR.
6. **Swap labels last** — `workflow:review`. **Stop.**

## Writable locations

| Location | Files |
|----------|-------|
| Branch | app code, tests, `workflow/PROJECT.md`, `docs/adr/`, `workflow/issues/{n}/` |
| Issue | short comments only |

## Hard rules

- **Never create a new branch.**
- **Commit handoff at start and complete.**
- **Never put artifacts in issue comments.**
- Push failure → short comment and **stop**; do not advance labels.
- **Label swap always last.** PR always **draft**.
