---
name: go-sqlc
description: Use when generating typed Go code from .sql files — sqlc.yaml config, query annotations, multi-package, integration with migrations.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [go-essentials, go-pgx, postgres]
---

# Go sqlc

**Iron Law: queries live in `.sql` files. `sqlc generate` produces typed Go. NEVER hand-edit the generated code — change the SQL and regenerate.**

## Why sqlc (vs ORM)

| Approach               | Verdict                                                                                                           |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **sqlc**               | you write SQL, get typed structs + methods; zero runtime overhead; compile-time errors when columns drift         |
| **GORM / ent**         | hides SQL; query generation is opaque; magic methods; runtime errors for typos; pick only if team allergic to SQL |
| **`database/sql` raw** | every query is a hand-rolled `rows.Scan` boilerplate factory — fine for ≤ 10 queries                              |

sqlc is the right answer for 90% of Postgres-backed Go services.

## Layout

```
yourapp/
├── internal/db/
│   ├── sqlc.yaml                # config
│   ├── migrations/              # versioned migrations (atlas/goose/dbmate)
│   │   └── 0001_users.sql
│   ├── queries/                 # input — your SQL
│   │   ├── users.sql
│   │   └── orders.sql
│   └── generated/               # output — DO NOT EDIT
│       ├── db.go
│       ├── models.go
│       └── users.sql.go
```

## sqlc.yaml

```yaml
version: "2"
sql:
  - engine: "postgresql"
    schema: "internal/db/migrations" # source of truth for types
    queries: "internal/db/queries"
    gen:
      go:
        package: "dbgen"
        out: "internal/db/generated"
        sql_package: "pgx/v5" # use pgx, not database/sql
        emit_interface: true # generates Querier — mockable
        emit_json_tags: true
        emit_pointers_for_null_types: true
        overrides:
          - db_type: "uuid"
            go_type: "github.com/google/uuid.UUID"
          - db_type: "timestamptz"
            go_type: "time.Time"
```

Pin `sqlc` version in `Makefile` or `tools.go` — generator differences create churn. Add `sqlc generate` to `make generate` and `make build`. CI runs it and fails if output is stale.

## Query annotations

```sql
-- name: GetUser :one
SELECT id, email, created_at FROM users WHERE id = $1;

-- name: ListUsersByOrg :many
SELECT id, email FROM users WHERE org_id = $1 ORDER BY created_at DESC LIMIT $2;

-- name: CreateUser :one
INSERT INTO users (email, org_id) VALUES ($1, $2)
RETURNING id, created_at;

-- name: DeleteUser :exec
DELETE FROM users WHERE id = $1;

-- name: BulkInsertEvents :copyfrom
INSERT INTO events (user_id, kind, payload) VALUES ($1, $2, $3);
```

| Annotation                              | Returns                                                     | Use                                                  |
| --------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------- |
| `:one`                                  | `(T, error)`                                                | exactly one row expected; `pgx.ErrNoRows` if missing |
| `:many`                                 | `([]T, error)`                                              | zero or more rows                                    |
| `:exec`                                 | `error`                                                     | INSERT/UPDATE/DELETE, no rows back                   |
| `:execrows`                             | `(int64, error)`                                            | rows affected matters                                |
| `:execresult`                           | `(sql.Result, error)`                                       | need `LastInsertId` etc.                             |
| `:copyfrom`                             | bulk insert using Postgres COPY — order-of-magnitude faster |
| `:batchone`, `:batchmany`, `:batchexec` | pgx batched queries (single round-trip)                     |

## Generated usage

```go
q := dbgen.New(pool)                   // pool is *pgxpool.Pool
user, err := q.GetUser(ctx, userID)
if errors.Is(err, pgx.ErrNoRows) { return nil, ErrNotFound }

// Constraint violations: same pgconn.PgError pattern as raw pgx — see `Skill(devkit:go-pgx)` for SQLSTATE codes (23505 unique, 23503 FK, 23514 check, 23502 not_null).

// Transactions — q.WithTx(tx) returns a fresh Querier
err = pgx.BeginTxFunc(ctx, pool, pgx.TxOptions{}, func(tx pgx.Tx) error {
    qt := q.WithTx(tx)
    if _, err := qt.CreateUser(ctx, dbgen.CreateUserParams{...}); err != nil { return err }
    return qt.LogEvent(ctx, dbgen.LogEventParams{...})
})
```

`emit_interface: true` produces a `Querier` interface — mock with [mockery](https://github.com/vektra/mockery) or hand-roll for tests. Real DB tests use testcontainers-go — see `Skill(devkit:go-testing)` for the `TestMain` pattern and `references/go-test-integration.md` for the full snippet.

## Multi-package configs

Need separate `Querier` per bounded context (users, orders, analytics)? Use multiple entries under `sql:`. Each gets its own package, its own queries dir, its own generated dir. Schema can be shared.

## Schema discovery — pointing at migrations

`schema:` accepts a directory of migration files OR a single dump. sqlc reads them in lexical order and builds its internal type catalog. Keep migrations forward-only and never edit a committed migration — change schema with a new file. Pair with `atlas`, `goose`, or `dbmate` for actual application.

## Anti-patterns

- Hand-editing files in `generated/` — diff-and-regenerate next CI run wipes you out
- Mixing sqlc + GORM in the same package — two truths about your schema
- Missing `make generate` step in build — drift between SQL and Go
- Query name = `:one` but multiple rows possible — runtime "multiple rows in result set"
- Putting business logic in the SQL (`CASE WHEN ... THEN bill_amount ...`) — move to Go
- `SELECT *` — sqlc can't infer column order stability; list columns explicitly
- Ignoring `pgx.ErrNoRows` because "the row should be there" — defensive `errors.Is` always
- Custom DB types without `overrides:` — sqlc gives you `interface{}` and you scan-cast at every call site

## Red flags

| Thought                                                  | Reality                                                                       |
| -------------------------------------------------------- | ----------------------------------------------------------------------------- |
| "I'll just edit the .go file"                            | Next `sqlc generate` deletes your change. Edit the .sql, regenerate.          |
| "We can write a quick ORM on top"                        | You're recreating ORM-rot one query at a time                                 |
| "Tests run against SQLite"                               | sqlc emits PG-specific SQL; SQLite mismatches are silent. Use testcontainers. |
| "Why does my Postgres array come back as `interface{}`?" | Missing `overrides:` — map it to `[]string` explicitly                        |

## Hand-off

For pool config + transactions + COPY: `Skill(go-pgx)`. For Postgres schema + indexes + EXPLAIN: `Skill(postgres)`. For test fixtures + testcontainers: `Skill(go-testing)`.
