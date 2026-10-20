---
name: messaging-and-streaming
description: >
  Design queueing and event streaming. Use when choosing a message queue or
  event log, decoupling services, async processing, Kafka/RabbitMQ/Pulsar,
  publish-subscribe, delivery semantics (at-most/at-least/exactly once),
  ordering, event-driven architecture, or backpressure. Triggers: "message
  queue", "Kafka", "pub/sub", "event-driven", "async processing", "delivery
  guarantees".
---

# Messaging and Streaming

Move data between services without tight coupling, and keep the pipeline
reliable.

## When to use
- Decoupling producers from consumers.
- Async/background processing.
- High-throughput event streaming or CDC.
- Choosing queue vs stream vs webhook.

## Queue vs stream
| Need | Use |
|---|---|
| Task distribution to workers (competing consumers) | Message queue |
| Durable ordered log, replay, many consumers | Event stream / log (Kafka) |
| High-throughput firehose, retention windows | Kafka-class |
| Legacy guaranteed messaging | MQ (avoid unless required) |

## Delivery semantics
- **At-most-once:** fast, may lose.
- **At-least-once:** no loss, duplicates possible → consumers must be
  **idempotent** (dedup keys, upsert).
- **Exactly-once:** effectively exactly-once *processing* via idempotent
  consumers + transactional offsets; end-to-end exactly-once is expensive and
  often unattainable.
See `...\delivery-semantics.md`.

## Design rules
- Make consumers idempotent; assume redelivery.
- Handle ordering only where required (partition by key).
- Dead-letter queue for poison messages; bounded retries.
- Backpressure/flow control; monitor consumer lag.
- Schema registry + evolution (Avro/Protobuf) for compatibility.
- Outbox pattern to atomically publish DB writes + events.
- Watch message size, key distribution (hot partitions), and retention.

## Event-driven architecture
- Pub/sub vs queue; choreography vs orchestration for workflows.
- Event sourcing + CQRS for auditable, replayable state.
- Cloud messaging patterns: fan-out, competing consumers, priority, dead
  letter, claim-check for large payloads.

## Checklist
- [ ] Pattern chosen (queue/stream) with rationale.
- [ ] Delivery semantics stated; consumers idempotent.
- [ ] Ordering + partitioning strategy defined.
- [ ] DLQ + retry policy + poison handling.
- [ ] Schema + versioning + registry.
- [ ] Backpressure + lag monitoring.
- [ ] Retention, size, and cost planned.

## Common pitfalls
- Non-idempotent consumers on at-least-once → duplicate side effects.
- Assuming global ordering.
- Unbounded queues hiding downstream failures.
- Hot partitions from a bad key.
- Publishing events outside the DB transaction (lost/phantom events).

## References
- `...\types-of-message-queue.md`, `...\explaining-the-4-most-commonly-used-types-of-queues-in-a-single-diagram.md`
- `...\how-do-message-queue-architectures-evolve.md`
- `...\the-ultimate-kafka-101-you-cannot-miss.md`, `...\why-is-kafka-fast.md`, `...\top-5-kafka-use-cases.md`, `...\can-kafka-lose-messages.md`
- `...\delivery-semantics.md`
- `...\top-6-cloud-messaging-patterns.md`
- `...\differences-in-event-sourcing-system-design.md`, `...\how-do-we-incorporate-event-sourcing-into-the-systems.md`
- `...\change-data-capture-key-to-leverage-real-time-data.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`distributed-systems`, `high-availability-and-resilience`,
`data-and-ai-pipelines`, `backend-architecture`.
