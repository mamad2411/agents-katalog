---
name: delete-git-branch
description: Safely delete a local or remote git branch
argument-hint: "[scope]"
related:
  - list-git
  - refactor-commit
  - resolve-github-pr

---

## Goal

Safely delete the specified git branch from local or remote

## Scope

Use when cleaning up branches that are no longer needed

## Execute

### 1. Identify Branch

> Goal: Identify the branch to delete

1. Run `git branch --all`
2. Confirm the branch name
3. Check that it is not `main`, `master`, or a protected branch

### 2. Check Merge Status

> Goal: Delete safely

1. Run `git branch --merged` to see which branches are already merged
2. If the branch is not merged → ask before deleting
3. If already merged → it can be deleted with `-d`

### 3. Delete Local Branch

> Goal: Delete the local branch

1. Run `git branch -d <branch>` for a merged branch
2. If not merged and the user confirms → run `git branch -D <branch>`

### 4. Delete Remote Branch

> Goal: Delete the remote branch

1. Run `git push origin --delete <branch>`
2. Or `git push origin :<branch>`
3. Verify that the remote branch was deleted

### 5. Cleanup

> Goal: Clean up local tracking

1. Run `git fetch --prune`
2. Run `git branch -vv` to check tracking

## Rules

### 1. Protect Main

- Never delete `main`, `master`, or the default branch
- Never delete a branch with an open PR without asking

### 2. Confirm Unmerged

- If the branch is not merged → ask before using `-D`
- State whether commits will be lost

### 3. Preserve Tags

- Deleting a branch does not delete tags pointing to its commits
- If needed, check the tags

- Use /list-git-commit if needed
- Use /refactor-commit if needed
- Use /resolve-github-pr if needed

## Expected Outcome

- The local branch is deleted
- The remote branch is deleted (if requested)
- Main/master is unaffected
- No commits lost without explicit intent
