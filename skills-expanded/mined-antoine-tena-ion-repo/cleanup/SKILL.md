---
name: cleanup
description: Remove the worktrees and local branches already merged into the integration branch, and the leftovers (agent worktrees, orphan directories). Use when the user asks to clean up worktrees or branches.
---

From the root of the repo, never switching the branch of the main tree. Integration branch: the
one the project's `CLAUDE.md` names, otherwise `develop` if it exists, otherwise `origin`'s
default branch.

1. `git fetch -q --prune origin`, then `git worktree prune`.
2. For each worktree of `git worktree list --porcelain` (except the main tree): note its branch,
   whether it has changes (`git -C <wt> status --porcelain`) and whether its branch is merged
   (`git merge-base --is-ancestor <branch> origin/<integration>`). A detached worktree (agents):
   check whether its HEAD is in `origin/<integration>`.
3. Show a table: worktree, branch, merged?, changes?, last commit. Sort into "removable" (merged
   and clean) and "to keep or decide"; in the latter, flag as probably forgotten a worktree not
   merged with no commit for more than two weeks, or with uncommitted changes, and ask what to
   do with it (finish, keep, remove).
4. **Ask for confirmation**, then for the removable ones: `git worktree remove <wt>` and
   `git branch -d <branch>` (never `-D`, never `--force` on a worktree with changes).
5. Local branches without a worktree that are merged: offer `git branch -d` the same way. Never
   delete a remote branch without explicit agreement.
6. Report in the `repo` plugin's `debrief` format (`output-styles/debrief.md`).
