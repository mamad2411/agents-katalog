---
name: resolving-merge-conflicts
description: "Resolves an in-progress git merge or rebase conflict by tracing why each side changed, reconciling every conflicted hunk, running the project's checks, and finishing the merge or rebase. Use when a merge, rebase, or pull stops on conflicts, or the user asks to resolve conflicts in an active merge or rebase. Not for standalone conflict-marker cleanup."
license: MIT
---

1. **See the current state** of the merge/rebase. Confirm that Git reports an active merge or rebase before editing or staging anything. If neither is active, stop and explain that standalone conflict-marker cleanup is ordinary editing outside this skill; do not create a merge commit or run a continuation command. Otherwise check git history and the conflicting files. Record the conflicted paths and existing unrelated staged, unstaged, and untracked work so it remains unchanged.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check the original issues. When there are many conflicts, hand this research to a sub-agent that returns only the intent of each side.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Always resolve; never `--abort`.

4. Discover the project's **automated checks** and run them, typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish the merge/rebase.** Stage only resolved conflict hunks and necessary merge-fix changes. Whole-file staging is safe only when that file contains no unrelated edits; otherwise isolate the resolution hunks while preserving unrelated edits and their original staged state. Inspect the staged diff against the recorded pre-resolution state before committing or continuing. For a merge, commit the merge resolution without including unrelated staged work; if it cannot be isolated safely, stop and report the blocker. If rebasing, use `git rebase --continue` and repeat for each conflict until all commits are rebased, preserving unrelated work throughout.
