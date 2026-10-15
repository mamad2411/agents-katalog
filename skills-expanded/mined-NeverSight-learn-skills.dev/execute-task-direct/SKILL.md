---
name: execute-task-direct
description: "[DEPRECATED] Use agkan-run-direct instead. Use when starting a development session to pick the highest priority Todo task from agkan, implement it directly without PR/branch, and mark it done."
---

> **DEPRECATED**: This skill has been renamed. Please use `agkan-run-direct` instead.
> `Skill("agkan-run-direct")`

# execute-task-direct

## Overview

A workflow to select the highest priority ready task from agkan, implement it directly without creating a branch or PR, and mark it as done.

---

## Workflow

### 1. Update Branch

```bash
git pull -p
```

### 2. Get Ready Tasks

```bash
agkan task list --status ready --json
```

### 3. Select One High-Priority Task

Evaluate tasks using the following criteria in descending order and select the top one:

**Skip tasks with `will-do-later` tag:**
Tasks with the `will-do-later` tag are intentionally deferred tasks, so skip them. Only select from tasks that do not have the `will-do-later` tag.

**Priority (read from `metadata` field in the list JSON response):**
```
High > Medium > Low
```

**Tags (used when priority is the same):**
```
bug > security > improvement > test > performance > refactor > docs
```

**When there are subtasks or blocker tasks**
Prioritize the target subtasks or blocker tasks (using the same importance and tag criteria)

### 4. Check for Blockers

```bash
agkan task block list <id> --json
```

If there are incomplete tasks in `blockedBy`, do not select that task. Instead, select a different task or handle the blocker tasks first.

### 5. Update Task Status to in_progress

```bash
agkan task update <id> status in_progress
```

### 6. Implementation and Completion

Use the **Task tool (general-purpose sub-agent)** to implement.
Do not use `Skill("execute-subtask-direct")`; instead, instruct the sub-agent to read the SKILL.md file directly.

> **Why SKILL.md path instead of `Skill()`?**
> Sub-agents spawned via the Task tool start with a fresh context. `Skill()` loads skill content into the current conversation, but a sub-agent needs its instructions embedded in its prompt. Providing the SKILL.md path directly in the prompt is the reliable way to pass workflow instructions to a sub-agent.

```
Task(
  subagent_type="general-purpose",
  description="Implement task #<id>",
  prompt="""
Please implement the following task.

Invoke the key-guidelines skill using the Skill tool: Skill("key-guidelines")

## Task Information
- ID: <id>
- Title: <title>
- Body: <body>

## Procedure
Load .claude/skills/execute-subtask-direct/SKILL.md and follow its procedures to implement.
"""
)
```

### 7. Re-fetch Task List and Continue or End Session

After the sub-agent completes, re-fetch the task list to pick up any newly added ready tasks:

```bash
agkan task list --status ready --json
```

If there is no instruction to end from the user and ready tasks exist (including newly added ones), select the next task and repeat from step 3 of the same workflow.

If no ready tasks remain, end the session.

---

## Priority Determination Flow

```
Ready task list
    ↓
Sort by priority (High → Medium → Low)
    ↓
Multiple tasks with same priority?
   Yes → Sort by tag priority (bug → security → ... → docs)
   No  → Select the top task
    ↓
Select one task and start
```

---

## Tag Priority List

See the canonical definition in `agkan/SKILL.md` (Tag Priority section).

---

## Important Notes

- Always select only one task (do not work on multiple tasks simultaneously)
- If no tasks exist, end the session
- Do not create branches or PRs (commit directly to the current branch)
- Update the task status to done after implementation is complete
