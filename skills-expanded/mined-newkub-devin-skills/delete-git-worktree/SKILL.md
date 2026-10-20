---
name: delete-git-worktree
description: Safely delete the specified git worktree
argument-hint: "[scope]"
related:
  - list-git
  - use-git-worktrees
  - cleanup
  - delete

---

## Goal

Remove the specified git worktree without harming the parent repository

## Scope

Use when you need to delete a specific worktree

## Execute

### 1. Identify Worktree

> Goal: Identify the worktree to delete

1. Run `git worktree list`
2. Or do `/list-git-worktree`
3. Confirm the path of the worktree to delete

### 2. Check Status

> Goal: Avoid deleting a worktree with changes

1. Run `git -C <worktree-path> status --porcelain`
2. If there are uncommitted/untracked changes → stop and ask first
3. If you want to discard the changes too → use `--force`

### 3. Remove Worktree

> Goal: Remove the worktree

1. Run `git worktree remove <path>`
2. If it is locked or has issues → run `git worktree remove --force <path>`
3. Verify with `git worktree list` again

### 4. Prune

> Goal: Clean up tracking

1. Run `git worktree prune`
2. Verify that the tracking references are removed

## Rules

### 1. Confirm Before Delete

- Ask the user before deleting
- Never delete a worktree with uncommitted changes without asking
- Never delete the main working tree

### 2. Force With Caution

- Use `--force` only when a normal remove is not possible
- State the reason before forcing

### 3. Preserve Branches

- Removing a worktree does not delete its branch
- If you also want to delete the branch → do `/delete-git-branch`

- Use /use-git-worktrees if needed
- Use /cleanup-worktree if needed

## Expected Outcome

- The worktree is removed
- `git worktree list` no longer shows it
- The branch still exists
- No uncommitted changes lost
