---
name: cli-forge-data
description: >
  Design and implement safe PostgreSQL database changes for Rust/SQLx applications. Use for new
  schemas, migrations, constraints, indexes, repositories, transaction boundaries, state machines,
  idempotency, concurrency control, queues, multi-tenancy, soft deletion, ledgers, outbox/inbox,
  repair jobs, or corrections handed off by cli-audit-data.
argument-hint: "[feature-component-or-database-change]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** Load the shared invariant contract first, then only the PostgreSQL/SQLx
> references needed by the requested change.

> **Language rule:** Write user-facing decisions and reports in the project's dominant language.
> Keep SQL, Rust identifiers, SQLSTATE values, and the mandatory uncertainty marker unchanged.

# Forge Data — Safe PostgreSQL and SQLx Changes

Design or implement database changes whose safety comes from explicit invariants, PostgreSQL
guarantees, short atomic operations, compatible evolution, and reproducible proof.

Read `../shared/data-invariants.md` before acting. Read `../gotchas.md` before producing output.
Read `../shared/data-invariant-catalog.md` when discovering domain rules, and
`../shared/postgres-sqlx-patterns.md` before writing non-trivial SQL.

## Modes

| Mode | Trigger | Behavior |
|---|---|---|
| Design | User asks for schema, transaction, migration, or data architecture | Produce a database decision and proof plan before code |
| Implementation | User asks to build/fix the change or accepts a design | Edit migrations/Rust/tests, then execute the relevant gates |
| Correction | `cli-audit-data` finding is supplied | Preserve the finding's invariant and close the smallest unsafe gap |

Do not implement in design-only mode. In implementation or correction mode, inspect the existing
schema and code before editing; never infer the database solely from Rust structs.

## Non-negotiable rules

1. Give every business fact one authoritative owner.
2. Protect persistent invariants in PostgreSQL whenever a declarative guarantee exists.
3. Put every write belonging to one business decision in one explicit transaction.
4. Never perform network I/O while a PostgreSQL transaction is open.
5. Treat zero affected rows as a business result when the command is conditional.
6. Give every retryable command an explicit idempotency protocol.
7. Retry a whole failed transaction, never one middle statement.
8. Use a transactional outbox/inbox protocol for cross-system effects.
9. Design migrations for old code, new code, and mixed-version deployment.
10. Never edit an already-applied migration silently.
11. Include tenant scope in database keys and references, not only query filters.
12. Make derived facts reconstructible or provide auditable detection and repair.
13. Never use SQLite or mocks as proof of PostgreSQL concurrency behavior.
14. Never claim cross-system exactly-once behavior without a demonstrated protocol.

## Workflow

### 1. Inspect existing truth

Inspect relevant migrations, tables, types, constraints, indexes, triggers, functions, views, RLS,
extensions, SQLx queries, transaction boundaries, background jobs, messages, external effects,
versions, migration runner, deployment order, and incident history.

Proceed with explicit assumptions when information is missing. Stop before destructive or
irreversible work whose semantics cannot be safely inferred.

### 2. Classify scope and criticality

Choose S/M/L/XL from `../shared/tiering.md` for output depth and L0-L3 from
`../shared/data-invariants.md` for proof depth. State both. Bias scope down and criticality up when
uncertain.

### 3. Write the decision and invariants

Complete the database decision, source-of-truth map, invariant matrix, conservation laws, and state
transition tables defined in `../shared/data-invariants.md`.

For each invariant choose:

- a primary PostgreSQL guarantee;
- defense in depth where useful;
- an audit query and threshold;
- a repair or reconstruction path;
- an executable proof.

Do not accept an invariant enforced only by Rust validation when PostgreSQL can protect it.

### 4. Break concurrent and failure cases

Write concrete A/B interleavings for every read-before-write flow. Cover duplicate requests, stale
writes, lost responses, crash boundaries, retries, old/new binaries, wrong tenant, cancellation,
and deadlock or serialization failure.

Prefer, in order:

1. declarative constraint plus atomic DML;
2. `INSERT ... ON CONFLICT` or conditional `UPDATE ... RETURNING`;
3. targeted row locking in a short transaction;
4. `SERIALIZABLE` with bounded whole-transaction retry;
5. advisory locking only with a stable key and shared documented protocol.

### 5. Select PostgreSQL guarantees

