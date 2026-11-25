---
name: closing-linear-issue
description: >-
  Use when the user says "close issue [ID]", "close [ID]", "finish closeout",
  or when a Linear issue already has a review-ready PR and this repository
  needs the merge, close, and cleanup phase
argument-hint: "[issue-id-or-pr]"
---

# Closing Linear Issues

## Overview

Finish the last mile after review once the PR has already been merged elsewhere: close linked issues and clean up branches and worktrees safely.

## When to Use

- A PR already exists for the issue.
- Review is complete and the issue is ready to close.
- Do not use for coding work or PR creation.

## Quick Reference

| Step | Requirement |
|---|---|
| 1 | Locate the PR and verify it is already merged |
| 2 | Stop if the PR is not merged yet |
| 3 | Read the merge result and closing metadata |
| 4 | Move linked issues to `Done` |
| 5 | Remove worktree and branches safely |

## Implementation

**Tool contract:** use the available Linear MCP tools needed for issue and comment operations in this workflow, plus `gh pr list`, `gh pr view`, `gh pr checks`, `git fetch`, `git worktree remove`, `git branch -D`, `git push origin --delete`, `git checkout`, and `git pull`. Retry once on failure, then stop and report the exact step.

**Readiness rules:**

- If no PR exists, stop and direct the user back to `raising-linear-pr`.
- If the PR is not already merged, stop and direct the user back to GitHub or `raising-linear-pr`.
- If the worktree is dirty at the start of this phase, stop immediately and direct the user back to `implementing-linear-issue`.
- If required checks fail, stop and report them.
- If the PR test plan is incomplete, stop and report the gap.
- When refreshing local `main`, stop and report if local `main` is dirty or has local-only commits not on `origin/main`.

**Merge and close rules:**

- This skill does not merge the PR or rewrite the reviewed branch.
- The PR must already be merged before this skill does any close or cleanup work.
- Read the merge result from the already-merged PR and capture the merge commit SHA when available.
- Move the primary issue and any linked `Fixes` or `Closes` issues to `Done`.
- Add a closing Linear comment with the PR URL and merge SHA.

**Cleanup rules:**

- Treat already-removed worktrees or branches as success.
- Keep the pre-merge safety rule strict: do not merge from a dirty worktree.
- After the PR is merged and the remote branch is deleted, treat the local feature worktree as disposable.
- During post-merge cleanup, auto-remove ignored and untracked local artifacts before removing the worktree.
- If tracked modifications still exist during post-merge cleanup, stop and report them explicitly instead of discarding them.
- Clean up the worktree, local branch, remote branch, and then refresh local `main`.
- Refreshing local `main` means fetching `origin/main`, verifying local `main` is clean and has no local-only commits, then making local `main` match `origin/main` exactly.
- If local `main` has diverged from `origin/main`, stop and report it instead of reconciling automatically.

**Boundary rules:**

- No plan mode.
- No new code changes.
- No new PR creation.
- No local merge or rebase ownership.
- Never merge the PR from this skill.

## Common Mistakes

- Trying to close the issue before a PR exists.
- Trying to run this skill before the PR is already merged.
- Treating this skill as the merge step instead of a post-merge close/cleanup step.
- Proceeding with merge or cleanup from a dirty worktree.
- Ignoring required checks or an incomplete PR test plan.
- Silently discarding tracked changes during post-merge cleanup.
- Silently rewriting or reconciling a diverged local `main`.
- Re-running the whole implementation flow instead of just merging and closing.
