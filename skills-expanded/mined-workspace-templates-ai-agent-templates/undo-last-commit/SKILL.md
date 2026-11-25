---
name: undo-last-commit
description: Undoes the most recent commit safely, keeps your work, and picks between soft reset, mixed reset and revert for your case.
disable-model-invocation: true
---

Undo the last commit. What the user wants: $ARGUMENTS (for example "keep changes staged", "it broke prod").

1. Run `git status`, `git log -n 3 --stat` and `git branch -vv`. Check whether the commit exists on the remote (`git branch -r --contains HEAD`).
2. Choose and explain:
   - Not pushed, want changes staged: `git reset --soft HEAD~1`.
   - Not pushed, want changes unstaged: `git reset --mixed HEAD~1`.
   - Only the message is wrong: tell the user `git commit --amend` fits, and do not run it unasked.
   - Pushed or shared: `git revert HEAD` so history is not rewritten.
   - Wrong branch: reset here, then offer `git switch` plus `git stash` or cherry-pick to move it.
3. Never run `git reset --hard` or `git clean`. If the working tree has other uncommitted edits, tell the user before resetting.
4. Print the hash of the commit being undone so it can be restored with `git reset --hard <hash>` or found in `git reflog`.

Show the commands, wait for approval, run them, then show `git status` and the final log.
