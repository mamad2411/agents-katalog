---
name: dispatch
description: Coordinate multi-step work across parallel agent workers using a shared task ledger and explicit dependencies. Use when a request needs decomposition, worker assignment, monitoring, or recovery.
icon: 🚀
alwaysAllow:
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - Task
  - Bash
  - Read
  - Glob
  - Grep
---

# Dispatch

Coordinate complex work by breaking it into tracked tasks, assigning owners, validating dependencies, and running workers in parallel through the host runtime's adapter.

<objective>
Turn a large request into a verifiable multi-worker execution plan that can run in Claude Code, Vesper, or a manual shared-board workflow.
</objective>

<essential_principles>

1. **Teach the protocol, not the brand.** The core skill is task decomposition, dependency management, dispatch, verification, and recovery. Runtime-specific setup belongs in adapter docs.

2. **One task ledger, one source of truth.** Every worker must read from and write to the same task ledger, whether that ledger is native task tools or a shared markdown/JSON file.

3. **Claim before doing.** A worker should claim ownership before editing files so parallel agents do not collide silently.

4. **Dependencies are explicit.** If a task needs another task's output, record that relationship instead of relying on memory or timing.

5. **Verification is part of the task.** Every task needs expected evidence: changed files, tests, docs, screenshots, or a concrete status update.

6. **Recovery preserves work first.** On failure or conflict, snapshot and compare before discarding or reassigning anything.

</essential_principles>

## When to Use

- The request spans 5+ meaningful implementation steps.
- Multiple files or subsystems can be worked on in parallel.
- You need progress tracking, ownership, or blocker visibility.
- The work may outlive one session or need handoff across agents.

## Do Not Use

- The task is a 1-3 step change you can finish directly.
- Only one file or one tightly coupled edit is involved.
- Parallel workers would spend more time coordinating than implementing.

## Success Criteria

- The work is decomposed into 3-10 concrete tasks.
- Each task has an owner or is explicitly ready to claim.
- Dependencies and file ownership are visible.
- Ready tasks can be dispatched in parallel without hidden conflicts.
- Each completed task includes evidence.
- The final report includes status, blockers, risks, and next actions.

## Required Reading

- [runtime-primitives.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/runtime-primitives.md)
- [universal-dispatch.md](/Users/tinnguyen/vesper-team-skills/dispatch/workflows/universal-dispatch.md)
- [dependency-patterns.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/dependency-patterns.md)
- [failure-recovery.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/failure-recovery.md)

Read this adapter doc only when it matches your runtime:

- [claude-code-adapter.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/claude-code-adapter.md)

## Runtime Adapters

| Runtime shape | Use when | Read next |
|---------------|----------|-----------|
| Native task tools + worker spawning | Your host exposes built-in task CRUD and subagents | [runtime-primitives.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/runtime-primitives.md), [claude-code-adapter.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/claude-code-adapter.md) |
| Shared workspace app with agent sessions | Your host can persist task state and spawn agents, but with different APIs | [runtime-primitives.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/runtime-primitives.md), [universal-dispatch.md](/Users/tinnguyen/vesper-team-skills/dispatch/workflows/universal-dispatch.md) |
| No native task tools | You must coordinate through a shared markdown or JSON board | [runtime-primitives.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/runtime-primitives.md), [universal-dispatch.md](/Users/tinnguyen/vesper-team-skills/dispatch/workflows/universal-dispatch.md) |

## Universal Task Spec

Every dispatched task should capture:

- `subject`: imperative title
- `outcome`: what done looks like
- `files`: expected files or surface area
- `blockedBy`: prerequisite task IDs
- `owner`: claimed worker, if any
- `evidence`: tests, diffs, docs, screenshots, or status proof

Minimal shared-board template:

```markdown
| ID | Subject | Owner | Status | Blocked By | Files | Evidence |
|----|---------|-------|--------|------------|-------|----------|
| 1 | Design auth flow | planner | done | - | docs/auth.md | design doc linked |
| 2 | Build backend endpoints | worker-a | in_progress | 1 | src/api/auth.ts | tests pending |
| 3 | Build login UI | worker-b | pending | 1 | src/ui/login.tsx | - |
```

