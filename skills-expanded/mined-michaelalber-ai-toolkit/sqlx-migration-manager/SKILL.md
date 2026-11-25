---
name: sqlx-migration-manager
audience: team
description: >
  SQLx migration lifecycle management with safety checks and rollback planning. Manages plain
  SQL migration files, compile-time query verification via sqlx prepare, and the offline query
  cache. Use when creating, reviewing, or applying database migrations in Rust/SQLx projects,
  managing sqlx migrate run/revert, regenerating the sqlx offline cache after schema changes, or
  planning zero-downtime migrations.
---

# SQLx Migration Manager

> "A migration that cannot be rolled back is a migration that has not been tested. SQLx's
> compile-time query verification is a gift — but only if you regenerate the cache after every migration."

## Core Philosophy

SQLx migrations are plain SQL files — no ORM-generated DDL, no code-first schema. That is a
strength: the SQL is explicit, reviewable, and portable. But SQLx's compile-time query verification
(`sqlx::query!` macros) means schema changes can break compilation, so the offline query cache
(`sqlx prepare`) must be regenerated after every migration. This skill manages the full lifecycle
with the same safety philosophy as `ef-migration-manager` and `alembic-migration-manager`: never
apply a migration you have not reviewed, never apply without testing the rollback, and always
regenerate the offline cache after applying.

**Non-Negotiable Constraints:**
1. REVIEW BEFORE APPLY — review the SQL before `sqlx migrate run`; never apply unreviewed SQL.
2. TEST THE ROLLBACK — `sqlx migrate revert` must work on a dev database before the migration is considered safe.
3. REGENERATE THE CACHE — run `sqlx prepare` after every `sqlx migrate run`; commit `.sqlx/`. Skipping it breaks compilation for everyone.
4. SEPARATE SCHEMA FROM CODE — schema changes and the code depending on them are separate commits; the migration runs first.
5. IDEMPOTENT WHERE POSSIBLE — `CREATE TABLE/INDEX IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS` (PostgreSQL 9.6+).

Full principle table, KB lookups, discipline rules, anti-patterns, and error recovery live in
`references/conventions.md`.

## Workflow

```
PLAN            Identify the schema change; assess data-loss risk (DROP/TRUNCATE/type change) and
                locking risk (table rewrites, index creation); plan the rollback SQL; decide whether
                zero-downtime is required. (Per-operation detail: dangerous-operations.md.)

CREATE          sqlx migrate add <descriptive-name>; write the forward SQL and the rollback SQL.

REVIEW (gate)   Read the file completely: no unintended data loss, acceptable locking, correct
                rollback SQL, idempotency where applicable. Do not proceed until reviewed.

TEST ROLLBACK   On a dev database: sqlx migrate run → verify schema → sqlx migrate revert → verify
                it returned to the previous state → sqlx migrate run again.

APPLY           sqlx migrate run → sqlx migrate info (shows applied) → cargo build (no errors).
                (Apply/rollback sequence + commands: migration-safety-checklist.md.)

REGENERATE      sqlx prepare → verify SQLX_OFFLINE=true cargo build → commit .sqlx/ with the migration.
```

**Exit criteria:** migration reviewed, rollback tested, applied and verified (`sqlx migrate info`),
offline cache regenerated and committed, `SQLX_OFFLINE=true cargo build` passes.

## State Block

```
<sqlx-migration-state>
phase: PLAN | CREATE | REVIEW | TEST_ROLLBACK | APPLY | REGENERATE_CACHE | COMPLETE
migration_name: [name]
database: postgresql | mysql | sqlite | unknown
migration_file: [path to .sql file]
sql_reviewed: true | false
rollback_tested: true | false
migration_applied: true | false
cache_regenerated: true | false
build_status: pass | fail | not-run
data_loss_risk: none | low | medium | high
locking_risk: none | low | medium | high
last_action: [description]
next_action: [description]
</sqlx-migration-state>
```

## Output Template

- **Migration review report, post-apply verification** — `references/output-templates.md`.
- **Per-operation locking/data-loss detail (DROP, ALTER TYPE, ADD COLUMN NOT NULL, CREATE INDEX, …)** — `references/dangerous-operations.md`.
- **Pre/post-apply checklists, rollback sequence, sqlx command reference, `.sqlx/` management** — `references/migration-safety-checklist.md`.
- **Principle table, KB lookups, discipline rules, anti-patterns, error recovery** — `references/conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `rust-feature-slice` | When a feature needs database tables, this skill provides the migration lifecycle; the feature's service uses `sqlx::query!` against the migrated schema. |
| `rust-architecture-checklist` | Verifies `sqlx::query!` macros are used (not raw SQL strings) and the offline cache is committed. |
| `rust-security-review` | Checks for SQL injection via `format!()` in SQL contexts; this skill enforces parameterized queries. |
| `ef-migration-manager` | Parallel skill for .NET/EF Core — same safety philosophy, different tooling. |
| `alembic-migration-manager` | Parallel skill for Python/Alembic — same safety philosophy, different tooling. |
