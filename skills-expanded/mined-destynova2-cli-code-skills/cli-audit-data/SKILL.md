---
name: cli-audit-data
description: >
  Audit PostgreSQL database safety in Rust/SQLx applications. Use for schemas, migrations,
  constraints, indexes, transactions, repositories, state transitions, idempotency, concurrency,
  queues, multi-tenancy, soft deletion, ledgers, auditability, repair, database incidents, or
  whenever SQLx and PostgreSQL changes could violate business invariants under retries, failures,
  mixed versions, or concurrent execution.
argument-hint: "[file-directory-migration-or-diff]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** Read detailed references only when the audited scope needs them.

> **Language rule:** Write user-facing reports in the project's dominant language. Keep SQL,
> identifiers, paths, SQLSTATE values, and the mandatory uncertainty marker unchanged.

# Audit Data — PostgreSQL and SQLx Safety

## Purpose

Detect database code that compiles and passes nominal CRUD tests but violates business logic
under concurrency, retries, failures, migration, mixed application versions, or data drift.

Treat the database as a dynamic system that must preserve explicit laws across every transition.
Physics, biomimicry, cybernetics and safety engineering are lenses for discovering risks; only
constraints, atomic operations, demonstrated transaction protocols and reproducible PostgreSQL
tests count as technical proof.

Read `../shared/data-invariants.md` before auditing; it owns the cross-skill criticality, invariant,
conservation, interleaving, proof-ladder, and uncertainty contracts. Read `../gotchas.md` last.

## Non-negotiable rules

1. Do not implement before identifying sources of truth and invariants.
2. Give every business fact one explicit owner and authoritative source.
3. Protect persistent invariants in PostgreSQL; Rust validation alone is not an integrity guarantee.
4. Analyze every `read -> decide -> write` sequence with at least two concurrent actors.
5. Give every retryable operation an explicit idempotency protocol.
6. Bound, observe and repair every eventually consistent fact.
7. Analyze every migration with old code, new code and mixed-version deployment.
8. Put all writes of one atomic business decision inside one explicit transaction boundary.
9. Never make external network calls while a PostgreSQL transaction is open.
10. Never ignore `rows_affected() == 0` when zero rows has business meaning.
11. Never silently edit an already-applied migration.
12. Never claim cross-system `exactly once` without a demonstrated protocol; use durable
    identity, idempotence and outbox/inbox patterns.
13. Never use SQLite or mocks as proof of PostgreSQL concurrency behavior.
14. Decide deletion, cascade, retention, anonymization and restoration explicitly.
15. Make every derived fact reconstructible or give it an auditable repair protocol.

## Criticality

Criticality L0-L3 measures data risk. It is independent from the S/M/L/XL scope tier in
`../shared/tiering.md`: a one-line ledger mutation can be scope S and criticality L3. Use the
definitions and reasoning order in `../shared/data-invariants.md`; when uncertain, choose the
higher criticality.

# Required audit workflow

## 1. Inspect existing truth

Before auditing:

- read all relevant migrations;
- inspect tables, columns, constraints, indexes, triggers, functions, views, RLS and extensions;
- find every Rust type and SQLx query touching the model;
- locate transaction boundaries and hidden pool acquisition;
- locate jobs, messages, webhooks and external side effects;
- identify PostgreSQL, SQLx and migration-runner versions;
- identify real deployment order and mixed-version duration;
- inspect previous incidents or bugs when available.

Never infer the database solely from Rust structs.

If information is missing, proceed with explicit assumptions. Block only before an irreversible or
potentially destructive action whose semantics cannot be safely inferred.

## 2. Reconstruct the database decision

Reconstruct this decision from code, migrations, tests and documentation. Mark missing or ambiguous
fields as findings rather than silently inventing intent.

```text
Business objective:
Out of scope:
Entities, owners and cardinalities:
Authoritative sources and derived copies:
Exact meaning of NULL:
Lifecycle and terminal states:
Business time, recorded time and authoritative clock:
Tenant and authorization boundary:
Deletion, retention, anonymization and restoration:
Identifier and uniqueness scope:
Dominant access paths and expected volumes:
Required consistency and convergence bound:
Deployment compatibility:
Assumptions:
```

Reject ambiguous words such as `unique`, `active`, `recent`, `deleted` or `synchronized` until
their scope and temporal meaning are explicit.

## 3. Build the source-of-truth map and invariant matrix

For each fact, record owner, copies, producer, consumers and reconstruction path.

