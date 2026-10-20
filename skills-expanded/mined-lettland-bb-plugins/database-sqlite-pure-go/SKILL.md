---
name: database-sqlite-pure-go
description: Use when using SQLite from Go — modernc.org/sqlite (pure-Go) vs mattn/go-sqlite3; WAL mode, concurrency, migrations.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: database
  languages: [go]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [go-essentials, go-pgx, postgres, migrations-overview, infra-docker-images]
---

# SQLite from Go (pure-Go vs CGo)

**Iron Law: WAL mode + busy_timeout on every open. One writer ever — serialize writes or set `db.SetMaxOpenConns(1)` for the write pool. Pick the driver before you write a query — switching mid-project is rewriting the test matrix.**

**Versions:** SQLite `3.50.x` (embedded in driver) · `modernc.org/sqlite` v1.36+ · `mattn/go-sqlite3` v1.14+ — _Both drivers bundle SQLite — your "SQLite version" is whatever the driver shipped. Bump driver, bump SQLite._

## Driver choice — make it once, deliberately

|                       | `modernc.org/sqlite`                                | `mattn/go-sqlite3`                                                                      |
| --------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Implementation        | Pure Go (SQLite C transpiled to Go via `ccgo`)      | CGo binding to upstream SQLite C                                                        |
| `CGO_ENABLED=0`       | ✅ Works                                            | ❌ Won't compile                                                                        |
| Cross-compile         | Trivial (`GOOS=linux GOARCH=arm64 go build`)        | Needs cross-toolchain (`zig cc`, `xx-cc`); often painful                                |
| Docker image          | `FROM scratch` / distroless static — works          | Needs glibc base (`distroless/base-debian12`) or `CGO_ENABLED=1` build chain in builder |
| Performance           | ~30-50% slower on write-heavy benches               | Native C speed                                                                          |
| Memory                | Higher GC pressure (more allocations)               | Lower, C-side                                                                           |
| Concurrency model     | Same single-writer (SQLite enforces)                | Same                                                                                    |
| Build time            | Slow first build (compiles ~1M LOC of generated Go) | Fast                                                                                    |
| Binary size           | Larger (~10 MB driver weight)                       | Smaller (~2 MB + libsqlite linkage)                                                     |
| `database/sql` driver | `sqlite` (registered as `sqlite`)                   | `sqlite3`                                                                               |

**Pick `modernc.org/sqlite` when:**

- You want `CGO_ENABLED=0` (smaller Docker image, no glibc dependency, `FROM scratch` runtime)
- Cross-compiling for ARM (Apple Silicon dev → x86 prod, or x86 dev → ARM Pi/server)
- The workload is read-heavy or moderate write (CLI local state, config DBs, sqlite-as-feature-store)

**Pick `mattn/go-sqlite3` when:**

- Max throughput matters (heavy write workload, embedded analytics)
- You're already in a CGo build (cgo-linked image libs, geos, etc.)
- You need SQLite extensions that the modernc port doesn't include (some FTS5 tokenizers, certain custom funcs)

## Connection string — set the pragmas in the DSN

```go
import _ "modernc.org/sqlite"   // or: _ "github.com/mattn/go-sqlite3"

dsn := "file:./state.db?" + url.Values{
    "_journal_mode": {"WAL"},
    "_busy_timeout": {"5000"},        // ms
    "_synchronous":  {"NORMAL"},       // WAL durability default; FULL for tighter
    "_foreign_keys": {"1"},            // FK enforcement off by default — turn it on
    "_txlock":       {"immediate"},   // grab writer lock on BEGIN, avoids SQLITE_BUSY mid-tx
}.Encode()

db, err := sql.Open("sqlite", dsn)   // "sqlite3" for mattn driver
```

**modernc uses `_pragma_name`; mattn uses `_pragma_name` (same), but check the driver's docs — mattn supports `?cache=shared`, modernc handles it differently.** When in doubt, run a setup statement:

```go
for _, p := range []string{
    "PRAGMA journal_mode=WAL;",
    "PRAGMA busy_timeout=5000;",
    "PRAGMA synchronous=NORMAL;",
    "PRAGMA foreign_keys=ON;",
    "PRAGMA temp_store=MEMORY;",
} {
    if _, err := db.Exec(p); err != nil { return err }
}
```

## WAL mode — mandatory for any concurrent reader

Default journal mode is `DELETE` — writers block readers, readers block writers. WAL flips this:

