---
name: execute-review
description: "[DEPRECATED] Use agkan-review instead. Use when checking review tasks against GitHub PR status to automatically move them to done or closed."
---

> **DEPRECATED**: This skill has been renamed. Please use `agkan-review` instead.
> `Skill("agkan-review")`

# execute-review

## Overview

Workflow to retrieve tasks with Review status in agkan, check the merge/close status of GitHub PRs, and automatically update their status.

---

## Workflow

### 1. Retrieve Review tasks

```bash
agkan task list --status review --json
```

### 2. Confirm PR URL for each task

Extract the PR URL from the task body in the format `PR: <URL>`.

If no URL is found, skip the task and output a message indicating manual verification is needed.

### 3. Check PR status on GitHub

```bash
gh pr view <PR URL> --json state,mergedAt
```

| Field | Meaning |
|-----------|------|
| `state` | `OPEN` / `CLOSED` / `MERGED` |
| `mergedAt` | Merge date/time (null if not merged) |

### 4. Move status based on PR status

| PR State | agkan Status | Command |
|--------|----------------|---------|
| `MERGED` | `done` | `agkan task update <id> --status done` |
| `CLOSED` (mergedAt is null) | `closed` | `agkan task update <id> --status closed` |
| `OPEN` | No change | Skip (still under review) |

---

## Decision Flow

```
Retrieve all Review tasks
    ↓
Repeat for each task
    ↓
Does the body contain "PR: <URL>"?
   No  → Skip (output message prompting manual verification)
   Yes → Check PR status
    ↓
What is the PR state?
   MERGED  → Move to done
   CLOSED  → Move to closed
   OPEN    → Skip (waiting for review)
    ↓
Move to next task (repeat until all tasks are processed)
```

---

## Notes

- PR URL is expected in the format `PR: <URL>` within the task body
- If PR URL is not found, prompt for manual verification (skip task)
- `done` means successful completion, `closed` means suspended or withdrawn
- The `gh` command is required and will not work in environments where it is unavailable
