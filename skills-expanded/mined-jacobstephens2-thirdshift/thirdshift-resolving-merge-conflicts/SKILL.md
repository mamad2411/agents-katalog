---
name: thirdshift-resolving-merge-conflicts
description: "Use when you need to resolve an in-progress git merge/rebase conflict."
---

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Identify generated files.** Treat a conflicting file as generated when the repository documents a command that produces it, or the file says it is generated. Find its sources and the repository's documented generator command.

4. **Resolve hand-written files and sources first.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Always resolve; never `--abort`.

5. **Regenerate generated files.** Once their source conflicts are resolved, run the repository's documented generator command and stage the regenerated output. Never hand-merge generated hunks.

6. Discover the project's **automated checks** and run them, typically typecheck, then tests, then format. Fix anything the merge broke.

7. **Finish the merge/rebase.** Stage everything, commit, and push. If rebasing, continue the rebase process until all commits are rebased.
