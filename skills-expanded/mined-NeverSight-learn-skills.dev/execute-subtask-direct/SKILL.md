---
name: execute-subtask-direct
description: "[DEPRECATED] Use agkan-subtask-direct instead. Use when a task has been selected and you need to implement it directly without PR/branch creation - handles implementation and marking done."
user-invokable: false
---

> **DEPRECATED**: This skill has been renamed. Please use `agkan-subtask-direct` instead.
> `Skill("agkan-subtask-direct")`

# execute-subtask-direct

## Overview

A workflow to directly implement a selected task without creating a branch or PR and mark it as complete.

---

## Workflow

### 1. Implementation

Implement according to the task requirements.

Refer to /key-guidelines during implementation to maintain code quality.

### 2. Commit

Stage files by specifying them explicitly. Do not use `git add -A` as it risks including unintended files such as `.env` or credentials.

```bash
git add <file1> <file2> ...
git commit -m "<commit message>"
git push
```

> **Note**: Do not use `git add -A` or `git add .`. Files containing `.env`, `credentials.*`, or secrets may be committed unintentionally.

### 3. Update task to done

```bash
agkan task update <id> --status done
```

---

## Important Notes

- Do not create a branch (work directly on the current branch)
- Do not create a PR
- Update directly to done after implementation is complete
- This skill is used after task selection (task selection is done with the `execute-task-direct` skill)
