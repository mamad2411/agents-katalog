---
name: agkan-icebox-subtask
description: Use when reviewing a single icebox task to decide whether to promote it to backlog or close it.
user-invokable: false
---

# agkan-icebox-subtask

## Overview

A sub-workflow that reviews a single icebox task in agkan and decides whether to promote it to `backlog` or close it as no longer needed.

---

## Workflow

### 1. Retrieve Task Details

```bash
agkan task get <id> --json
```

### 2. Evaluate the Task

Evaluate the task against the following criteria:

**Promote to backlog (`backlog`) when:**
- The requirement or background is now clear enough to plan
- External blockers have been resolved
- The task has become relevant due to changed circumstances

**Close (`closed`) when:**
- The need no longer exists
- A duplicate task already exists in backlog or later stages
- It was superseded by another approach or decision

**Keep in icebox when:**
- Still waiting on external factors
- Not enough information to decide yet (leave as-is)

### 3. Add Notes if Needed

If the reason for the decision is non-obvious, add context to the task body before updating status:

```bash
# First, retrieve the existing body
agkan task get <id> --json
# Write body to tmp file and update using --file to preserve newlines
cat > /tmp/agkan_body_$$.md << 'BODY'
<existing body>

<reason for decision>
BODY
agkan task update <id> --file /tmp/agkan_body_$$.md
```

### 4. Update Status

```bash
# Promote to backlog
agkan task update <id> --status backlog

# Close as no longer needed
agkan task update <id> --status closed

# Keep in icebox — no update needed
```

---

## Notes

- Icebox is not a permanent graveyard — each task deserves a clear decision
- When promoting to backlog, the task will be picked up by `agkan-planning` next
- Do not move icebox tasks directly to `ready`; always go through `backlog` → planning first
- This skill is used after task selection (task selection is done by the `agkan-icebox` skill)
