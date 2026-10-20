---
name: kafka-consumer-patterns
description: >
  Use when building, reviewing, or debugging a Kafka consumer: delivery semantics,
  offset-commit strategy, consumer-group rebalancing, idempotent processing,
  dedup, poison-message handling, dead-letter topics, ordering, or backpressure.
  MUST be loaded when: a repo consumes from Kafka using any client.
user-invocable: false
---

# Kafka Consumer Patterns

Reliability rules for the **consumer side** of Kafka, independent of client library and version — translate them to the repo's actual client API by mirroring existing consumers (see `agent-guidelines` → "Match Existing Code"). Config names are the canonical Kafka names; a client may expose them under a different key.

The fact everything below rests on: **a correctly-built Kafka consumer is at-least-once, so it WILL see duplicates** (rebalance, retry, crash-before-commit). Reliability comes from making processing tolerate redelivery, not from trying to prevent it.

## Anti-patterns (reject in review)

Each names the mechanism that makes it fail, so the finding can say why.

- **Auto-commit left on for non-trivial processing.** `enable.auto.commit=true` commits the *previously polled* batch on a timer during the next `poll()`; process asynchronously or hold records across polls and the committed position moves past unprocessed work → silent loss. For at-least-once: disable it and commit after processing succeeds.
- **Committing before processing succeeds** — degrades to at-most-once unless that is an explicit, documented choice. Never commit past a record not successfully handled or routed to a DLQ: "handled the error by skipping it" is how data loss looks in code.
- **No idempotency on an at-least-once consumer** → the guaranteed duplicates corrupt state. Preference order: naturally idempotent writes (upsert by business key, set-to-value not increment) → dedup on a business idempotency key → dedup on `(topic, partition, offset)`. The dedup record and the side effect are one transaction, or the bug is back. External calls (HTTP, payment, email) use the downstream's idempotency key or dedup before calling.
- **No commit in the rebalance revocation callback.** Revocation → assignment is two phases; `onPartitionsRevoked` (or equivalent) is the last chance to `commitSync` offsets for partitions about to be lost. `commitSync` there and on shutdown; `commitAsync` in the steady loop only — it has no retry, and a failed async commit can be superseded by a later successful one.
- **`catch (...) { /* skip */ }` in the poll loop** → invisible data loss. Classify transient (network, timeout, 5xx → bounded backoff retry) vs permanent (validation, deserialization, 4xx → no in-loop retry); after bounded retries route to a dead-letter topic or parking store with context (topic/partition/offset, error, timestamp), alert, then commit past it. Deserialization failures are DLQ'd as raw bytes before they crash `poll()`.
- **Heavy synchronous work on the poll thread exceeding `max.poll.interval.ms`** → the member is evicted → rebalance → the batch is reprocessed elsewhere (duplicate work, livelock). Lower `max.poll.records`, move work off the poll thread, or `pause()`/`resume()` partitions so polling (heartbeating) continues while in-flight work is bounded.
- **Assuming ordering across partitions.** Ordering is per-partition only; key by the entity whose order matters, and do not parallelize within a partition in a way that reorders. Effective parallelism is capped by partition count.
- **Claiming exactly-once for a pipeline with a non-Kafka sink.** Kafka transactions (`transactional.id`, `enable.idempotence`, `sendOffsetsToTransaction`, downstream `isolation.level=read_committed`) cover Kafka-to-Kafka consume-transform-produce only; a DB write or HTTP call inside the consumer is still at-least-once and falls back to idempotency.
- **`auto.offset.reset` left to default without a decision.** It decides where a new group or an expired offset starts: `latest` silently skips backlog, `earliest` reprocesses history, `none` forces the decision by erroring.
- **Consumer lag left unmonitored.** A stalled or slow consumer looks healthy from inside; lag is the only signal that it is falling behind.
- **An assignment strategy that differs from the rest of the group.** All members must agree on it; cooperative-sticky avoids stop-the-world revocation.
- **An unexpected schema crashing the consumer.** Respect the schema-registry compatibility mode, and handle a schema that does not match it as a poison message.

---

_Grounded in the Apache Kafka and Confluent consumer / delivery-semantics documentation. Timeouts and intervals (`auto.commit.interval.ms`, `session.timeout.ms`, `heartbeat.interval.ms`, `max.poll.interval.ms`) have version-dependent defaults — read them from the cluster/client version in use rather than from memory._
