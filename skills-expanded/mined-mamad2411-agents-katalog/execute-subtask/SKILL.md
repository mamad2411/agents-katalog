---
name: execute-subtask
description: "[DEPRECATED] Use agkan-subtask instead. Use when a task has been selected and you need to implement it in an isolated (forked) context - handles in_progress update, branch creation, implementation, PR creation, and marking done."
user-invokable: false
metadata:
  context: fork
---

> **DEPRECATED**: This skill has been renamed. Please use `agkan-subtask` instead.
> `Skill("agkan-subtask")`

# execute-subtask

## Overview

Workflow to implement a selected task on a fork (worktree), create a PR, and complete the task.

### About `context: fork` in frontmatter

The `context: fork` field in the frontmatter indicates that this skill is designed to run in an isolated worktree (forked context). When an Agent invokes this skill, it executes in a separate worktree environment rather than the current working directory. This isolation ensures that branch creation and file changes do not interfere with the parent context.

---

## Workflow

### 1. Create Branch

```bash
git checkout -b <branch-name>
```

Branch name is generated from task ID and title (example: `feat/42-add-login-page`).

### 2. Write Branch Name to Task

```bash
# First, retrieve the existing body
agkan task get <id> --json
# Write body to tmp file and update using --file to preserve newlines
cat > /tmp/agkan_body_$$.md << 'BODY'
<existing body>

Branch: <branch-name>
BODY
agkan task update <id> --file /tmp/agkan_body_$$.md
```

### 3. Implementation

Implement according to the task content.

Refer to /key-guidelines during implementation to maintain code quality.

### 4. Commit and Push

```bash
git add -A
git commit -m "<commit message>"
git push -u origin <branch-name>
```

### 5. Create PR

```bash
gh pr create --title "<title>" --body "<body>"
```

### 6. Add PR Information to Task

```bash
# First, retrieve the existing body
agkan task get <id> --json
# Write body to tmp file and update using --file to preserve newlines
cat > /tmp/agkan_body_$$.md << 'BODY'
<existing body>

PR: <PR URL>
BODY
agkan task update <id> --file /tmp/agkan_body_$$.md
```

### 7. Update Task to Review

```bash
agkan task update <id> --status review
```

---

## Important Notes

- Do not mark task as done before PR is merged (mark as done after PR review and merge)
- This skill is used after task selection (task selection is done with `execute-task` skill)
