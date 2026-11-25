---
name: using-jj-workspaces
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated jj workspaces with safety verification
---

# Using jj Workspaces

## Overview

jj workspaces create isolated working copies sharing the same repository. Work on multiple changes simultaneously without affecting the original working copy.

**Core principle:** Safety verification + clean baseline = reliable isolation.

**Announce at start:** "I'm setting up an isolated jj workspace."

## Critical Safety Rules

**jj tracks everything in the working copy.** If `.workspaces/` isn't in `.gitignore`, workspace files pollute the parent workspace's commit.

**Always ensure both `.workspaces/` and `.jj-*` are in `.gitignore` before creating workspaces.**

The `.jj-*` pattern catches conflict marker files (like `.jj-do-not-resolve-this-conflict`) that jj creates during conflict resolution. If these get into git's index and are then removed from disk, Nix flake evaluation will fail looking for nonexistent files.

## Workflow Checklist

### 1. Ensure Patterns are Ignored

Workspaces live in `.workspaces/` at the repo root. jj also creates `.jj-*` conflict marker files.

- [ ] Check if `.workspaces/` in `.gitignore`: `grep -q ".workspaces" .gitignore`
- [ ] Check if `.jj-*` in `.gitignore`: `grep -q ".jj-" .gitignore`
- [ ] If not, add them: `echo -e ".workspaces/\n.jj-*" >> .gitignore`
- [ ] If files already tracked: `jj file untrack ".workspaces/**" ".jj-*"`

### 2. Create Workspace

```bash
# Create parent directory if needed (jj won't create it)
mkdir -p .workspaces

jj workspace add .workspaces/<feature-name> --name <feature-name>

# Example
jj workspace add .workspaces/auth --name auth
```

### 3. Enter and Initialize

```bash
cd <workspace-path>

# Once you've entered the workspace, you're working with a new empty revision,
# so describe your intent as you would normally
jj desc -m "WIP: <description of feature>"
```

### 4. Run Project Setup

Auto-detect and run appropriate setup:

```bash
# Nix/direnv (usually auto-activates)
[ -f flake.nix ] && direnv allow

# Go
[ -f go.mod ] && go mod download

# Node.js
[ -f package.json ] && npm install

# Rust
[ -f Cargo.toml ] && cargo build

# Python (use uv, never pip)
[ -f pyproject.toml ] && uv sync
```

### 5. Verify Clean Baseline

Run tests to confirm workspace starts clean:

```bash
# Use project-appropriate command
go test ./...
npm test
cargo test
uv run pytest
```

- **Tests pass**: Report ready, proceed with work
- **Tests fail**: Report failures, **ask user** whether to proceed or investigate

### 6. Report Ready

```
Workspace ready at <full-path>
Workspace name: <name>
Tests: <N> passing
Ready to implement <feature>
```

## Command Reference

| Task | Command |
|------|---------|
| Create workspace | `jj workspace add <path> --name <name>` |
| Create at specific revision | `jj workspace add <path> --name <name> -r <rev>` |
| List workspaces | `jj workspace list` |
| Forget workspace | `jj workspace forget <name>` |
| Fix stale workspace | `jj workspace update-stale` |
| Get repo root | `jj workspace root` |

## Completing Work and Cleanup

When work is done, bring changes to the mainline and remove the workspace.

### 1. Finalize Your Changes (from workspace)

```bash
# Verify work is complete
jj st
jj diff

# Ensure meaningful description
jj desc -m "Final description of changes"
```

**IMPORTANT: Avoid interactive commands in automated contexts.** Commands like `jj squash` without explicit revision targets can open an interactive editor, blocking background agents indefinitely. If you need to combine commits:

```bash
# WRONG - may prompt interactively
jj squash -m "message"

# RIGHT - explicit non-interactive squash into parent
jj squash --into @- -m "message"

# SIMPLER - just describe the current commit (usually sufficient)
jj desc -m "Final description"
```

For workspace agents, prefer `jj desc` over `jj squash` unless you explicitly have multiple commits to combine.

### 2. Integrate to Mainline

Changes are already in the shared repo, but you need to position them correctly:

```bash
# Return to main workspace
cd <original-root>

# Check where your workspace changes landed
jj log

# If changes need rebasing onto main:
jj rebase -r <workspace-change> -d main

# Move main bookmark forward to include your work
jj bookmark set main -r <your-final-change>
```

