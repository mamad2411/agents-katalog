---
name: schema-diff-review
description: Reviews a schema change or migration diff for risk, missing indexes and rollback, and returns a verdict with line references.
disable-model-invocation: true
---

Review the schema change: $ARGUMENTS (branch, commit range, or empty for the current diff against main).

1. Run `git diff <base>...HEAD --stat` and read every changed migration, model and schema file, and the tables they touch.
2. Check each statement for: locks on large tables, rewrites of the table, dropped or truncated columns, narrowing type changes, NOT NULL or unique constraints added to existing data, renamed columns that old code still reads.
3. Check design: missing foreign keys, missing indexes on new foreign keys and filtered columns, duplicate or unused indexes, wrong types for money and time, missing defaults.
4. Check order: can the old application version run against the new schema, and the new code against the old schema?
5. Check rollback: is there a working down step, and what data is lost if used?
6. Do not edit or run anything.

Return a verdict (approve, change, block), then findings in a table: severity, file:line, problem, fix. End with the rollback plan in 3 steps and ask if you should draft the fixes.
