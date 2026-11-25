---
name: branch-cleanup
description: Lists merged and stale local branches, shows exactly what would be removed and deletes only the ones you approve.
disable-model-invocation: true
---

Clean up local branches. Options from the user: $ARGUMENTS (for example a staleness window like 90d).

1. Run `git fetch --prune` and `git branch -vv`. Identify the default branch and the current branch; both are protected, with `main`, `master`, `develop` and `release*`.
2. Group the rest: **merged** (`git branch --merged <default>`), **gone** (upstream deleted), **stale** (no commit in 90 days or the given window) and **active**.
3. For each non-merged candidate show last commit date, author, and the count of commits not in the default branch (`git rev-list --count <default>..<branch>`). Mark any with unpushed commits as at risk.
4. Print the plan as a table of branch, group, last commit and risk, with the exact command for each deletion.
5. Delete nothing yet. Ask which groups to remove. Use `git branch -d` for merged ones; use `-D` only for branches the user names one by one after seeing their unmerged commits. Never touch remote branches.

After deleting, print the commit hash of each removed branch so it can be restored with `git branch <name> <hash>`.
