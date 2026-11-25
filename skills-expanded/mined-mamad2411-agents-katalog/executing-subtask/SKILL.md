---
name: executing-subtask
description: >
  Execute a single subtask from a Jira task plan. The user must specify which
  task number to execute. Use when the user says "execute task 3", "work on task
  2", "implement task 1", "start task 5 for PROJECT-1234", or "run subtask N".
  Requires that the task plan exists at docs/<TICKET_KEY>-tasks.md. Executes
  ONLY the specified task — never continues to the next one without explicit
  user approval.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Bash
  - agent
  - mcp__jira__*
---

# Executing Subtask

## Purpose

Execute exactly ONE task from the task plan. Delegate the actual implementation
to the `task-executor` subagent (see `./task-executor.md` in this skill folder)
to keep the main agent's context clean for coordination and review. After
execution, validate the work and update tracking artifacts.

## Inputs

| Input         | Source              | Required | Example    |
| ------------- | ------------------- | -------- | ---------- |
| `TICKET_KEY`  | User / `$ARGUMENTS` | Yes      | `JNS-6065` |
| `TASK_NUMBER` | User / `$ARGUMENTS` | Yes      | `3`        |

Both the ticket snapshot (`docs/<TICKET_KEY>.md`) and the task plan
(`docs/<TICKET_KEY>-tasks.md`) must exist. If either is missing, tell the user
which prerequisite skill to run.

## Subagents

This skill uses one subagent, colocated in this folder:

| Subagent      | File                 | Purpose                            |
| ------------- | -------------------- | ---------------------------------- |
| task-executor | `./task-executor.md` | Performs the actual implementation |

Before delegating, read the subagent file to understand its contract (expected
input format, output format, and rules). The path is relative to this skill's
directory.

## Output

- Implemented code / configuration changes for the specified task.
- Updated task plan with execution status.
- Jira subtask transitioned (if Jira MCP available).

## Execution Steps

### 1. Load and validate the task

Read `docs/<TICKET_KEY>-tasks.md` and extract `## Task <TASK_NUMBER>`.

**Pre-flight checks — stop if any fail:**

- [ ] The task exists in the plan.
- [ ] Dependencies listed in `Dependencies / prerequisites` are marked complete.
- [ ] `Questions to answer before starting` are all resolved (no unresolved items
      without a recorded fallback).

If pre-flight fails, tell the user what needs to be resolved first and stop.

### 2. Prepare the execution brief

Build a self-contained execution brief that includes ONLY what the subagent
needs:

```markdown
# Execution Brief — <TICKET_KEY> Task <N>: <Title>

## Objective

<from task plan>

## Relevant Requirements and Context

<from task plan, plus any resolved decisions from the Decisions Log>

## Implementation Notes

<from task plan>

## Definition of Done

<from task plan>

## Likely Files / Artifacts Affected

<from task plan>

## Resolved Questions & Decisions

<any answers from the Decisions Log that affect this task>

## Constraints

- Only implement what is described above.
- Do not modify files unrelated to this task.
- If you encounter ambiguity not covered here, STOP and report it — do not guess.
- Run existing tests to verify you haven't broken anything.
- If the definition of done includes new tests, write them.
```

Write this brief to `docs/<TICKET_KEY>-task-<N>-brief.md`.

### 3. Delegate to the task-executor subagent

```
agent task-executor "Execute the task described in docs/<TICKET_KEY>-task-<N>-brief.md"
```

The subagent performs the implementation in an isolated context.

### 4. Review the subagent's work

After the subagent completes, review:

- [ ] **Definition of done:** Check each condition against actual changes.
- [ ] **Scope containment:** Verify no files outside `Likely files affected`
      were modified unexpectedly (unless justified).
- [ ] **Tests pass:** Run the project's test suite (or relevant subset).
- [ ] **No regressions:** If existing tests exist, confirm they still pass.

If review finds issues, provide specific feedback and re-invoke the subagent
with corrections. Limit to **3 retry cycles** — after that, report remaining
issues to the user.

### 5. Update tracking

#### a. Update the task plan

In `docs/<TICKET_KEY>-tasks.md`, update the task section:

```markdown
**Status:** ✅ Complete (<YYYY-MM-DD>)
**Implementation summary:** <2–3 sentence summary of what was done>
**Files changed:**

- `path/to/file1.ts` — <what changed>
- `path/to/file2.ts` — <what changed>
```

#### b. Update Jira (if MCP available)

- Transition the subtask to "In Progress" at the start of execution.
- Transition the subtask to "Done" after successful review.
- Add a comment to the subtask summarizing what was implemented.

#### c. Clean up

Delete the temporary execution brief file:
`docs/<TICKET_KEY>-task-<N>-brief.md`

### 6. Report to user

```
Task <N> complete: <Title>

Summary: <what was done in 2–3 sentences>

Files changed:
- <list>

Tests: <passing / N new tests added>

Jira subtask <KEY>: transitioned to Done.

⚠️ Remaining items (if any):
- <anything that couldn't be fully resolved>

Ready for the next task? Let me know which one to tackle.
```

## Safety Rules

- **One task at a time.** Never auto-continue to the next task.
- **Scope discipline.** Do not implement anything outside the task's scope, even
  if it seems like a quick win.
- **Fail loudly.** If the subagent encounters ambiguity or a blocker, surface it
  to the user immediately rather than making assumptions.
- **Preserve the plan.** The task plan is the source of truth. If execution
  reveals the plan needs changes, propose the change to the user — don't
  silently modify the plan.
