---
name: agkan-planning
description: Use when reviewing backlog tasks to assess decomposition, implementation readiness, and priority ordering before development begins.
---

# agkan-planning

## Overview

A planning workflow that uses agkan to review backlog tasks and make decisions about decomposition, moving to Ready status, and deferring tasks.

---

## Workflow

### 1. Retrieve Backlog Tasks

```bash
agkan task list --status backlog --json
```

### 2. Review Tasks One by One with Sub-agents

For each task, use the **Task tool (general-purpose sub-agent)** to review.
Do not use `Skill("agkan-planning-subtask")`. Instead, instruct the sub-agent to read the SKILL.md file directly.

> **Why SKILL.md path instead of `Skill()`?**
> Sub-agents spawned via the Task tool start with a fresh context. `Skill()` loads skill content into the current conversation, but a sub-agent needs its instructions embedded in its prompt. Providing the SKILL.md path directly in the prompt is the reliable way to pass workflow instructions to a sub-agent.

```
Task(
  subagent_type="general-purpose",
  description="Review task #<id>",
  prompt="""
Please review the following backlog task.

## Task Information
- ID: <id>
- Title: <title>
- Body: <body>

## Procedure
Read .claude/skills/agkan-planning-subtask/SKILL.md and follow its procedures to review.

## Important Constraint
Your role is ONLY to review the task and update its status in agkan (e.g., move to ready, decompose, or tag for deferral).
Do NOT implement the task. Do NOT edit any source code or codebase files.
"""
)
```

If a task ID is specified by the user, retrieve and review only that target task:

```bash
agkan task get <id> --json
```

Then delegate only that single task to a sub-agent using the same Task call format above.

### 3. Re-fetch Backlog Tasks and Continue or End Session

After the sub-agent completes, re-fetch the backlog task list to pick up any changes (e.g., tasks added by decomposition):

```bash
agkan task list --status backlog --json
```

If there is no instruction to end from the user and backlog tasks remain, select the next task and repeat from step 2.

If no backlog tasks remain, end the session.

---

## Decision Flow

```
Retrieve backlog tasks
    ↓
Delegate one task to sub-agent
    ↓
Sub-agent reviews and makes decision
  - Content unclear? → Research code → Add to task
  - Can be decomposed? → Split into subtasks → Close original task
  - Ready to implement now? → Move to Ready
  - Otherwise → Add "will-do-later" tag and keep in Backlog
    ↓
Move to next task (repeat until all are done)
```

---

## Tag Priority

See the canonical definition in `agkan/SKILL.md` (Tag Priority section).

---

## Important Notes

- Tasks with the "will-do-later" tag should be reconsidered after all Ready tasks are completed
- When decomposing tasks, inherit the content from the original task
- Only move to Ready tasks that are "ready to start immediately"
- Icebox tasks are **not** handled by this skill — use `agkan-icebox` to review and promote icebox tasks to backlog first
