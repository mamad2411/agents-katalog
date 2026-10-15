---
name: isolate
description: Use when starting task work that needs branch isolation, before planning or coding — creates a worktree branching from current remote main with freshness verification and project setup
---

# Isolate

Create a worktree branched from the latest `origin/main` so task work never starts on stale code.

**Announce:** "Setting up an isolated worktree for this task."

## Inputs

- **Branch name:** from `/orient` Step 1 (e.g., `feat/auth`, `fix/login-crash`). Ask if not provided.
- **Base ref:** `origin/main` (default). Different base only when explicitly stacking on another feature branch.

## Already in a Worktree?

If the session CWD is already inside a linked worktree (not the primary), freshen the branch instead of creating a new one:

```bash
WORKTREE="<absolute-path-to-current-worktree>"
git -C "$WORKTREE" fetch origin main
git -C "$WORKTREE" merge origin/main
```

If conflicts arise, stop and present them to the user. Do not auto-resolve.

After freshening, skip ahead to **Baseline test**.

## Step 1: Select directory

| Priority | Check | Action |
|----------|-------|--------|
| 1 | `.worktrees/` exists | Use it |
| 2 | `worktrees/` exists | Use it |
| 3 | Both exist | `.worktrees/` wins |
| 4 | CLAUDE.md specifies | Follow preference |
| 5 | None found | Ask user (`.worktrees/` recommended) |

## Step 2: Verify gitignored

```bash
git check-ignore -q .worktrees
```

If NOT ignored, fix before proceeding:

```bash
echo ".worktrees" >> .gitignore
git add .gitignore
git commit -m "chore: gitignore worktree directory"
```

## Step 3: Fetch and create

A worktree branched from a stale local `main` means baked-in merge conflicts. Always fetch first, always branch from `origin/main`.

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
WORKTREE_DIR="$REPO_ROOT/.worktrees/<name>"

git fetch origin main
git worktree add "$WORKTREE_DIR" -b <prefix>/<name> origin/main
```

Claude Code: optionally call `EnterWorktree({path})` to move session CWD into the new worktree.

## Step 4: Install dependencies

Auto-detect from manifest files:

| File | Command |
|------|---------|
| `pnpm-lock.yaml` | `pnpm install` |
| `yarn.lock` | `yarn install` |
| `package-lock.json` | `npm install` |
| `package.json` (no lockfile) | Ask before installing |
| `Cargo.toml` | `cargo build` |
| `requirements.txt` | `pip install -r requirements.txt` |
| `pyproject.toml` | `poetry install` |
| `go.mod` | `go mod download` |

Run from the worktree path: `pnpm --dir "$WORKTREE_DIR" install`

## Step 5: Baseline test

Run the project's test suite. If tests fail, report failures and ask whether to proceed. Do not silently continue.

## Report

```
Worktree ready at <absolute-path>
Branch: <prefix>/<name> (from origin/main @ <short-sha>)
Tests: <N> passing
```

## Path Discipline

`cd` does not persist between Claude Code Bash calls. Use absolute paths for all file operations and `git -C <abs-path>` for git commands.

## Integration

**Called by:** /task (Step 2), /brainstorming, /build
**Pairs with:** /ship (cleans up worktree after work is done)
