---
description: Prevent Cursor co-authorship in git commits
alwaysApply: true
---

# No Cursor Co-Authorship

**CRITICAL RULE**: Never add any form of Cursor attribution to git commits.

## Prohibited

The following MUST NEVER appear in any commit message:

- `Co-authored-by: Cursor <cursoragent@cursor.com>`
- `Co-authored-by: Cursor Agent`
- Any reference to "Cursor", "cursoragent", or similar in commit metadata

## Git Commits

When making commits:

1. Use only the user's name and email as author
2. Do not add any co-author trailers
3. Keep commit messages focused on the actual changes

## Example

```bash
# ✅ CORRECT - Clean commit
git commit -m "feat: add new feature"

# ❌ WRONG - Has Cursor co-authorship
git commit -m "feat: add new feature

Co-authored-by: Cursor <cursoragent@cursor.com>"
```

## If Co-Author Appears

If a commit accidentally includes Cursor co-authorship, immediately:

1. Use `git commit --amend` with a clean message
2. Or use `git commit-tree` to create a clean commit
3. Force push the corrected history

This is a strict IP/attribution requirement - no exceptions.
