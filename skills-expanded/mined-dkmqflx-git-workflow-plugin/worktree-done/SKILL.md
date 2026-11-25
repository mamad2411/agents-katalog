---
name: worktree-done
description: Remove the current git worktree, switch the main checkout to the base branch, and delete the feature branch. Use when the user has finished work started with the worktree skill (or `/worktree`) and wants to clean up — phrases like "워크트리 정리해줘", "워크트리 삭제해줘", "clean up this worktree", "remove worktree", "/worktree-done". Do NOT use from the main checkout (not a worktree) — that is the branch-done skill.
license: MIT
metadata:
  author: dkmqflx
  version: "1.0.0"
---

# Worktree Done

Remove the current git worktree, switch the main checkout to the base branch, and delete the feature branch.

Use this when finishing work that was started with the `worktree` skill (or `/worktree`).

## When to apply

Cleaning up after work done **inside a worktree**. **Do not apply** from the main checkout — that is `branch-done`.

## Steps

1. Verify the current directory is inside a **worktree** (not the main checkout).
   - Compare `git rev-parse --git-dir` and `git rev-parse --git-common-dir`. If they are equal, this is the main checkout — stop and tell the user to use the `branch-done` skill instead.
2. Record the current worktree path (`git rev-parse --show-toplevel`) and current branch name (`git rev-parse --abbrev-ref HEAD`).
3. Determine the base branch:
   - Try `git symbolic-ref refs/remotes/origin/HEAD` and strip the `refs/remotes/origin/` prefix.
   - If that fails, use the first of `dev`, `main`, `master` that exists locally (`git show-ref --verify --quiet refs/heads/<name>`).
   - If none exist, stop and ask the user which branch is the base.
4. If the recorded branch is the base branch (or is itself `dev`, `main`, or `master`), stop and notify the user.
5. Check for uncommitted changes (`git status --porcelain`). If any exist, stop and report them — do not force removal.
6. Resolve the main checkout path: parse `git worktree list --porcelain` and take the first `worktree <path>` entry.
7. `cd` into the main checkout path.
8. Checkout the base branch and pull latest:
   ```bash
   git checkout <base branch> && git pull
   ```
9. Remove the worktree:
   ```bash
   git worktree remove <recorded worktree path>
   ```
10. Delete the feature branch locally:
    ```bash
    git branch -D <recorded branch>
    ```
11. Confirm in one line: `Worktree removed → back on <base branch>, deleted <branch>`

## Guardrails

- Never run `git worktree remove --force`. If removal fails due to dirty state, stop and report.
- Never delete the base branch or other protected branches (`main`, `master`, `dev`).
- Do not run this from the main checkout — that is `branch-done`'s job.
