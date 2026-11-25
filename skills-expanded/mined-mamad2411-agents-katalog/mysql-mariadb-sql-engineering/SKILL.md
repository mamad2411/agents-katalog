---
name: mysql-mariadb-sql-engineering
description: MySQL and MariaDB SQL engineering guidance. Use with sql-engineering when adding, changing, reviewing, testing, or optimizing MySQL or MariaDB schemas, SQL queries, migrations, transactions, constraints, indexes, views, stored routines, replication, privileges, storage engines, connection pooling, or query performance in any language stack. Explicitly name which engine and version a change targets when MySQL and MariaDB diverge. Do not use for unchanged-SQL ORM or adapter mechanics. Use api-design when migrations or query outputs affect published contracts and observability-engineering for MySQL/MariaDB telemetry signals.
---

# MySQL And MariaDB SQL Engineering

Use this skill with [`sql-engineering`](../sql-engineering/SKILL.md) for
database-native MySQL and MariaDB work independent of the application language.
Let the database-neutral skill establish shared SQL behavior and use this skill
for MySQL/MariaDB-specific semantics. Use
[`postgresql-sql-engineering`](../postgresql-sql-engineering/SKILL.md) or
[`sqlite-sql-engineering`](../sqlite-sql-engineering/SKILL.md) instead when the
target engine is PostgreSQL or SQLite, and only for comparison here. Use
[`rust-persistence-sql`](../rust-persistence-sql/SKILL.md) for Rust SQLx or
SeaQuery adapter details against a MySQL/MariaDB backend.

MySQL and MariaDB forked from a shared codebase and remain close, but they are
no longer interchangeable: version numbers do not align, replication formats
diverge, and each has features the other lacks. Identify which engine and
version a change actually targets before relying on version-specific behavior.
Never assume a MariaDB fix or feature applies to MySQL, or the reverse.

## Use When

- Designing or reviewing tables, constraints, indexes, views, stored
  procedures/functions, triggers, migrations, transactions, privileges,
  replication topology, or storage engine choice.
- Writing or reviewing SQL queries, query plans (`EXPLAIN`), pagination, bulk
  operations, reporting queries, or data repair scripts.
- A change needs database correctness, performance, security, observability,
  or rollback evidence on MySQL or MariaDB.
- Deciding whether code must work identically on both engines, or is scoped to
  one.

Do not use this skill for generic in-memory domain logic, ORM-only API usage
with no SQL/schema behavior, or PostgreSQL/SQLite-specific behavior except when
comparing it to MySQL/MariaDB.

## Security Review Routing

Load [`security-review`](../security-review/SKILL.md) when MySQL/MariaDB work
touches user/role privileges, `DEFINER`-context views or routines, dynamic SQL
or injection risk, tenant isolation, audit logging, sensitive
migrations/backfills, data repair scripts, secrets (including
`.my.cnf`/connection strings), or production-data access. Pair it with
[`security-review-evidence`](../security-review-evidence/SKILL.md) when
evidence includes redacted SQL, `EXPLAIN`/`ANALYZE` output, schema diffs,
audit/log samples, dumps, or migration artifacts.

## API and Observability Routing

- Load [`api-design`](../api-design/SKILL.md) when MySQL/MariaDB migrations,
  views, stored routines, reporting outputs, or constraint-error mapping
  affect an external contract or compatibility promise.
- Load [`observability-engineering`](../observability-engineering/SKILL.md)
  when MySQL/MariaDB work changes slow-query log, migration, connection-pool,
  lock-wait, deadlock, replication-lag, or runbook signals.

## Workflow

1. Inspect the real database surface: migrations, schema dumps, SQL files,
   query builders, ORM mappings, seed data, test fixtures, migration tool,
   target engine (MySQL or MariaDB) and major/minor version, storage engines
   in use, replication topology, and CI database setup. Verify
   version-sensitive behavior in the official documentation for that target
   engine and version, not only the current documentation and not the other
   engine's documentation.
2. State the data behavior before implementation. Use BDD-style examples for
   observable rules such as uniqueness, authorization, lifecycle transitions,
   conflict handling, and partial-write prevention.
3. Model the boundary. Use DDD language for entities, value objects,
   aggregate-like consistency boundaries, repositories, and invariants. Do not
   let table shape leak into core domain APIs without a deliberate adapter.