For each invariant, use:

| ID | Testable invariant | Scope | Always/eventual | Primary guarantee | Secondary defense | Detection | Repair | Proof |
|---|---|---|---|---|---|---|---|---|

Systematically consider:

- value domain, unit, precision and nullability;
- identity, uniqueness and cardinality;
- referential integrity and tenant ownership;
- conservation of money, stock, quota, points or rights;
- state transitions;
- temporal overlap and event order;
- idempotency;
- derived-data consistency;
- retention, audit and deletion.

Invariants must be positive, observable and falsifiable. Never accept `normally`, `unlikely`,
`the service should` or `eventually` without a bound.

For a detailed discovery checklist, read `../shared/data-invariant-catalog.md`.

## 4. Express conservation laws and state transitions

For every conserved resource, write:

```text
Resource and unit:
State before:
Inputs:
Outputs:
State after:
Bounds:
Rounding rule:
Atomic operation:
Audit/reconstruction:
```

Examples:

```text
stock_after = stock_before + receipts - reservations - shipments
balance_after = balance_before + credits - debits
quota_total = available + reserved + consumed
```

For money or exact quantities:

- never use floating point;
- include currency or unit in the invariant scope;
- define rounding and residual-unit allocation;
- prefer immutable entries and compensating corrections for audit-critical history.

For every lifecycle entity, produce a transition table containing command, source state,
preconditions, target state, writes, external effects and replay behavior.

Do not update a state without checking current state or version. A conditional update that returns
zero rows is a business result, not silent success.

## 5. Search for concurrent and failure counterexamples

For each read-before-write flow, produce an interleaving table with actors A and B.

At minimum test mentally and, for L2+, on PostgreSQL:

- duplicate creation;
- two updates from one stale version;
- two reservations for the final unit;
- two workers picking one task;
- duplicate request or event;
- response lost after commit;
- crash after DB write but before acknowledgement;
- out-of-order events;
- old and new binaries running together;
- stale replica read followed by a critical write;
- deadlock or serialization retry;
- client cancellation while execution continues.

Resolve races in this preference order:

1. declarative constraint + atomic DML;
2. `INSERT ... ON CONFLICT` or conditional `UPDATE ... RETURNING`;
3. targeted row locks in a short transaction;
4. `SERIALIZABLE` with bounded retry of the entire transaction;
5. advisory locks only with a stable key and a documented shared protocol.

Never rely on a preliminary `SELECT` to enforce uniqueness or available capacity.

For idempotency, define key scope, request hash, result persistence, in-progress behavior,
payload mismatch behavior, expiration and cleanup.

## 6. Choose PostgreSQL guarantees

Prefer declarative mechanisms:

| Need | Primary mechanism |
|---|---|
| mandatory value | `NOT NULL` |
| row-local rule | `CHECK` |
| identity/idempotence | `UNIQUE` or unique index |
| conditional uniqueness | partial unique index |
| reference | `FOREIGN KEY` |
| same-tenant reference | composite key/FK including `tenant_id` |
| temporal non-overlap | range type + `EXCLUDE` |
| state/version transition | conditional `UPDATE ... RETURNING` |
| concurrent creation | `INSERT ... ON CONFLICT` |
| work queue | row locking, often `SKIP LOCKED`, with starvation analysis |
| cross-system side effect | transactional outbox + idempotent inbox |

Rules:

- name constraints for reliable error mapping;
- choose every `ON DELETE` and `ON UPDATE` explicitly;
- do not pretend a row `CHECK` guarantees a multi-row invariant;
- include tenant scope in keys and references, not only query filters;
- redesign uniqueness, restoration and purge around soft deletion;
- use triggers only when a central DB guarantee justifies their hidden complexity, and test and
  observe them explicitly;
- treat RLS as defense in depth, not the only tenant-integrity mechanism;
- justify indexes from concrete access paths and representative volumes.

Read `../shared/postgres-sqlx-patterns.md` before reviewing non-trivial SQL.

## 7. Review SQLx implementation safety

Prefer compile-time checked `query!`, `query_as!`, `query_scalar!` and `query_file!` variants.

Require:

- explicit columns, never application `SELECT *`;
- bound values only;
- `QueryBuilder::push_bind` for dynamic values;
- allowlisted identifiers for dynamic table/column/order names;
- explicit nullability and type semantics;
- `RETURNING` when it removes a race-prone second read;
- explicit handling of zero affected rows;
- mapping by SQLSTATE and named constraint where available;
- distinct domain errors for absence, conflict, idempotent replay and technical failure;
- no default value substituted silently for a missing row.