## Workflow

### 1. Choose the Adapter

- Identify which runtime primitives you have: task create, task update, task list, claim owner, spawn worker, recover failure.
- If those primitives are missing, use a shared markdown or JSON board instead of pretending native tools exist.
- Verify: you can name the single task ledger every worker will use.

### 2. Intake the Request

- Capture target outcome, constraints, verification method, and risky files.
- Check whether an existing task ledger already has active work. If yes, warn before mixing unrelated tasks.
- Verify: you can state the final deliverable and how it will be checked.

### 3. Decompose into 3-10 Tasks

- Split by deliverable, file ownership, or dependency boundary.
- Keep each task independently testable and scoped to one worker.
- Include `Files:` or equivalent ownership hints in each task.
- Verify: each task is clear enough to hand to a worker without extra interpretation.

### 4. Declare Dependencies and Conflicts

- Mark prerequisite relationships explicitly.
- Serialize tasks that touch the same files or same fragile shared boundary.
- Use [dependency-patterns.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/dependency-patterns.md) when choosing graph shape.
- Verify: there are no circular dependencies and no hidden file overlap.

### 5. Claim and Dispatch Ready Work

- Claim ownership before a worker starts editing.
- Dispatch only tasks whose blockers are satisfied.
- Match worker capability to task risk. For tool-heavy coding, use a model/runtime combination that reliably uses the required tools. In Claude Code, `sonnet` is a safe default; lighter models may be fine for low-risk tasks if they behave well in your environment.
- Verify: every in-progress task has one owner and one clear completion action.

### 6. Monitor and Rebalance

- Re-list the board periodically.
- Start newly ready tasks, split stale tasks, and surface blockers early.
- Keep updates short: completed, in progress, blocked, ready.
- Verify: the coordinator can explain current status in one compact report.

### 7. Recover Safely

- On timeout, inspect partial work before retrying.
- On conflict, preserve both sides before reverting anything.
- On blocker failure, either retry, create a workaround task, or explicitly re-plan downstream tasks.
- Use [failure-recovery.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/failure-recovery.md).
- Verify: no work is discarded without being reviewed or intentionally superseded.

### 8. Close with a Dispatch Report

- Summarize completed tasks, active blockers, risks, and next actions.
- Record evidence for each completed task.
- Leave the board in a state the next coordinator can resume cleanly.

Recommended final report shape:

```markdown
## Dispatch Report

- Completed: 1, 2, 4
- In progress: 3
- Blocked: 5 (waiting on 3)
- Risks: API schema may change after review
- Evidence: auth tests green, docs updated, migration file added
- Next actions: finish task 3, then unblock task 5
```

## Anti-Patterns

- Treating one vendor's task API as the definition of dispatch
- Spawning workers without a shared task ledger
- Starting blocked tasks
- Parallelizing edits to the same files without serialization
- Over-decomposing tiny work into dozens of tasks
- Dropping or overwriting conflicting work before comparing it

## References

- Universal workflow: [universal-dispatch.md](/Users/tinnguyen/vesper-team-skills/dispatch/workflows/universal-dispatch.md)
- Runtime contract: [runtime-primitives.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/runtime-primitives.md)
- Claude Code adapter: [claude-code-adapter.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/claude-code-adapter.md)
- Claude task tool syntax: [task-tools-api.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/task-tools-api.md)
- Claude task storage details: [task-architecture.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/task-architecture.md)
- Dependency examples: [dependency-patterns.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/dependency-patterns.md)
- Failure modes: [failure-recovery.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/failure-recovery.md)
- End-to-end example: [example-oauth.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/example-oauth.md)
- Installation and packaging: [README.md](/Users/tinnguyen/vesper-team-skills/dispatch/README.md)

## Next Step

- Use [universal-dispatch.md](/Users/tinnguyen/vesper-team-skills/dispatch/workflows/universal-dispatch.md) to run the protocol.
- If you are in Claude Code, load [claude-code-adapter.md](/Users/tinnguyen/vesper-team-skills/dispatch/references/claude-code-adapter.md) before using wrapper scripts or hook setup.
