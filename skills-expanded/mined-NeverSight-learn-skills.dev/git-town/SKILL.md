---
name: git-town
description: Use when working with git town for stacked branch workflows, creating or navigating branch stacks, syncing stacked changes, proposing PRs for stacked branches, or encountering git town commands like hack, append, up, down, propose, sync, ship, prepend, compress, undo, switch.
---

# Git Town

Git Town is a high-level CLI that automates Git workflows, with first-class support for **stacked changes** — a series of dependent feature branches reviewed and merged independently.

## GitHub Authentication

**Use `gh` CLI instead of a Personal Access Token (PAT).**

```bash
# Configure git town to use gh CLI for GitHub auth
git config --global git-town.github-connector gh
```

This delegates all authentication and token management to `gh`, which handles token storage securely. PATs stored via `git config` sit in plaintext in your Git configuration.

Only fall back to a PAT if `gh` is unavailable:

```bash
git config --global git-town.github-token <token>
# or via env var: GIT_TOWN_GITHUB_TOKEN=<token>
```

**Known bug:** When using the API/PAT connector and your `origin` targets a fork, git town cannot find PRs targeting the upstream repository. The `gh` connector handles this correctly.

## Initial Setup

```bash
# Interactive setup: sets main branch, perennials, sync strategy, etc.
git town init
```

Config file (`git-town.toml` or `.git-town.toml` at repo root):

```toml
[branches]
main = "main"

[hosting]
forge-type = ""  # auto-detect: github, gitlab, bitbucket, gitea, forgejo

[sync]
feature-strategy = "merge"  # or "rebase" or "compress"
```

## Core Stacking Workflow

### Starting a Stack

```bash
# Create a new feature branch off main (syncs main first if workspace is clean)
git town hack <branch-name>

# Start the branch and immediately open a PR
git town hack <branch-name> --propose

# Carry uncommitted changes from current branch to the new one
# (does NOT sync when workspace is dirty — commit first if you want a clean base)
git town hack <branch-name>
```

### Extending a Stack

```bash
# Add a child branch on top of the current branch
git town append <branch-name>

# Insert a new branch BETWEEN current branch and its parent
git town prepend <branch-name>
```

Stack shape reference:

```
main
 \
  1-refactor          ← git town hack 1-refactor
   \
    2-rename          ← git town append 2-rename  (on 1-refactor)
     \
      3-feature       ← git town append 3-feature (on 2-rename)
```

### Navigating a Stack

```bash
# Move to parent branch (up the stack toward main)
git town up

# Move to child branch (down the stack away from main)
git town down

# Interactive visual branch switcher (VIM motions)
git town switch

# Filter switch to branches matching a pattern
git town switch feature-

# Show full branch hierarchy
git town branch
```

### Syncing

```bash
# Sync current branch (pulls from parent + tracking branch)
git town sync

# Sync every branch in the current stack
git town sync --stack

# Sync ALL local branches (recommended habit — safe to run anytime)
git town sync --all

# Sync without pushing (reduces CI pressure)
git town sync --no-push

# Sync but skip pulling updates from parent (useful in busy monorepos)
git town sync --detached
```

**Sync often.** Unsynced stacks accumulate phantom merge conflicts. `git town undo` can revert any failed sync to the exact pre-sync state.

### Opening Pull Requests

```bash
# Open PR for the current branch (syncs branch first in detached mode)
git town propose

# Open PRs for ALL branches in the current stack at once
git town propose --stack

# Pre-populate title and body
git town propose --title "My feature" --body "Description here"

# Read body from a file
git town propose --body-file ./pr-body.md
```

Git Town automatically targets the correct parent branch as the PR base. When `1-refactor` is merged, run `git town sync` and the stack re-roots itself at `main`.

### Shipping

```bash
# Merge the current branch (must be direct child of main)
git town ship

# Ship with a specific commit message
git town ship -m "feat: add feature"

# Ship a specific branch by name
git town ship <branch-name>
```

