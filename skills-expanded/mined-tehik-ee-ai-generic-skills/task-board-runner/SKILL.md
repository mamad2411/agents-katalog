---
name: task-board-runner
description: Runs folder-based task queues for IDE work using paths like Agent_reports/Tasks/To-Do, To-Validate, and Done; processes tasks, writes artifact subfolders, routes completed work to To-Validate or Done, runs a second-pass validation workflow to move items to Done or back to To-Do with review notes, and splits business briefs into tasks. Use when the user mentions task folders, validation queues, or Jira-style boards.
---

# Task board runner

## When this applies

The user gives **paths** (or agrees to defaults), commonly:

- **`Agent_reports/Tasks/To-Do/`** — pending tasks
- **`Agent_reports/Tasks/To-Validate/`** — finished first pass, awaiting review
- **`Agent_reports/Tasks/Done/`** — approved / final

Paths may differ per project — use the user’s directories when provided.

Or they ask to turn a **business brief / Jira dump** into many task files.

## What to do

1. **Execute the canonical workflow/command** (same IDs across IDEs):
   - Processing the queue: **`/process-task-board`**
   - Second-pass validation (e.g. stronger model): **`/validate-task-board`**
   - Brief → tasks: **`/business-brief-to-tasks`**
   - Partner / vendor sanity check: **`/validate-external-proposal`**
2. **Do not invent** folder layouts if the user specified paths — use theirs.
3. **Create artifact subfolders** under the output path whenever a task produces multiple files (diagrams, models, extra notes), and add a short `README.md` inside that subfolder.
4. **`type: code` is not a shortcut.** After opening `/process-task-board`, you must **run the full primary workflow/command** (`/implement-feature`, `/fix-bug`, or `/refactor`) and **complete every phase**, including nested flows (`/analyze-codebase`, `/create-branch`, `/run-tests`, `/update-docs`, `/conventional-commit`, etc.). The task board only tracks folders; **quality gates live in those workflows.**
5. If `Agent_reports/Tasks/board-config.yaml` exists, use it as defaults (paths, repos, execution policy, merge target, git strategy). User prompt overrides config.
6. For any run that includes `type: code`, resolve Git end-state from config first:
   - if `git.strategy` is `mr` or `auto_merge_target`, apply it directly
   - if `git.strategy` is `ask` (or missing), ask once at start:
     - **MR mode:** keep commits on branch and finish MR-ready
     - **auto-merge mode:** merge branch to `git.merge_target_branch` and switch back to `git.merge_target_branch`
   Apply the chosen mode consistently unless user overrides per task.
   - if `execution.create_branch_before_changes` is `true`, branch creation is mandatory before first code change:
     - never modify code on `git.merge_target_branch` (or `main`/`develop`)
     - if currently on target branch, run `/create-branch` first
     - if branch creation cannot be completed safely, mark task blocked and do not proceed with code edits
7. Always update task file content before moving states:
   - append execution/validation summary with completed conditions and references (commits, MR, artifacts, tests)
   - set status by destination (`pending_validation` for To-Validate, `done` only for Done)
   - never mark `done` when item is moved to validation
8. If completion requires extra follow-up work, create a new task in `To-Do` and reference it from the current task (`follow_up_tasks` or explicit IDs) before changing state.

## State transition rules (strict)

Treat task board processing as repeatable cycles. Running the command many times must be safe.

- From **`To-Do`**:
  - completed first pass -> move to **`To-Validate`** with `status: pending_validation`
  - never move directly to `done` unless policy explicitly says direct Done path
- From **`To-Validate`**:
  - if validation fails -> move back to **`To-Do`** with clear review notes (issues, risks, discoveries, required fixes)
  - if validation passes -> move to **`Done`** with `status: done`
- **Done is earned, not assumed**:
  - if acceptance criteria are still not met, task must not move to Done
  - repeated runs must keep unfinished items in `To-Do`/`To-Validate` until criteria are truly satisfied

## Minimal prompt style (recommended)

Use short commands; keep project defaults in config:

- `/task-board-runner @Agent_reports/Tasks/To-Do`
- optional override: `... move completed to @Agent_reports/Tasks/Done`

If config contains repos and execution policy (`single_task_at_a_time`, merge target, git strategy), no need to repeat them in each prompt.

## Quick reference — task `type` (frontmatter)

| `type` | `code_workflow` | Primary workflow | Must also follow (when primary says so) |
|--------|----------------|-----------------|----------------------------------------|
| `code` | `implement-feature` (default for new work) | `/implement-feature` | `/analyze-codebase`, `/create-branch`, `/update-docs`, `/run-tests`, `/conventional-commit`, … |
| `code` | `fix-bug` | `/fix-bug` | same pattern; regression test required per `fix-bug` |
| `code` | `refactor` | `/refactor` | `/run-tests` before and after; `/create-branch`, `/update-docs`, `/conventional-commit` |
| `analysis` | — | (write-up) | optional `/analyze-codebase` if repo deep-dive needed |
| `validation` | — | `/validate-external-proposal` | — |
| `breakdown` / `epic` | — | `/business-brief-to-tasks` | — |

Optional task fields: `code_workflow: implement-feature | fix-bug | refactor` in YAML frontmatter (see `/process-task-board`).

## Workflow/command index

Canonical IDs: `implement-feature`, `fix-bug`, `refactor`, `analyze-codebase`, `create-branch`, `run-tests`, `update-docs`, `conventional-commit`, `update-dependencies`, `release`, plus board flows above.