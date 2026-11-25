---
name: sql
description: "SQL and relational-database engineering with dialect branches for Postgres, MySQL, Oracle, and SQLite. Load whenever writing, editing, or reviewing SQL: a .sql file, a schema migration, a raw query embedded in application code, index/EXPLAIN/tuning work, or stored procedures/triggers. NOT for ORM entity mapping where no SQL is written (that is /be), and NOT for analytics/warehouse modeling (that is /data)."
---

# SQL (language skill)

A knowledge skill, not an agent: it loads from context whenever SQL is being written or
reviewed. Role agents (/be, /dba, /rev, /arch) route into it; it carries the language,
the dialect references carry the engines.

## Trigger

Load this skill when:
- Editing or creating a `.sql` file
- Writing or reviewing a schema migration
- A raw SQL string is embedded in application code, in any host language — `sqlx`/
  `rusqlite` in Rust, `JdbcTemplate` or `@Query(nativeQuery = true)` on the JVM, `sql`
  tagged templates in JS/TS, DB-API strings in Python
- Designing an index, reading an `EXPLAIN` plan, or tuning a query shape
- Writing stored procedures, triggers, or views

Do NOT load for:
- ORM entity mapping where no SQL string is written — that is /be
- Analytics / warehouse / dbt modeling — that is /data

## Context

SQL is code that happens to run in someone else's engine. It is reviewed like code, planned
like code, and versioned like code — the fact that it executes inside a database server
changes none of that. This skill enforces three outcomes: no injection surface anywhere a
value meets a statement, no silent schema drift between what the migrations say and what the
database is, and no query shape merged without plan evidence.

## Documentation Lookup (MANDATORY)

Features are version-gated. A statement that parses on your laptop can fail — or silently
behave differently — on the deployed server. **Verify the target server's actual version
before using a feature**, with a live check, not the project README.

| Feature (examples) | Requires |
|---|---|
| `uuidv7()`, B-tree skip scan | PostgreSQL 18+ |
| Additional `ALGORITHM=INSTANT` ALTER variants | MySQL 8.0.29+ |
| `BOOLEAN` type, DDL `IF [NOT] EXISTS` | Oracle 23ai+ |
| Enforced `CHECK` constraints | MySQL 8.0.16+ (parsed-and-ignored before that) |
| `STRICT` tables | SQLite 3.37+ |
| `RETURNING` | SQLite 3.35+ |

Version-check one-liners:

| Dialect | Check |
|---|---|
| Postgres | `SELECT version();` |
| MySQL | `SELECT @@version;` |
| Oracle | `SELECT banner_full FROM v$version;` |
| SQLite | `SELECT sqlite_version();` |

Current major lines (verify at write time — these drift):
- **PostgreSQL 18** (2025-09).
- **MySQL** — 8.4 is the widely deployed LTS baseline; 9.7 the current LTS; 26.x the
  calendar-versioned Innovation line.
- **Oracle AI Database 26ai** — the 23ai family renumbered; on-prem GA January 2026.
- **SQLite 3.51.3+** (2026-03, contains a WAL-reset database-corruption fix).

Use Context7 MCP / WebSearch for the target dialect and version before relying on any
feature or default you have not verified on that version.

> **Volatility note.** Managed platforms (RDS/Aurora, Cloud SQL, serverless Postgres
> offerings, hosted MySQL forks) often run one or two major versions behind the current
> release, and gate, rename, or pre-tune features. The version check above runs against
> the *deployed* server — that answer wins over any changelog.

## Dialect selection (read first)

| Engine | Detect | Load |
|---|---|---|
| Postgres | `postgres`/`postgresql` driver or DSN, `plpgsql`, `pg_` catalog queries | `references/postgres.md` |
| MySQL / MariaDB | `mysql` driver, `jdbc:mysql:`, InnoDB DDL clauses | `references/mysql.md` |
| Oracle | `oracle` driver, `jdbc:oracle:thin:`, PL/SQL blocks | `references/oracle.md` |
| SQLite | file-based DB; `rusqlite` / `better-sqlite3` / `node:sqlite` / `sqlite-jdbc` | `references/sqlite.md` |
| Any — reviewing SQL or migrations | /rev context, PR with `.sql` or embedded SQL in the diff | `references/sql-review.md` |

