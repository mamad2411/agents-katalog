---
name: squash-commits
description: Turns a messy branch history into a few clear commits with proper messages, showing the plan before rewriting anything.
disable-model-invocation: true
---

Squash the commits on this branch. Instructions: $ARGUMENTS (for example the base branch or "single commit").

1. Find the base: `git merge-base HEAD <base>` with the given base or the default branch. Show `git log --oneline <base>..HEAD` and `git diff --stat <base>..HEAD`.
2. If any of these commits exist on a shared remote branch that others may use, warn and ask before continuing.
3. Propose groups: related commits by files and purpose, ordered so each group builds and passes tests alone. Give each a message in the project's style (check recent `git log -n 10 --oneline`), with a body explaining why.
4. Print the plan: new commit message, commits folded into it, files.
5. Create a backup: `git branch backup/<branch>-<date>`.
6. After approval, rewrite without interactive tools: `git reset --soft <base>` then commit each group by staging its files, or a scripted `git rebase`. Verify `git diff backup/<branch>` is empty.

Report the new log and the backup name. Do not push; mention that `--force-with-lease` is required if already pushed.
