---
name: worktree-cleanup
description: Use when worktrees are accumulating in .claude/worktrees/ or .worktrees/, when starting a new feature and needing to verify no stale worktrees exist, or when the user says "clean up worktrees", "list worktrees", "stale branches". Also use periodically when MEMORY.md references multiple worktrees in resume points.
---

# Worktree Cleanup

## Overview

Audit and clean up git worktrees that are no longer needed. Stale worktrees waste disk space, cause confusion about which branch is active, and can lead to merge conflicts. This skill provides a safe process for identifying and removing worktrees that have been merged or abandoned.

## Fast path: the shared engine (use this first)

For helpdesk-style repos, prefer the single hardened engine over hand-rolling the steps below — it encodes the full proven-safe recipe (memory: `worktree-accumulation`, 2026-06-25):

```bash
# DRY-RUN (default — shows KEEP/WOULD REMOVE per worktree, changes nothing):
~/.claude/scripts/cleanup-merged-worktrees.sh --repo /Users/ben/helpdesk --fetch
# APPLY (patch-backs uncommitted work, then removes):
~/.claude/scripts/cleanup-merged-worktrees.sh --repo /Users/ben/helpdesk --fetch --apply
```

What it gets right that the manual steps below miss:
- **Every location in one pass.** `git worktree list` enumerates `.cursor/`, `~/.codex/`, `.Codex/` (case variant), `.cache/`, `.claude/`, `.worktrees/` — all registered to the same `.git`. No per-dir hunting.
- **Removable = merged into dev OR main, OR remote branch GONE** (deleted on merge; repo has `delete_branch_on_merge:true`). The old `git branch --merged dev`-only check misses main-merged and rebase/merge-deleted branches.
- **KEEPS active worktrees** — remote branch still exists AND not merged = open/in-flight PR. Never touched.
- **Commits are never lost** — branch refs survive `worktree remove`; only uncommitted *working-tree* changes are at risk, and those are **patch-backed** to `~/.claude/worktree-backups/<date>/` before any `--force`.
- **Never touches** the main checkout, the current session's worktree, or locked worktrees. Git ops are wrapped with an 8s timeout (worktree ops hang under Cursor/agent lock contention).
- `--scope session --current <path>` cleans just one worktree (used by the SessionEnd hook and skill teardown steps). `--no-force` leaves dirty worktrees untouched instead of patch-and-force.

The manual process below is the fallback / explanation of what the engine does — use it for non-helpdesk repos or to understand the classification.

## When to Use

- Before starting a new feature (verify clean state)
- When MEMORY.md references 3+ worktrees
- When disk space is a concern
- Periodically (weekly maintenance)
- When user asks about active branches or worktrees

## Process

### Step 1: List All Worktrees

```bash
# Git's built-in worktree list
git worktree list

# Also check common worktree locations
ls -la .claude/worktrees/ 2>/dev/null
ls -la .worktrees/ 2>/dev/null
```

### Step 2: Check Each Worktree Status

For each worktree, determine:

```bash
# Check if branch was merged to dev
git branch --merged dev | grep <branch-name>

# Check for uncommitted changes in worktree
git -C <worktree-path> status

# Check last commit date
git -C <worktree-path> log -1 --format="%ci %s"
```

### Step 3: Classify Worktrees

| Worktree | Branch | Last Commit | Merged? | Uncommitted? | Status |
|----------|--------|-------------|---------|--------------|--------|
| `.worktrees/feat-x` | `feat/x` | 2026-03-01 | Yes | No | Safe to remove |
| `.worktrees/fix-y` | `fix/y` | 2026-03-04 | No | Yes | Active — keep |
| `.claude/worktrees/old` | `feat/old` | 2026-02-20 | No | No | Stale — ask user |

Classification rules:
- **Safe to remove**: Merged to dev AND no uncommitted changes
- **Active**: Has recent commits or uncommitted changes — keep
- **Stale**: Not merged, no recent activity, no uncommitted changes — ask user
- **Orphaned**: Worktree directory exists but branch is deleted — remove

### Step 4: Present Findings

```
## Worktree Audit

**Total worktrees**: [N]
**Safe to remove**: [N] (merged, no uncommitted work)
**Active**: [N] (keep)
**Stale**: [N] (need user decision)

### Safe to Remove
- `.worktrees/feat-x` (`feat/x`) — merged to dev 2026-03-01
- `.worktrees/fix-y` (`fix/y`) — merged to dev 2026-02-28

### Active (keeping)
- `.worktrees/feat-z` (`feat/z`) — uncommitted changes, last activity today

### Stale (need your decision)
- `.worktrees/old-thing` (`feat/old-thing`) — last commit 2026-02-15, NOT merged
  - Has 3 commits not on dev. Delete or merge?

### Recommended Action
Remove [N] merged worktrees? (Y/n)
```

### Step 5: Remove (with user confirmation)

Only remove after user confirms:

```bash
# Remove worktree
git worktree remove <worktree-path>

# If branch is also no longer needed
git branch -d <branch-name>

# Force remove if worktree has issues
git worktree remove --force <worktree-path>
```

### Step 6: Update MEMORY.md

Remove references to deleted worktrees from MEMORY.md resume points. Update any resume points that reference cleaned-up branches.

## Safety Rules

1. **NEVER remove a worktree with uncommitted changes** without explicit user confirmation
2. **NEVER delete branches that aren't merged** without user confirmation
3. **NEVER force-remove** without explaining what will be lost
4. **Always check MEMORY.md** for active resume points before removing

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Removing active worktree | Always check for uncommitted changes first |
| Deleting unmerged branch | Only delete branches merged to dev |
| Not updating MEMORY.md | Remove stale resume points after cleanup |
| Force-removing without asking | Always get user confirmation for force operations |
