---
name: cleanup-complete-branches
description: >-
  Clean up completed Git branches and worktrees for this repository, both
  locally and on GitHub. Use when the user says "/cleanup-complete-branches",
  "$cleanup-complete-branches", "clean up complete branches", "remove merged
  branches", "delete completed worktrees", "prune old worktrees", or asks to
  remove local and remote branches after pull requests are merged or closed.
---

# Cleanup Complete Branches

Remove completed worktrees, local branches, and GitHub branches without touching
active work.

## Workflow

### 1. Start With A Preview

Always run the bundled script in dry-run mode first:

```bash
python3 .agents/skills/cleanup-complete-branches/scripts/cleanup_complete_branches.py
```

Dry-run mode fetches and prunes remotes, then reports what would be removed.
It must not delete anything.

Review the output before applying changes. Treat these as blockers:

- A worktree is dirty.
- A branch has no merged GitHub PR and is not merged into `origin/main`.
- The branch name is protected.
- GitHub CLI authentication is missing and completion cannot be proven from git
  history alone.

### 2. Apply The Cleanup

If the dry run only lists completed branches and clean worktrees, apply it:

```bash
python3 .agents/skills/cleanup-complete-branches/scripts/cleanup_complete_branches.py --apply
```

The script removes clean completed worktrees first, then deletes matching local
branches, then deletes matching `origin` branches on GitHub.

### 3. Optional Cases

Only remove closed-but-unmerged PR branches when the user explicitly asks for
branches from abandoned or closed PRs to be removed:

```bash
python3 .agents/skills/cleanup-complete-branches/scripts/cleanup_complete_branches.py --apply --include-closed-unmerged
```

Use `--force-worktrees` only when the user explicitly accepts losing uncommitted
files inside completed worktrees:

```bash
python3 .agents/skills/cleanup-complete-branches/scripts/cleanup_complete_branches.py --apply --force-worktrees
```

## Safety Rules

- Never delete `main`, `master`, `develop`, `dev`, `release`, `staging`, or
  `production`.
- Never delete the currently checked-out branch.
- Never delete a dirty worktree unless the user explicitly requested force.
- Prefer GitHub PR status for squashed PRs, because git ancestry may not show
  squashed branches as merged.
- If a branch is ambiguous, report it and leave it alone.
- Do not close GitHub issues or PRs as part of cleanup.

## Reporting

Summarize:

- Worktrees removed or skipped.
- Local branches removed or skipped.
- GitHub branches removed or skipped.
- Any branches that need the user's decision.
