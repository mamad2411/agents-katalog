---
name: resolving-merge-conflicts
description: Resolve an in-progress git merge or rebase conflict by understanding each change's intent, resolving every hunk, running checks, and finishing the operation. Use when a merge/rebase is stopped on conflicts. Not for preventing conflicts or for aborting.
---
1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour. Always resolve; never `--abort`.

4. Discover the project's **automated checks** and run them, typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish the merge/rebase.** Stage everything and commit. If rebasing, continue the rebase process until all commits are rebased.

## Purpose
Finish a conflicted merge/rebase correctly without losing either side's intent.

## When to use
`git status` shows an unfinished merge or rebase with conflicted files.

## When NOT to use
- No conflict in progress.
- The user explicitly wants to abort.

## Edge cases and failure handling
- Intents are incompatible -> pick the side matching the merge goal and record the trade-off; do not invent behaviour.
- Generated or lock files conflict -> regenerate with the package manager rather than hand-merging.
- Rebase with many commits -> repeat resolve/continue per commit.

## Validation
- No conflict markers remain (`git grep -n "<<<<<<<"` empty); typecheck, tests and formatting pass; merge/rebase completed and committed.

## Output requirements
Summary: files resolved, decisions and trade-offs, checks run.

## Example
```text
Both branches edit `price()` -> read both commits/PRs -> keep new rounding and the discount rule -> run tests -> `git rebase --continue`.
```

## Related skills
code-review, tdd