> **Note:** Most teams should use their forge's web UI or merge queue. `git town ship` is for offline mode or when the forge auto-deletion of branches is not configured.

Ship order: **always ship oldest (closest to main) branch first**. Descendant branches cannot be shipped until ancestors are merged.

For stacked changes, prefer the **fast-forward ship strategy** to avoid phantom conflicts:

```toml
[ship]
strategy = "fast-forward"
```

## Stack Restructuring

```bash
# Change the parent of the current branch interactively
git town set-parent

# Swap the current branch with its parent (reverse their order)
git town swap

# Extract current branch out of the stack (make it a standalone branch off main)
git town detach

# Move commits from current branch to a new child/sibling branch (visual dialog)
git town hack --beam
git town append --beam
```

## Compressing Commits

Always sync before compressing. Compressing an unsynced branch can include unrelated commits from the parent.

```bash
# Squash all commits on the current branch into one
git town compress

# Squash all branches in the current stack
git town compress --stack

# Squash with a custom message
git town compress -m "feat: refactor architecture"
```

> **Bug to avoid:** Running `git town compress` before `git town sync` when `main` is ahead of your branch can result in your compressed commit containing unrelated files from `main`. Always sync first.

## Error Recovery

```bash
# Undo the last fully-executed git town command (restores exact pre-command state)
git town undo

# After resolving a merge conflict, resume the suspended command
git town continue

# Skip conflicts on the current branch and continue
git town skip

# Test-drive a command without executing it
git town <command> --dry-run
```

## Quick Reference

| Goal | Command |
|------|---------|
| Start a new independent branch off main | `git town hack <name>` |
| Add a dependent branch to the stack | `git town append <name>` |
| Insert a branch before the current one | `git town prepend <name>` |
| Move toward main in the stack | `git town up` |
| Move away from main in the stack | `git town down` |
| Jump to any branch visually | `git town switch` |
| Show stack hierarchy | `git town branch` |
| Sync current branch | `git town sync` |
| Sync entire stack | `git town sync --stack` |
| Sync all branches | `git town sync --all` |
| Open a PR | `git town propose` |
| Open PRs for whole stack | `git town propose --stack` |
| Squash commits on branch | `git town compress` |
| Merge feature into main | `git town ship` |
| Undo last command | `git town undo` |
| Resume after conflict | `git town continue` |
| Preview without executing | `git town <cmd> --dry-run` |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Compressing before syncing | Run `git town sync` first; compress on an unsynced branch includes parent commits |
| Shipping a branch that isn't a direct child of main | Ship oldest branches first; use `git town set-parent` to verify lineage |
| Expecting `hack` to sync when workspace is dirty | `git town hack` skips sync when you have uncommitted changes — stash or commit first |
| Using PAT connector on a fork | Switch to `gh` connector: `git config git-town.github-connector gh` |
| `git config --global user.email` not set | Git Town reads email from global config; `includeIf` blocks in `.gitconfig` require the remote URL to exist before they apply, so email may appear unset on a fresh clone |
| Panics after `set-parent` + `sync` on a branch with no remote | Known bug in some versions; run `git push` to create the tracking branch before running `sync` |

## Git Aliases (Optional Convenience)

```ini
# Add to ~/.gitconfig
[alias]
  hack      = town hack
  append    = town append
  prepend   = town prepend
  propose   = town propose
  sync      = town sync
  ship      = town ship
  up        = town up
  down      = town down
  sw        = town switch
```

## Best Practices for Stacked Changes

1. **One concern per branch** — single-responsibility branches are easier to review and conflict less
2. **Sync frequently** — run `git town sync --all` multiple times per day; `git town undo` makes it safe
3. **Avoid unnecessary stacking** — independent changes should be separate stacks off `main`, not chained
4. **Ship oldest-first** — after a branch merges, sync to let git town re-root the stack automatically
5. **Enable rerere** — `git config --global rerere.enabled true` lets Git reuse conflict resolutions across rebases
6. **Prefer fast-forward merges** — eliminates phantom conflicts in squash-merge workflows