4. Design schema and migration order: new objects, backfill, constraints,
   indexes, locks, deploy compatibility, rollback, and validation queries.
5. Implement SQL with bound parameters, explicit columns, deliberate
   transaction scope, and safe error mapping at the application edge.
6. Verify with the target engine and version: migration from empty database,
   migration from a representative previous schema, focused query tests, and
   `EXPLAIN`/`EXPLAIN ANALYZE` inspection for performance-sensitive paths.

## MySQL vs MariaDB: What Actually Diverges

Ranked by how often each difference causes an incident or a wrong assumption:

1. **Storage engine defaults and availability.** Both default to InnoDB for
   normal transactional tables. MariaDB also ships **Aria** (MyISAM's crash-safe
   successor, used for some system tables) and, in server builds that include
   it, **ColumnStore** for analytics. MySQL ships NDB Cluster (MySQL Cluster)
   as a separate product; MariaDB does not. Do not assume a storage engine
   available on one is available, or behaves the same, on the other.
2. **Replication and clustering.** MariaDB's **Galera-based multi-master
   clustering** (MariaDB Cluster) has no direct MySQL equivalent; MySQL's
   closest comparable is InnoDB Cluster/Group Replication, a different
   technology with different failure modes and operational tooling.
   Binlog formats and GTID implementations are not wire-compatible between the
   two engines even though both call the concept "GTID." Do not point one
   engine's replica at the other's binlog stream and expect it to work.
3. **JSON support.** MySQL 5.7+ has a native binary `JSON` column type with
   validation and indexed generated columns. MariaDB has **no native JSON
   type**: `JSON` is an alias for `LONGTEXT` with a `CHECK` constraint that
   validates JSON shape, and it lacks MySQL's binary storage and some JSON
   functions. A schema that relies on MySQL's compact JSON storage or a
   JSON-typed generated/virtual index will not behave the same on MariaDB.
4. **Window functions and CTEs.** MySQL added both in 8.0 (2018). MariaDB
   added both earlier, in 10.2 (2017). A query written against an old MySQL
   5.7 target cannot use either; check the actual minimum supported version on
   each engine independently, not "MySQL 8 or newer" as a stand-in for
   MariaDB.
5. **Optimizer and `EXPLAIN` output.** MariaDB has its own optimizer
   (including optimizer switches MySQL lacks, such as engine-condition
   pushdown tuning) and its own `EXPLAIN FORMAT=JSON` / `ANALYZE FORMAT=JSON`
   shape. MySQL 8.0.18+ supports `EXPLAIN ANALYZE` in a Postgres-like text tree
   format; MariaDB's `ANALYZE FORMAT=JSON` (10.1+) predates that and looks
   different. Do not copy `EXPLAIN` interpretation guidance across engines
   without checking the actual output shape.
6. **Authentication and user management.** MySQL 8 defaults to
   `caching_sha2_password`; MariaDB defaults to `mysql_native_password` (or
   `ed25519`/`unix_socket` in some builds). Client libraries and connection
   poolers must support the target engine's default auth plugin, or
   connections fail after an otherwise-compatible schema migration.
7. **System versioning and temporal tables.** MariaDB 10.3+ has built-in
   `SYSTEM VERSIONING` for temporal/history tables. MySQL has no equivalent;
   the same behavior requires application-level or trigger-based history
   tables.
8. **Invisible/instant columns and online DDL.** Both support some form of
   `ALGORITHM=INSTANT` column add (MySQL 8.0.12+, MariaDB 10.3+/10.4+
   depending on the operation), but the exact set of DDL operations eligible
   for instant/online execution differs by engine and version. Confirm the
   specific `ALTER TABLE` is actually instant/online on the target
   engine/version before assuming a large table migration is cheap.
9. **Licensing and distribution.** MySQL Community Edition is GPL; MySQL
   Enterprise Edition is proprietary. MariaDB is GPL/LGPL/BSD depending on
   component, with no proprietary tier. This affects which build a vendor or
   managed-cloud offering actually ships, and which features (e.g., MySQL
   Enterprise Audit, Enterprise Encryption) exist at all.

When in doubt, treat MySQL and MariaDB as related but distinct engines: state
the target engine and version explicitly in schema docs, migration comments,
and CI matrix configuration, and test both independently if the codebase
claims to support both.

## Storage Engine Selection

