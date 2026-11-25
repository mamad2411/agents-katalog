---
name: go-pgx
description: Use when accessing Postgres from Go with pgx/v5 — pgxpool sizing, prepared statements, COPY, transactions, TCP keepalives.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [go-essentials, go-sqlc, postgres]
---

# Go pgx / pgxpool

**Iron Law: one `*pgxpool.Pool` per process, lifecycle-managed. Size the pool deliberately, set TCP keepalives, use prepared statements. Never open a connection per request.**

## Pool setup

```go
cfg, err := pgxpool.ParseConfig(dsn)
if err != nil { return nil, fmt.Errorf("parse dsn: %w", err) }

cfg.MaxConns        = 25                    // see sizing below
cfg.MinConns        = 2
cfg.MaxConnLifetime = 1 * time.Hour
cfg.MaxConnIdleTime = 5 * time.Minute
cfg.HealthCheckPeriod = 30 * time.Second

// TCP keepalive — survive NAT/idle-timeout dropouts in cloud envs
cfg.ConnConfig.ConnectTimeout = 5 * time.Second
cfg.ConnConfig.RuntimeParams["application_name"] = "myservice"
cfg.ConnConfig.DialFunc = func(ctx context.Context, net_, addr string) (net.Conn, error) {
    d := &net.Dialer{KeepAlive: 10 * time.Second}   // probe every 10s
    return d.DialContext(ctx, net_, addr)
}

pool, err := pgxpool.NewWithConfig(ctx, cfg)
```

**TCP keepalive recipe (Linux): idle=10s, interval=5s, count=3** — connection dies after ~25s of no response, well before NAT drops it (typically 60s+). Set via `SO_KEEPALIVE` + `TCP_KEEPIDLE/INTVL/CNT` (use `golang.org/x/sys/unix` for the syscalls, or set `net.KeepAlivePeriod`).

## Sizing the pool

| Knob                | Rule of thumb                                                                                      |
| ------------------- | -------------------------------------------------------------------------------------------------- |
| `MaxConns`          | `min(cpu_cores * 2, db_max_connections / num_instances - headroom)` — typically 10-50 per instance |
| `MinConns`          | 2-5 to avoid cold-start spikes; 0 if cost-sensitive                                                |
| `MaxConnLifetime`   | 30m-1h — cycles through pgbouncer transparently, picks up TLS cert rotation                        |
| `MaxConnIdleTime`   | 1-5m — shed connections during low traffic                                                         |
| `HealthCheckPeriod` | 30s-1m — detects half-open connections                                                             |

Postgres `max_connections` default is 100. If you run 10 service instances at 25 each, you've already used 250 — increase Postgres or front with pgbouncer (transaction mode).

## Queries

```go
type User struct {
    ID    uuid.UUID `db:"id"`
    Email string    `db:"email"`
}

// Single row — check constraint violations BEFORE generic wrap so the typed errors fire
var u User
err := pool.QueryRow(ctx,
    `SELECT id, email FROM users WHERE id = $1`, id,
).Scan(&u.ID, &u.Email)
if errors.Is(err, pgx.ErrNoRows) {
    return nil, ErrNotFound
}
if err != nil {
    // Constraint violations: use pgconn.PgError + SQLSTATE codes
    // 23505 unique_violation, 23503 foreign_key_violation, 23514 check_violation, 23502 not_null
    var pgErr *pgconn.PgError
    if errors.As(err, &pgErr) {
        switch pgErr.Code {
        case "23505": return nil, ErrDuplicate
        case "23503": return nil, ErrFKViolation
        }
    }
    return nil, fmt.Errorf("get user %s: %w", id, err)
}

// Many rows — defer rows.Close() ALWAYS
rows, err := pool.Query(ctx, `SELECT id, email FROM users WHERE org_id = $1`, orgID)
if err != nil { return nil, err }
defer rows.Close()
users, err := pgx.CollectRows(rows, pgx.RowToStructByName[User])
```

`pgx.CollectRows` + `RowToStructByName` (v5+) is the modern path — no manual `for rows.Next()` boilerplate. Struct field `db:"col_name"` tags map columns when names diverge from field names (snake_case columns vs CamelCase fields).

## Bulk inserts — use COPY

```go
_, err := pool.CopyFrom(ctx,
    pgx.Identifier{"events"},
    []string{"user_id", "kind", "payload"},
    pgx.CopyFromSlice(len(events), func(i int) ([]any, error) {
        return []any{events[i].UserID, events[i].Kind, events[i].Payload}, nil
    }),
)
```

**COPY beats batched INSERTs by 10-100x for > 100 rows.** For ≤ 50, regular INSERT is fine.

## Transactions + isolation

```go
err := pgx.BeginTxFunc(ctx, pool, pgx.TxOptions{
    IsoLevel: pgx.Serializable,
}, func(tx pgx.Tx) error {
    if _, err := tx.Exec(ctx, `UPDATE accounts SET bal = bal - $1 WHERE id = $2`, amt, from); err != nil {
        return err
    }
    if _, err := tx.Exec(ctx, `UPDATE accounts SET bal = bal + $1 WHERE id = $2`, amt, to); err != nil {
        return err
    }
    return nil
})
```

`BeginTxFunc` auto-commits on nil error, rolls back otherwise — preferred over manual `Begin`/`Commit`. On `Serializable` you MUST retry on `40001 serialization_failure` — wrap with a retry loop (max 3 attempts, jittered backoff).

| Isolation                 | When                                                                   |
| ------------------------- | ---------------------------------------------------------------------- |
| `ReadCommitted` (default) | most reads; phantom reads acceptable                                   |
| `RepeatableRead`          | multi-statement read consistency within txn                            |
| `Serializable`            | money, inventory, anything with "lost update" risk — retry on conflict |

## Prepared statements

pgx auto-prepares statements (LRU cache, default 512). Don't fight it — let the same SQL string be reused and pgx caches the plan. For pgbouncer **transaction-mode**, set `cfg.ConnConfig.PreferSimpleProtocol = true` OR disable statement cache — otherwise prepared statements break across pooled connections.

## Anti-patterns

- Opening a connection per request (`pgx.Connect`) instead of pool — connection storm
- Missing `defer rows.Close()` — connection leak under errors
- Ignoring TCP keepalives in cloud (`KeepAlive: 10s`) — silent half-open connections after NAT drops
- Catching errors with `err.Error() == "..."` instead of `errors.Is(err, pgx.ErrNoRows)`
- `Serializable` without a retry loop — `40001` errors leak to user
- Building SQL with `fmt.Sprintf` — that's how injection enters the codebase, parameterize with `$1, $2`
- Holding a `*pgx.Conn` past the function boundary — leak; use `pool.Acquire` + `defer conn.Release()` if you must
- `MaxConns` left at default unchecked — saturates Postgres

## Red flags

| Thought                                | Reality                                                                        |
| -------------------------------------- | ------------------------------------------------------------------------------ |
| "It's fast on my laptop"               | Localhost has no NAT, no TLS overhead, no contention                           |
| "Just use `database/sql` + pgx driver" | You get half the pgx features; v5 native API is the win                        |
| "We'll add pgbouncer later"            | Add it before you have 200 connections; switching with prod traffic is painful |
| "Why is it failing every 5 minutes?"   | Cloud NAT idle-timeout — set keepalives                                        |

## Hand-off

For typed queries from `.sql` files: `Skill(go-sqlc)`. For Postgres index/EXPLAIN/tuning: `Skill(postgres)`. For request context plumbing: `Skill(go-essentials)`.
