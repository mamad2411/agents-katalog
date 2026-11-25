---
name: find-dead-code
description: Finds unused exports, files and dependencies and shows the evidence for each, so you can delete with confidence.
disable-model-invocation: true
---

Find dead code in: $ARGUMENTS (whole project if empty).

1. Use the project's own tools first if present (knip, ts-prune, depcheck, vulture, deadcode, `go vet`). Otherwise search by hand.
2. For each candidate export, file or dependency, search the whole repository, including tests, scripts, config, templates and docs, for the name and its string forms.
3. Check dynamic use before calling anything dead: route or plugin auto-loading, dependency injection, reflection, `require(variable)`, framework conventions such as pages and migrations, and exports meant for outside consumers.
4. Rate each: **certain** (no reference anywhere), **likely** (referenced only by other dead code or tests), **unsure** (dynamic or public use possible).
5. Never delete anything in this step.

Report a table with item, location, evidence (the searches run and their results), and confidence. List unused dependencies separately with the file that last imported them. Then ask which group to remove, and run the tests after removal.
