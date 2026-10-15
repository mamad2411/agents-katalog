---
name: agkan-planning-subtask
description: Use when reviewing a single backlog task to assess decomposition, implementation readiness, and priority ordering.
user-invokable: false
---

# agkan-planning-subtask

## Overview

A sub-workflow that reviews a single Backlog task in agkan, makes decisions on decomposition, Ready status movement, and deferral.

---

## Workflow

### 1. Content Review, Supplementation, and Task List Creation

- If task content is unclear, investigate and confirm details by examining the code
- Append the investigated content to the task description:

```bash
# First, retrieve the existing body
agkan task get <id> --json
# Then update by concatenating existing body with new content
agkan task update <id> --file /dev/stdin << 'EOF'
<existing body>

<additional content>
EOF
```

- If the task contains multiple pieces of work, organize the content and append it to the description in task list format:

When creating a task list, it is advisable to use the Explore subagent (Agent tool with subagent_type="Explore") to examine the code, understand the task content, and then use Plan mode to create the task list if investigation is needed.

```- Task content summary
- [ ] Work item 1
- [ ] Work item 2
- [ ] Work item 3
```

**MANDATORY: After completing content review and creating the task list, you MUST write the planning results back to the task body. This step is REQUIRED and must NOT be skipped under any circumstances.**

```bash
# REQUIRED: Write planning results to task body
# Always execute this step regardless of whether content was changed
agkan task get <id> --json
# Then update with the full body including planning results
agkan task update <id> --file /dev/stdin << 'EOF'
<full updated body with planning results, scope, implementation approach, and task list>
EOF
```

### 2. Task Decomposition Decision

**Decomposition Granularity Standard: 1 Task = 1 PR = 1 Feature (Modification)**

- Decompose so that when a PR is merged, that feature or modification is complete
- Do not divide tasks such that a PR merge results in an incomplete state
- Only split when multiple independent features or modifications are mixed in a single task

If a task contains scope exceeding the above standard, split it into sub-tasks:

```bash
# Create new tasks after splitting
# Use --parent to maintain the parent-child relationship with the original task
# This makes the task hierarchy visible in `agkan task list --tree`
agkan task add "<sub-task name>" "<details>" --parent <original-id>

# Close the original task as split (or update it)
agkan task update <id> --status closed
```

### 3. Ready Status Movement Decision

Move to Ready if **all** of the following conditions are met:

- No blockers (dependent tasks are completed)
- Scope that can be implemented as a single PR
- Implementation approach is clear

Before moving to Ready, verify there are no blocking tasks:

```bash
agkan task block list <id> --json
```

If blockers exist, do not move to Ready. Keep in Backlog and apply the `will-do-later` tag (see Step 4).

When moving a task to Ready, also set the priority at this point:

```bash
agkan task update <id> --status ready --priority <value>
```

Priority values: `critical` / `high` / `medium` / `low`

Priority determination criteria:

| Value | Criteria |
|-------|----------|
| `critical` | Production failures, security issues, blockers for other tasks |
| `high` | Important features with near deadlines, bugs with significant user impact |
| `medium` | Normal feature additions, improvements (default) |
| `low` | Nice-to-have, work on if time permits |

### 4. Deferral Decision

For tasks that are "something to do later but not now," attach the `will-do-later` tag and keep it in Backlog:

```bash
# Create the tag if it does not exist
agkan tag add "will-do-later"
# Attach the tag to the task
agkan tag attach <task-id> <tag-id-or-name>
```

Deferral criteria:
- Low impact on current priorities
- Dependent tasks are not yet completed
- Resources or information are insufficient

---

## Tag Priority

See the canonical definition in `agkan/SKILL.md` (Tag Priority section).

Tag attachment command:

```bash
# Create the tag if it does not exist
agkan tag add "<tag>"
# Attach the tag to the task
agkan tag attach <task-id> <tag-id-or-name>
```

---

## Notes

- When decomposing tasks, inherit the content of the original task
- Move to Ready only for tasks that can be "started immediately"
- This skill is used after task selection (task selection is done by the `agkan-planning` skill)

---

## STRICT PROHIBITION

**Do NOT implement tasks.** This skill's sole responsibility is to review tasks and update their status in agkan. The following actions are strictly forbidden:

- Editing source code files
- Creating or modifying any files in the codebase (other than agkan task updates via CLI)
- Implementing features, fixes, or any code changes described in the task

If a task is ready for implementation, move it to Ready status and stop. Implementation is handled by a separate workflow (`agkan-run`).
