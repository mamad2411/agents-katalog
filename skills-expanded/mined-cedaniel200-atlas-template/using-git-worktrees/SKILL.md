---
name: using-git-worktrees
description: Use at session start, when creating change artifacts, or before implementing a plan - resolves the workspace policy (worktree by default, human-requested feature branch as exception) and never writes on the base branch; prefers native worktree tools over git worktree
license: MIT
---

# Using Git Worktrees

## Overview

Ensure work happens in an isolated workspace. Prefer your platform's native worktree tools. Fall back
to manual git worktrees only when no native tool is available.

**Core principle:** Detect existing isolation first. Then use native tools. Then fall back to git.
Never fight the harness.

**Workspace policy:** every change is written on its own branch. The default is a worktree; a simple
feature branch in the main checkout is an exception the human requests explicitly. The base branch is
never written to. This skill applies at three trigger points:

1. **Session start** — report the current branch, whether the working directory is a worktree and the
   active change. Do not create anything yet.
2. **Before creating change artifacts** — isolate first if the current branch is the base branch.
3. **Before implementing a plan** — same check.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Step 0: Detect Existing Isolation

**Before creating anything, check if you are already in an isolated workspace.**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside git submodules. Before concluding
"already in a worktree," verify you are not in a submodule:

```bash
# If this returns a path, you're in a submodule, not a worktree — treat as normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**If `GIT_DIR != GIT_COMMON` (and not a submodule):** you are already in a linked worktree. Skip to
Step 2. Do NOT create another worktree. Report: *"Already in isolated workspace at `<path>` on branch
`<name>`."* (Detached HEAD: note that branch creation is needed at finish time.)

**If `GIT_DIR == GIT_COMMON` (or in a submodule):** you are in a normal repo checkout. Resolve consent
from the preference already declared in `AGENTS.md` or the session instructions. When the declared
default is a worktree, do not ask again. Ask only when no preference exists:

> "Would you like me to set up an isolated worktree? It protects your current branch from changes."

If the user declines, work in place only when they asked for a simple feature branch and the working
tree is clean. Never work on the base branch: isolate, or stop and ask. Record the exception in the
change.

## Step 1: Create Isolated Workspace

**Two mechanisms. Try them in this order.**

### 1a. Native Worktree Tools (preferred)

Do you already have a way to create a worktree? It might be a tool named like `EnterWorktree`,
`WorktreeCreate`, a `/worktree` command, or a `--worktree` flag. If so, use it and skip to Step 2.
Native tools handle directory placement, branch creation and cleanup automatically; using
`git worktree add` when you have one creates phantom state your harness cannot see or manage.

### 1b. Git Worktree Fallback

**Only if Step 1a does not apply.**

#### Directory Selection

Explicit user preference always beats observed filesystem state.

1. Check your instructions for a declared worktree directory preference.
2. Check for an existing project-local directory: `ls -d .worktrees` (preferred) or `ls -d worktrees`.
   If both exist, `.worktrees` wins.
3. Otherwise default to `.worktrees/` at the project root.

#### Safety Verification (project-local directories only)

**MUST verify the directory is ignored before creating the worktree:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If NOT ignored:** add it to `.gitignore`, commit, then proceed. Prevents accidentally committing
worktree contents.

#### Create the Worktree

```bash
path="$LOCATION/$BRANCH_NAME"
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**Sandbox fallback:** if `git worktree add` fails with a permission error, tell the user the sandbox
blocked it and work in the current directory instead.

## Step 2: Project Setup

Run the project's install command from `AGENTS.md` § Comandos (`INSTALL_COMMAND`). If it is `N/A`,
skip this step. Do not guess stack-specific commands.

## Step 3: Verify Clean Baseline

Run the project's test command (`TEST_COMMAND`). If it is `N/A`, state that there is no automated
baseline.

**If tests fail:** report failures and ask whether to proceed or investigate. **If they pass:** report
ready.

### Report

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Already in linked worktree | Skip creation (Step 0) |
| In a submodule | Treat as normal repo (Step 0 guard) |
| Native worktree tool available | Use it (Step 1a) |
| No native tool | Git worktree fallback (Step 1b) |
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check instruction file, then default `.worktrees/` |
| Directory not ignored | Add to `.gitignore` + commit |
| Permission error on create | Sandbox fallback, work in place |
| Tests fail during baseline | Report failures + ask |
| `INSTALL_COMMAND` is `N/A` | Skip dependency install |

## Red Flags

**Never:**
- Write on the base branch: isolate the change or stop and ask
- Create a worktree when Step 0 detects existing isolation
- Use `git worktree add` when you have a native worktree tool (e.g., `EnterWorktree`)
- Skip Step 1a by jumping straight to Step 1b's git commands
- Create a worktree without verifying it's ignored (project-local)
- Skip baseline test verification
- Proceed with failing tests without asking

**Always:**
- Run Step 0 detection first
- Prefer native tools over git fallback
- Follow directory priority: explicit instructions > existing project-local directory > default
- Verify the directory is ignored for project-local
- Use the project's `INSTALL_COMMAND` / `TEST_COMMAND`
- Verify a clean test baseline

## References

Read only when needed:

- [`references/common-mistakes.md`](references/common-mistakes.md) — the five recurring mistakes and
  their fixes.
