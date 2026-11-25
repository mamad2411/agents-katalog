---
name: using-git-worktrees
description: Use before non-trivial work on a default branch to isolate changes in a feature branch or dedicated git worktree.
---

# Using Git Worktrees

## Safe branch isolation
1. Check `git status --short` and current branch.
2. If on `main` or `master`, create a feature branch or worktree before edits.
3. Never discard uncommitted user changes.
4. Keep commits atomic and named after the task or requirement.

Common commands:
```bash
git switch -c feature/<slug>
# or
git worktree add ../<repo>-<slug> -b feature/<slug>
```

