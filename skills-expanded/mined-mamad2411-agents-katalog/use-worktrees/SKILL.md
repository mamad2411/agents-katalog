---
name: use-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback
---

# Using Git Worktrees

## Overview

Ensure work happens in an isolated workspace. Prefer your platform's native worktree tools. Fall back to manual git worktrees only when no native tool is available.

**Core principle:** Identify the work lifecycle and pin its base first. Then
detect existing isolation, use native tools, or fall back to git. Never let the
caller's current `HEAD` choose a new branch's base implicitly.

**Announce at start:** "I'm using the use-worktrees skill to set up an isolated workspace."

## Lifecycle Gate (before Step 0)

Before inspecting the checkout, establish four values:

- `WORKSPACE_ID` — stable identity for this project, feature, or plan;
- `WORK_MODE` — `new` or `continue`;
- `BASE_BRANCH` — the branch this work must eventually merge into; and
- `BASE_SHA` — the verified commit from which a new worktree must fork.

The plan or calling workflow should provide these values. For new work with no
declared base, resolve the repository's configured default branch and confirm it
with your human partner before creating anything. Then resolve the commit:

```bash
BASE_SHA=$(git rev-parse "${BASE_BRANCH}^{commit}")
```

Record `WORKSPACE_ID`, `BASE_BRANCH`, and `BASE_SHA` in the plan ledger or other
durable workflow state. A branch name alone can move; a SHA alone does not
preserve merge intent.

`WORK_MODE=continue` is an explicit continuation declaration. It must name the
expected existing work branch or detached workspace. Never infer continuation
merely because the current directory is a linked worktree.

## Step 0: Detect Existing Isolation

**Before creating anything, check if you are already in an isolated workspace.**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside git submodules. Before concluding "already in a worktree," verify you are not in a submodule:

```bash
# If this returns a path, you're in a submodule, not a worktree — treat as normal repo
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**If `GIT_DIR != GIT_COMMON` (and not a submodule):** You are already in a
linked worktree. Reuse it only when `WORK_MODE=continue` and its branch/workspace
matches `WORKSPACE_ID`'s recorded state. Verify that `BASE_SHA` is the recorded
base (or an ancestor when the base branch has advanced).

For `WORK_MODE=new`, or when the recorded identity does not match, this is an
unrelated linked worktree. Do not reuse it and do not branch from its `HEAD`.
Create the new workspace from the repository's main checkout using the pinned
`BASE_SHA` in Step 1.

Report with branch state:
- On a branch: "Already in isolated workspace at `<path>` on branch `<name>`."
- Detached HEAD: "Already in isolated workspace at `<path>` (detached HEAD, externally managed). Branch creation needed at finish time."

**If `GIT_DIR == GIT_COMMON` (or in a submodule):** You are in a normal repo checkout.

Has the user already indicated their worktree preference in your instructions? If not, ask for consent before creating a worktree:

> "Would you like me to set up an isolated worktree? It protects your current branch from changes."

Honor any existing declared preference without asking. If the user declines consent, work in place and skip to Step 2.

## Step 1: Create Isolated Workspace

**Choose the branch name first, then try the two creation mechanisms in order.**

### 1a. Branch Name

A native worktree tool and the git fallback both need the work branch name.
Derive it before creating either workspace.

For repos on any other forge, use whatever convention that repo's `CONTRIBUTING`
or `CODEOWNERS` documents; if there is none, `feature/<slug>` is a safe default.

### 1b. Native Worktree Tools (preferred)

The user has asked for an isolated workspace (Step 0 consent). Do you already
have a way to create a worktree? It might be a tool with a name like
`EnterWorktree`, `WorktreeCreate`, a `/worktree` command, or a `--worktree`
flag. **In this repo, use `moe jig worktree create <branch> [--base <ref>]`** —
it handles placement in `.moe/worktrees/`, gitignore, and lineage verification.
If you have a native tool, use it and skip to Step 2.

Native tools handle directory placement, branch creation, and cleanup
automatically, but they do not get to choose lineage. Pass `BASE_SHA` when the
tool accepts a base. If it only branches from the caller's `HEAD`, invoke it
only from a checkout whose `HEAD` equals `BASE_SHA`, then verify the created
workspace's merge base. If neither is possible, do not silently stack the new
work on the current branch; use the git fallback or report that the harness
cannot create the requested workspace safely.

Only proceed to Step 1c if you have no usable native worktree tool available.

### 1c. Git Worktree Fallback

**Only use this if Step 1b does not apply** — you have no native worktree tool available. Create a worktree manually using git.

#### Directory Selection

Resolve the primary checkout from the common Git directory so directory
selection does not happen inside an unrelated linked worktree:

```bash
PRIMARY_ROOT=$(git -C "$GIT_COMMON/.." rev-parse --show-toplevel)
```

Follow this priority order under `PRIMARY_ROOT`. Explicit user preference
always beats observed filesystem state.

1. **Check your instructions for a declared worktree directory preference.** If the user has already specified one, use it without asking.

2. **Check for an existing project-local worktree directory:**
   ```bash
   ls -d "$PRIMARY_ROOT/.moe/worktrees" 2>/dev/null # Preferred
   ls -d "$PRIMARY_ROOT/.worktrees" 2>/dev/null     # Legacy
   ls -d "$PRIMARY_ROOT/worktrees" 2>/dev/null      # Alternative
   ```
   If found, use the first match. `.moe/worktrees` wins over `.worktrees` wins over `worktrees`.

3. **If there is no other guidance available**, default to `.moe/worktrees/` at the project root.

#### Safety Verification (project-local directories only)

**MUST verify directory is ignored before creating worktree:**

```bash
git -C "$PRIMARY_ROOT" check-ignore -q .moe/worktrees 2>/dev/null ||
  git -C "$PRIMARY_ROOT" check-ignore -q .worktrees 2>/dev/null ||
  git -C "$PRIMARY_ROOT" check-ignore -q worktrees 2>/dev/null
