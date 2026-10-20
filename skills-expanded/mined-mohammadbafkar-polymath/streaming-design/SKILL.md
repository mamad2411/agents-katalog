---
name: streaming-design
description: Design a streaming topology (Kafka/Pulsar/Kinesis) — topics, partitioning key, delivery semantics, consumer groups, retention/compaction, ordering, and backpressure.
---

# streaming-design

> A stream is a durable, partitioned, replayable log — not a queue. The partition key decides ordering, parallelism, and hot-spots all at once, so choose it first.

## When to use

- Standing up or reshaping a Kafka/Pulsar/Kinesis topic and its producers/consumers.
- Deciding delivery semantics, partition count/key, or retention for an event stream.
- A workflow invokes `polymath-streaming:streaming-design`.

Not this when: you are designing the *business* event flow (saga, choreography, outbox) — that is `polymath-architecture:event-driven-design`. For windowed/stateful computation over the stream, `polymath-streaming:stream-processing`.

## Inputs

- The events, their volume/throughput, ordering needs, and consumer count.
- Durability/replay and retention requirements.

## Procedure

1. **Topic design**: one topic per event type/bounded purpose; name and own it. Decide schema + a registry with a compatibility rule (backward/forward).
2. **Partition key** — the central decision: pick a key that (a) co-locates events that must stay ordered (e.g. per-entity id), (b) spreads load evenly (avoid a hot key), (c) supports the consumer parallelism you need. Ordering is per-partition only — there is no global order.
3. **Partition count**: size for peak consumer parallelism and throughput headroom; remember repartitioning later breaks key→partition mapping. State the number and why.
4. **Delivery semantics**: at-least-once (default; consumers must be idempotent), at-most-once (lossy, rare), or exactly-once (transactions/idempotent producer — costs throughput; use only where dupes are unacceptable). Name the choice and the dedup mechanism.
5. **Consumer groups**: one group per independent consumer concern; within a group, partitions divide across members. Plan rebalancing behavior and offset-commit strategy (commit after processing, not before).
6. **Retention / compaction**: time/size retention for event logs; log compaction for changelog/“latest state per key” topics. State replay expectations.
7. **Backpressure & lag**: monitor consumer lag; decide what happens when consumers fall behind (scale out, pause producers, or shed) — never silently unbounded.
8. **Failure handling**: dead-letter topic for poison messages, and a retry/skip policy.

## Output

- A one-page topology spec: topics + schemas + compatibility, the partition key + count rationale, delivery semantics + dedup, consumer groups + offset strategy, retention/compaction, lag/backpressure plan, and the DLQ policy.

## Quality bar

- The partition key is justified against ordering, load spread, and parallelism together.
- Delivery semantics are stated, and at-least-once is paired with idempotent consumers.
- Offsets commit after successful processing; a DLQ exists for poison messages.
- Consumer lag is monitored with a defined behavior when consumers fall behind.
