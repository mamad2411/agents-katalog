---
name: optimize-postgres
description: Optimize PostgreSQL performance, serverless connection pooling, ephemeral database branching, EXPLAIN ANALYZE execution plan tuning, and zero-downtime migrations. Use when tuning queries, configuring poolers, branching databases, or rolling out DDL.
version: 1.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Optimize Postgres

Use this skill to tune PostgreSQL performance, configure serverless connection pooling, implement ephemeral database branching, analyze query execution plans, and enforce zero-downtime migration safeguards.

## When to Use

- configuring serverless connection poolers (Supavisor, PgBouncer) in transaction or session modes
- resolving prepared statement conflicts and sizing connection pools using mathematical limits
- orchestrating ephemeral copy-on-write database branches (Neon) for PRs and isolated CI test runs
- diagnosing slow queries via `EXPLAIN (ANALYZE, BUFFERS)` to eliminate sequential scans and disk spills
- designing composite, partial, expression, and covering indexes for high-throughput queries
- executing zero-downtime schema evolution with lock timeouts and concurrent DDL safeguards

## Core Rules

- **Enforce Lock Timeouts on DDL**: all DDL migrations must execute `SET lock_timeout = '2s';` to prevent lock queue pile-ups from starving connection pools
- **Mandate Concurrent Indexing**: index creation and deletion on live tables must use `CREATE INDEX CONCURRENTLY` and `DROP INDEX CONCURRENTLY` outside transaction blocks; detect and drop `INVALID` indexes on failure
- **Transaction Mode Prepared Statement Discipline**: when connecting through transaction poolers (port 6543), drivers and ORMs must disable named prepared statements (`statement_cache_size=0`)
- **Pool Sizing Boundedness**: backend database pool sizing must adhere to $(2 \times \text{CPU cores}) + \text{spindle\_count}$; never over-allocate backend connections to match client concurrency
- **Buffer-Verified Query Plans**: query tuning must assert `EXPLAIN (ANALYZE, BUFFERS)` evidence; verify `shared hit` ratios, eliminate `external merge` disk spills by sizing `work_mem`, and verify index selectivity
- **Two-Phase Constraint Rollouts**: adding constraints to large tables must use `NOT VALID` followed by `VALIDATE CONSTRAINT` to avoid long-running exclusive locks
- detailed pooling architectures and tuning scripts: [`references/pooling-branching-and-tuning.md`](references/pooling-branching-and-tuning.md)

## Suggested Process

### 1. Evaluate Persistence Architecture & Workload
Inspect connection topology (direct vs pooler, transaction vs session mode). Identify bottleneck: connection starvation, slow query latency, or DDL lock contention.

### 2. Configure Connection Pooling & Driver Flags
Select pooling mode (Transaction mode for serverless APIs; Session mode for migrations/listeners). Configure driver flags to bypass named prepared statements in transaction mode.

### 3. Orchestrate Ephemeral Branch for Safe Testing
Provision an isolated CoW database branch (Neon API) from main. Direct test runners and migration validation to the ephemeral branch URL.

### 4. Profile & Optimize Query Plans
Run `EXPLAIN (ANALYZE, BUFFERS)` on slow queries. Identify Seq Scans, row estimate discrepancies, and disk spills. Construct optimal composite, partial, or covering indexes.

### 5. Formulate Zero-Downtime Migration
Draft migration script with `SET lock_timeout = '2s'`. Apply `CREATE INDEX CONCURRENTLY`. Split large table backfills into keyset-paginated batches with sleep intervals.

### 6. Verify Execution & Teardown
Verify index builds cleanly without `indisvalid=false`. Execute regression test suite against ephemeral branch. Teardown branch and emit migration artifacts.

## Checklist

- [ ] `SET lock_timeout = '2s';` declared at the head of every DDL migration script
- [ ] live index creation uses `CREATE INDEX CONCURRENTLY` outside transaction blocks
- [ ] scripts inspect and remediate any `indisvalid=false` failed concurrent indexes
- [ ] transaction mode poolers configured with driver prepared statement caching disabled
- [ ] backend connection pool size mathematically aligned with CPU cores and I/O capacity
- [ ] query optimizations verified using `EXPLAIN (ANALYZE, BUFFERS)` showing zero disk spills
- [ ] large constraints added using two-phase `NOT VALID` and `VALIDATE CONSTRAINT` pattern
- [ ] table backfills batched via keyset pagination (500–2000 rows) with throttling sleeps
- [ ] ephemeral database branches verified and destroyed upon CI pipeline completion
- [ ] `schema-migration.json` and `implementation-result.json` emitted and validated

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/schema-migration.json`** — Declares migration changes, lock safety notes, concurrent index status, and backfill parameters.
- **`contracts/schemas/implementation-result.json`** — Documents execution plan metrics, buffer improvements, and test verification evidence.

## Failure Modes

- **Lock Queue Starvation**: DDL blocks behind query, starving incoming requests. Mitigation: enforce `SET lock_timeout = '2s'`.
- **Prepared Statement Collisions in Pooler**: `prepared statement does not exist` errors in transaction mode. Mitigation: disable client prepared statement caching or use simple protocol.
- **Memory Spill to Disk**: sorts or hashes exceed `work_mem` causing 10x latency penalty. Mitigation: tune `work_mem` based on `EXPLAIN (BUFFERS)` analysis.
- **Dangling Invalid Indexes**: failed concurrent index consumes storage and write I/O. Mitigation: automated query checking `WHERE NOT indisvalid` with concurrent drop.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: ensure connection pooling uses non-superuser credentials; restrict DDL privileges to dedicated migration users.
- **ASI05 RCE Guard**: never interpolate untrusted identifiers into DDL statements or query analyzer strings.
- **ASI07 Inter-Agent Communication**: emit structured `schema-migration.json` detailing locking behavior and rollout safety.

## Related Skills

- **create-migration**: Author additive schema migrations and rollback scripts
- **implement-auth**: Configure Row-Level Security policies and session claims
- **add-api-endpoint**: Integrate tuned database queries into API route handlers
- **performance-profiling**: Capture end-to-end service latency and database metrics
- **write-tests**: Author database integration tests run against ephemeral branches
