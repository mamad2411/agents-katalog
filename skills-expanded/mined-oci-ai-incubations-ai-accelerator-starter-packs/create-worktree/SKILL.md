---
name: create-worktree
description: Use when needing an isolated git worktree for testing, parallel work, or deployment isolation. Triggers on "create a worktree", "isolated workspace", "worktree off current branch", or before integration tests that need branch isolation.
---

# Create Worktree

Creates a detached git worktree. Uses `--detach` to avoid the "already checked out" error that occurs when trying to check out the same branch in two worktrees.

## Step 1: Ask the User

Before creating the worktree, ask:

> Which base do you want for the worktree?
> 1. **Current branch** (`<show branch name>`) — for testing in-progress work
> 2. **Latest main** — for a clean baseline or independent work

If the user already specified (e.g., "worktree off main" or "worktree off current branch"), skip the question.

## Step 2: Create Worktree

### Off the current branch

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
WORKTREE_NAME="worktree-$(date +%s)"
WORKTREE_PATH="/tmp/${WORKTREE_NAME}"

git worktree add --detach "${WORKTREE_PATH}" HEAD

cd "${WORKTREE_PATH}"
echo "Working in: ${WORKTREE_PATH} (detached at ${CURRENT_BRANCH})"
```

### Off latest main

```bash
git fetch origin main
WORKTREE_NAME="worktree-$(date +%s)"
WORKTREE_PATH="/tmp/${WORKTREE_NAME}"

git worktree add --detach "${WORKTREE_PATH}" origin/main

cd "${WORKTREE_PATH}"
echo "Working in: ${WORKTREE_PATH} (detached at origin/main)"
```

## Step 3: Verify

Always confirm the worktree is based on the expected source:

```bash
REPO_ROOT=$(git -C "${WORKTREE_PATH}" rev-parse --show-toplevel 2>/dev/null || echo "<original-repo-path>")

echo "Worktree HEAD:    $(git -C ${WORKTREE_PATH} rev-parse HEAD)"
echo "Current branch:   $(git rev-parse HEAD)"
echo "Main branch:      $(git rev-parse main)"
```

- If based on current branch: worktree HEAD should match current branch HEAD and differ from main.
- If based on main: worktree HEAD should match main and differ from current branch HEAD (unless on main).

**Report the verification result to the user** — explicitly confirm which branch it's based on.

## Step 4: Change into the Worktree

After verification, **always `cd` into the worktree** so all subsequent commands run inside it:

```bash
cd "${WORKTREE_PATH}"
```

**Important:** Claude Code's shell state does not persist `cd` across tool calls — each Bash invocation resets to the project root. To work around this, **prefix every subsequent command with `cd "${WORKTREE_PATH}" &&`** or use absolute paths rooted at `${WORKTREE_PATH}`. For example:

```bash
cd "${WORKTREE_PATH}" && terraform init -backend=false
```

Confirm to the user that the working directory is now the worktree path and that all subsequent commands will target it.

## Cleanup

Before removing, **always check for uncommitted changes** in the worktree:

```bash
git -C "${WORKTREE_PATH}" status --short
```

- If output is empty: safe to remove.
- If there are uncommitted changes: **warn the user** and ask whether to commit, stash, or discard before proceeding. Never silently destroy uncommitted work.

Then remove:

```bash
git worktree remove "${WORKTREE_PATH}" --force 2>/dev/null
```

## Why --detach?

Git prevents two worktrees from checking out the same branch. Without `--detach`, you get:

```
fatal: 'feature/my-branch' is already checked out at '/path/to/repo'
```

`--detach` creates the worktree at the same commit without locking the branch name. The main working directory keeps its branch reference undisturbed.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `git worktree add path branch` without `--detach` | Use `--detach` to avoid "already checked out" |
| Assuming the user wants current branch | Always ask — they may want main for a clean baseline |
| Forgetting to `cd /tmp` before removing worktree | Must exit the worktree directory before `git worktree remove` |
| Not verifying the worktree commit matches the source | Run the verification step and report to the user |
| Staying in the original repo after creating worktree | Always `cd` into the worktree so subsequent work happens there |
