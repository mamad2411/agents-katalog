---
name: sloth-worktree
description: "Use when starting client engagement work that needs isolation — an isolated workspace per engagement so one client's branch never bleeds into another's, via native tools or a git worktree fallback."
---

# Sloth Worktree — One Workspace Per Engagement 🦥

## Overview

Every Maycrest engagement gets its own isolated workspace. Client A's branch never touches
client B's checkout. Prefer the platform's native worktree tool; fall back to manual git
worktrees only when no native tool exists.

**Core principle:** Detect existing isolation first. Then native tools. Then git. Never fight the harness.

**Announce at start:** "Using sloth-worktree to set up an isolated workspace."

## Step 0: Detect Existing Isolation

**Before creating anything, check whether you're already isolated.**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside a submodule. Verify first:

```bash
# Returns a path → you're in a submodule, not a worktree. Treat as a normal repo.
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**If `GIT_DIR != GIT_COMMON` (and not a submodule):** already in a linked worktree. Skip to
Step 3. Do NOT nest another worktree. Report branch state — on a branch: "Already isolated at
`<path>` on `<name>`." Detached HEAD: "Already isolated at `<path>` (detached HEAD,
externally managed). Branch creation needed at finish time."

**If `GIT_DIR == GIT_COMMON` (or a submodule):** normal checkout. Has Corey already stated a
worktree preference? Honor it. Otherwise ask consent:

> "Set up an isolated worktree? It protects your current branch from changes."

If Corey declines, work in place and skip to Step 3.

## Step 1: Create the Workspace

**Two mechanisms — try them in this order.**

### 1a. Native Worktree Tools (preferred)

Do you already have a way to create a worktree — a tool named something like `EnterWorktree`
or `WorktreeCreate`, a `/worktree` command, or a `--worktree` flag? Use it and skip to Step 3.
Native tools handle placement, branch creation, and cleanup. Running `git worktree add` when a
native tool exists creates phantom state the harness can't see. Only continue to 1b if you
have no native tool.

### 1b. Git Worktree Fallback

**Directory selection** — explicit preference always beats observed state:

1. Corey's declared worktree directory, if stated — use it without asking.
2. Existing project-local dir: `ls -d .worktrees 2>/dev/null` (preferred), else `ls -d worktrees 2>/dev/null`. If both exist, `.worktrees` wins.
3. Existing global legacy dir: `~/.config/superpowers/worktrees/$(basename "$(git rev-parse --show-toplevel)")`.
4. No guidance: default to `.worktrees/` at project root.

**Safety (project-local only) — verify the dir is ignored before creating:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

If NOT ignored: add to `.gitignore`, commit, then proceed. This prevents accidentally
committing worktree contents. Global dirs need no verification.

**Create:**

```bash
git worktree add "$path" -b "$BRANCH_NAME"   # e.g. .worktrees/aos-booking-intake
cd "$path"
```

**Sandbox fallback:** if `git worktree add` fails with a permission error, tell Corey the
sandbox blocked creation and you're working in the current directory instead — then run setup
and baseline tests in place.

## Step 3: Project Setup

Auto-detect and run setup for the stack:

```bash
[ -f package.json ]     && npm install            # Node / Expo / Next.js
[ -f Cargo.toml ]       && cargo build            # Rust
[ -f requirements.txt ] && pip install -r requirements.txt
[ -f pyproject.toml ]   && poetry install
[ -f go.mod ]           && go mod download
```

## Step 4: Verify Clean Baseline

Run the project's tests so the workspace starts clean (`npm test` / `cargo test` / `pytest` / `go test ./...`).

**Tests fail:** report failures, ask whether to proceed or investigate.
**Tests pass:** report ready.

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <engagement-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Already in linked worktree | Skip creation (Step 0) |
| In a submodule | Treat as normal repo (Step 0 guard) |
| Native worktree tool available | Use it (Step 1a) |
| No native tool | Git fallback (Step 1b) |
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Corey's preference, then default `.worktrees/` |
| Global legacy path exists | Use it (backward compat) |
| Directory not ignored | Add to `.gitignore` + commit |
| Permission error on create | Sandbox fallback, work in place |
| Tests fail during baseline | Report + ask |
| No manifest file | Skip dependency install |

## Red Flags

**Never:**
- Create a worktree when Step 0 detects existing isolation
- Use `git worktree add` when a native tool exists — the #1 mistake; if you have it, use it
- Jump straight to Step 1b, skipping the native-tool check
- Create a project-local worktree without verifying it's ignored
- Skip baseline test verification
- Proceed with failing tests without asking

**Always:**
- Run Step 0 detection first
- Prefer native tools over the git fallback
- Follow directory priority: existing > global legacy > Corey's preference > default
- Verify the directory is ignored for project-local
- Auto-detect and run project setup
- Verify a clean test baseline

## Integration with the Maycrest roster

- Set up the worktree before executing a [sloth-blueprint](../sloth-blueprint/SKILL.md) plan or [sloth-build](../sloth-build/SKILL.md) run.
- Each engagement branch (e.g. `aos-booking-intake`) is the unit [sloth-ship](../sloth-ship/SKILL.md) merges, PRs, or discards at finish time.
- Hand the certified branch to `maycrest-ops:reality-checker` before client handoff.

---
*Adapted from the MIT-licensed [obra/superpowers](https://github.com/obra/superpowers) project (© 2025 Jesse Vincent). See [NOTICE](../../NOTICE).*
