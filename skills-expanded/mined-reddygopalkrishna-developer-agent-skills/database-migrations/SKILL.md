---
name: database-migrations
description: Plans and writes zero-downtime database schema migrations (expand/contract, safe indexes, batched backfills, rollback). Use when adding, renaming or dropping columns or tables, changing types or constraints, adding indexes, or backfilling data on a live database.
license: MIT
---

# Zero-Downtime Database Migrations

During every deploy, the old and new versions of the application run against the same schema at the same time. Every migration must work with both the code running now and the code being deployed, and must never hold a lock that blocks traffic for longer than you would accept as an outage.

## When to use

- Adding, renaming, dropping or retyping columns and tables on a database that serves traffic.
- Adding indexes, foreign keys, unique, NOT NULL or CHECK constraints to existing tables.
- Backfilling or transforming existing rows.
- Reviewing a migration file (hand-written or ORM-generated) before it ships.

Not for: designing a brand-new schema with no live data (use the database-schema-design skill), or tuning slow queries (use sql-optimization).

## Workflow

1. **Identify the engine, version and tool.** Run `SELECT version();` (PostgreSQL) or `SELECT VERSION();` (MySQL). Lock behaviour changes between versions. Find the migration tool (Flyway, Liquibase, Alembic, Django, Rails, Prisma, EF Core, golang-migrate, ...) and whether it wraps each migration in a transaction.
2. **Read the actual SQL.** For ORM-generated migrations, print the SQL before judging it (see "Inspect generated SQL" below). Never review only the ORM diff.
3. **Classify every statement** with the risk table below. Anything not "safe" needs a pattern.
4. **Split into expand → migrate → contract phases**, each shipped as its own deploy. One migration should do one risky thing.
5. **Guard every DDL statement** with a lock timeout (PostgreSQL `SET lock_timeout`, MySQL `SET SESSION lock_wait_timeout`) so it fails fast instead of queueing behind a long query and blocking everything after it.
6. **Move data changes out of schema migrations.** Backfills run as batched, resumable jobs, not inside the DDL transaction.
7. **Rehearse on a production-sized copy.** Record duration, locks taken and replication lag. A migration that takes 50 ms on a dev database can take an hour on 500 million rows.
8. **Write the rollback or forward-fix plan** before running anything. Mark the steps that are irreversible.
9. **Stop and get explicit confirmation from the user before running any migration against a shared, staging or production database.** Show them the exact SQL, expected duration and rollback plan.

## Expand / contract

The universal pattern for any change that would break running code:

| Phase | Schema change | App change | Reversible? |
|---|---|---|---|
| 1. Expand | Add the new column/table/index, nullable or with a default | None yet | Yes |
| 2. Dual write | — | Write to old and new; read old | Yes |
| 3. Backfill | Batched job copies old → new | — | Yes |
| 4. Switch reads | Optionally add constraints (NOT NULL, FK) on new | Read new, still write both | Yes |
| 5. Stop old writes | — | Write only new; remove all references to old | Yes |
| 6. Contract | Drop old column/table | — | **No** — take a backup first |

Each phase is a separate deploy. Phase 6 waits until every running instance (including workers, cron jobs, and other services sharing the database) has stopped referencing the old structure.

### Ordering migrations against deploys

| Change | Run migration | Then |
|---|---|---|
| Add table, nullable column, index | Before the app deploy | App starts using it |
| Add column the new code requires | Before the app deploy, nullable or with a default | Add NOT NULL later, after backfill |
| Drop column or table | After the code stops referencing it | — |
| Rename column or table | Never in one step | Expand/contract: add new, dual write, backfill, switch, drop old |
| Change column type | Never in place on a large table | New column + backfill + switch, unless the change is metadata-only for your engine |
| Add NOT NULL / FK / CHECK | After every writer sets valid values and the backfill is done | Validate without blocking (see engine references) |

ORMs that list columns explicitly in SELECT and INSERT (most do) fail as soon as a mapped column disappears. Remove the mapping and deploy first:

- Rails: `self.ignored_columns += ["legacy_status"]`, deploy, then drop.
- Django: remove the field from the model using `migrations.SeparateDatabaseAndState` so state changes without dropping the column; drop it in a later migration.
- EF Core, Hibernate/JPA, Prisma, SQLAlchemy: remove the property/field and deploy; drop the column in a later migration.

## Risk classification

