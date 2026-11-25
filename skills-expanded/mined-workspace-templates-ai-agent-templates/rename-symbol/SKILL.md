---
name: rename-symbol
description: Renames a function, class or variable everywhere, including strings, docs and tests, then verifies the build still passes.
disable-model-invocation: true
---

Rename a symbol: $ARGUMENTS (format: old to new).

1. Confirm the old name's definition and kind (function, class, field, column, env var, route). If the new name already exists in scope, stop and report the clash.
2. Find all uses with the language server or `grep -rnw` across code, tests, config, docs, scripts, templates, CI files and SQL. Search also for case variants (camelCase, snake_case, kebab-case, UPPER_CASE) and for the name inside strings.
3. Sort hits into: real references to rename; same word with another meaning (leave); public or persisted names such as an API field, database column, event name or env var, where renaming breaks clients or stored data.
4. If a public or persisted name is involved, stop and ask first, since it needs a migration or a deprecation alias.
5. Apply the rename to the real references only. Do not reformat other lines.
6. Run the type check, build and tests. Grep once more for the old name and explain each remaining hit.

Report the count of changed files and the leftover hits. Ask before committing.