Use named `NOT NULL`, `CHECK`, `UNIQUE`, partial unique indexes, foreign keys, composite tenant
keys, exclusion constraints, conditional DML, or outbox/inbox as appropriate.

Choose every `ON DELETE` and `ON UPDATE` action. Do not claim a row `CHECK` protects a multi-row
invariant. Justify indexes from real access paths and representative volumes. Use triggers only
when their central guarantee outweighs hidden complexity and they are observable and tested.

### 6. Implement with SQLx

Prefer compile-time checked `query!`, `query_as!`, `query_scalar!`, and `query_file!` variants.
Require explicit columns, bound values, allowlisted dynamic identifiers, justified nullability,
`RETURNING` where it removes a second read, zero-row handling, and error mapping by SQLSTATE and
named constraint.

Place the transaction boundary at the business use case and pass the same transaction or
connection through participating functions. Do not reacquire from the pool inside the use case.
Verify the exact SQLx `Executor`/`Transaction` API against the project's pinned version.

### 7. Evolve the schema compatibly

Classify the migration as additive, compatible transformation, backfill, destructive, locking,
rewriting, extension-dependent, or version-incompatible.

For non-trivial changes use:

```text
EXPAND -> MIGRATE -> SWITCH -> CONTRACT
```

Prove old/old, old/new, new/old, new/new, and old+new/new combinations where deployment overlap
exists. Analyze locks, rewrite, disk, replication lag, pool impact, batch size, resumability,
interruption recovery, and runner transaction behavior. Contract only after telemetry proves old
representations and binaries are gone.

### 8. Build homeostasis

For critical invariants define audit query, frequency, metric, threshold, owner, dry-run repair,
audited repair, and replay path. For eventual consistency define nominal and maximum lag,
user-visible degraded behavior, retry limit, failed-item storage, and escalation.

### 9. Implement the proof ladder

Use the database T0-T4/M0 mapping in `../shared/data-invariants.md`.

At minimum run the commands supported by the project version:

```bash
cargo fmt --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo sqlx prepare --workspace --check
cargo test --workspace
```

For L2+, use synchronized transactions against real PostgreSQL. For L3, add property-based or
state-model proof, crash-boundary simulation, full replay, and repair testing. Never report a
command as successful unless it ran.

### 10. Pass the done gate

Apply `../shared/done-gate.md`: confirm the decision and baseline before editing, keep the change
reversible during implementation, and capture reproducible post-verification. Apply
`../shared/determinism.md` to fixtures, IDs, clocks, retry schedules, and migration data.

Run `/cli-audit-data` after implementation for L1+ changes or whenever this skill was triggered by
a database-safety finding.

## Mandatory output

End with:

1. scope tier and data criticality;
2. database decision;
3. sources of truth and invariant matrix;
4. conservation laws and state machine;
5. concurrency and idempotency analysis;
6. PostgreSQL guarantees;
7. SQLx implementation notes;
8. migration compatibility matrix;
9. proof executed and not executed;
10. homeostasis and repair;
11. residual risks and rollback/forward-repair path;
12. every runtime-dependent claim as:

```text
À PROUVER SUR POSTGRESQL RÉEL — ...
```

When running under `cli-cycle`, emit `.claude/cli-forge-data.json` using
`../shared/result-schema.md`.

## Dynamic handoffs

| Condition detected | Recommend | Why |
|---|---|---|
| Implementation or migration is ready for an independent safety gate | `/cli-audit-data` | Verify invariants and dangerous interleavings |
| Contract intent is missing or disagrees with code | `/cli-audit-drift` | Establish semantic ownership |
| Component architecture or API boundary is unresolved | `/cli-forge-lld` | Anchor the database design in the component design |
| Backup, restore, failover, or incident response is incomplete | `/cli-forge-resilience` | Build operational proof |
| Query/index/locking performance is uncertain | `/cli-forge-perf` | Measure rather than speculate |
| A state machine or data flow needs visualization | `/cli-forge-schema` | Generate the appropriate Mermaid diagram |

**Rule:** recommend handoffs; do not execute them automatically outside `cli-cycle`.

## Completion criterion

The change is complete only when its laws are explicit, PostgreSQL protects them as far as
possible, concurrent and failure executions have concrete answers, old and new versions can
coexist safely, proof is reproducible, and remaining drift is observable and repairable.