Transactions:

- place the boundary at the business use case;
- pass the same transaction/connection to every participating function;
- do not reacquire from the pool inside the use case;
- keep transactions short;
- do no network I/O inside them;
- retry the whole transaction, not one middle statement;
- bound retries and emit metrics;
- choose isolation explicitly when `READ COMMITTED` is insufficient;
- treat timeout/cancellation as potentially unknown outcome until confirmed through idempotence
  or a read-back protocol.

The exact SQLx `Executor`/`Transaction` form is version-dependent. Verify it in the project rather
than generalizing from another release.

Run, adapted to the project version:

```bash
cargo fmt --check
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo sqlx prepare --workspace --check
cargo test --workspace
```

Never claim success for commands that were not executed.

## 8. Handle distributed effects

When a committed decision must trigger HTTP, payment, email, webhook or broker publication:

1. write business state and outbox event in the same transaction;
2. publish durably and replayably;
3. assign a stable event ID and version;
4. deduplicate on the consumer side with inbox or a unique business key;
5. define ordering scope, retry, dead-letter and replay;
6. distinguish business compensation from technical rollback.

Never imply that a PostgreSQL commit and an external call are atomic.

## 9. Design migration as evolution

Classify each change as additive, compatible transformation, backfill, destructive, locking,
rewriting, extension-dependent or version-incompatible.

For non-trivial changes use:

```text
EXPAND -> MIGRATE -> SWITCH -> CONTRACT
```

Fill this compatibility matrix:

| Application | Schema | Read | Write | Verdict |
|---|---|---|---|---|
| old | old |  |  | baseline |
| old | new |  |  |  |
| new | old |  |  |  |
| new | new |  |  |  |
| old + new | new |  |  |  |

Analyze locks, table rewrite, disk, replication lag, pool impact, batch size, resumability,
idempotence and interruption recovery. Verify runner behavior before `CREATE INDEX CONCURRENTLY`
or any operation incompatible with a transaction wrapper.

Prefer forward repair over destructive rollback when new writes cannot be represented by the old
schema. Never contract until metrics prove the old representation and old binaries are gone.

## 10. Build homeostasis

For every critical invariant define:

```text
Audit query:
Frequency:
Metric and threshold:
Alert owner:
Dry-run repair:
Audited repair action:
Replay/reconstruction path:
```

For eventual consistency also define nominal and maximum lag, user-visible behavior during drift,
retry limit, failed-item storage and escalation if convergence never occurs.

Automatic destructive repair requires guardrails, dry-run and an immutable audit record.

## 11. Run a safety pre-mortem

Apply these guide words to each critical command:

```text
none, more, less, partial, duplicate, reversed, early, late, stale,
out of order, wrong tenant, wrong unit, after timeout, after crash, old version
```

Produce the five most dangerous failures with prevention, detection, containment, repair and test.
Also find one combined failure where two supposedly sufficient defenses fail together.

## 12. Decide whether to formalize

Use a small Alloy, TLA+/PlusCal or executable state model when any applies:

- L3;
- independent writers;
- conserved money, stock, quota or rights;
- retries + variable order + irreversible effects;
- leader/lease/lock/reservation protocol;
- complex relation-based authorization;
- critical temporal exclusion;
- prior concurrency incident;
- the interleaving cannot be explained clearly on one page.

Use Alloy for relationships/cardinality, TLA+/PlusCal for concurrent protocols, and property-based
tests for transformations and algebraic laws. A model complements, never replaces, PostgreSQL tests.

## 13. Test the proof

Minimum:

- **All levels:** nominal path, rejected constraints, missing row/zero affected, empty-database
  migration, SQLx schema verification.
- **L1+:** every forbidden transition, duplicate/idempotency, delete/restore/reference behavior,
  migration from N-1, old code on new schema when deployments overlap.
- **L2+:** real PostgreSQL, synchronized concurrent transactions, stale version, wrong tenant,
  serialization/deadlock retry, lost response, replayed outbox/inbox, invariant audit.
- **L3:** property-based tests, crash-boundary simulation, full replay, repair test, and formal-model
  output or a written justification for omission.

Do not replace these proofs with mocks.

# Review mode

Classify findings:

- **BLOCKER:** corruption, data loss, wrong money, cross-tenant access, authorization bypass,
  uncontrolled destructive migration, unprotected invariant;
