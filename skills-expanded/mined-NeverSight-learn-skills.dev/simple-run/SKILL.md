---
name: simple-run
description: >
  Orchestrate the full implementation of a feature by looping through its issues.json task list,
  invoking simple-implement for each task sequentially until all tasks are done. Use this skill
  whenever the user wants to auto-complete a feature, run through all tasks, automate implementation,
  or execute the full task queue without manual intervention. Trigger on phrases like "run all tasks",
  "auto-implement", "complete the feature", "run through the issues", "implement everything",
  "execute the task list", or any request that implies looping through tasks automatically.
disable-model-invocation: true
---

# Simple Run — Orchestrate Feature Implementation

You are an orchestrator. Your job is to drive a feature from `tasks_ready` to `done` by
repeatedly invoking **simple-implement** in a sequential loop — one task at a time — until
the work queue is empty or a stopping condition is met.

You do NOT implement code yourself. You delegate each task to a sub-agent that follows the
**simple-implement** skill, then inspect the result and decide whether to continue.

## Folder convention

Same as all simple-* skills:

```
docs/
  index.json              ← feature manifest
  visual.md               ← app-level visual design (optional)
  <feature-name>/
    spec.md
    design.md
    issues.json           ← work queue
    progress-log.md       ← updated by each sub-agent
```

## Workflow

### 1. Initialize

- Identify the feature to work on. If the user specifies a feature name, use it. Otherwise,
  check `docs/index.json` for features with status `"tasks_ready"` or `"in_progress"`.
- Read `docs/<feature-name>/issues.json` to understand the full scope.
- Count total tasks, completed tasks, and remaining tasks. Report this to the user as a
  starting summary (e.g., "Feature `auth` has 12 tasks: 4 done, 8 remaining.").
- Update `docs/index.json` to set the feature status to `"in_progress"` if not already.

### 2. Loop

For each iteration:

**a) Check for the next available task:**
- Read `issues.json` (fresh each iteration — the sub-agent may have added new tasks).
- Apply the same task-selection algorithm as simple-implement:
  1. Filter to `status: "todo"`.
  2. Exclude tasks with unmet dependencies (any `depends_on` task that is not `"done"`).
  3. Pick the lowest `priority` number. Break ties by lowest ID.

**b) If a task is available, spawn a sub-agent:**
- Launch a sub-agent with access to the full project codebase and the docs folder.
- Instruct the sub-agent to follow the **simple-implement** skill for the specific feature
  and task ID.
- The sub-agent prompt should include:
  - The feature name and task ID.
  - The path to the docs folder.
  - An instruction to follow simple-implement's workflow (orient → pick → understand →
    implement → verify → update state → summarize).
  - An instruction NOT to ask for user confirmation — operate autonomously.

**c) After the sub-agent completes:**
- Read the updated `issues.json` to confirm the task status changed.
- Read the latest entry in `progress-log.md` to understand what happened.
- If the task is `"done"`, continue to the next iteration.
- If the task is `"blocked"`, log the blocker and decide:
  - If other non-blocked tasks remain, skip to the next one.
  - If all remaining tasks are blocked, stop and report to the user.

**d) Report progress:**
- After each completed task, briefly log progress (e.g., "✓ TASK-auth-003 done. 6/12 complete.").

### 3. Stopping conditions

Stop the loop when any of these conditions is met:

1. **All tasks are `"done"`.** The feature is complete.
2. **All remaining tasks are `"blocked"`.** Human intervention is needed.
3. **A sub-agent fails catastrophically** (crashes, produces no output, or leaves the
   codebase in a broken state). Stop and report.
4. **The user intervenes.** If running interactively, the user can stop the loop at any time.

### 4. Finalize

When the loop ends:

- Read the final state of `issues.json` and `progress-log.md`.
- Update `docs/index.json`:
  - If all tasks are done, set feature status to `"done"`.
  - If stopped due to blockers, leave status as `"in_progress"`.
- Provide a final summary to the user:
  - Total tasks completed in this run.
  - Any tasks that were blocked and why.
  - Any new tasks that were discovered during implementation.
  - Overall feature status.

## Important notes

- **Strictly sequential.** Run one sub-agent at a time. The next sub-agent needs to see the
  file changes and state updates from the previous one. Parallelism is a future extension
  that would require a locking/merge strategy for `issues.json` and `progress-log.md`.

- **You are the orchestrator, not the implementer.** Do not write code, run tests, or modify
  files yourself (except `docs/index.json`). All implementation work happens inside sub-agents.

- **Fresh reads each iteration.** Always re-read `issues.json` at the start of each loop
  iteration. The sub-agent may have added new tasks, changed priorities, or updated
  dependencies.

- **Respect the stopping conditions.** Don't retry blocked tasks — they're blocked for a
  reason. Don't force through failures. The progress log and issue statuses are the
  communication channel — keep them accurate.

- **Sub-agent isolation.** Each sub-agent should be treated as a fresh, stateless session.
  Pass it all the context it needs (feature name, task ID, docs path) — don't assume it
  has memory of previous iterations.

- **Keep the user informed.** Even in automated mode, progress visibility matters. Report
  after each task so the user can monitor and intervene if needed.
