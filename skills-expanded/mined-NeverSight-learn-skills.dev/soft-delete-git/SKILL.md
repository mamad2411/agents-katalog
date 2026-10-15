---
name: soft-delete-git
description: Safely soft-delete a merged Git branch by switching to the default branch, pulling latest, and running `git branch -d`. Use when the user wants to clean up, remove, or delete a local branch after merging, or says "soft delete this branch" / "delete my branch". Escalates to the user instead of force-deleting if the branch is unmerged, except squash-merged PRs verified via `gh`.
---

# Soft Delete Git Branch Workflow

## Invocation behavior

When this skill is invoked without an explicit branch name, target the currently checked-out branch. Invocation of the skill is authorization to begin the workflow immediately: inspect the working tree and determine the current branch without asking which branch to delete.

Only ask the user how to proceed when:
- The working tree is dirty.
- The current branch is the default branch.
- Safe deletion fails and force deletion would require confirmation.

Do not ask the user to name or confirm the current branch before starting.

## Steps:

1. **Check for uncommitted changes**
   ```bash
   git status --porcelain
   ```
   If the working tree is dirty, stop and ask the user how to proceed (commit, stash, or discard) before switching branches.

2. **Get current branch name**
   ```bash
   git branch --show-current
   ```
   If already on the default branch, there is no branch to delete — stop and ask the user which branch they meant.

3. **Determine the default branch**
   ```bash
   git symbolic-ref --short refs/remotes/origin/HEAD
   ```
   This returns e.g. `origin/main` — the default branch is the part after `origin/`. If the ref is unset, fall back to `main`.

4. **Check out the default branch**
   ```bash
   git checkout <default-branch>
   ```

5. **Pull latest changes**
   ```bash
   git pull
   ```

6. **Soft delete the previous branch**
   ```bash
   git branch -d <branch-name>
   ```

7. **If soft delete fails, check for a squash merge**

   `git branch -d` fails for branches merged via GitHub's "Squash and merge", because the branch tip is never an ancestor of the default branch. Check whether the branch's PR was actually merged:
   ```bash
   gh pr view <branch-name> --json state,mergedAt
   ```
   - If the PR state is `MERGED`, confirm with the user, then delete with `git branch -D <branch-name>`.
   - Otherwise, escalate to the user rather than force-deleting.

## Notes:
- Uses lowercase `-d` for soft delete (safe delete that prevents deletion of unmerged branches)
- Never use uppercase `-D` (hard delete) except in the verified-squash-merge case above, and only after confirming with the user
- The workflow ensures the default branch is up to date before attempting the delete
