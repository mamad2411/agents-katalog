---
name: agkan-subtask-direct
description: Use when a task has been selected and you need to implement it directly without PR/branch creation - handles in_progress update, implementation, and marking done.
user-invokable: false
---

# agkan-subtask-direct

## Overview

A workflow to directly implement a selected task without creating a branch or PR and mark it as complete.

---

## Workflow

### 1. Update Task to In Progress

```bash
agkan task update <id> --status in_progress
```

### 2. Check for Pre-assigned Branch

Before implementing, check if a branch has been pre-assigned via task metadata:

```bash
BRANCH=$(agkan task meta get <id> branch 2>/dev/null)
if [ -n "$BRANCH" ]; then
  git fetch origin
  git checkout "$BRANCH"
fi
```

If `$BRANCH` is set, all subsequent commits and pushes must target that branch.

### 3. Implementation

Implement according to the task requirements.

Refer to /key-guidelines during implementation to maintain code quality.

### 4. Static Analysis / Lint Check (if applicable)

If the project has a static analysis or lint tool configured, run it before committing:

- TypeScript: `npx tsc --noEmit`
- ESLint: `npx eslint .`
- RuboCop: `bundle exec rubocop`
- Ruff (Python): `ruff check .`
- Other: run the appropriate tool for the project language

Fix any errors before proceeding.

### 5. Commit

Stage files by specifying them explicitly. Do not use `git add -A` as it risks including unintended files such as `.env` or credentials.

```bash
git add <file1> <file2> ...
git commit -m "<commit message>"
# If a branch was checked out from metadata, push to it; otherwise push to current branch
git push -u origin <branch-name-or-current>
```

> **Note**: Do not use `git add -A` or `git add .`. Files containing `.env`, `credentials.*`, or secrets may be committed unintentionally.

### 6. Update task to done

Only execute this step if implementation succeeded — specifically, if the commit (Step 4) completed without critical errors (permission errors, push failures, etc.).

**If a critical error occurred** (e.g., git push failed, permission denied, commit failed), do NOT update the status to done. Leave the task as `in_progress` and record the error details in the task body:

```bash
# On error: record what went wrong in the task body (optional but recommended)
agkan task get <id> --json
# Write body to tmp file and update using --file to preserve newlines
cat > /tmp/agkan_body_$$.md << 'BODY'
<existing body>

Error: <error description>
BODY
agkan task update <id> --file /tmp/agkan_body_$$.md
# Do NOT run: agkan task update <id> --status done
```

**If implementation succeeded**, update to done:

```bash
agkan task update <id> --status done
```

---

## Important Notes

- Do not create a branch (work directly on the current branch)
- Do not create a PR
- **Only update to done if implementation succeeded** — if a critical error occurred, keep the task as `in_progress`
- If a critical error occurs (git push failure, commit failure, permission error), keep the task as `in_progress` and record the error
- This skill is used after task selection (task selection is done with the `agkan-run-direct` skill)