### 3. Remove the Workspace

```bash
# Forget the workspace record
jj workspace forget <workspace-name>

# Remove directory (verify path first!)
rm -rf <workspace-path>
```

**Before `rm -rf`**: Verify the path is actually your workspace directory. Never blindly delete.

### 4. Post-Integration Cleanup

After merging multiple workspaces or resolving conflicts:

```bash
# Clean stale jj artifacts from git's index
# NOTE: jj uses git as its storage backend. During conflict resolution,
# jj creates .jj-* marker files that can end up in git's index. When jj
# removes them from disk, git doesn't know - leaving "ghost" entries.
# This is one of the few cases where using git commands in a jj workflow
# is correct - we're fixing git's index, not managing version control.
git status --porcelain | grep -E "^\?\?.*\.jj-|^[AD].*\.jj-" && \
  git rm --cached .jj-* 2>/dev/null; \
  git reset HEAD .jj-* 2>/dev/null

# Verify Nix environment still works (if using nix-direnv)
direnv allow
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `.workspaces/` not in gitignore | Add it before creating workspace |
| `.jj-*` not in gitignore | Add it - conflict markers can break Nix flakes |
| Stale `.jj-*` in git index | `git rm --cached .jj-*` after conflict resolution |
| Working on parent revision | Make sure your `CWD` is the workspace directory |
| Workspace shows "stale" | Run `jj workspace update-stale` |
| Cryptic workspace names | Always use `--name <descriptive-name>` |
| Using pip for Python | Use `uv sync` instead |
| Deleting workspace without integrating | Rebase/squash and move bookmarks before forget/rm |
| Using `jj squash` in background agents | Use `jj desc -m "msg"` instead - squash can prompt interactively |
| Using `-i` flags (interactive mode) | Never use `jj` with interactive flags in automated contexts |

## Example Workflow

```
You: I'm setting up an isolated jj workspace.

[Check .workspaces/ - exists]
[Verify .workspaces/ and .jj-* are in .gitignore - confirmed]
[Create workspace: jj workspace add .workspaces/auth --name auth]
[cd .workspaces/auth]
[jj desc -m "WIP: implement auth feature"]
[Run npm install]
[Run npm test - 47 passing]

Workspace ready at /home/dev/myproject/.workspaces/auth
Workspace name: auth
Tests: 47 passing
Ready to implement auth feature
```

## Red Flags

**Never:**
- Create workspace without verifying `.workspaces/` and `.jj-*` are in `.gitignore`
- Skip baseline test verification
- Proceed with failing tests without asking
- Use `git worktree` commands - use `jj workspace` instead
- Use interactive jj commands in automated contexts

**Always:**
- Verify ignore patterns before workspace creation
- Auto-detect and run project setup
- Verify clean test baseline
- Use `--name` for descriptive workspace names

## Parallel Workspaces and Merge Conflicts

When running multiple workspaces in parallel, anticipate which files multiple streams will touch.

**Before starting parallel work:**
- Identify "hot" files that multiple streams need to modify
- Consider having one stream "own" the integration file, with others adding isolated modules
- Design changes to minimize overlap (new files > modifying shared files)

**When conflicts occur:**
- jj creates `.jj-do-not-resolve-this-conflict` marker files
- Resolve conflicts in the merged working copy
- After resolution, clean git index: `git status --porcelain | grep jj`

## Interactive Command Warning

**Background agents and automated scripts must avoid interactive jj commands.** These will hang indefinitely waiting for user input:

| Command | Problem | Alternative |
|---------|---------|-------------|
| `jj squash` (no args) | May open editor | `jj desc -m "msg"` or `jj squash --into @- -m "msg"` |
| `jj split` | Always interactive | Don't use in automation |
| `jj resolve` | Opens merge tool | Use manual conflict resolution |
| Any command with `--edit` | Opens editor | Use `-m "message"` instead |

## Integration

**Called by:**
- **brainstorming** (Phase 4) - REQUIRED when design is approved and implementation follows
- **subagent-driven-development** - REQUIRED before executing any tasks
- **executing-plans** - REQUIRED before executing any tasks
- Any skill needing isolated workspace

**Pairs with:**
- **finishing-a-development-branch** - REQUIRED for cleanup after work complete