- **HIGH:** race, missing idempotence, unknown result, long lock, split transaction, duplicate effect;
- **MEDIUM:** unobserved drift, missing repair, unsuitable index, misleading error mapping;
- **LOW:** readability or debt without immediate safety impact.

Map severity to `../shared/triage.md`: BLOCKER/HIGH are normally Tier 3, MEDIUM is Tier 2, and LOW
is Tier 1. Record confidence separately; severity is consequence, not certainty.

Every finding must include:

```text
Severity:
Location:
Invariant:
Concrete scenario/interleaving:
Consequence:
Minimal correction:
Structural correction:
Regression test:
```

Never write `race condition` without showing a possible execution.

Use `references/review-templates.md` for reusable tables. Read
`references/order-reservation-review.md` when a complete worked example is useful.

# High-signal red flags

Immediately investigate:

- `SELECT` then `INSERT` for uniqueness;
- `SELECT` then unconditional decrement;
- ignored zero-row update;
- application `SELECT *`;
- exact quantity stored as float;
- unique key or FK missing tenant scope;
- soft delete with unchanged uniqueness semantics;
- state update without source state/version;
- inner function reacquiring from the pool;
- HTTP call inside a transaction;
- event publication after commit without outbox;
- non-idempotent consumer;
- unproven `exactly once` claim;
- retrying one statement inside a failed transaction;
- edited applied migration;
- destructive schema change in the same rollout as code cutover;
- non-resumable backfill;
- derived data with no reconstruction path;
- eventual consistency without a maximum lag and alert;
- SQLite test presented as PostgreSQL proof.

# Mandatory final output

End every audit with these sections:

1. **Verdict** — exactly `SAFE`, `SAFE WITH CONDITIONS` or `UNSAFE`.
2. **Database decision**.
3. **Sources of truth**.
4. **Invariant matrix**.
5. **Conservation laws**.
6. **State machine**.
7. **Concurrency and idempotency analysis**.
8. **PostgreSQL guarantees**.
9. **SQLx implementation notes**.
10. **Migration plan and compatibility matrix**.
11. **Proof tests executed and not executed**.
12. **Homeostasis: audit, metrics and repair**.
13. **Safety pre-mortem**.
14. **Unproven points**, each written as:

```text
À PROUVER SUR POSTGRESQL RÉEL — ...
```

When running under `cli-cycle`, also emit `.claude/cli-audit-data.json` following
`../shared/result-schema.md`. Put severity, invariant ID, concrete interleaving, proof status, and
criticality in `findings[].metadata`. The prose report remains authoritative.

## Dynamic handoffs

| Condition detected | Recommend | Why |
|---|---|---|
| Database decision or safe SQLx implementation is missing | `/cli-forge-data` | Design or implement the correction from explicit invariants |
| Intended behavior and migrations/code disagree | `/cli-audit-drift` | Record and verify semantic contracts |
| PostgreSQL concurrency or migration proof is weak | `/cli-audit-test` | Audit the complete test strategy and proof ladder |
| Backup, restore, drift repair, or production topology is unsafe | `/cli-forge-resilience` | Build operational proof and repair paths |
| Locking, query plans, indexes, pool pressure, or latency need measurement | `/cli-forge-perf` | Establish a reproducible database performance gate |
| Migration ordering is displaced across image, entrypoint, CI, and app startup | `/cli-audit-hanoi` | Audit precedence and blast radius |

**Rule:** recommend handoffs; do not execute them automatically outside `cli-cycle`.

## Integration with other cli-* skills

| Skill | Relationship |
|---|---|
| `cli-forge-data` | Designs and implements the correction; this skill reviews its safety proof |
| `cli-audit-drift` | Checks invariant intent against implementation history |
| `cli-audit-review` | Reviews the whole diff; this skill supplies database-specific blocking gates |
| `cli-audit-test` | Scores test strategy; this skill defines PostgreSQL-specific proof cases |
| `cli-forge-lld` | Owns the component design; this skill deepens schema, transaction, and migration safety |
| `cli-forge-resilience` | Owns prod parity, recovery, failure injection, and incident memory |
| `cli-cycle` | Runs this audit when PostgreSQL/SQLx or migration signals are present |

# Completion criterion

A database change is safe only when its laws are explicit, PostgreSQL protects them as far as
possible, dangerous interleavings have concrete answers, migrations permit coexistence, and every
remaining drift is detectable and repairable.