SQLite embedded from Rust also has a dedicated embedding reference on the Rust side:
`../rust/references/sqlite-rusqlite.md` (connection setup and pooling in code; the engine
semantics stay in `references/sqlite.md`).

Two edge rules:
- A repo can be multi-dialect — a server engine plus embedded SQLite for local state is
  common. Load each branch for the files that touch it; do not average the dialects.
- ORM-*generated* SQL is /be's concern right up until someone writes or overrides a
  statement by hand — from that moment the statement is this skill's artifact like any
  other, review rules included.

## The altitude contract

Three altitudes, one owner each:

- **/arch** decides which engines and topologies exist — one Postgres vs Postgres-plus-cache,
  sharding, multi-region. Its reference:
  `../../../architecture/solution-architect/references/data-and-storage.md`.
- **This skill** owns the committed SQL artifacts — queries, DDL, migration files, their
  correctness, their plans, their dialect semantics.
- **/dba** operates the engine — executes risky migrations on live tables,
  replication/backup/vacuum/pooling, production plan regressions.

Boundary examples:
- This skill writes the expand-migrate-contract migration files; **/dba** runs the
  online-schema-change play on the two-terabyte table.
- This skill reads `EXPLAIN` before merge; **/dba** chases the plan that regressed in
  production.
- Transaction scope and isolation chosen *in the code* are this skill; connection-pool
  sizing and server tuning that make those choices survive load are **/dba**.
- Vector/ANN index tuning belongs to /dba's
  `../../data/dba/dba/references/vector-db-tuning.md` — link to it, never duplicate it.

## Core standards (BLOCKING at review)

**1. SQL is code.**
Every statement lives in the repo, is reviewed like code, and lints clean (sqlfluff 4.x);
nothing is pasted from a REPL into production. A statement that exists only in a session
history is unreviewable, unrepeatable, and unrevertable.

```bash
pipx install sqlfluff
sqlfluff lint --dialect postgres <paths>    # or: mysql | oracle | sqlite
```

**2. Parameterized-only.**
Values enter via bind parameters, always — string-assembled SQL is a BLOCKING finding.
Identifiers (table/column names) cannot be bound: map them through a static allowlist, never
through user input. `LIKE` patterns escape `%` and `_` before binding.

```text
BAD  (BLOCKING)   "SELECT * FROM users WHERE email = '" + email + "'"
GOOD              "SELECT id, email FROM users WHERE email = ?"    bind(email)
ORDER BY column   sort_col = ALLOWED_SORTS[input]    -- static map; identifiers can't be bound
LIKE pattern      bind("%" + escape_like(term) + "%")  -- escape % and _ inside term
```

**3. Migrations are versioned and linear.**
Timestamp- or sequence-numbered files; the applied set is tracked **in the database**
(`schema_migrations` table; `PRAGMA user_version` for SQLite); an applied migration is never
edited — a fix is a new migration. The repo states its rollback policy: the default is
forward-only with restore-tested backups; write down-migrations only if you actually
rehearse them, because an unrehearsed down-migration is a second untested change.
Concurrent branches can mint colliding numbers — the branch that merges second renumbers;
the in-database applied set is what makes a collision loud instead of silent.

**4. Expand-migrate-contract for anything a live app reads.**
Additive change first → dual-write/backfill (batched) → switch reads → contract in a later
release. `NOT NULL` and type changes are always staged: add nullable → backfill → validate →
enforce. The one-release big-bang ALTER is how a deploy takes the product down.

```text
release N:    ADD COLUMN new_col NULL                  (expand — additive, instant)
release N:    dual-write from the app; backfill in batches
release N+1:  switch reads to new_col; validate no NULLs remain
release N+2:  enforce NOT NULL; drop the old column    (contract)
```

**5. Transaction scope is deliberate.**
One unit of work per business action; never a user or network wait inside an open
transaction; the isolation level is chosen and commented wherever it matters; retries on
serialization failure exist wherever SERIALIZABLE (or snapshot conflicts) can fire. A
transaction held across an HTTP call is a lock held across someone else's outage. The
comment shape when isolation matters:

```sql
-- REPEATABLE READ: balance check and debit must see one snapshot.
-- Serialization-failure retry lives in the caller (max 3 attempts).
```

