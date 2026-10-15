---
name: git-sync-dev-submodules
version: 1.1.0
license: MIT
description: >
  Fast local dev sync for Git worktrees. Use when an agent needs to (1) update
  the current worktree branch onto the latest `origin/dev`, or (2) when run
  from a `dev` worktree, fast-forward `dev` and rebase every other clean
  worktree onto local `dev`.
---

# Git Sync Dev Worktrees

## Overview
- Keep the flow local-first and fast: fetch once, then sync branches with `merge --ff-only` or `rebase`.
- Use `--dry-run` to preview actions before changing git state.
- The skill name is unchanged for compatibility, but the workflow no longer handles submodules.

## Scripts
- `scripts/sync-dev-to-current-branch.sh`
  - Run in any non-detached worktree.
  - If current branch is `dev`, fast-forward it to `origin/dev`.
  - Otherwise, rebase the current branch onto `origin/dev`.
- `scripts/sync-dev-worktrees.sh`
  - Run from a `dev` worktree.
  - Fast-forward the current `dev` worktree to `origin/dev`.
  - Rebase every other clean, non-detached worktree onto local `dev`.

## Defaults
- Remote: `origin`
- Dev source branch: `dev`

## Options
- `--remote <name>`: remote name to fetch from (default `origin`)
- `--dev-branch <name>`: source branch to sync against (default `dev`)
- `--dry-run`: print the plan without changing git state
- `--help`: print usage

## Common Commands
```bash
# Sync only the current worktree
bash "<path-to-skill>/scripts/sync-dev-to-current-branch.sh"

# Sync every worktree from a dev worktree
bash "<path-to-skill>/scripts/sync-dev-worktrees.sh"

# Preview the current-worktree sync without changing git state
bash "<path-to-skill>/scripts/sync-dev-to-current-branch.sh" --dry-run
```

## Reporting
- Report updated worktrees.
- Report skipped detached or dirty worktrees.
- Report failures after aborting a conflicted batch rebase.
- Report current branch alignment against the target dev branch when syncing a single worktree.
