---
name: delete-cicd-fails
description: Delete failed CI/CD workflow runs from the current or a specified repo
argument-hint: "[workflow-or-run-id-or-all]"
related:
  - resolve-errors
  - ask-me
  - run-deploy
---

## Goal

Delete failed CI/CD workflow runs from the current or a specified repo, with user confirmation before deletion

## Scope

Use for cleaning up failed workflow runs whose history is no longer needed

See also: /resolve-errors

## Execute

### 1. Detect Target

> Goal: Identify the repo, workflow, and run IDs to delete

1. Run `gh auth status` to check authentication
2. If not authenticated → do `/ask-me`
3. If given `<run-id>` from the argument → delete only that run ID
4. If given `<workflow>` from the argument → delete that workflow's failed runs
5. If given `all` → delete all failed runs in the repo
6. If no argument → do `/resolve-errors`, list the runs first, then ask the user

### 2. Confirm

> Goal: Confirm before deleting

1. Summarize the number of run IDs to delete
2. If the count > 1 or it is `all` → ask the user before deleting
3. If the user does not confirm → stop and report

### 3. Delete Runs

> Goal: Delete the failed runs

1. Build the list of database IDs to delete
2. Run `gh run delete <databaseId>` one run at a time
3. If any run cannot be deleted → record the error and continue
4. Report the number of runs deleted successfully and unsuccessfully

### 4. Verify

> Goal: Check that no failed runs remain

1. Run `gh run list --status failure --limit 50`
2. If any remain → report them and recommend `/resolve-errors`
3. If none remain → report success

## Rules

### 1. User Confirmation

- Deleting multiple runs or `all` must always be confirmed first
- Do not delete runs whose status is not `completed` or `failure`
- No force delete

### 2. Dry Run Option

- If the user passes `--dry-run` → list the runs to be deleted without actually deleting them

### 3. Safety

- Do not delete runs related to the current branch unless the user explicitly says so
- Do not expose secrets or tokens in output
- Use /run-deploy if needed

## Expected Outcome

- The selected failed workflow runs are deleted from GitHub
- A report of the number of runs deleted successfully and unsuccessfully
- No failed runs remain after deletion
