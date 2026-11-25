---
name: rc-sqlx
description: "Implements and reviews SQLx 0.8+ with PostgreSQL in Rust — PgPool, query/query_as, bind parameters, transactions, migrations, compile-time macros, database tests. Use when writing or changing SQLx/Postgres access from Rust. Do not use for Axum routing alone (rc-axum), SvelteKit (rc-sveltekit), Rust idioms (rc-rust), or non-Rust ORMs."
user-invocable: true
model: sonnet
effort: medium
---

# SQLx 0.8 + PostgreSQL

Async SQL for Rust without a heavy ORM. Target: **sqlx 0.8.x**, **PostgreSQL 16** (compatible with 14+). Complements `rc-sql` (general SQL design) and `rc-axum` (HTTP layer).

## Core workflow

1. **Schema first** — migrations under version control; no ad-hoc prod DDL from app code without a migration path.
2. **Pool** — one `PgPool` in app state; tune `max_connections` to VPS/DB limits.
3. **Queries** — always **bind** parameters (`$1`, `$2`); never `format!` user input into SQL.
4. **Mapping** — `query_as` / `FromRow` or compile-time `query_as!` when `DATABASE_URL` is available at build.
5. **Transactions** — multi-step writes use `pool.begin()` → commit/rollback.
6. **Security** — least-privilege DB role; secrets only in env. Read `references/security.md`.
7. **Test** — `sqlx::test` or isolated DB. Read `references/testing.md`.

## Reference guide

| Topic | File | Load when |
| ----- | ---- | --------- |
| Pool, query_as, transactions, macros | `references/guide.md` | Implementing queries |
| Injection, roles, secrets | `references/security.md` | Reviewing data access |
| Migrations (sqlx-cli / embed) | `references/migrations.md` | Schema changes |
| Integration tests | `references/testing.md` | DB tests |

## Must do

- Use **bound** parameters for all dynamic values (Postgres `$n`).
- Prefer `query_as::<_, T>` or `query_as!` into serde/FromRow structs.
- Set pool size consciously (small VPS: start with 5–10).
- Run migrations in deploy pipeline before app start (or controlled startup migrate).
- Map `sqlx::Error` to domain/HTTP errors without leaking SQL internals to clients.

## Must not do

- Share one long-lived transaction across HTTP requests.
- Use the superuser role for the app in production.
- Commit migrations that are not reversible or documented when data loss is possible.
- Ignore offline mode needs for CI (`SQLX_OFFLINE=true` + `.sqlx` data) if using macros without a live DB.

## Output template

1. Migration SQL (up, and down if required)
2. Rust types (`FromRow` / domain models)
3. Query functions (pool/tx receiver)
4. Error mapping
5. Tests + `cargo test` / sqlx prepare notes

## Related skills

- `rc-axum` — wire pool into `State`
- `rc-sql` — indexes, EXPLAIN, schema design depth
- `rc-observability` — slow query / pool metrics
