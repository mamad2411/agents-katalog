---
name: wave
description: >-
  Break a Plan into numbered Waves and write task briefs under .waves/. Use when
  the user asks to plan, split, or prepare work for Waves; use wave-iterate to
  execute or resume a planned Wave.
---

# Wave

Cut the Plan into numbered **Waves**. A Wave is one moment: every task in it is merge-independent and can run in parallel. Tasks inside a Wave are letters (`1A`, `1B`). Each task ships as its own pull request. Start the next Wave only after every PR in the current Wave is merged and none of the halt labels below are present.

Dependencies belong in a later Wave. If `B` needs `A` merged first, `A` and `B` are different Waves.

Every run **must** break the Plan into tasks and write each task to a markdown file. Do not keep the breakup only in chat. Prefer tasks small enough for **Composer 2.5**. This skill plans only: `/wave-iterate` evaluates, resumes, and executes the current Wave.

## Halt, checker, merge

Treat these three as the only gate:

| Signal | What it is | What to do |
| --- | --- | --- |
| Halt labels | `needs-human`, `needs-decision`, `blocked` on a Wave PR | Stop. Report the PR URLs and labels. Wait for the user. |
| Checker | A GitHub check run failed, or a bot requested changes | Keep working that task: fix, push, re-run **validate**. |
| Merge | Every PR in this Wave is merged, and no halt label is present | Start the next Wave. |

Follow **validate** on each open Wave PR (give it the PR number or URL). After a checker fix, validate that PR again.

**Done when (gate):** halt labels are acted on as a stop, checker failures are still in iteration, and the next Wave starts only on the merge row.

## 1. Cut the Plan

Read the Plan in this conversation. Assign every Plan item to exactly one task id `{wave}{letter}` (Wave `1`, `2`, …; letters `A`, `B`, …). Put two items in the same Wave only when they can merge in any order onto the same base.

Mark each task **Kind** as `implementation` or `research`. Split work so most tasks are `implementation` and small enough for Composer 2.5. Use `research` only when the work is investigation, docs, or API facts with little or no product-code ship.

Derive `<topic>` as a kebab-case slug from the Plan title. If the Plan has no title, ask the user for a short topic slug before writing files.

Show the board, then write the task files (step 2):

```text
Wave 1
  1A  implementation  <title>  — <one-line scope>
  1B  research        <title>
Wave 2
  2A  implementation  <title>
```

**Done when:** every Plan item appears exactly once, same-Wave tasks have no merge-order dependency, each row has a Kind, and the board is visible to the user.

## 2. Write task files

On every run (including when advancing to a later Wave), write or overwrite one markdown file per task. Paths are relative to the repo root:

```text
.waves/<topic>-<wave-no>/<kebab-title>-<task-no>.md
```

Default root is `.waves/` at the repo root. Do not write under `waves/` unless the user names a different root.

- `<topic>` — kebab-case Plan title
- `<wave-no>` — Wave number (`1`, `2`, …)
- `<kebab-title>` — kebab-case of that task's title
- `<task-no>` — full board id (`1A`, `1B`, `2A`, …)

Example: `.waves/checkout-redesign-1/add-login-1A.md`

Each file is the **full task brief**. Use this shape:

```markdown
# <task-no> <title>

- Task id: <task-no>
- Wave: <wave-no>
- Topic: <topic>
- Kind: implementation | research
- Model: <set in step 3; leave blank until then>
- Base: <branch or SHA>
- Status: planned
- PR: <leave blank until opened>
- Quality: not-run

## Scope

<only this task's Plan scope>

## Ship

- Implement, commit, push, and open one PR
- Stop after the PR URL exists
- Do not implement sibling tasks or later Waves
```

Write **every** Wave's files when cutting the Plan. When a Wave starts, rewrite that Wave's files if the board or base SHA changed.

**Done when:** every board row has a file at that path, and the files match the current board.

## 3. Hand off to iteration

Tell the user that the Plan is staged, summarize the Wave board, and direct them to run `/wave-iterate` when they want to evaluate the next actionable Wave and continue. Do not select models, create worktrees, launch workers, validate PRs, or make GitHub changes.

**Done when:** every board row has a task file and the user has a concise board summary plus the `/wave-iterate` next step.
