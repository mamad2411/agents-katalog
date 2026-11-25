---
name: branch-done
description: Delete the current feature branch and switch back to the base branch after opening a PR. Use when the user has just opened a PR and wants to clean up — phrases like "PR 올렸으니 정리해줘", "브랜치 정리해줘", "정리하고 돌아가줘", "clean up this branch", "delete feature branch", "/branch-done". Do NOT use inside a git worktree — that is the worktree-done skill.
license: MIT
metadata:
  author: dkmqflx
  version: "1.0.0"
---

# Branch Done

After opening a PR, delete the current feature branch and switch back to the base branch.

## When to apply

Cleaning up the **main checkout** after opening a PR. **Do not apply** inside a worktree — that is `worktree-done`.

## Steps

1. Record the current branch name: `git rev-parse --abbrev-ref HEAD`.
2. Determine the base branch:
   - Try `git symbolic-ref refs/remotes/origin/HEAD` and strip the `refs/remotes/origin/` prefix.
   - If that fails, use the first of `dev`, `main`, `master` that exists locally (`git show-ref --verify --quiet refs/heads/<name>`).
   - If none exist, stop and ask the user which branch is the base.
3. If the current branch is the base branch (or is itself `dev`, `main`, or `master`), stop and notify the user — nothing to clean up.
4. Checkout the base branch and pull latest:
   ```bash
   git checkout <base branch> && git pull
   ```
5. Delete the previous feature branch locally:
   ```bash
   git branch -D <recorded branch>
   ```
6. Confirm in one line: `Cleaned up → back on <base branch>, deleted <branch>`