```

**If NOT ignored:** Add to .gitignore, commit the change, then proceed.

**Why critical:** Prevents accidentally committing worktree contents to repository.

#### Create the Worktree

```bash
# Determine path based on chosen location
path="$LOCATION/$BRANCH_NAME"

git -C "$PRIMARY_ROOT" worktree add "$path" -b "$BRANCH_NAME" "$BASE_SHA"
cd "$path"

test "$(git merge-base HEAD "$BASE_SHA")" = "$BASE_SHA"
```

**Sandbox fallback:** If `git worktree add` fails with a permission error (sandbox denial), tell the user the sandbox blocked worktree creation and you're working in the current directory instead. Then run setup and baseline tests in place.

### 1d. One Worktree Per Parallel Worker

When dispatching parallel implementer subagents per the worktree gate
(`dispatch-agents`, "The gate"), each concurrent worker gets its
OWN linked worktree. Two workers writing into one checkout defeats the
isolation the gate is built on and reintroduces the exact `(conflicts)`
hazard the parallel-implementation ban was rooted in.

For each worker, follow Step 1b first — use the harness's native worktree tool
when one is available, per the "never fight the harness" rule. Only fall back
to `git worktree add` (Step 1c) when no native tool is offered. Whichever path
you take, create the worktree BEFORE dispatch: the worker's brief hands it a
concrete path to `cd` into, not an instruction to make one for itself.

Each parallel worker's worktree branches from ONE recorded base SHA shared
across the wave (see `sdd` "Wave grouping" and
`dispatch-agents` "The divergent-tree rule"). A worker branched
from a stale base will cite the same file coordinates as its siblings but
read different content there. Recording the base once, before the wave
dispatches, is the safeguard.

Create every worktree first, then validate the complete set before dispatching
any worker. **In this repo, use `moe jig worktree create` per worker and
`moe jig worktree validate <path1> <path2> ...` to check the set.** Without
jig, verify manually:

```bash
git -C "$worker_cwd" rev-parse --path-format=absolute --git-dir
git -C "$worker_cwd" rev-parse --path-format=absolute --git-common-dir
```

For every worker, the resolved Git directory must differ from the resolved
common directory; that proves the cwd is a linked worktree rather than the main
checkout. The resolved paths must also be pairwise-unique linked Git directories
across the wave; comparing cwd strings is not enough because two aliases or
symlinks can name the same checkout.

Parallel implementation has exactly two rungs: (1) worktree-isolated parallel
dispatch after the complete set passes validation, then (2) sequential dispatch
of the entire wave. If native creation, `git worktree add`, or any validation
command fails for even one worker, use rung two from the controller's current,
validated tree. Do not dispatch the valid subset in parallel, and never fall
back to parallel dispatch without isolation.

## Step 2: Project Setup

Auto-detect and run appropriate setup:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## Step 3: Verify Clean Baseline

Run tests to ensure workspace starts clean:

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**If tests fail:** Report failures, ask whether to proceed or investigate.

**If tests pass:** Report ready.

### Report

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| New work | Record `WORKSPACE_ID`, `BASE_BRANCH`, and `BASE_SHA` before inspecting isolation |
| Matching linked worktree + explicit continuation | Reuse it after verifying recorded identity and base |
| Unrelated linked worktree | Never reuse its branch or implicit `HEAD` |
| In a submodule | Treat as normal repo (Step 0 guard) |
| Branch name needed (any path) | Derive per Step 1a |
| Native worktree tool available | Use it with the pinned base (Step 1b) |
| No usable native tool | Git worktree fallback (Step 1c) |
| Parallel worker dispatch | Validate pairwise-unique linked Git dirs for every worker (Step 1d) |
| Any parallel worktree setup failure | Dispatch the entire wave sequentially (Step 1d) |
| `.moe/worktrees/` exists | Use it (verify ignored) |
| `.worktrees/` exists | Use it — legacy (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Multiple exist | `.moe/worktrees/` wins over `.worktrees/` wins over `worktrees/` |
| None exists | Check instruction file, then default `.moe/worktrees/` |
| Directory not ignored | Add to .gitignore + commit |
| Permission error on create | Sandbox fallback, work in place |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'm obviously not in a worktree — no need to check" | Run Step 0. Harness-created isolation and submodules both fool eyeballing; the detection commands settle it. |
| "`git worktree add` is quicker than hunting for a native tool" | A native tool (e.g. `EnterWorktree`) owns placement, branching, and cleanup. Bypassing it is the #1 mistake — it creates phantom state your harness can't see or manage. |
| "The worktree directory is surely ignored already" | Run `git check-ignore`. An unignored worktree directory commits the whole tree into the repo. |
| "Any directory name works" | Explicit instructions beat an existing project-local directory, which beats the `.moe/worktrees/` default. |
| "The workspace is fresh — baseline tests can wait" | A dirty baseline makes every later failure ambiguous. Run the tests now; proceeding past failures is your human partner's call. |
