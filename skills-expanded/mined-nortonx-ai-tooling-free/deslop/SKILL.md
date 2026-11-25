---
name: deslop
description: Remove AI-generated code slop from a branch. Use when cleaning up AI-generated code, removing unnecessary comments, defensive checks, or type casts. Checks diff against main and fixes style inconsistencies.
---

# Remove AI Code Slop

Check the diff against main and remove all AI-generated slop introduced in this branch.

**Scope: source code only.** For prose (reports, docs, specs, ADRs, PR descriptions) use `deslop-prose`. Nothing below applies to a Markdown document, so running this skill on one does almost nothing.

## What to Remove

- Extra comments that a human wouldn't add or are inconsistent with the rest of the file
- Extra defensive checks or try/catch blocks that are abnormal for that area of the codebase (especially if called by trusted/validated codepaths)
- Casts to `any` to get around type issues
- Inline imports in Python (move to top of file with other imports)
- Any other style that is inconsistent with the file

## Process

1. Get the branch diff: `git diff <base>...HEAD`, with `<base>` from `git symbolic-ref --short refs/remotes/origin/HEAD`, else `origin/main`, else `origin/master`. If none resolves, ask.
2. Review each changed file for slop patterns
3. Remove identified slop while preserving legitimate changes
4. Report a 1-3 sentence summary of what was changed
