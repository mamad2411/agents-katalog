---
name: clean-up
description: Housekeeping — remove merged local and remote branches, prune stale remote tracking refs, close resolved GitHub issues and merged PRs, clean up leftover worktrees. Use when the user says "clean up", "cleanup", "prune branches", "remove merged branches", "close issues", "tidy up", "housekeeping", or "delete old branches".
---

# Clean Up

Audit first, act second. Always show what will be removed before removing it.

## 1. Audit

Run all of these before touching anything:

```bash
# Branches merged into main/master (safe to delete)
git branch --merged main | grep -v '^\*\|main\|master\|develop'

# Remote tracking refs that no longer exist on the remote
git remote prune origin --dry-run

# Leftover worktrees
git worktree list

# Merged PRs (open on GitHub but already merged)
gh pr list --state merged --limit 20

# Open issues that reference a merged PR or are labelled "resolved"
gh issue list --state open --label resolved 2>/dev/null || true
```

Present the full audit to the user before proceeding. Confirm before any destructive step.

## 2. Remove Merged Local Branches

```bash
# Delete branches already merged into main
git branch --merged main \
  | grep -v '^\*\|main\|master\|develop' \
  | xargs -r git branch -d
```

Skip: `main`, `master`, `develop`, the current branch (`*`), and any branch the user explicitly wants to keep.

## 3. Remove Merged Remote Branches

```bash
# For each merged branch identified in §1, delete from origin
git push origin --delete <branch-name>
```

Do not bulk-delete. Delete one branch at a time and confirm each succeeds before moving on.

## 4. Prune Remote Tracking Refs

```bash
# Remove local refs to branches deleted on the remote
git fetch --prune
```

This is non-destructive to local branches — it only removes stale `origin/<branch>` pointers.

## 5. Clean Up Worktrees

```bash
git worktree list
```

For each worktree that is no longer needed (branch merged, work abandoned):

```bash
git worktree remove <path>
git branch -d <branch>
```

If the worktree has uncommitted changes, warn the user — do not remove it without explicit confirmation.

## 6. Close Merged PRs

```bash
# List merged PRs still showing as open
gh pr list --state merged

# Close any that are still open
gh pr close <number>
```

## 7. Close Resolved Issues

```bash
# Close issues linked to merged PRs or explicitly marked resolved
gh issue close <number> --comment "Resolved — closing."
```

Only close issues where the resolution is clear: the linked PR merged, the issue is labelled `resolved`/`wontfix`, or the user says to close it. Do not close issues speculatively.

## 8. Report

```
Cleaned up:
  Local branches deleted:  <list or "none">
  Remote branches deleted: <list or "none">
  Remote refs pruned:      <N>
  Worktrees removed:       <list or "none">
  PRs closed:              <list or "none">
  Issues closed:           <list or "none">
```
