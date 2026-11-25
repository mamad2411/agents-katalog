---
name: agkan-review
description: Use when checking review tasks against GitHub PR status to automatically move them to done or closed.
---

# agkan-review

## Overview

Workflow to retrieve tasks with Review status in agkan, check the merge/close status of GitHub PRs, and automatically update their status.

---

## Workflow

### 1. Retrieve Review tasks

```bash
agkan task list --status review --json
```

### 2. Initialize summary counters

Before processing tasks, initialize the following counters to track results:

- `done_count = 0`
- `closed_count = 0`
- `skipped_open_count = 0`
- `no_pr_count = 0`

### 3. Confirm PR URL for each task

First, extract the PR URL from the task body in the format `PR: <URL>`.

If no URL is found in the body, check the task metadata as a fallback:

```bash
agkan task meta list <id>
```

Use the value of the `pr` key if present.

If no URL is found in either the body or metadata, increment `no_pr_count`, skip the task and output a message indicating manual verification is needed.

### 4. Check PR status on GitHub

```bash
gh pr view <PR URL> --json state,mergedAt
```

| Field | Meaning |
|-----------|------|
| `state` | `OPEN` / `CLOSED` / `MERGED` |
| `mergedAt` | Merge date/time (null if not merged) |

### 5. Move status based on PR status

| PR State | agkan Status | Command | Counter |
|--------|----------------|---------|---------|
| `MERGED` | `done` | `agkan task update <id> status done` | Increment `done_count` |
| `CLOSED` (mergedAt is null) | `closed` | `agkan task update <id> status closed` | Increment `closed_count` |
| `OPEN` | No change | Skip (still under review) | Increment `skipped_open_count` |

### 6. Display summary after all tasks are processed

After processing all tasks, display a summary of the results:

```
done: <done_count>件, closed: <closed_count>件, スキップ(OPEN): <skipped_open_count>件, PR未設定: <no_pr_count>件
```

Example output:

```
done: 2件, closed: 0件, スキップ(OPEN): 0件, PR未設定: 6件
```

### 5. Add comment recording the reason for status change

After updating status to `done` or `closed`, record the merge date/time and reason:

```bash
agkan task comment add <id> "<comment>"
```

Comment format by status:

| Status | Comment Example |
|--------|----------------|
| `done` | `Merged at <mergedAt>. PR was merged and task is complete.` |
| `closed` | `PR was closed without merging. Task moved to closed.` |

Example commands:

```bash
# When merged
agkan task comment add <id> "Merged at 2026-03-22T10:00:00Z. PR was merged and task is complete."

# When closed without merge
agkan task comment add <id> "PR was closed without merging. Task moved to closed."
```

---

## Decision Flow

```
Retrieve all Review tasks
    ↓
Initialize counters (done=0, closed=0, skipped_open=0, no_pr=0)
    ↓
Repeat for each task
    ↓
Does the body contain "PR: <URL>"?
   Yes → Use that URL
   No  → Check metadata: agkan task meta list <id>
            Does metadata contain "pr" key?
               Yes → Use that URL
               No  → Increment no_pr_count → Skip (output message prompting manual verification)
    ↓
Check PR status
    ↓
What is the PR state?
   MERGED  → Move to done → Increment done_count → Add comment with mergedAt timestamp
   CLOSED  → Move to closed → Increment closed_count → Add comment noting PR closed without merge
   OPEN    → Skip (waiting for review) → Increment skipped_open_count
    ↓
Move to next task (repeat until all tasks are processed)
    ↓
Display summary: done: X件, closed: X件, スキップ(OPEN): X件, PR未設定: X件
```

---

## Notes

- PR URL is first looked up in the task body in the format `PR: <URL>`
- If not found in the body, the `pr` key from `agkan task meta list <id>` is used as a fallback
- If PR URL is not found in either location, prompt for manual verification (skip task)
- `done` means successful completion, `closed` means suspended or withdrawn
- The `gh` command is required and will not work in environments where it is unavailable
