---
name: execute-icebox
description: "[DEPRECATED] Use agkan-icebox instead. Use when reviewing icebox tasks to decide whether to promote them to backlog or close them as no longer needed."
---

> **DEPRECATED**: This skill has been renamed. Please use `agkan-icebox` instead.
> `Skill("agkan-icebox")`

# execute-icebox

## Overview

A workflow to review `icebox` tasks and decide whether to promote each one to `backlog` or close it.

**Icebox definition:** Tasks that are ideas or candidates not yet ready for planning. They have unclear requirements, are on hold pending external factors, or are low-priority items that may be addressed in the future.

---

## When to Run

- When icebox tasks have accumulated and need periodic review
- When external conditions change and previously deferred tasks may now be relevant
- When starting a new planning cycle and wanting to surface hidden candidates

---

## Workflow

### 1. Retrieve Icebox Tasks

```bash
agkan task list --status icebox --json
```

### 2. Review Tasks One by One with Sub-agents

For each task, use the **Task tool (general-purpose sub-agent)** to review.
Do not use `Skill("execute-icebox-subtask")`. Instead, invoke it by having the sub-agent read the SKILL.md file:

```
Task(
  subagent_type="general-purpose",
  description="Review icebox task #<id>",
  prompt="""
Please review the following icebox task.

## Task Information
- ID: <id>
- Title: <title>
- Body: <body>

## Procedure
Read .claude/skills/execute-icebox-subtask/SKILL.md and follow its procedures to review.
"""
)
```

If a task ID is specified by the user, retrieve and review only that target task:

```bash
agkan task get <id> --json
```

Then delegate only that single task to a sub-agent using the same Task call format above.

### 3. End Session or Continue

Repeat until all tasks are processed. If there is no end instruction from the user, select the next task and repeat from step 2.

---

## Decision Flow

```
Retrieve icebox tasks
    ↓
Delegate one task to sub-agent
    ↓
Sub-agent reviews and makes decision
  - Requirements now clear? → Promote to backlog
  - No longer needed / superseded → Close
  - Still unclear / waiting → Keep in icebox
    ↓
Move to next task (repeat until all are done)
```

---

## Important Notes

- Icebox is not a permanent graveyard — review it periodically
- When promoting to backlog, the task will be picked up by `execute-planning` next
- Do not move icebox tasks directly to `ready`; always go through `backlog` → planning first
