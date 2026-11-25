---
name: kafka-patterns
description: Topic design, partition strategies, consumer group patterns, exactly-once processing, and dead letter queue handling. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When designing event-driven systems, Kafka topics, consumers, or sagas/outbox patterns. Pair with backend-dev, kafka-expert, event-sourcing-expert.
---

# Kafka Patterns (Grok Port)

Topic design, partitioning, consumer groups, exactly-once, DLQ, and outbox/saga patterns for reliable event streaming. Grok-native: Production Contract, hooks (on_event / on_api_feature), compound from real incidents, palace for architectural decisions, claim-verif on every "exactly-once" claim.

## Topic & Partition Design
- Partition key = entity that must be ordered (orderId, userId, tenantId). Never random for stateful consumers.
- Partitions = throughput target / consumer parallelism. Start conservative; re-partition is painful.
- Retention: time-based (7d/30d) + size; compact for state topics (last value per key).
- Naming: `<domain>.<entity>.<event>` e.g. `orders.order.created`, `payments.payment.succeeded`.

## Consumer Groups & Processing
- One consumer group per logical subscriber (order-processor, notification-service, analytics).
- `enable.auto.commit=false` + manual commit after successful side effects (or use transactions).
- Idempotent producers + transactional.id for exactly-once end-to-end (EOS).

## Exactly-Once + Outbox (for DB + Kafka atomicity)
Pattern: write to outbox table in same tx as business data, then relay to Kafka (or use Debezium CDC).

```sql
-- In business tx
BEGIN;
INSERT INTO orders (...) VALUES (...);
INSERT INTO outbox (aggregate_type, aggregate_id, event_type, payload)
VALUES ('order', '123', 'OrderCreated', '{"id":"123",...}');
COMMIT;
```

Relay (idempotent via event id):
- Read unprocessed outbox rows.
- Produce with key = aggregate_id, headers for event id / version.
- On success mark processed (or delete); on failure DLQ + retry.

## Dead Letter Queue (DLQ) + Retry
- Non-retryable errors (validation, business rule) → DLQ immediately.
- Transient (network, DB down) → retry with backoff + jitter, max N, then DLQ.
- DLQ topic: same schema + error headers (error_type, error_msg, original_offset, retry_count).
- Monitor DLQ lag; human or automated re-drive process.

## Grok Integration (Production Contract)
- Primary: backend-dev + kafka-expert + event-sourcing-expert.
- Fire on_event_driven_change, on_api_feature, on_db_change when topics, producers, consumers, or outbox tables are introduced/modified.
- Pre-Flight (mandatory): "Partition key correct for ordering needs? Consumer group isolation? Idempotency / exactly-once required? Outbox or CDC for DB consistency? DLQ + monitoring plan? Schema evolution / compatibility strategy (backward/forward)?"
- Ledger: every new topic, partition change, consumer group, outbox addition, or breaking schema evolution with task_id + compatibility note + rollback (reprocess from offset or compacted state).
- Handoff: topic list + partition counts + key strategy, consumer group mapping, exactly-once proof (or "at-least-once + idempotency"), DLQ runbook, schema registry subjects, offset management strategy, test matrix (happy + poison + rebalance).
- Friction + compound: every "duplicate orders because no idempotency key on consumer" or "rebalance caused 30min lag because partitions=1" → compound to preflight rules and shared producer/consumer templates.
- Palace: "Chose outbox + relay over Debezium for this service because we needed custom enrichment before publish and full control over retry; rejected 2PC because operational complexity".
- Claim-verification: Two-pass. Grep "produce" or "XADD" or "outbox" → read_file actual producer + consumer code + run integration test with failure injection → "Outbox table + relay with idempotency on (aggregate_id, event_id) exists at services/orderEventPublisher.ts:42 and test 'exactly-once on DB failure' passes ✓VERIFIED". Never claim "idempotent" or "no dups" without reading code + evidence.
- Pair with: event-driven-patterns, backend-patterns, api-patterns, test-enforcement (chaos + rebalance tests), sast-patterns (no secrets in payloads), observability (consumer lag, DLQ size, processing latency).

## When to Activate
- Designing or changing any Kafka topic, producer, consumer, outbox, or schema.
- Swarm Phase 2 (event/backend tracks) + Phase 3 review.
- Before deploys that publish/consume critical events.
- PRs touching Kafka config, outbox tables, or consumers.
- Reliability or data consistency reviews.

See .grok/skills/event-driven-patterns/SKILL.md (if present), backend-patterns, preflight, compound-learnings, memory-palace + layered-recall (store "why this partition key" decisions). Always test rebalance, poison, and exactly-once paths. Production Contract: ledger + handoff + preflight + friction on every streaming change.

Events are the source of truth for state in event-driven systems. Bad partitioning or missing idempotency is data corruption that is very hard to repair.
