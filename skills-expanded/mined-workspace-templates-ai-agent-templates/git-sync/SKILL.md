---
name: git-sync
description: Brings your current branch up to date with its upstream by rebase or merge, resolves small conflicts and reports what changed.
disable-model-invocation: true
---

Sync the current branch with: $ARGUMENTS (its upstream, or origin/main if none).

1. Run `git status` and stop if the tree is dirty; offer `git stash` and wait for approval. Run `git fetch --all --prune`.
2. Show `git rev-list --left-right --count HEAD...<target>` and the incoming commit subjects.
3. Choose the method. Rebase if the branch is local or has only your commits. Merge if the branch is pushed and others may have based work on it. State the choice and why.
4. Run it. On conflict, list the files; resolve only trivial ones (imports, whitespace, adjacent edits) and explain each. Stop and ask on anything touching logic. Never use `--strategy-option theirs` or `ours` blindly.
5. After a rebase, run the tests. Do not push. If the branch was already pushed and you rebased, say that a `--force-with-lease` push is needed and wait for the user to ask for it.

Report commits applied, files changed upstream, conflicts resolved, and the test result.
