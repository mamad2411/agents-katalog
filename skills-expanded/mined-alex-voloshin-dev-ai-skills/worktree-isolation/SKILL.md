---
name: worktree-isolation
description: Git worktree branch isolation for feature development and bugfixes — branch naming, worktree setup, branch verification, and safe cleanup. Use when developing features or fixing bugs in isolated branches via git worktree.
user-invocable: false
---

# Worktree Isolation

Procedure for isolating feature and bugfix work on dedicated branches using git worktree. Prevents accidental commits to the wrong branch and keeps the main working tree clean.

## Branch Naming

Derive the branch name from the task context. Use the git-conventions branch naming format:

| Source | Branch name |
|---|---|
| Bug ticket with ID | `fix/<ID>-<short-description>` — e.g. `fix/BUG-044-null-payment-response` |
| Feature PRD | `feature/<feature-name>` — use the feature folder name or the title from the PRD, kebab-cased |
| Feature folder | `feature/<folder-name>` — match the directory that holds the feature spec |
| Hotfix | `hotfix/<ID>-<short-description>` |
| Refactor | `refactor/<short-description>` |

Rules:
- Always lowercase, hyphen-separated
- Include the ticket/bug ID when one exists
- Keep the description portion under 40 characters
- Never use generic names like `dev`, `temp`, `wip`, or `my-branch`

## Setup Procedure

Execute these steps in order before writing any code:

### 1. Determine Branch Name

```
BRANCH_NAME = derive from task context (see table above)
```

### 2. Check if Branch Already Exists

```bash
# Check local branches
git branch --list "$BRANCH_NAME"

# Check remote branches
git branch -r --list "origin/$BRANCH_NAME"
```

- If the branch exists locally — use it
- If the branch exists only on remote — fetch and track it
- If the branch does not exist anywhere — create it from the current main branch

### 3. Create or Enter the Worktree

```bash
# If branch does not exist — create worktree with new branch
git worktree add ../worktree-$BRANCH_NAME -b "$BRANCH_NAME"

# If branch already exists locally
git worktree add ../worktree-$BRANCH_NAME "$BRANCH_NAME"

# If branch exists only on remote
git fetch origin "$BRANCH_NAME"
git worktree add ../worktree-$BRANCH_NAME "$BRANCH_NAME"
```

The worktree path sits alongside the main repo directory. Adjust the path if the environment requires a different location.

### 4. Verify Branch

After entering the worktree, always confirm:

```bash
git branch --show-current
```

**Hard rule**: the output MUST match `$BRANCH_NAME`. If it does not — stop and fix before writing any code. Do not proceed on the wrong branch.

## During Development

### Branch Guard

Before every commit, verify the current branch:

```bash
current=$(git branch --show-current)
if [ "$current" != "$BRANCH_NAME" ]; then
  echo "ERROR: on branch '$current', expected '$BRANCH_NAME'" >&2
  exit 1
fi
```

Never switch branches inside the worktree. The worktree is locked to its branch. If you need a different branch, create a separate worktree.

### Commit Rules

- Commit only to the designated branch
- Follow the project's commit message conventions
- Do not merge main into the feature branch inside the worktree — rebase if needed

## Cleanup

After the feature is merged or the work is complete:

```bash
# From the main working tree (not from inside the worktree)
git worktree remove ../worktree-$BRANCH_NAME

# If the branch was merged, delete it
git branch -d "$BRANCH_NAME"
```

Do not delete the worktree while it has uncommitted changes. Commit or stash first.

## Error Recovery

| Problem | Action |
|---|---|
| Worktree path already exists | Check if it belongs to this branch. If yes, reuse. If stale, run `git worktree prune` then retry |
| Branch exists but worktree does not | Create worktree pointing to the existing branch |
| Detached HEAD in worktree | Run `git checkout "$BRANCH_NAME"` inside the worktree |
| Worktree locked | Run `git worktree unlock ../worktree-$BRANCH_NAME` then retry |

## Integration

- **Used by**: `feature-dev` skill, `bugfix` skill
- **Follows**: `git-conventions` rule (branch naming, commit messages)
