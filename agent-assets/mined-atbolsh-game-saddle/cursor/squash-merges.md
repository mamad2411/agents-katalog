---
description: Collapse a feature branch onto master with git merge --squash
alwaysApply: true
---

# Squash-merge onto master

When merging a branch onto master, collapse it to ONE commit:

```bash
git merge --squash <branch>
git commit
```

Never a plain `git merge` for a multi-commit branch. A merge commit keeps
every intermediate commit in master's history; squash makes the landed
work one reviewable commit with one message.

Context: the 2026-08 `extra-notebooks-and-modes` merge landed unsquashed.