**6. EXPLAIN-before-merge.**
Every new query shape ships with plan evidence at realistic cardinality — a hundred-row dev
table lies about everything (the planner seq-scans it, and is right to). The
scratch-container check below is the cheap way to get honest evidence before merge.

**7. Every index is justified.**
The migration adding an index names the query it serves, in a comment; unused indexes get
removed — each one taxes every write. The N+1 workflow: dev-environment query logging on; a
loop containing a query is a review smell; fix with joins, batched `IN`, or window functions.

**8. NULL is a third truth value.**
Every predicate over a nullable column is reviewed for NULL behaviour: `NOT IN` with a NULL
in the subquery returns nothing; aggregates skip NULLs; `= NULL` is never true; and
UNIQUE-with-NULLs differs per dialect — Postgres, MySQL, and SQLite allow repeated NULLs
in a UNIQUE column (Postgres 15+ can opt out with `NULLS NOT DISTINCT`), while Oracle does
not index an all-NULL key at all; the dialect references carry the details. If you have not
stated what a NULL does to the predicate, you have not finished the query.

**9. Test data is managed.**
Deterministic factories/fixtures; each test isolated by a rolled-back transaction or a
throwaway schema; never production dumps with PII — a test database is not an exemption from
data protection.

**10. Zero schema drift.**
Migrations are the single source of truth for schema. Any second DDL surface — ORM model
definitions, bootstrap `IF NOT EXISTS` blocks — is verified equal to migration-head by a
test, or removed. Two schema sources become two answers to "what does this table look like",
and the stale one is always the one someone reads. The test shape: dump the migrated schema
and the second surface's schema, normalize, diff — an empty diff or a red build.

## The scratch-container empirical check

A conclusion *reasoned* from code about what rows will do — which end a `LIMIT` truncates,
what a NULL does to a predicate, whether two columns can desync — is a hypothesis until it
runs. This extends the `verify-landed` precedent: a scratch database and four lines of SQL
settle in ninety seconds what argument gets wrong across several rounds. Build the smallest
table that can exhibit the question, then ask it.

Reach for it whenever the open question is one of:
- which end a `LIMIT` truncates when the `ORDER BY` has no tiebreaker
- what a NULL does to a predicate, an aggregate, or a unique constraint
- what `ON CONFLICT` / upsert actually does to the non-listed columns
- collation, case, or truncation behaviour on the target version
- what a trigger fires on — and what it sees in `old`/`new`

Rules of the check:
- Never run it against a shared dev server — the point is a throwaway engine at a known
  version, matching the deployment target.
- Seed data deterministically inside the heredoc; the reviewer must be able to rerun the
  exact check from the PR text.
- Paste the output into the PR next to the claim it supports. Reasoning that was never
  executed is labelled as reasoning.

### Postgres

The password is not optional — the official image refuses to start without
`POSTGRES_PASSWORD`, so a bare `docker run postgres` fails and the check never happens.

```bash
docker run --rm -d --name scratch-pg -e POSTGRES_PASSWORD=scratch postgres:18
until docker exec scratch-pg pg_isready -U postgres -q; do sleep 1; done
docker exec -i scratch-pg psql -U postgres -v ON_ERROR_STOP=1 <<'SQL'
-- build the smallest table that can exhibit the question, then ask it
CREATE TABLE t (id int PRIMARY KEY, v text);
INSERT INTO t VALUES (1, NULL), (2, 'x');
SELECT count(*) FROM t WHERE v NOT IN (SELECT v FROM t);   -- 0: NULL poisons NOT IN
SQL
docker rm -f scratch-pg
```

### MySQL

Initialization takes tens of seconds — poll before piping SQL, or the check silently runs
against a server that is not up yet.

```bash
docker run --rm -d --name scratch-my -e MYSQL_ROOT_PASSWORD=scratch mysql:8.4
until docker exec scratch-my mysqladmin ping -uroot -pscratch --silent 2>/dev/null; do sleep 2; done
docker exec -i scratch-my mysql -uroot -pscratch <<'SQL'
CREATE DATABASE scratch;
USE scratch;
-- smallest table that can exhibit the question, then ask it
SQL
docker rm -f scratch-my
```

