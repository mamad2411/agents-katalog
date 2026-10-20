---
name: cleanup-worktree
description: Remove unused git worktrees and prune stale worktree tracking metadata
argument-hint: "[scope]"
related:
  - suggest-next-action
  - report
  - run-clean
  - run-cleanup
---

## Goal

Remove unused git worktrees, reclaim disk space, and safely prune leftover tracking metadata

## Scope

Use for git repositories with multiple worktrees when you need to remove unwanted worktrees or prune worktrees that were deleted from disk but are still tracked

## Execute

### 1. List Worktrees

> Goal: Know which worktrees exist

1. Run `git worktree list`
2. Record path, branch, commit, and status
3. Identify the main worktree (main working directory)
4. Identify removable worktrees: no uncommitted changes and not main

### 2. Check Worktree Status

> Goal: Confirm the worktree is safe to remove

1. cd into the target worktree and run `git status --short`
2. If there are uncommitted changes → report and stop unless the user confirms
3. Check that the worktree's branch has no important unpushed work, or that if pushed, the branch still exists on the remote
4. If there is any risk → use `/suggest-next-action`

### 3. Remove Worktree

> Goal: Remove the worktree

1. Run `git worktree remove <path>`
2. If the worktree was already deleted directly from the filesystem → use `git worktree remove <path>` or `git worktree prune`
3. If it is locked or has leftover tracking → run `git worktree unlock <path>` first
4. Verify `git worktree list` again

### 4. Prune Orphaned Tracking

> Goal: Remove stale tracking metadata

1. Run `git worktree prune --dry-run` to see which worktrees would be pruned
2. If appropriate → run `git worktree prune`
3. Verify `git worktree list` again

### 5. Verify And Report

> Goal: Summarize the results

1. Use `/report` showing: Path, Branch, Action, Status
2. Confirm the main working directory is unaffected
3. Run `/suggest-next-action`

## Rules

### 1. Safety

- Never remove the main working directory
- Never remove a worktree with uncommitted changes without user confirmation
- Never remove a branch on the remote without a clear instruction

### 2. Force When Needed

- If `git worktree remove <path>` fails → use `git worktree remove --force <path>` with confirmation
- Use `--force` only for worktrees with uncommitted changes when the user accepts

### 3. No Data Loss

- Check `git status` inside the worktree before removing
- If there are important changes → recommend committing, stashing, or moving them first
- Verify the branch still exists on the remote or locally after removal

### 4. Cleanup Scope

- Prune all orphaned tracking entries with no real worktree
- Never prune worktrees that are still in use
- Use /run-clean if needed
- Use /run-cleanup if needed

## Expected Outcome

- Unused worktrees are removed
- Stale tracking metadata is pruned
- Main working directory keeps working normally
- Report of the remaining worktrees
