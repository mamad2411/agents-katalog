---
name: database-migrations
description: Use when adding or changing a DB migration or schema, running migrations, or debugging null/missing response fields after a migration — the migration rules (additive, reversible, immutable, seed-vs-migration, push filters into SQL) and the "null fields = unapplied migration" gotcha.
metadata:
  author: Ken Nguyễn <ntnpro@gmail.com>
---

# Database & migrations

## Migration rules
- NEVER alter database schema manually — always generate a migration file.
- Migration files are IMMUTABLE once merged to main; create a new one to fix, never edit an existing migration.
- Every migration MUST be reversible — implement both `up` and `down`.
- After generating a migration, verify it runs clean on a fresh DB before committing.
- NEVER seed production-specific data inside migration files; use dedicated seed scripts. (Migrations =
  schema/DDL or transforming existing data; seeds = initial/reference or test data/DML — keep them apart.)
- Push row filters into the SQL `WHERE` — never fetch broadly and post-filter in application code
  (`rows.filter(...)` on a status/type/date condition the DB could evaluate). If the repository helper
  can't express the condition, extend the helper with an optional query/selector param; don't work
  around it in the service layer.

## Null fields after migration (debugging gotcha)
When API response fields appear as `null` for a specific record type, **check whether the migration
that adds those columns has actually been applied** before assuming the data was never saved.

Root cause: a new nullable column is added via migration, but the migration hasn't run on the
environment being tested. JavaScript's `undefined != null` evaluates to `false` (loose equality), so
an absent column (`undefined`) looks identical to a null column in guards like
`ctx.doc.field != null ? ... : null` — both silently return `null`. Invisible until you inspect the schema.

**Rule:** before testing/debugging any feature that reads new DB columns, run `pnpm migration:run`
(or equivalent) on the local DB first. If response fields are unexpectedly null, check
`SHOW COLUMNS FROM <table>` before investigating code or data.

**Before concluding there's a deployment/CI bug**, verify whether the migration file itself was
actually merged to a deployed branch. Run `git log origin/rc..HEAD --oneline` (or equivalent base) —
if the migration commit appears there, the columns are absent simply because the PR hasn't merged
yet, not because of a pipeline failure. Don't add CI/deployment changes to fix a missing migration
that's still on a feature branch.

## Migration-related release readiness
Before a schema-touching feature is "done": all DB changes have migration files that run on a clean
DB; pending migrations have been applied on the local DB before testing schema-dependent features.
(Full release checklist → `release-safety` skill.)
