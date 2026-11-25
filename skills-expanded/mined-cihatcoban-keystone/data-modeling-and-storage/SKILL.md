---
name: data-modeling-and-storage
description: Designs schemas, constraints, indexes and storage choices, and changes them safely with expand-contract migrations. Triggers - design the schema, add a column, write the migration, which database, document database or relational, index this query, slow query, backfill.
---

# Data Modeling and Storage

Data outlives every application that touches it. Code is rewritten in a
weekend; a schema mistake propagates into backups, exports, downstream systems
and other teams' assumptions, and is still there years later. Treat schema
changes as the least reversible thing you do.

## Choosing storage

Start from the access pattern, not the trend.

| Need | Fit |
|---|---|
| Relationships, invariants across rows, transactions | Relational. The default; earn your way off it |
| Unknown/variable attributes on a known entity | Relational + JSON column, not a document store |
| Truly schemaless, aggregate-at-a-time access | Document store |
| Ephemeral, high-churn, expiring | Key-value cache |
| Append-only, time-ordered, heavy aggregation | Time-series or columnar |
| Full-text relevance ranking | Search index — as a *derived* store, never the source of truth |
| Similarity over embeddings | Vector index, usually as an extension of the primary store |
| Graph traversal many hops deep | Graph store — only if traversal depth is genuinely the workload |

**Polyglot persistence has a real price:** consistency between stores becomes
your problem. Every additional store is a sync path that can be stale, a backup
to test, and a failure mode. One store with an extension usually beats two.

## Schema discipline

1. **Constrain at the database.** `NOT NULL`, uniqueness, foreign keys, check
   constraints. Application-only validation is bypassed by the next importer,
   job or console session. The database is the last line that always holds.
2. **Types carry meaning.** Timestamps with timezone, always UTC. Money as
   decimal or minor-unit integers — never floating point. Enumerations as a
   constrained text column or lookup table, not an ad-hoc string.
3. **Natural key vs surrogate key.** Use a surrogate primary key; still declare
   a unique constraint on the natural key. Without it, duplicates arrive.
4. **Normalize until it hurts, denormalize until it works.** Start normalized.
   Denormalize only with a measurement showing the join is the bottleneck, and
   write down how the copy stays correct.
5. **Nullable means "unknown", not "not yet set".** Three-valued logic in
   queries is where silent wrong answers come from. Prefer a default or a
   separate state column.
6. **Soft delete is a design decision.** `deleted_at` means every query needs
   the filter and every unique index must account for it. Often an archive
   table is cleaner.

## Indexing

- Index for the **queries you run**, confirmed by an execution plan — not for
  columns that "look important".
- Composite index column order matters: equality predicates first, then range,
  then sort. A prefix of the index is usable; a suffix is not.
- Every index costs write throughput and storage. Audit for unused indexes as
  deliberately as you add them.
- Verify with the planner (`EXPLAIN ANALYZE` or equivalent) **on
  production-like data volume**. A sequential scan on 500 test rows is fast and
  tells you nothing.
- Watch for index-defeating predicates: a function applied to the column, a
  leading wildcard, an implicit type cast.
- Choose the index shape the plan needs: a **partial** index for a hot subset
  (unbilled orders), a **covering** index with included columns for an
  index-only read, an **expression** index for a computed predicate. Each one
  only with a plan that uses it.

## Migrations: expand / contract

Never change in place. Three phases, three deploys:

| Phase | Action | Rollback |
|---|---|---|
| **Expand** | Add the new column/table, nullable. Write to both old and new. | Stop writing to new |
| **Migrate** | Backfill in batches. Switch reads to new, keep comparing against old. | Switch reads back |
| **Contract** | After a clean observation window, stop writing old and drop it. | None — this is the one-way step |

Rules:

- Each phase is a separate deploy that must work with the **previous** version
  of the application still running. Code and schema deploy at different
  instants; assume both orders happen.
- Backfill in bounded batches with a sleep. One `UPDATE` over a large table
  locks it and takes the system down.
- Add `NOT NULL` only after the backfill completes, as its own migration.
- **Bound every lock wait.** Run DDL with a short lock timeout and retry. A DDL
  waiting for its lock blocks every later query on the table, so one long
  transaction plus an unbounded wait is an outage.
- **Schema and data changes are separate migrations**, and a migration that
  has run anywhere shared is never edited — write a new one.
- Every migration has a tested `down`; CI runs up → down → up. In production,
  `down` is safe only before data is written in the new shape; after that,
  roll back with a new forward migration.
- Destructive changes ship alone, never inside a feature change.

What rewrites a table or blocks writes differs per engine — adding a default,
`NOT NULL`, a foreign key, an index, changing a type. Before writing the
migration, look the operation up for the project's engine and version in
`references/migration-engine-lookup.md` (PostgreSQL, MySQL, SQLite).

## Consistency and transactions

- One transaction should modify one consistency boundary (one aggregate).
  Needing two usually means the boundary is wrong.
- Keep transactions short. Never perform network I/O inside one.
- Know your isolation level and what it does *not* prevent — see
  `concurrency-and-consistency`.
- Cross-store consistency is not free: use the transactional outbox pattern
  rather than "write to DB then publish", which loses events on crash.

## Data you must be able to answer for

- **Retention**: how long, and what deletes it
- **Personal data**: which columns, justified, findable for an erasure request
- **Reproducibility**: can a derived value be recomputed from raw input? Keep
  the raw input if not
- **Backups**: taken, and *restored in a drill* — an untested backup is a
  hypothesis

## Exit checklist

- [ ] Constraints live in the schema, not only in application code
- [ ] Timestamps are timezone-aware UTC; money is not floating point
- [ ] Every index justified by a plan on realistic data volume
- [ ] Migration follows expand → migrate → contract, one phase per deploy
- [ ] Each phase is compatible with the previous application version
- [ ] Backfills are batched; `down` migration exists and is tested in CI
- [ ] Each DDL runs with a lock timeout; its rewrite and lock cost was looked up
      for this engine and version, not assumed
- [ ] Schema and data changes are separate migrations; no applied migration
      was edited
- [ ] Destructive change is in its own change set
- [ ] Retention and personal-data columns documented
