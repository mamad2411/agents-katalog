---
name: migration-safety
description: "MANDATORY before any destructive database or schema work — DROP TABLE/COLUMN, TRUNCATE, DELETE or UPDATE across rows, irreversible ALTERs, data backfills, schema migrations. Forces the method: state the exact target → dry-run to count what's affected → write the rollback → only then execute. Triggers on \"drop the table\", \"delete the old rows\", \"clean up the data\", \"truncate\", \"remove the column\", \"write a migration\", \"alter the schema\", \"backfill\", any raw SQL against a real database."
---

# Migration Safety

**Destroyed data has no kill switch.** Every other mistake in this toolchain
can be reverted — a bad edit, a wrong commit, a broken build. A `DROP TABLE`
against the wrong database, a `DELETE` that forgot its `WHERE`, an
`ALTER TABLE … DROP COLUMN` on prod: those are permanent, and the model
reaches for them with the same casual confidence it edits a README.

## The rule

> **No destructive SQL without a declared plan.** State the target, prove the
> blast radius with a dry-run, write the rollback — *then* execute. The plan
> comes first or the statement doesn't run.

## What counts as destructive

- `DROP TABLE` / `DROP DATABASE` / `DROP SCHEMA`
- `ALTER TABLE … DROP COLUMN` (and any ALTER that discards data — type
  narrowing, NOT NULL on a column with nulls)
- `TRUNCATE`
- `DELETE FROM …` with no `WHERE`
- `UPDATE … SET …` with no `WHERE`

Not destructive (the gate never fires): `CREATE`, `ALTER … ADD`, `SELECT`,
`INSERT`, and any `DELETE`/`UPDATE` with a `WHERE` clause.

## The method: target → dry-run → rollback → execute

### Step 1 — State the target

Name exactly what is being changed, and where. Which database (dev? staging?
**prod?**), which table, which rows. "Clean up old records" is not a target;
"delete rows in `staging.sessions` older than 90 days, ~14k rows" is.

### Step 2 — Dry-run

Prove the blast radius before touching it:

```sql
-- before: DELETE FROM sessions WHERE created_at < now() - interval '90 days'
SELECT count(*) FROM sessions WHERE created_at < now() - interval '90 days';
```

For a `DROP COLUMN`, check the column for non-null data first. For a schema
migration, run it against a dev copy. If the count surprises you, the plan
was wrong — good, that's the point.

### Step 3 — Rollback plan

State how this gets undone *before* it happens:

- a backup/snapshot taken (`pg_dump`, a point-in-time restore window),
- a down-migration written alongside the up,
- or — if it genuinely can't be undone — say that out loud and get the human
  to confirm. "Irreversible" is a thing you declare, never a thing you
  discover.

### Step 4 — Declare, then execute

Write the plan where the hook can see it. Either a `.migration-plan` file in
the project root:

```
target: staging.sessions — rows older than 90 days (~14,203 per dry-run SELECT)
dry-run: count verified 2026-06-11; matches expectation from retention policy
rollback: pg_dump of sessions taken to backups/sessions-20260611.sql; down-migration n/a
```

…or, for a one-off, a sentinel line in your reply:

```
MIGRATION-SAFETY: ALLOW — dropping staging.tmp_import (dry-run: 0 dependent FKs); rollback: table recreated from import script
```

The PreToolUse hook blocks destructive SQL — run via Bash or written into a
`.sql`/migration file — until one of those exists. Delete the
`.migration-plan` file when the migration ships so a stale plan can't
whitewash the next one.

## Avoiding false alarms

The gate only fires on the irreversible shapes. `WHERE`-scoped deletes and
updates, additive migrations, SELECTs, and SQL in comments all pass. Writes
to files outside `.sql`/migration paths are never scanned — a `DROP TABLE`
in a test fixture or doc doesn't block.

## Kill switch

False positive (a seeded test database, a scratch SQLite file):
`touch .migration-safety-off` in the project root, or
`export MIGRATION_SAFETY_GATE=off`.

## Pairs with

- **`verify-before-done`** — the dry-run is the verification; this skill just
  makes it happen *before* the destructive step instead of after.
- **`no-silent-assumptions`** — "assuming this only touches staging" is
  exactly the guess Step 1 forces into the open.
- **`scope-guard`** — scope the files; this scopes the data.
