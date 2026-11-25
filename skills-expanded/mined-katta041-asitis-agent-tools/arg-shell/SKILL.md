---
name: arg-shell
description: Shows the git history for a path. Use when asked about the history of a file.
arguments: [path]
---

History: !`git log --oneline -- $path`

```!
git blame $ARGUMENTS
```
