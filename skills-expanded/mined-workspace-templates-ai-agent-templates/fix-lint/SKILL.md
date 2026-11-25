---
name: fix-lint
description: Runs your linter, applies only safe fixes, then lists every remaining finding with a reason so nothing is silenced by accident.
disable-model-invocation: true
---

Fix lint problems in: $ARGUMENTS (whole project if empty).

1. Find the project's linter from package.json scripts, pyproject.toml, .golangci.yml or CI config. Use its own command, not a different tool. Run it first and record the count of errors and warnings.
2. Apply the tool's safe autofix only (for example `eslint --fix`, `ruff check --fix`). Do not use unsafe-fix flags.
3. Fix remaining findings by hand only when the change cannot alter behavior: unused imports and variables, missing await, wrong types in an annotation. Read the surrounding code before each edit.
4. Never add disable comments, loosen rules or edit the lint config to make errors vanish.
5. Re-run the linter and the test command. If tests fail, revert the last change and list it instead.

Report: before and after counts, the files changed, and a table of leftover findings with rule, location and why it needs a decision. Do not commit.
