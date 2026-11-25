---
name: post-merge-sync
description: Use only when the owner explicitly asks to clean up after a merged AIP pull request - verify the merge live, sync the actual main worktree safely, remove the merged feature worktree if clean, delete only the local feature branch, and report exact merge/main SHAs. Never delete a remote branch.
---

# Post-merge sync

This skill is deliberately conservative because the repository may have several worktrees and the
shared checkout may be on an unrelated branch.

## Procedure

1. **Verify the merge live.** Read the PR with GitHub and require `state=MERGED`. Capture
   `headRefName` and `mergeCommit.oid` directly from that response. If the PR is not merged, stop.
2. **Fetch main without switching the current checkout:** `git fetch origin main`.
3. **Verify ancestry.** Require the captured merge commit to be an ancestor of `origin/main`.
   Report and stop if it is not.
4. **Find worktrees explicitly** with `git worktree list --porcelain`.
   - If a worktree has `refs/heads/main`, require it to be clean, then fast-forward it with
     `git -C <main-worktree> pull --ff-only origin main`.
   - If no main worktree exists, do not repurpose or switch another worktree. `origin/main` is the
     synchronized reference; report that no local main worktree was present.
5. **Remove the merged feature worktree only if safe.** If a worktree is attached to the captured
   head branch, require it to be clean, then remove it with `git worktree remove <path>`. A dirty
   worktree is a stop condition; never discard its changes.
6. **Delete only the local feature branch.** After the feature worktree is gone and the branch is
   confirmed merged into `origin/main`, delete it with `git branch -d <headRefName>` if it exists.
   Never run `git push --delete`, `git branch -D`, or otherwise delete the remote branch unless
   the owner separately asks.
7. **Report exact state:** PR number, merge SHA, `origin/main` SHA, local main-worktree SHA if one
   exists, removed worktree path, and whether the local feature branch was deleted.

No test suite is required: this skill changes no repository content.
