---
name: applying-ddia
description: Use when designing, reviewing, debugging, simplifying, or explaining data systems involving databases, storage, data models, indexes, replication, sharding, transactions, consistency, distributed failures, caches, retries, events, queues, logs, schemas, batch or stream processing, reliability, recovery, or scalability; or when designing personal-data retention/deletion, privacy-sensitive data architectures, or automated decision systems whose data pipelines affect people.
---

# Applying DDIA

Make engineering decisions in this order:

1. Restate the actual product behavior and measurable workload/SLO.
2. Identify invariants: what must never be committed or observed.
3. Specify required guarantees per operation; name what may be stale, delayed, duplicated, reordered, approximate, unavailable, or lost.
4. Mark systems of record and derived/rebuildable state.
5. Walk concurrency, timeout, crash, retry, lag, partition, overload, and recovery paths that can violate the invariants.
6. Read only the relevant references below—normally one to three.
7. Compare realistic alternatives on guarantees, failure behavior, latency, throughput, cost, and operational/recovery complexity.
8. Recommend the simplest sufficient architecture. State assumptions, main trade-offs, and measurable conditions that would change the answer.

Do not start from a technology and justify it afterward. Complexity needs a concrete requirement.

For vendor-, product-, or version-specific behavior, use current official documentation as the authority. Apply DDIA to reason about the guarantees and trade-offs; do not infer a current product guarantee from the book or these references alone.

## Choose references

- Broad review: [architecture-review.md](references/architecture-review.md). Load [common-architecture-mistakes.md](references/common-architecture-mistakes.md) only for an explicitly requested simplification or a technology-first/over-complex design.
- Database/workload choice: [requirements-and-database-choice.md](references/requirements-and-database-choice.md) and [decision-tables.md](references/decision-tables.md).
- Models, storage, or indexes: [data-modeling-storage-and-indexes.md](references/data-modeling-storage-and-indexes.md).
- Replication, geography, sharding, or hot keys: [replication-and-partitioning.md](references/replication-and-partitioning.md).
- Transactions, isolation, or consistency: [transactions-and-consistency.md](references/transactions-and-consistency.md).
- Timeouts, clocks, leases, fencing, consensus, or failover: [distributed-failures-and-coordination.md](references/distributed-failures-and-coordination.md).
- Retries, duplicates, or ordering: [retries-idempotency-and-ordering.md](references/retries-idempotency-and-ordering.md).
- Events, queues, logs, CDC, or outbox: [events-queues-and-logs.md](references/events-queues-and-logs.md).
- Batch, streams, windows, backfills, or schema evolution: [batch-streaming-and-schema-evolution.md](references/batch-streaming-and-schema-evolution.md).
- Reliability, overload, restoration, or operability: [reliability-recovery-and-operability.md](references/reliability-recovery-and-operability.md).
- Personal-data retention/deletion, privacy-sensitive architecture, or consequential automated-decision pipelines: [responsible-data-systems.md](references/responsible-data-systems.md).

For DDIA source verification or deeper teaching nuance, use [source-notes/coverage-map.md](source-notes/coverage-map.md) and one relevant chapter note. Do not load chapter notes during ordinary work.

## Working and teaching modes

For real work, be concise and concrete. Use: **Recommendation**, **Why**, **Important assumptions**, **Main failure modes and recovery/operations**, **When to reconsider**. Discuss alternatives only when material; do not lecture about DDIA.

When explicitly teaching, explain the mental model, why the problem exists, a concrete example and failure scenario, competing approaches, and how the concept appears in real systems.
