---
name: orm-overview
description: Use when choosing a database access layer across Go, Python, TS/JS — covers sqlc/sqlx, SQLAlchemy, Prisma, Drizzle; query-builders vs full ORMs.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: database
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [sql, postgres, migrations-overview, php-doctrine]
---

# ORM Overview

**Iron Law: ORMs save typing, not architecture. Push schema-of-record into the database. Prefer query-builders (sqlc/sqlx/drizzle) over full ORMs (SQLAlchemy/Prisma) when the team can write SQL.**

An ORM hides SQL — convenient until you need to debug a 200ms query that the ORM generated as a Cartesian disaster. A query-builder hides drivers and typos but lets you read the SQL. Full ORMs justify themselves only when you genuinely need unit-of-work, dirty tracking, and identity map; most apps don't.

## Tool comparison

| Tool            | Language  | Type-safety                    | Magic level                                     | Raw-SQL escape                  | Pick when                                                |
| --------------- | --------- | ------------------------------ | ----------------------------------------------- | ------------------------------- | -------------------------------------------------------- |
| **sqlx** (Rust) | Rust      | compile-time, against live DB  | low                                             | native (`sqlx::query!`)         | Rust app; want compile-time SQL checks                   |
| **SQLAlchemy**  | Python    | runtime (mypy plugin helps)    | high (unit of work, identity map, lazy loading) | `text()` + `connection.execute` | Python app, complex domain, need UoW                     |
| **Prisma**      | TS / Node | compile-time, generated client | high (managed schema, generated client)         | `$queryRaw`                     | Greenfield TS app, want best DX                          |
| **Drizzle**     | TS / Node | compile-time, schema in TS     | low (query-builder shape)                       | `db.execute(sql\`…\`)`          | TS app, team can read SQL, wants type-safe SQL-shape API |

**Honourable mention**: `sqlc` (Go/Python/Kotlin) — generates type-safe code from `.sql` files. The SQL _is_ the source of truth. For Go, `Skill(devkit:go-sqlc)` covers it in depth.

## sqlx (Rust)

```rust
let row = sqlx::query!("SELECT id, email FROM users WHERE id = $1", id)
    .fetch_one(&pool).await?;
```

- **Strength**: `query!` macro checks SQL against the live database at compile time. No models, no abstraction — you write SQL, types are inferred from the schema. Async-first.
- **Weakness**: needs `DATABASE_URL` at compile time (or offline mode via `sqlx prepare`). No relationship traversal magic — you JOIN explicitly.
- **Gotcha**: `query!` vs `query_as!` — the former returns an anonymous struct, the latter maps to a named one. Pick `query_as!` for anything passed across function boundaries.

## SQLAlchemy (Python)

```python
session.execute(
    select(User).where(User.email == email).options(selectinload(User.orders))
)
```

- **Strength**: most expressive ORM out there. SQLAlchemy 2.0's typed `select()` is genuinely good. Unit of work, identity map, sophisticated relationship loading strategies.
- **Weakness**: largest surface area of any tool here. Lazy loading is on by default and N+1s are the most common production bug. The relationship API is a career's worth of footguns.
- **Patterns**: Use `selectinload` (separate IN query) for collections, `joinedload` (JOIN) for to-one. Set `lazy="raise"` on every relationship to ban lazy loading entirely — force explicit loading at query time.
- **Async**: use `AsyncSession` + `await session.execute(...)`. Don't mix sync and async sessions.

## Prisma (TS)

```ts
const user = await prisma.user.findUnique({
  where: { id },
  include: { orders: { take: 10 } },
});
```

- **Strength**: best DX of any TS option. Generated client is fully typed. Migrations integrated. Studio (`prisma studio`) is a usable GUI.
- **Weakness**: Prisma owns the schema dialect — features Postgres has that Prisma doesn't model (partial indexes with complex conditions, exclusion constraints, some constraint types) fall back to raw migration SQL, breaking the schema-as-source-of-truth promise. Generated queries can be inefficient (especially `include` fan-outs) — read the SQL via `$queryRaw` or `prisma.$on('query', …)`.
- **Patterns**: `include` for one-shot reads, separate queries for paginated children, `$queryRaw` for anything Prisma can't express cleanly.

## Drizzle (TS)

```ts
const users = await db
  .select()
  .from(usersTable)
  .leftJoin(ordersTable, eq(ordersTable.userId, usersTable.id))
  .where(eq(usersTable.id, id));
```

- **Strength**: query-builder, not an ORM. SQL shape is visible in the code. Schema is TS, migrations diff TS → SQL. Type-safe end-to-end. Fast.
- **Weakness**: no unit of work, no identity map — by design. Relations API (`db.query.users.findMany({ with: { orders: true } })`) is more ergonomic but generates LATERAL JOINs that surprise some teams.
- **Patterns**: query-builder (`.select().from(...)`) when you want SQL-shape; relations API for nested reads. Both produce one query — no lazy loading exists.

## Decision matrix

| Situation                                         | Reach for                              |
| ------------------------------------------------- | -------------------------------------- |
| Greenfield TS, team values DX                     | Prisma                                 |
| TS, team can write SQL, wants visible queries     | Drizzle                                |
| Python, simple CRUD app                           | SQLAlchemy Core + Alembic              |
| Python, rich domain model with unit-of-work needs | SQLAlchemy ORM 2.0                     |
| Rust, want compile-time SQL checks                | sqlx                                   |
| Go, SQL-first                                     | sqlc (see `Skill(go-sqlc)` if present) |
| Polyglot org, want one schema source-of-truth     | Atlas + per-language thin clients      |

## Anti-patterns (common across all four)

- **Lazy loading in tight loops.** `for user in users: print(user.orders)` is N+1 regardless of ORM. See `Skill(sql)`.
- **ORM magic that hides query cost.** Log every query in dev. Count queries per request in tests (`assertNumQueries(2)`).
- **Mixing two ORMs in one app.** Two transaction scopes, two identity maps, double the schema drift surface. Pick one.
- **Fighting the ORM.** When the ORM can't express what you need cleanly, drop to raw SQL (`$queryRaw`, `text()`, `db.execute`, `sqlx::query`) and move on. Don't spend a day defeating the query builder.
- **Using ORM models as API DTOs.** Couples wire format to schema; every column change is a breaking API change. Separate types at the boundary.
- **Application-level cascades / soft-delete instead of DB constraints.** The DB is the last honest guard. ORM-only invariants get violated by every script that bypasses the ORM.
- **`SELECT *` via the ORM.** Every ORM does this by default; every ORM lets you scope it. Scope it for hot queries.
- **Trusting autogen migrations** without reading them. Alembic misses constraint changes; Drizzle and Prisma can generate destructive diffs for renames. Read every line — see `Skill(migrations-overview)`.

## Red flags

| Thought                                    | Reality                                                                                |
| ------------------------------------------ | -------------------------------------------------------------------------------------- |
| "I'll add an index later when it's slow."  | "Later" = a Sunday outage. Indices live alongside the query design.                    |
| "The ORM will figure out the right query." | Sometimes. The other times you ship a Cartesian product. Log queries.                  |
| "We need an ORM for productivity."         | You need a query layer with type-safety. That's often a query-builder, not a full ORM. |
| "We can swap ORMs later."                  | You won't. Pick deliberately; the schema/migration story is the lock-in.               |

## Hand-off

For SQL semantics the ORM is generating: `Skill(sql)`. For diagnosing slow ORM queries: `Skill(sql)`. For the migration tool that usually pairs with each ORM: `Skill(migrations-overview)`. For Postgres-specific schema/index/JSONB: `Skill(postgres)`.
