---
name: git-move
description: Use git mv for tracked files to preserve history.
---

# Git move

**Why:** A plain `mv` makes git record a delete + add, so `git log --follow`, `git blame`, and review diffs lose the file's history and show the move as a full rewrite.

When moving or renaming a tracked file (one not covered by `.gitignore`), use `git mv {source} {dest}` instead of `mv`. Git then records a rename and preserves history; any content change shows as a normal diff on top of the rename.

## Examples

```sh
# BAD — git loses history; the file appears as deleted + added
mv src/utils/format.ts src/lib/format.ts
git add .

# GOOD — git tracks the rename; history is preserved
git mv src/utils/format.ts src/lib/format.ts
```
