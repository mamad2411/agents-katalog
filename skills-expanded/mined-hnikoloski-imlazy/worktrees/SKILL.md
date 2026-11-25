---
name: worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans — ensures an isolated workspace exists via native tools or git worktree fallback
---

# worktrees

## Overview

Ensure work happens in an isolated workspace. Prefer your platform's native worktree tools. Fall back to manual git worktrees only when no native tool is available.

**Core principle:** Detect existing isolation first. Then use native tools. Then fall back to git. Never fight the harness.

## Step 0: Detect existing isolation

**Before creating anything, check if you are already in an isolated workspace.**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

**Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside git submodules. Verify you're not in one:
```bash
git rev-parse --show-superproject-working-tree 2>/dev/null
```

If that returns a path, you are in a submodule — treat as normal repo.

**If `GIT_DIR != GIT_COMMON` (and not a submodule):** Already in a linked worktree. Skip to Step 3 (Project Setup). Do NOT create another worktree.

**If `GIT_DIR == GIT_COMMON`:** Normal repo checkout. Ask for consent before creating a worktree: "Would you like me to set up an isolated worktree? It protects your current branch from changes." If declined, work in place.

## Step 1: Create isolated workspace

Try in this order:

### 1a. Native worktree tools (preferred)

Check if your harness provides a native worktree tool (names like `EnterWorktree`, `WorktreeCreate`, `/worktree`, or a `--worktree` flag). If yes, use it and skip to Step 3. Native tools handle directory placement, branch creation, and cleanup automatically.

### 1b. Git worktree fallback (only if 1a does not apply)

**Directory selection** (priority order):
1. Declared user preference in your instructions
2. Existing project-local `.worktrees/` or `worktrees/` directory
3. Existing global `~/.config/imlazy/worktrees/<project>/`
4. Default: `.worktrees/` at project root

**Safety verification** (project-local directories only):
```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```
If NOT ignored: add to `.gitignore`, commit, then proceed.

**Create the worktree:**
```bash
project=$(basename "$(git rev-parse --show-toplevel)")
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

If `git worktree add` fails with a permission error (sandbox denial), tell the user and work in the current directory instead.

## Step 3: Project setup

Auto-detect and run appropriate setup:
```bash
if [ -f package.json ]; then npm install; fi
if [ -f Cargo.toml ]; then cargo build; fi
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi
if [ -f go.mod ]; then go mod download; fi
```

## Step 4: Verify clean baseline

Run the project test suite. If tests fail, report failures and ask whether to proceed or investigate. If tests pass, report ready.

## Quick reference

| Situation | Action |
|-----------|--------|
| Already in linked worktree | Skip creation (Step 0) |
| In a submodule | Treat as normal repo |
| Native worktree tool available | Use it (Step 1a) |
| No native tool | Git worktree fallback (Step 1b) |
| `.worktrees/` exists | Use it (verify ignored) |
| Neither exists | Default `.worktrees/` at project root |
| Directory not ignored | Add to .gitignore + commit |
| Permission error on create | Work in place, tell user |
| Tests fail on baseline | Report + ask before proceeding |

## Red flags — never

- Create a worktree when Step 0 detects existing isolation
- Use `git worktree add` when you have a native worktree tool
- Create project-local worktree without verifying it is gitignored
- Skip baseline test verification
- Proceed with failing tests without asking
