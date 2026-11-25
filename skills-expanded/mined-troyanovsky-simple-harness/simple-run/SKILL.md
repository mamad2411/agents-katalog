---
name: simple-run
description: >
  Orchestrate full feature implementation: loop through a feature's issues.json, invoking
  simple-implement for each task until all are done or a blocker is hit. Use when the user wants
  to auto-complete a feature, run through all tasks, or execute the task queue without manual
  intervention. Triggers: "run all tasks", "auto-implement", "complete the feature", "implement
  everything", "execute the task list".
disable-model-invocation: true
---

# Simple Run — Orchestrate Feature Implementation

You are an orchestrator. Your job is to drive a feature from `tasks_ready` to `done` by
repeatedly invoking **simple-implement** in a sequential loop — one task at a time — until
the work queue is empty or a stopping condition is met.

You do NOT implement code yourself. You delegate each task to a sub-agent that follows the
**simple-implement** skill, then inspect the result and decide whether to continue.

## Folder convention

Same as all simple-\* skills:

```
docs/
  index.json              ← feature manifest
  visual.md               ← app-level visual design (optional)
  <feature-name>/
    spec.md
    spec/                 ← optional detail files (if spec.md was split)
    design.md
    design/               ← optional detail files (if design.md was split)
    issues.json           ← work queue
    progress-log.md       ← updated by each sub-agent
```

## Workflow

### 1. Initialize

- Require a clean git worktree before changing state. If uncommitted changes exist, stop and ask
  the user how to handle them.
- Identify the feature to work on. If the user specifies a feature name, use it. Otherwise,
  check `docs/index.json` for features with status `"tasks_ready"` or `"in_progress"`.
  If multiple features qualify, ask the user which one to run.
- Read `docs/<feature-name>/issues.json` to understand the full scope.
- Count total tasks, completed tasks, and remaining tasks. Report this to the user as a
  starting summary (e.g., "Feature `auth` has 12 tasks: 4 done, 8 remaining.").
- Update `docs/index.json` to set the feature status to `"in_progress"` if not already.
- **Capture a test baseline.** Run the full test suite and record pass/fail results.
  This lets review sub-agents distinguish pre-existing failures from new regressions.
  Refresh the baseline after each successful commit.

### 2. Loop

For each iteration:

**a) Check for the next available task:**

- Read `issues.json` (fresh each iteration — the sub-agent may have added tasks or changed
  priorities and dependencies).
- Apply the same task-selection algorithm as simple-implement:
  1. Filter to `status: "todo"`.
  2. Exclude tasks with unmet dependencies (any `depends_on` task that is not `"done"`).
  3. Pick the lowest `priority` number. Break ties by lowest ID.
- If unfinished tasks remain but none is available, stop and report the blocked, missing, or
  cyclic dependency state.

**b) If a task is available, spawn a sub-agent:**

- Launch a sub-agent — a fresh, stateless session with no memory of prior iterations — with
  access to the full project codebase and the docs folder.
- Instruct the sub-agent to follow the **simple-implement** skill for the specific feature
  and task ID.
- The sub-agent prompt should include:
  - The feature name and task ID.
  - The path to the docs folder.
  - An instruction to follow simple-implement's workflow (orient → pick → understand →
    implement → verify → update state → summarize).
  - The flag `[INVOCATION_MODE: automated]` — this is the contract signal that tells
    simple-implement it is running in automated mode and should not pause for user
    confirmation under any circumstances.

**c) After the sub-agent completes:**

- Read the updated `issues.json` to confirm the task status changed.
- Read the latest entry in `progress-log.md` to understand what happened.
- If the task is `"blocked"`, log the blocker and decide:
  - If other non-blocked tasks remain, skip to the next one.
  - If all remaining tasks are blocked, stop and report to the user.
- If the task is `"done"`, proceed to the review step (d).
- If the task is neither `"done"` nor `"blocked"`, stop and report the invalid sub-agent result.

**d) Review and commit:**

Spawn a **review sub-agent** with the test baseline (from step 1) and the git diff.
The reviewer evaluates:

- **Correctness** — bugs, edge cases, side effects, collateral impact on related code.
- **Tests** — coverage added/updated, suite passes locally. Compare failures against
  baseline to separate regressions from pre-existing issues. Re-run any non-baseline
  failure once before counting it (handles flaky tests).