| Operation | Risk | Safe pattern |
|---|---|---|
| Add nullable column, no default | Safe | — |
| Add column with a constant default | PostgreSQL 11+: metadata only. MySQL 8: usually `ALGORITHM=INSTANT` | Volatile defaults (`random()`, `gen_random_uuid()`, `clock_timestamp()`) rewrite the table in PostgreSQL — add nullable, backfill, then set the default |
| Create index | Blocks writes for the whole build | PostgreSQL `CREATE INDEX CONCURRENTLY`; MySQL `ALGORITHM=INPLACE, LOCK=NONE` |
| Add unique constraint | Blocks writes while it builds the index; fails on duplicates | Find duplicates first; build the unique index concurrently, then attach it |
| Add foreign key | Locks both tables while it scans | PostgreSQL `NOT VALID` then `VALIDATE CONSTRAINT`; index the referencing column |
| Add NOT NULL to existing column | Full scan under an exclusive lock | PostgreSQL: CHECK `NOT VALID` → `VALIDATE` → `SET NOT NULL` (12+) |
| Change column type | Usually rewrites the table under an exclusive lock | New column + backfill + switch |
| Rename column/table | Fast, but breaks every running instance | Expand/contract |
| Drop column/table | Breaks running code; irreversible | Remove references first; back up; confirm with the user |
| UPDATE/DELETE many rows | Long locks, bloat, replication lag | Batched job |

Read [references/postgres.md](references/postgres.md) when the database is PostgreSQL (lock levels, exact recipes, non-transactional migrations per tool, finding blockers).
Read [references/mysql.md](references/mysql.md) when the database is MySQL or MariaDB (online DDL, metadata locks, gh-ost and pt-online-schema-change).

## Batched backfills

Run backfills as a separate script or job that commits per batch, is safe to re-run, and can be stopped at any time.

```sql
-- One batch. The job loops :start from min(id) to max(id) in steps of :batch_size,
-- commits after each batch, and sleeps briefly between batches.
UPDATE orders
SET    status_v2 = status
WHERE  id >= :start
  AND  id <  :start + :batch_size
  AND  status_v2 IS NULL;
```

- Walk the primary key in ranges. `WHERE new_col IS NULL LIMIT n` without an index rescans the table on every batch.
- Start with 1,000-10,000 rows per batch and measure; aim for batches that finish in well under a second.
- Watch replication lag and database CPU between batches; pause when lag grows.
- Make it idempotent (the `IS NULL` guard) and log progress so it can resume after a crash.
- Rows written during the backfill must already be handled by dual-write code (phase 2), otherwise you race.

## Inspect generated SQL

| Tool | How to see the SQL before running it |
|---|---|
| Django | `python manage.py sqlmigrate <app> <migration>` |
| Alembic | `alembic upgrade <rev> --sql` (offline mode) |
| EF Core | `dotnet ef migrations script <from> <to>` |
| Liquibase | `liquibase update-sql` |
| Prisma | `prisma migrate dev --create-only`, then read the generated `migration.sql` |
| Flyway, golang-migrate, Rails SQL files | The migration file is the SQL; read it |

## Rollback vs forward fix

- Down migrations are rarely tested and often destroy data (dropping a column that has new writes in it). Prefer forward fixes: a new migration that corrects the problem.
- Expand-phase steps are cheap to roll back: leave the unused column in place, roll back the app.
- Contract-phase steps (drops, destructive type changes) are irreversible. Before them: confirm a recent backup or snapshot exists and that restore has been tested, and get explicit user approval.
- Because each phase is backward compatible, rolling back the **application** one version is always safe. Keep it that way.

## Testing

- Run all migrations from an empty database in CI, and against a recent anonymised snapshot when possible.
- Run the **previous** app version's test suite against the **new** schema to prove backward compatibility.
- Rehearse long operations on production-sized data and record how long they took.
- Check that the migration is idempotent or that the tool records it as applied exactly once.

## Anti-patterns

- **One migration that adds a column, backfills it and sets NOT NULL** in a single transaction — holds locks for the whole backfill. Split it.
- **No lock timeout** — the DDL waits behind one long-running query, and every query after it queues behind the DDL. That is an outage caused by a "fast" statement.
- **Renaming in place** — instantly breaks every running instance still using the old name.
- **Editing a migration that already ran somewhere** — environments diverge and checksum-validating tools (Flyway, Liquibase) refuse to run. Add a new migration instead.
- **Trusting ORM-generated migrations unread** — they happily emit table rewrites and blocking index builds.
- **Mixing schema changes and large data changes** in one migration.
- **Dropping a column the ORM still selects** — the deploy order was wrong.
- **Testing only on a small dev database** — lock duration and rewrite cost scale with table size.

## Done when

- Every step is backward compatible with the code currently deployed, and the deploy order is written down.
- Every DDL statement is guarded by a lock timeout or an explicit online-DDL clause.
- Indexes and constraints on large tables are built without blocking writes.
- Backfills are batched, idempotent, resumable and run outside the DDL transaction.
- The plan was rehearsed on production-sized data, with durations recorded.
- Rollback or forward-fix steps are written; irreversible steps are flagged and have a verified backup.
- The user explicitly approved running it against any shared or production database.

## References

- [references/postgres.md](references/postgres.md) — read for PostgreSQL lock levels, step-by-step recipes, non-transactional migrations per tool, and queries to find blocking sessions.
- [references/mysql.md](references/mysql.md) — read for MySQL/MariaDB online DDL, metadata locks, and online schema change tools.
