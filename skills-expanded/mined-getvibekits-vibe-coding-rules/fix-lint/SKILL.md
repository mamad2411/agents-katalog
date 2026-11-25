---
name: fix-lint
description: Run the linter and fix the problems it reports without changing what the code does.
argument-hint: [optional: folder or file]
disable-model-invocation: true
---

Fix lint problems in: $ARGUMENTS (if empty, the whole project).

1. Find the lint command this project uses (package.json scripts, a Makefile or the README) and run it.
2. Fix the problems it reports, one file at a time.
3. Don't change what the code does. If a fix would change behavior, list it and skip it.
4. Run the linter again and show me what's left.
