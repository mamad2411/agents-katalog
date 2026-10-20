---
name: cleanup-git-branch
description: Delete old git branches that are merged or no longer used
argument-hint: "[filter]"
related:
  - cleanup-branches-merged
  - delete
  - run-clean
  - run-cleanup
---

## Goal

Clean old branches out of the repository

## Scope

Use when local or remote branches are merged or abandoned — focused on ad-hoc deletion of individual branches or small groups (including force-delete `-D` when needed); for a dry-run + PR cross-check sweep of all branches merged into `main` → use `/cleanup-branches-merged`

## Execute

### 1. Identify Candidates

> Goal: Identify Candidates

1. `git branch --merged main` for local
2. `git branch -r --merged main` for remote
3. Check for branches with no recent commits
4. Exclude `main`, `master`, release branches, and long-lived branches per project conventions

### 2. Confirm With Team

> Goal: Confirm With Team

1. Confirm first in shared repos before deleting
2. Verify the branch has no unmerged commits
3. Back up the ref if there is any risk

### 3. Delete

> Goal: Delete

1. `git branch -d <branch>` for local (merged)
2. `git branch -D <branch>` to force
3. `git push origin --delete <branch>` for remote
4. `git remote prune origin` to clean up tracking

## Rules

- Never delete the default branch
- Check merge status first
- Get confirmation before deleting shared branches
- Keep release/hotfix branches per policy

- Use /delete-git-branch if needed
- Use /run-clean if needed
- Use /run-cleanup if needed

## Expected Outcome

- Old branches removed
- Repository clean
- No data loss