### SQLite

No container needed — the engine is a binary on your machine.

```bash
sqlite3 :memory: <<'SQL'
CREATE TABLE t (id INTEGER PRIMARY KEY, v TEXT) STRICT;
INSERT INTO t VALUES (1, NULL), (2, 'x');
SELECT count(*) FROM t WHERE v NOT IN (SELECT v FROM t);
SQL
```

### Oracle

`gvenzl/oracle-free` is an example image, not an endorsement; the licence terms are
Oracle's. The first pull is multiple gigabytes and startup takes minutes. If no Oracle
instance is reachable and the pull is not worth it, **skipping the empirical check for
Oracle is acceptable — say so** ("unverified on Oracle") rather than guessing and
presenting the guess as a result.

```bash
docker run --rm -d --name scratch-ora -e ORACLE_PASSWORD=scratch gvenzl/oracle-free
until docker exec scratch-ora healthcheck.sh 2>/dev/null; do sleep 10; done
docker exec -i scratch-ora sqlplus -s system/scratch@localhost/FREEPDB1 <<'SQL'
-- smallest table that can exhibit the question, then ask it
SQL
docker rm -f scratch-ora
```

## Templates

### Migration file header

Every migration file starts with this header. A migration whose header cannot be filled in
is a migration whose consequences have not been thought through.

```sql
-- migration: 20260809143000_orders_status_index
-- purpose:   open-orders dashboard list; the status+created_at scan was sequential
-- phase:     expand (contract: none — additive only)
-- index:     idx_orders_status_created serves
--            SELECT ... FROM orders WHERE status = $1 ORDER BY created_at DESC LIMIT $2
-- locks:     CREATE INDEX CONCURRENTLY — no table-level write lock expected
-- rollback:  forward-only (repo policy); DROP INDEX CONCURRENTLY is the rehearsed undo
CREATE INDEX CONCURRENTLY idx_orders_status_created
    ON orders (status, created_at DESC);
```

### Applied-set tracking table

```sql
-- The one legitimate IF NOT EXISTS: the tracker's own bootstrap.
CREATE TABLE IF NOT EXISTS schema_migrations (
    version    VARCHAR(64) PRIMARY KEY,  -- the migration file's timestamp/sequence id
    applied_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

SQLite projects use `PRAGMA user_version` instead — the pattern is in
`references/sqlite.md`.

### Batched backfill

```sql
-- One bounded batch, keyed by a PK range — the portable shape. (A LIMIT subquery
-- over the target table is NOT portable: MySQL rejects updating a table selected
-- in its own subquery (error 1093), and Oracle has no LIMIT.) The runner advances
-- :last_id by the range width each pass until past MAX(id), pausing between
-- batches and watching replica lag. Never one UPDATE across the whole table:
-- that is one giant transaction, one giant lock, one giant replication event.
UPDATE orders SET status_v2 = status
WHERE status_v2 IS NULL
  AND id >  :last_id
  AND id <= :last_id + 10000;
```

### Keyset pagination

```sql
-- First page
SELECT id, created_at, title FROM posts
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Next page: strictly after the last row seen — cost independent of depth,
-- and the (created_at, id) tiebreaker makes the ordering deterministic.
SELECT id, created_at, title FROM posts
WHERE (created_at, id) < ($1, $2)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Row-value comparison `(a, b) < ($1, $2)` works on Postgres and SQLite (3.15+). MySQL
parses it but does not use the composite index for it, and Oracle rejects it outright —
on those two, write the expanded form:

```sql
WHERE created_at < :1 OR (created_at = :1 AND id < :2)
```

## Workflow note

This skill owns no gates. Schema/migration changes are an `ARCH_APPROVED` trigger in the
workflow — the `workflow-engine` decides whether the gate fires, and /dba reviews migration
safety when it does. New query shapes carry their `EXPLAIN` evidence into the code review;
the reviewer's pass is `references/sql-review.md`.

Proportionality still applies: a one-line fix to an existing query does not summon the full
gauntlet. But a migration — any migration — at least states its lock expectation and its
rollback stance, because those are the two questions the incident review will ask.

## Checklist

