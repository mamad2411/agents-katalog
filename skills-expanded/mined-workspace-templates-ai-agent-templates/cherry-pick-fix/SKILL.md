---
name: cherry-pick-fix
description: Cherry-picks a fix commit onto a release branch, resolves conflicts with you and runs the tests there before anything is pushed.
disable-model-invocation: true
---

Backport a fix. Arguments (commit then target branch): $ARGUMENTS

1. Parse the two values. Run `git show --stat <commit>` and confirm it is a single fix, not a merge. For a merge commit ask which parent to use with -m.
2. Ensure a clean tree with `git status --porcelain`. Fetch, then create `backport/<short-hash>-<branch>` from the target: `git switch -c ... origin/<branch>`.
3. Run `git cherry-pick -x <commit>` so the origin hash is recorded.
4. On conflict, list each file with `git diff --name-only --diff-filter=U`, show both sides and explain what changed on the release branch. Propose a resolution and apply it only for trivial cases; ask about anything that changes behavior.
5. Detect the test command from package.json, Makefile or pyproject and run it. If the fix needs code that does not exist on this branch, say so and stop.

Report the branch name, resolved files and test results. Offer the push command but do not run it. Abort with `git cherry-pick --abort` if the user declines.