- **InnoDB is the default and correct choice for almost all tables** on both
  engines: it is transactional (ACID), supports row-level locking, foreign
  keys, crash recovery, and MVCC. Choose it unless a specific, named
  requirement rules it out.
- **MyISAM** is legacy: no transactions, no foreign keys, table-level locking,
  and it is not crash-safe. Do not choose it for new tables. It survives in
  old schemas and for a narrow set of full-text-search or read-only archival
  cases predating InnoDB's full-text support (InnoDB has supported `FULLTEXT`
  indexes since MySQL 5.6 / MariaDB 10.0.5); re-evaluate those cases against
  InnoDB `FULLTEXT` before keeping MyISAM.
- **Aria (MariaDB only)** is MyISAM's crash-safe successor, used internally
  for some system/temporary tables. It is not a general transactional engine;
  do not choose it as an InnoDB substitute for application tables that need
  transactions.
- **MEMORY/HEAP** tables are useful only for genuinely disposable, small,
  session-scoped or cache data that can be lost on restart without
  consequence. Row-level locking is not available (table-level locks), and
  data does not survive a server restart.
- **CSV, ARCHIVE, BLACKHOLE** are special-purpose (data exchange, compressed
  append-only logging, replication testing) and not appropriate as
  general-purpose application storage.
- Verify the engine of an existing table before assuming InnoDB behavior:
  `SHOW TABLE STATUS LIKE 'table_name'` or
  `SELECT engine FROM information_schema.tables WHERE table_schema = ? AND table_name = ?`.
  A mixed-engine schema (some InnoDB, some MyISAM) cannot enforce foreign keys
  across those tables and loses transactional guarantees for the non-InnoDB
  ones.

## Schema Design

### Normalization and Data Types

- Normalize first (3NF as the default target); denormalize only for a
  measured read need with an explicit ownership and refresh story, same as any
  other engine.
- Choose types by semantics, not convenience:
  - Use `INT`/`BIGINT` for integer identity and counts; do not use `VARCHAR`
    for numeric IDs. Prefer `BIGINT UNSIGNED` for auto-increment surrogate
    keys expected to exceed ~2.1 billion rows (`INT UNSIGNED` for smaller,
    bounded tables).
  - Use `DECIMAL(p,s)` for money and other exact values; never `FLOAT` or
    `DOUBLE` for currency or anything compared for exact equality — binary
    floating point cannot represent most decimal fractions exactly.
  - Use `DATETIME` for wall-clock/local values with no timezone conversion
    intent, and `TIMESTAMP` when you want automatic UTC storage and
    conversion tied to the session/server timezone (and note `TIMESTAMP`'s
    range ends in 2038 on both engines; use `DATETIME` for far-future dates).
  - Use `VARCHAR(n)` sized to the real constraint, not a round number picked
    without a rationale; use `TEXT`/`MEDIUMTEXT`/`LONGTEXT` only for genuinely
    unbounded content, and know that indexing them requires a prefix length
    (`INDEX (col(191))`) or a generated column.
  - Use `ENUM` sparingly, only for a genuinely closed, rarely-changing value
    set documented at the schema level; prefer a lookup table or `CHECK`
    constraint (MySQL 8.0.16+ / MariaDB 10.2+ enforce `CHECK`; earlier
    versions parse but silently ignore it) when the set changes with data
    rather than schema.
  - Use `BOOLEAN`/`TINYINT(1)` for two-state facts; both engines store it as
    `TINYINT(1)` — this is cosmetic, not a real boolean type, so do not rely
    on driver-level boolean coercion without checking how the client library
    maps it.
  - Use native `JSON` on MySQL for genuinely semi-structured, sparse, or
    schema-flexible attributes only, not as a substitute for columns and
    relations; on MariaDB, remember `JSON` is `LONGTEXT` plus a `CHECK`
    constraint, so its indexing and validation story differs (index it via a
    generated column, same as MySQL).
- Set the connection/schema character set to `utf8mb4` (not legacy `utf8`,
  which is a 3-byte-max alias that cannot store the full Unicode range,
  including many emoji and some CJK characters) and an appropriate collation
  (`utf8mb4_0900_ai_ci` on MySQL 8, `utf8mb4_general_ci` or a version-specific
  `utf8mb4_unicode_520_ci`/`utf8mb4_uca1400_ai_ci` on MariaDB depending on
  version). Set this at database, table, and column creation time
  deliberately; do not inherit a server default that predates the project.

