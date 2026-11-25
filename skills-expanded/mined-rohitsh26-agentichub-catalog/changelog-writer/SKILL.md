# changelog-writer

Turn a range of merged pull requests into a clean, human-readable changelog
entry grouped by type (Added / Changed / Fixed / Removed).

## When to use

Ask for this before cutting a release, when you have a set of merged PRs since
the last tag and want a `CHANGELOG.md` section that reads well.

## How to write the entry

1. Collect the merged PRs in the range (title, number, author, labels).
2. Group each PR under one of: Added, Changed, Fixed, Removed. Use the PR's
   labels first; fall back to the verb in the title.
3. Write one bullet per user-visible change in plain language — describe the
   effect on the user, not the implementation. Drop pure-internal refactors.
4. Lead each bullet with the change, end with the PR number in parentheses.
5. Put the version and date as the heading. Keep it to a single screen.

## Rules

- Never invent a change that isn't backed by a PR in the range.
- Merge duplicate bullets that describe the same user-facing change.
- If a PR is ambiguous, prefer Changed over guessing.