- **Architecture hygiene** — adherence to project conventions (`AGENTS.md`, `CLAUDE.md`).
  No violations of KISS/YAGNI/SOLID/DRY (unnecessary abstractions, duplicated logic,
  god-objects, etc.). File/folder organization consistent with existing structure.
- **Scope** — flag unexpected file changes outside the task's expected footprint.

Reviewers report reproducible correctness, security, test, scope, or architecture findings —
not preferences, speculative improvements, or unrelated cleanup. Triage findings as:

- **Defects:** Fix findings that affect the current task or feature in the current review cycle.
  This includes pre-existing findings that must be corrected for the current task or feature to
  work correctly. Send all defects to one fix sub-agent, then re-review. Allow 2 fix-agent attempts
  after the initial review; if a defect remains, abandon the task.
- **Execution decisions:** The orchestrator resolves scoped, reversible choices using the spec,
  existing conventions, and the simplest safe option. Include the decision in the fix instructions
  when code changes are needed.
- **Principal decisions:** Surface choices that are cross-cutting, long-lasting, expensive to
  reverse, or materially affect permissions, data, public behavior, business rules, or multiple
  user journeys. Block the task only when it cannot safely proceed; otherwise choose a conservative,
  reversible default and retain the decision for the final report.
- **Pre-existing or unrelated findings:** Stop and escalate critical issues such as security or
  data-loss risks. Retain other material findings for the final report; ignore minor observations.

Review findings do not create tasks in `issues.json`. If review requires abandoning a task, restore
only that task's changes to the last committed state before marking it `"blocked"` and logging the
outcome. Once no defects or blocking decisions remain, stage only the reviewed task and state files,
inspect the staged diff, then commit referencing the task ID (e.g.,
`feat(auth): TASK-auth-003 — add session refresh logic`). Refresh the test baseline and continue.

**e) Report progress:**

- After each completed task, briefly log progress (e.g., "✓ TASK-auth-003 done. 6/12 complete.").

### 3. Stopping conditions

Stop the loop when any of these conditions is met:

1. **All tasks are `"done"`.** The feature is complete.
2. **All remaining tasks are `"blocked"`.** Human intervention is needed.
3. **A sub-agent fails catastrophically** (crashes, produces no output, or leaves the
   codebase in a broken state). Stop and report.
4. **A critical out-of-scope issue is discovered.** Stop and escalate it to the user.
5. **The queue is invalid.** No task is selectable because dependencies are missing or cyclic,
   or a sub-agent returns an invalid task status.
6. **The user intervenes.** If running interactively, the user can stop the loop at any time.

### 4. Finalize

When the loop ends:

- Read the final state of `issues.json` and `progress-log.md`.
- Update `docs/index.json`:
  - If all tasks are done, set feature status to `"done"`.
  - Otherwise, leave feature status as `"in_progress"`.
- Provide a final summary to the user:
  - Total tasks completed in this run.
  - Any tasks that were blocked and why.
  - Any new tasks that were discovered during implementation.
  - Deduplicated principal decisions needing attention, including the default taken and impact
    of changing it.
  - Material pre-existing or unrelated findings that warrant engineering follow-up.
  - Overall feature status.
- If the feature is now complete and a **simple-simplify** skill is available, remind the user they
  can run it to audit the completed implementation for unnecessary complexity. This is a manual,
  report-only follow-up — never invoke it automatically.
- If the feature is now complete and a **simple-distill** skill is available, remind the user they
  can run it to promote the feature's durable decisions and behavior into app-level docs and archive
  the feature folder. This is a reminder only — never invoke it automatically.

## Important notes

- **Strictly sequential.** Run one sub-agent at a time — each needs to see the file and state
  changes from the previous one. Parallelism would require a locking/merge strategy for
  `issues.json` and `progress-log.md`; it's a future extension.

- **You are the orchestrator, not the implementer.** Don't write production code. You may inspect
  repository state, run orchestration-level verification, manage reviewed commits, and update
  `docs/index.json`; all implementation happens inside sub-agents.

- **File size guard.** After each completed task, check whether `issues.json` has ≥ 15 done
  tasks or `progress-log.md` exceeds 300 lines. If either threshold is hit, notify the user
  and suggest running `/simple-cleanup` before continuing. Don't hard-stop the loop — the
  user decides whether to clean up now or later.