**Before writing**
- [ ] Target server version confirmed with a live check, not assumed
- [ ] The dialect reference for the target engine loaded
- [ ] NULL and failure cases listed for every predicate over a nullable column
- [ ] Plan expectation stated ("index scan on X", "hash join at N rows")

**Before merge**
- [ ] `sqlfluff lint` clean on the correct dialect
- [ ] `EXPLAIN` output at realistic cardinality attached to the PR
- [ ] Any claim about row behaviour backed by a scratch check — or explicitly labelled
      unverified, with the reason
- [ ] Migration linear — no renumbering, no edits to applied files — with a complete header
- [ ] Backfills batched, with a stated batch size and pause between batches

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|---|---|---|
| Implicit cast in a predicate (string literal against an int column, mismatched collation) | The cast applies per-row and silently disables the index | Match bind types to column types; check the plan for a cast node |
| `SELECT *` in production code | Fetches unneeded columns, breaks on schema change, defeats covering indexes | Name the columns — the query states its contract |
| `NOT IN (SELECT nullable_col ...)` | One NULL in the subquery makes the whole predicate return zero rows | `NOT EXISTS`, or `WHERE col IS NOT NULL` inside the subquery |
| `UPDATE`/`DELETE` without `WHERE` | One statement rewrites or empties the whole table | Always a `WHERE`; a deliberate full-table write carries a comment saying so |
| OFFSET pagination at depth | `OFFSET n` scans and discards n rows — page cost grows with page number | Keyset pagination: `WHERE (created_at, id) < ($1, $2) ORDER BY ... LIMIT` |
| Per-row autocommit loop | One transaction (and often one fsync) per row — orders of magnitude slower | One transaction around the batch, or multi-row statements |
| EAV (entity-attribute-value) where columns belong | No types, no constraints, joins on strings, nothing indexable | Real columns; JSON for the genuinely dynamic remainder |
| A JSON blob where columns belong | Queried fields buried in JSON lose types, constraints, and index access | Promote queried fields to columns or indexed generated columns |
| `ORDER BY` without a deterministic tiebreaker under `LIMIT` | Rows with equal keys order arbitrarily — pagination skips and repeats rows | Append a unique column: `ORDER BY created_at, id` |
| Editing an applied migration | Databases that already ran it silently diverge from the file | Applied files are immutable; the fix is a new migration |
| Leading-wildcard `LIKE '%term%'` as the only search plan | Cannot use a B-tree index — a full scan on every search | Full-text search (tsvector / FULLTEXT / FTS5) or a trigram index |
| Timestamps without a timezone policy | A naive timestamp means whatever each writer meant | Store UTC; one documented policy per database; timezone-aware types where the dialect has them |
| Unbounded `IN` lists | Thousand-element lists blow parse/plan cost and driver parameter limits | Array binds (`= ANY($1)`), a values/temp-table join, or batched chunks |
| Bootstrap `CREATE TABLE IF NOT EXISTS` as the migration story | Existing installs never get altered — every install diverges silently | Versioned migrations; `IF NOT EXISTS` only for the migration tracker itself |

## Deep-dive references (load on demand)

Load the branch the current file touches — not the whole directory.

- `references/postgres.md` — Postgres semantics: MVCC/vacuum implications for SQL, lock-aware
  DDL, plan reading, PG-specific features by version.
- `references/mysql.md` — MySQL/InnoDB semantics: online DDL algorithms, gap locking,
  replication-aware migration constraints.
- `references/oracle.md` — Oracle semantics: PL/SQL, DDL auto-commit, optimizer behaviour,
  23ai/26ai feature gates.
- `references/sqlite.md` — SQLite semantics: single-writer/WAL, the per-connection pragma
  contract, `user_version` migrations, STRICT tables, FTS5.
- `references/sql-review.md` — the reviewer's pass: no-config lint/grep commands, migration
  checklist, fixed severity mapping.
- `../rust/references/sqlite-rusqlite.md` — embedding SQLite from Rust (driver-side
  templates; pairs with `references/sqlite.md`).
- `../../data/dba/dba/references/vector-db-tuning.md` — /dba's ANN/vector index tuning; link,
  never duplicate.
- `../../../architecture/solution-architect/references/data-and-storage.md` — /arch's
  engine and topology decisions this skill implements but does not make.
