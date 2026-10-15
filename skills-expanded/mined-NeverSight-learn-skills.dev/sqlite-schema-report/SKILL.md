---
name: sqlite-schema-report
description: Vendor-neutral skill to summarize a SQLite database schema (tables, columns, indexes, foreign keys) and emit a portable report.
---

## When to invoke
- You received a SQLite database file and need a quick schema overview.
- You want to document a local database before migrating or integrating.

## Inputs needed
- `--db` path to a SQLite database.
- Optional: `--tables` comma-separated list of tables (default: all user tables).

## Workflow
1. Open database in read-only mode.
2. Discover user tables.
3. For each table, capture columns/types, indexes, and foreign keys.
4. Emit a JSON report.

## Output format
- JSON written to `--output`.

## Guardrails
- Read-only: never modify the database.
- Do not infer semantics beyond the declared schema.

## Reference code
- `sqlite_schema_report.py` uses Python stdlib `sqlite3`.
