---
name: sql-antipatterns
description: Forbidden SQL patterns — SELECT *, missing CONCURRENTLY on indexes, unsafe migrations, missing FK indexes. Applies when editing SQL files.
user-invocable: false
---

# SQL anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Errors
- AP-SQL-002 — Always `CREATE INDEX CONCURRENTLY` in migrations on live tables; run outside a transaction.
- AP-SQL-003 — Add columns nullable first, backfill, then add constraint `NOT VALID` → `VALIDATE CONSTRAINT`.

## Warnings
- AP-SQL-001 — Name every column in SELECT; never use `SELECT *` in application queries.
- AP-SQL-004 — Create an index on every foreign key column; missing FK indexes cause full-table scans.
- AP-SQL-006 — Use `ALGORITHM=INPLACE, LOCK=NONE` or gh-ost for large-table MySQL ALTERs.
- AP-SQL-007 — Paginate with keyset/cursor (`WHERE id > ?`) instead of `OFFSET`; OFFSET degrades at scale.

Details for any ID: `reference/<ID>.md`
