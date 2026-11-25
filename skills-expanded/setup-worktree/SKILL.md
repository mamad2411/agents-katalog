---
name: setup-worktree
description: Set up a git worktree for a feature branch in a new web session. Use when user says "setup worktree", "checkout branch", "start feature", or provides a branch name or issue number at the start of a session.
---

# Setup Worktree

Configure the current session to work on a specific feature branch. Designed for web-initiated sessions via `claude remote-control --spawn worktree`, but works in any context.

## Instructions

### Step 1: Parse the Input

The argument is passed after the skill invocation (e.g., `/setup-worktree 155` or `/setup-worktree 155-my-feature`).

- **Digits only** (e.g., `155`) → treat as a GitHub issue number
- **String with hyphens** (e.g., `155-my-feature`) → treat as a full branch name
- **No argument** → ask the user for an issue number or branch name

### Step 2: Fetch Latest

```bash
git fetch origin --prune
```

### Step 3: Resolve the Branch

**If input is a GitHub issue number:**

1. Search for an existing branch matching the pattern `{number}-*`:

   ```bash
   # Check remote
   git branch -r --list "origin/{number}-*"
   # Check local
   git branch --list "{number}-*"
   ```

2. **If a matching branch is found** → use it (prefer remote if local doesn't exist yet).

3. **If no matching branch exists** → create one:
   - Fetch the issue details using the available GitHub tools (owner, repo, issue_number). Extract the `title` from the result.
   - Slugify: lowercase, replace spaces and special characters with hyphens, remove consecutive hyphens, trim trailing hyphens, truncate to reasonable length
   - Branch name: `{number}-{slug}` (e.g., `155-add-user-dashboard`)
   - Create from main:
     ```bash
     git checkout -b {branch} origin/main
     ```
   - Do NOT push automatically. Tell the user: "Branch `{branch}` created locally. Push with `git push -u origin {branch}` when ready."

**If input is a full branch name:**

1. Check if it exists remotely or locally.
2. **If found** → proceed to checkout.
3. **If not found** → show similar branches and stop:
   ```bash
   git branch -r --list "origin/*{partial}*" | head -10
   ```

### Step 4: Check for Worktree Conflicts

Before checking out, verify the branch isn't already active in another worktree:

```bash
git worktree list --porcelain
```

Look for `branch refs/heads/{branch}` in the output.

**If the branch is checked out in another worktree** → stop and tell the user:
> "Branch `{branch}` is already checked out in worktree at `{path}`. What would you like to do?"

Do NOT attempt to resolve this automatically.

### Step 5: Check Out the Branch

**If the branch exists locally:**

```bash
git checkout {branch}
git pull --ff-only || echo "Pull skipped (no upstream or diverged)."
```

**If the branch only exists on remote:**

```bash
git checkout -b {branch} origin/{branch}
```

### Step 6: Confirm Setup

Report back with:

- Branch name and working directory
- Latest commit: `git log --oneline -1`
- Check if a plan exists at `plans/{branch}/plan.md` — if so, mention it so the user knows there's prior context

## Critical Rules

- **Stop on worktree conflicts** — never force-checkout or detach other worktrees. Ask the user.
- **Never force-checkout over uncommitted changes** — if `git status` shows changes, warn the user.
- **Branch naming convention is `{issue-number}-{slug}`** — lowercase, hyphen-separated, derived from the issue title. Examples: `126-add-import-retry-policy`, `148-allow-custom-page-size-in-the-datatable`.
- **Always branch from `main`** when creating new branches.
- **Do not push automatically** — the user decides when to push. Inform them the branch is local-only after creation.