### Indexing Strategy

- InnoDB tables are **clustered by primary key**: row data is physically
  stored in primary-key order, and every secondary index stores the primary
  key as a pointer back to the row. A wide or ever-changing primary key
  bloats every secondary index and causes page splits on insert. Prefer a
  narrow, monotonically increasing primary key (an auto-increment surrogate,
  or a `BIGINT` when using something like a Snowflake ID) for high-write
  tables; avoid `UUID` (random v4) as a primary key on write-heavy InnoDB
  tables because it causes random-order inserts, index fragmentation, and
  poor cache locality — if UUIDs are required, use a time-ordered variant
  (UUIDv7, or MySQL 8.0's `UUID_TO_BIN(UUID(), true)` swapped-byte encoding)
  or add a separate auto-increment clustering key.
- Index every foreign key column. Unlike PostgreSQL, both engines require an
  index on the referencing column to define the foreign key constraint at
  all, so this is enforced at DDL time — but confirm the index actually
  matches your join/filter pattern rather than relying on the FK-mandated
  index as sufficient for query performance.
- Build indexes to match real predicates: equality columns first, then range
  columns, matching the **leftmost-prefix rule** for composite indexes — an
  index on `(a, b, c)` serves queries filtering on `a`, `a+b`, or `a+b+c`, but
  not on `b` alone or `c` alone.
- Use covering indexes (all selected/filtered/sorted columns present in the
  index) to let the optimizer serve a query from the index alone, avoiding a
  lookup into the clustered row; check `Using index` in `EXPLAIN` `Extra` to
  confirm.
- Use prefix indexes (`INDEX (col(20))`) for long `VARCHAR`/`TEXT` columns
  only after checking selectivity with
  `SELECT COUNT(DISTINCT LEFT(col, 20)) / COUNT(*) FROM table` — a prefix
  index that is not selective enough will not be used, and it cannot serve
  as a covering index or sort key.
- Do not index every column speculatively. Every index adds write cost
  (extra B-tree maintenance on every insert/update/delete) and storage.
  Justify each index with a real query, and drop indexes proven unused via
  `sys.schema_unused_indexes` (`performance_schema`-based, both engines) or
  the equivalent `information_schema` query.
- Use `FULLTEXT` indexes (InnoDB, MySQL 5.6+/MariaDB 10.0.5+) for genuine text
  search instead of `LIKE '%term%'`, which cannot use a B-tree index at all.

### Constraints

- Use `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, and foreign keys for invariants the
  database must enforce; do not rely on application code alone for
  uniqueness or referential integrity.
- Use `CHECK` constraints for value-shape invariants: enforced since MySQL
  8.0.16 and MariaDB 10.2.1. Confirm the target version before relying on
  `CHECK` — older versions parse it but silently ignore it, which is a
  correctness trap, not a compatibility warning.
- Choose foreign key actions deliberately (`ON DELETE CASCADE/RESTRICT/SET
  NULL/NO ACTION`, `ON UPDATE CASCADE`). InnoDB is the only engine here that
  enforces foreign keys; a table on MyISAM or MEMORY silently accepts and
  ignores FK syntax with no enforcement.
- `NOT NULL` plus a documented `DEFAULT` beats a nullable column with
  application-level "treat null as X" logic; nulls should mean "genuinely
  unknown/inapplicable," not "empty by convention."
- Run with `sql_mode` including `STRICT_TRANS_TABLES` (or `STRICT_ALL_TABLES`)
  in every environment, including local dev and CI. Without strict mode, both
  engines historically silently truncated or coerced out-of-range/invalid
  values instead of raising an error — a schema that looks constrained is not
  actually protecting data if strict mode is off. Confirm the effective mode
  with `SELECT @@sql_mode`, since managed hosting defaults vary.

### Migrations

- Distinguish online (non-blocking, `ALGORITHM=INSTANT` or `INPLACE`) DDL from
  a full table rebuild (`ALGORITHM=COPY`), and check which algorithm a
  specific `ALTER TABLE` actually uses on the target engine/version via
  `EXPLAIN` or by consulting the online-DDL support table in the version's
  documentation — the same-looking `ALTER TABLE` can be instant on one
  version and a full table copy (locking, or replication-lag-inducing) on
  another.
- Adding a column with a default is instant on modern MySQL (8.0.12+) and
  MariaDB (10.3.7+/10.4+ depending on type); do not assume this on older
  targets, and never assume it cross-engine without checking each one.
- For large tables where in-place/instant DDL is unavailable or still too
  disruptive, use an external online-schema-change tool
  (`pt-online-schema-change`, `gh-ost`) rather than a blocking `ALTER TABLE`
  in production; these differ in trigger-based vs. binlog-based approach and
  each has its own foreign-key and trigger caveats — confirm the repository's
  chosen tool before assuming either is a drop-in default.
- Foreign-key-checked migrations on large tables can be slow; disabling
  `FOREIGN_KEY_CHECKS` for a single controlled migration transaction is
  sometimes appropriate, but never leave it disabled as ambient session state
  and never use it to skip validating data that should already satisfy the
  constraint.
- Plan rollback and deploy-order compatibility the same as any other engine:
  additive-first changes, backfill, validate, then remove/rename in a later
  deploy.

## Query And Transaction Checklist

- Select explicit columns. Avoid `SELECT *` — it defeats covering indexes,
  breaks silently when columns are added/reordered, and wastes network/memory
  on unused data.
- Bind user-controlled values via prepared statements or parameterized
  driver APIs. Never concatenate untrusted input into SQL.
- Keep predicates sargable: avoid wrapping an indexed column in a function or
  implicit type conversion in `WHERE` (`WHERE DATE(created_at) = ?` cannot use
  an index on `created_at`; `WHERE created_at >= ? AND created_at < ?` can).
  Implicit string-to-number or number-to-string comparisons silently defeat
  indexes the same way — match types exactly.
- Joins preserve intended cardinality; verify with row-count checks or
  `EXPLAIN` row estimates that a join is not silently multiplying rows.
- Paginate with keyset pagination (`WHERE (sort_col, id) > (?, ?) ORDER BY
  sort_col, id LIMIT ?`) for large or frequently-changing result sets instead
  of `LIMIT offset, count`, which gets slower as `offset` grows (the server
  still scans and discards `offset` rows) and shifts results under concurrent
  writes.
- Scope transactions to exactly one consistency boundary. Default isolation
  is `REPEATABLE READ` on both engines (unlike PostgreSQL's default of `READ
  COMMITTED`) — this affects phantom-read and gap-locking behavior; know which
  isolation level the code actually needs rather than accepting the default
  by omission.
- Name lock-ordering and retry assumptions for concurrent writes. InnoDB's
  `REPEATABLE READ` uses next-key locking (record + gap locks) for
  index-scanning `UPDATE`/`DELETE`/`SELECT ... FOR UPDATE`, which can produce
  more blocking and more deadlocks than `READ COMMITTED` under high
  concurrency; consider `READ COMMITTED` explicitly for write-heavy
  hotspots where gap locking causes contention, after confirming the
  application does not depend on repeatable-read semantics elsewhere in the
  same transaction.
- Use `INSERT ... ON DUPLICATE KEY UPDATE` for upserts; understand it requires
  a unique/primary key to trigger and that it is a MySQL/MariaDB-specific
  syntax with different semantics from PostgreSQL's `ON CONFLICT` (it can
  update on **any** unique key collision, not just the one you intended,
  if the table has more than one).
- Prefer set-based operations and batched writes (`INSERT ... VALUES (...),
  (...), (...)` or bulk-load tools) over row-at-a-time loops from application
  code; each round trip costs real latency at scale, and single-row
  autocommit inserts are especially costly under `sync_binlog=1` /
  `innodb_flush_log_at_trx_commit=1` durability settings.

## EXPLAIN And Query Optimization

- Run `EXPLAIN` (or `EXPLAIN FORMAT=JSON` for detail on cost estimates,
  filtered percentage, and applied optimizations) before trusting a query's
  performance. Read the `type` column for join/access strategy — from best to
  worst it runs roughly `system` > `const` > `eq_ref` > `ref` > `range` >
  `index` > `ALL` (full table scan); `ALL` on a nontrivial table is the
  signal to add or fix an index.
- Check `key` (which index was actually chosen — `NULL` means none was used),
  `rows` (estimated rows examined — large relative to expected result size
  means a weak filter or missing index), and `Extra`: `Using filesort` and
  `Using temporary` on a hot query usually mean the query needs an index that
  matches its `ORDER BY`/`GROUP BY`, or that it can be rewritten to avoid the
  sort; `Using index` (covering index) and `Using index condition` (index
  condition pushdown) are good signs; `Using where` alone after an index
  lookup just means a residual filter applied outside the index, which is
  often fine.
- Use `EXPLAIN ANALYZE` for real (not just estimated) execution timing and row
  counts: available on MySQL 8.0.18+ and MariaDB 10.1+ (`ANALYZE FORMAT=JSON`
  on MariaDB uses a different, JSON-only output format than MySQL's text tree
  — do not expect the same shape). `EXPLAIN ANALYZE` **actually executes** the
  query (including `UPDATE`/`DELETE`/`INSERT ... SELECT`); wrap mutating
  statements in a transaction and roll back on disposable or safe data:
  ```sql
  START TRANSACTION;
  EXPLAIN ANALYZE UPDATE orders SET status = 'shipped' WHERE customer_id = ?;
  ROLLBACK;
  ```
- Use the slow query log (`slow_query_log`, `long_query_time`,
  `log_queries_not_using_indexes`) and `performance_schema`
  (`events_statements_summary_by_digest`) or `sys` schema views
  (`sys.statement_analysis`) to find real offenders under production load
  rather than guessing from query text alone.
- Do not claim a performance improvement without comparable before/after
  evidence (timing or `EXPLAIN ANALYZE` output) captured under representative
  data volume and warm/cold cache conditions — `EXPLAIN` alone estimates,
  it does not measure.
- Watch for the N+1 query pattern from ORMs and application loops: one query
  to fetch a list, then one additional query per row to fetch related data.
  Replace with a single join, a batched `WHERE id IN (...)` fetch, or the
  ORM's eager-loading/prefetch feature. This is invisible in isolated unit
  tests against small fixtures and only shows up as real latency at
  production row counts — verify with query logging or count assertions in
  integration tests, not by inspection alone.

## Connection Management And Transactions

- Use connection pooling (application-side pool, or a proxy such as
  ProxySQL/MySQL Router, or driver-native pooling) rather than opening a new
  connection per request; connection setup/teardown and thread creation are
  real overhead, and MySQL/MariaDB's default thread-per-connection model
  means an unbounded connection count competes directly for server memory and
  CPU. Size the pool against the server's `max_connections` and the number of
  application instances sharing it, not against a per-instance guess in
  isolation.
- Always use parameterized queries / prepared statements from the driver, not
  string formatting, for any value that originates outside the code. This is
  both a correctness practice (type coercion, quoting) and the primary SQL
  injection defense.
- Keep transactions short: open, do the minimal necessary reads/writes,
  commit or rollback promptly. A transaction held open across an external
  network call, a slow report render, or user think-time holds InnoDB locks
  and old MVCC read-view snapshots (bloating the InnoDB undo log / history
  list) for the whole duration.
- Handle deadlocks (`ER_LOCK_DEADLOCK`, error 1213) with a bounded retry at
  the transaction boundary; InnoDB detects and breaks deadlocks by rolling
  back one transaction automatically, so the calling code must be prepared to
  retry idempotently rather than treat it as a fatal error.
- Set explicit, sane timeouts: `innodb_lock_wait_timeout` for row-lock waits,
  and a statement/connection timeout appropriate to the workload, rather than
  relying on defaults tuned for a different traffic profile.
- Do not rely on autocommit-per-statement for multi-statement business
  operations; wrap them explicitly in `START TRANSACTION` / `COMMIT` so a
  partial failure cannot leave inconsistent state.

## Anti-Patterns

Ranked roughly by how much damage each does in a typical application:

1. **`SELECT *` in application queries.** Breaks covering indexes, pulls
   unnecessary large/`TEXT`/`JSON` columns over the wire, and silently changes
   behavior when a column is added. Select exactly what the caller needs.
2. **N+1 queries from ORMs or loops.** One list query followed by one query
   per row for related data. Invisible at small scale, expensive in
   production. Fix with joins, `WHERE id IN (...)` batching, or eager
   loading.
3. **Storing data in the wrong type**, especially: numeric IDs as `VARCHAR`,
   money as `FLOAT`/`DOUBLE`, dates/times as strings, booleans as ad hoc
   `'Y'`/`'N'` strings instead of `TINYINT(1)`/`BOOLEAN`, and structured data
   as an unindexed `TEXT` blob of delimited values. Each blocks correct
   comparison, sorting, and indexing.
4. **Legacy `utf8` (not `utf8mb4`) character set.** Truncates or rejects
   4-byte Unicode characters (emoji, some CJK) with confusing errors far from
   the actual cause. Use `utf8mb4` for all new schemas.
5. **`LIMIT offset, count` pagination on large or hot tables.** Degrades as
   `offset` grows and shifts under concurrent writes. Use keyset/seek
   pagination.
6. **No index on foreign key columns** (only possible on non-InnoDB tables,
   since InnoDB requires one) or, more commonly, an index that does not
   actually match the query's filter/join/sort pattern.
7. **Speculative indexing** — adding indexes "just in case" without a query
   to justify them. Every index has a real write-amplification and storage
   cost; unused indexes are pure overhead.
8. **Building SQL by string concatenation** with any user-controlled value,
   instead of bound parameters. This is the direct path to SQL injection and
   should be treated as a security defect, not a style preference.
9. **Wrapping an indexed column in a function in `WHERE`** (`WHERE
   YEAR(created_at) = 2024`), which prevents index use even though an
   equivalent range predicate would use it.
10. **Ambient non-strict `sql_mode`.** Silently truncates or coerces invalid
    data instead of rejecting it at write time, undermining every type and
    length constraint in the schema.
11. **Long-held transactions or connections without pooling**, causing lock
    contention, MVCC history-list bloat, and connection exhaustion under
    load.
12. **Assuming MySQL and MariaDB are interchangeable** — deploying against
    one engine's tested behavior (JSON storage, replication, optimizer
    output, auth plugin) without verifying the other actually supports it the
    same way.
13. **Treating application-layer validation as a substitute for database
    constraints** on invariants that matter (uniqueness, required fields,
    referential integrity).

## Commands

Prefer repository recipes when they exist, especially for SQL scripts. When
direct commands are needed:

```sh
mysql --defaults-extra-file=path/to/client.cnf -e "SOURCE path/to/query.sql;"
mysql -e "SHOW CREATE TABLE table_name\G"
mysql -e "EXPLAIN FORMAT=JSON SELECT ...;"
mysql -e "EXPLAIN ANALYZE SELECT ...;"          -- MySQL 8.0.18+ / MariaDB 10.1+ (different output)
mysqldump --single-transaction --routines --triggers db_name > dump.sql
```

Never put credentialed DSNs, passwords, or connection strings in argv, shell
history, logs, examples, or reports; use a `--defaults-extra-file`, an
environment variable sourced outside the command, or a repository-owned
recipe instead.

For mutating `EXPLAIN ANALYZE`, always wrap in a transaction and roll back on
disposable or safe data — it executes the statement, it does not simulate it:

```sql
START TRANSACTION;
EXPLAIN ANALYZE UPDATE ...;
ROLLBACK;
```

## Testing And Review

- Use TDD for query bugs when practical: write a failing fixture or
  integration test that proves the old behavior is wrong.
- Use BDD examples for data behavior users can observe: duplicate prevention,
  authorization, lifecycle state, conflict responses, and atomicity.
- Test constraints, transactions, and DDL against the actual target engine
  and version — not SQLite, not the other of MySQL/MariaDB, and not mocks.
  If the project claims support for both engines, run the suite against both
  in CI rather than assuming parity.
- Review plans with `EXPLAIN`/`EXPLAIN ANALYZE` for expensive queries under
  representative data and current statistics (`ANALYZE TABLE` refreshes
  InnoDB's persistent optimizer statistics if they are stale). Do not claim a
  performance improvement without comparable evidence.
- Review security for injection, least privilege, `DEFINER`-context routine
  and view scope, secret handling, audit logging, and safe error messages.
- Review observability for slow queries, migration failures, connection-pool
  saturation, deadlocks, lock waits, and replication lag.

## Anti-Pattern Verification Note

Before flagging a migration or query as broken on "MySQL/MariaDB" generically,
confirm which specific engine and version was actually tested; a finding true
on MySQL 5.7 may be fixed in MySQL 8.0, and a finding true on MySQL may not
apply to MariaDB at all (or the reverse). Cite the engine and version alongside
any claimed defect.

## Successful Use

The final handoff names the data behavior protected, the target engine(s) and
version(s) verified, migrations or SQL changed, database-specific checks run,
query-plan or performance evidence when relevant, and any deploy, rollback, or
cross-engine-compatibility risk that remains.