- **Readers do not block writers.** Readers see a snapshot from when their transaction started.
- **Writers do not block readers.** A single writer at a time still applies; multiple writers serialize.
- **Three files on disk**: `state.db`, `state.db-wal`, `state.db-shm`. Backups need all three (or use SQLite's `.backup` / `VACUUM INTO`).

`PRAGMA journal_mode=WAL` is persistent — set once per DB file, survives reopens. Verify with `PRAGMA journal_mode;`.

**WAL gotcha — NFS / network filesystems**: WAL relies on shared-memory (`-shm` file) mmap'd across processes. NFS does not provide coherent shared memory. **Do not put a WAL-mode SQLite database on NFS.** Local disk only, or use a real RDBMS.

## busy_timeout — the only sane retry strategy

When the writer lock is held, other writers get `SQLITE_BUSY` immediately. `busy_timeout=5000` tells SQLite to retry-with-backoff internally for up to 5s before returning the error.

```go
// Without busy_timeout: every concurrent write returns SQLITE_BUSY, you implement retry
// With busy_timeout=5000: SQLite handles the wait; you only see SQLITE_BUSY after 5s of contention
```

5s is a reasonable default for batch workers; lower (500ms-1s) for user-facing requests where you'd rather fail fast and let the client retry.

## Concurrency model — one writer

SQLite serializes writes at the database file level. **This is the central design fact.**

Implications:

- Multiple processes opening the same DB file contend on the writer lock. Fine for ≤ a few processes; falls apart at dozens.
- Within one process, multiple goroutines writing through `database/sql` will serialize at the SQLite level. The pool may show 10 connections but only one writes at a time.
- For tightly-contended writers, run the writes through a **single connection** to avoid `SQLITE_BUSY` thrash:

```go
writeDB, _ := sql.Open("sqlite", dsn)
writeDB.SetMaxOpenConns(1)         // serialize writes through one conn
writeDB.SetMaxIdleConns(1)

readDB, _ := sql.Open("sqlite", dsn + "&mode=ro")
readDB.SetMaxOpenConns(8)          // readers parallel under WAL
```

Two pools, one read-only — keeps writes from being blocked by long-running readers' connection use. The OS-level read concurrency stays parallel under WAL.

**`_txlock=immediate`** grabs the writer lock on `BEGIN` instead of waiting for the first write — turns mid-transaction `SQLITE_BUSY` into upfront contention, which is easier to retry around.

## In-memory for tests

```go
// Each Open gets its own DB
db, _ := sql.Open("sqlite", "file::memory:?cache=shared")

// Or named, shared across opens in same process
db, _ := sql.Open("sqlite", "file:test_db?mode=memory&cache=shared")
```

In-memory + `cache=shared` is the testing pattern — every test gets an isolated DB via `t.TempDir()` for file-backed tests, or named in-memory for tests that genuinely need fresh schema per case.

**Run schema migrations in `TestMain` or per-test setup.** SQLite has no `CREATE DATABASE` — migration is the schema bootstrap.

## Migrations — pick a tool

| Tool                       | Notes                                                              |
| -------------------------- | ------------------------------------------------------------------ |
| **golang-migrate/migrate** | Versioned `up`/`down` SQL files; widely used; native SQLite driver |
| **pressly/goose**          | Versioned, supports Go-defined migrations alongside SQL            |
| **rubenv/sql-migrate**     | Library + CLI, embeddable                                          |
| **atlas (ariga.io/atlas)** | Declarative schema (HCL/SQL diffing); heavier but powerful         |

For embedded apps shipping their own DB, **embed migrations** with `//go:embed migrations/*.sql` and run on startup. No external migration binary required at deploy time.

```go
//go:embed migrations/*.sql
var migrationsFS embed.FS

func migrate(db *sql.DB) error {
    src, _ := iofs.New(migrationsFS, "migrations")
    m, _ := migrate.NewWithSourceInstance("iofs", src, "sqlite://./state.db")
    return m.Up()
}
```

## Common gotchas

- **NFS / SMB / FUSE filesystems** break WAL's shared-memory assumptions — corruption follows. Local disk only.
- **Multiple processes writing the same DB** at high rate — single-writer contention crushes throughput. Move to Postgres or partition by process.
- **Forgetting `PRAGMA foreign_keys=ON`** — FK constraints DEFINED in schema are silently NOT enforced (SQLite default for backward compat). Set the PRAGMA on every connection (it's per-connection, not per-file).
- **Backup with `cp` while the DB is open** — captures inconsistent state. Use `VACUUM INTO 'backup.db'` or the SQLite `.backup` API for live backup.
- **`SELECT` holds a transaction open** if you don't iterate to completion or `Close()` the rows — under WAL this pins WAL frames and grows the `-wal` file. Always `defer rows.Close()`.
- **WAL file grows unbounded** under read-heavy + steady writes — schedule `PRAGMA wal_checkpoint(TRUNCATE)` periodically or set `PRAGMA wal_autocheckpoint=1000` (default).
- **Cross-compile from macOS to Linux with mattn** — needs `CC=zig cc -target x86_64-linux-musl` or similar; modernc avoids the whole problem.
- **Driver registration name mismatch** — `sql.Open("sqlite3", ...)` for mattn, `sql.Open("sqlite", ...)` for modernc. Easy typo, error is `unknown driver`.
- **Boolean column?** SQLite has no boolean type — stored as INTEGER 0/1. Scan into `*bool` works in both drivers, but raw `SELECT col` over CLI shows `0`/`1`.

## Hand-off

For PostgreSQL when SQLite stops scaling (multiple writers, network access, real concurrency): `Skill(postgres)`, `Skill(go-pgx)`. For migration-tool deep-dive: `Skill(migrations-overview)`. For Go idioms in general: `Skill(go-essentials)`. For shipping the binary in a distroless image (the main reason to pick modernc): `Skill(infra-docker-images)`.
