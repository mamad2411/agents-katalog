---
name: event-driven-architecture
description: Designs reliable event-driven systems - events vs commands, event styles, schema evolution, ordering and partition keys, at-least-once delivery with idempotent consumers, transactional outbox, retries and dead-letter queues, replay, lag monitoring, choreography vs orchestration. Use when adding a message broker or queue, publishing or consuming events (Kafka, RabbitMQ, SQS, Pub/Sub, Service Bus), messages are duplicated, lost or out of order, or a consumer is stuck on a poison message. Not for in-process event emitters.
license: MIT
---

# Event-Driven Architecture

Assume every message can arrive twice, late, or out of order, and that producers and consumers will be deployed at different times. A design is correct only if it stays correct under those conditions: idempotent consumers, explicit ordering keys, compatible schema changes, and a place for messages that can't be processed.

## When to use

- Introducing a broker, queue or stream between services.
- Designing event contracts or changing an existing event schema.
- Bugs with duplicate processing, lost messages, ordering, or stuck consumers.
- Choosing between choreography (events) and orchestration (a coordinator) for a multi-step process.

Not for: in-process observers or UI event handlers. For whether to go async at all, see the system-design skill.

## Messages: events, commands, queries

| Type | Meaning | Naming | Coupling |
| --- | --- | --- | --- |
| Event | A fact that happened; producer doesn't know who listens | Past tense: `OrderPlaced` | Low: any number of consumers |
| Command | A request for one specific receiver to do something | Imperative: `ChargePayment` | Higher: sender expects a handler |
| Query | A request for data with a response | `GetOrderStatus` | Usually better as a synchronous API |

Don't disguise commands as events (`PleaseSendEmailEvent`). If you need a specific outcome from a specific service, it's a command; send it to that service's queue.

## Event styles

| Style | Payload | Use when | Watch out |
| --- | --- | --- | --- |
| Event notification | IDs and minimal facts | Consumers need to know something changed; they fetch details if needed | Callbacks to the producer add load and coupling |
| Event-carried state transfer | The relevant state at the time | Consumers keep their own local copy; producer must not be called back | Larger messages; consumers hold stale-but-consistent copies |
| Event sourcing | Events are the system of record; state is rebuilt from them | Strong audit/temporal needs, complex domains | High complexity: snapshots, projections, schema evolution forever. Don't adopt casually |

Default: event-carried state transfer for integration events between services.

## Workflow

1. **Name the events in domain language** (see the domain-driven-design skill). One event per meaningful business fact, not per database row change.
2. **Define the envelope.** Every event carries: unique event ID, type, schema version, occurred-at timestamp (UTC), producer/source, the aggregate/entity ID, and correlation and causation IDs for tracing. The CloudEvents specification is a good standard envelope (required attributes: `id`, `source`, `specversion`, `type`).
3. **Define the payload as a contract.** Use a schema (Avro, Protobuf or JSON Schema) stored in a registry or the repo. Payloads include everything consumers need without calling back, and nothing internal.
4. **Choose the partition/ordering key.** Pick the entity whose events must be processed in order (usually the aggregate ID: `orderId`). Order is guaranteed only within a partition/key, never across the whole topic.
5. **Publish reliably with the transactional outbox** (below). Never "write to the database, then publish" as two independent steps.
6. **Make every consumer idempotent** (below).
7. **Design failure handling:** bounded retries with backoff, then a dead-letter queue with alerting and a replay path.
8. **Plan schema evolution** before the first release. Read [references/schema-evolution.md](references/schema-evolution.md).
9. **Monitor:** consumer lag (messages and time), DLQ depth, processing error rate, end-to-end latency from occurred-at to processed.

## Delivery semantics

- **At-least-once is the realistic default.** Brokers redeliver after timeouts, crashes and rebalances; producers retry after ambiguous failures. Duplicates will happen.
- **At-most-once** (ack before processing) loses messages on crashes. Use only for data you can afford to lose (some metrics).
- **Exactly-once** claims are scoped. For example, Kafka transactions can make read-process-write between Kafka topics exactly-once, but side effects outside the broker (database writes, emails, payments) still need idempotency. Treat "exactly-once" as "effectively once via idempotency".

## Transactional outbox

```
BEGIN;
  UPDATE orders SET status = 'placed' WHERE id = :id;
  INSERT INTO outbox (id, aggregate_id, type, payload, created_at)
  VALUES (:event_id, :id, 'OrderPlaced', :payload, now());
COMMIT;
-- A relay (polling the outbox table, or change data capture such as Debezium)
-- publishes rows to the broker and marks or deletes them.
```

- State change and event are committed atomically; the relay may publish an event more than once, which idempotent consumers absorb.
- Publish in `created_at`/sequence order per aggregate to keep ordering.
- Clean up published outbox rows on a schedule.

## Idempotent consumers

Pick one per consumer:

| Technique | How |
| --- | --- |
| Dedupe table | In the same transaction as the side effect, insert the event ID into `processed_events` with a unique constraint; on conflict, skip |
| Natural idempotency | Upserts and set-style updates (`SET status = 'shipped'`) instead of increments |
| Version check | Apply only if `event.version` is greater than the stored version for that entity; ignore older or equal |
| Idempotency key at the external API | Pass the event ID as the idempotency key to payment/email providers that support it |

Ack/commit the message only after the side effect and dedupe record are committed.

## Ordering

- Same key always goes to the same partition (Kafka partitions, SQS FIFO message groups, Pub/Sub ordering keys, Service Bus sessions).
- Increasing the partition count changes which partition a key maps to; ordering per key can break during the change. Plan partition counts up front.
- Concurrency inside a consumer (thread pools, async handlers) can reorder messages from one partition. Process per key sequentially if order matters.
- When strict order is impossible, make handlers order-tolerant with version checks.

## Retries, poison messages and DLQs

1. Retry transient errors (timeouts, 5xx, lock conflicts) a few times with exponential backoff and jitter.
2. Don't retry permanent errors (validation failure, unknown schema version): send straight to the DLQ.
3. Don't block a partition forever on one bad message: after N attempts move it to a DLQ or a delayed retry topic so later messages continue. (If strict per-key order matters, park the key's later messages too, or stop and alert.)
4. Every DLQ has: an alert, an owner, a way to inspect messages, and a tested replay tool.
5. Store the failure reason, attempt count and original topic/partition/offset with the dead-lettered message.

## Replay and reprocessing

- Keep events long enough to rebuild consumers (topic retention, or an archive in object storage).
- Replays only work with idempotent consumers. Test replay in staging first.
- Kafka: reset a consumer group with `kafka-consumer-groups.sh --reset-offsets` (`--to-datetime`, `--to-earliest`, `--shift-by`); it runs as a dry run unless `--execute` is given, and the group must have no active members. **Resetting offsets or replaying in production reprocesses real side effects: show the dry-run result and get explicit confirmation first.**

## Choreography vs orchestration

| Choreography (services react to events) | Orchestration (a coordinator sends commands) |
| --- | --- |
| Few steps, loosely related reactions (send email, update search index) | Multi-step business process with ordering, timeouts and compensation (checkout, onboarding) |
| No single owner of the flow needed | One team owns the end-to-end flow and its state |
| Risk: the flow is invisible; hard to answer "where is order 123?" | Risk: the orchestrator becomes a god service |

For orchestrated multi-step flows with compensation, see the saga pattern in the resilience-patterns skill. Workflow engines (Temporal-style durable execution, cloud step-function services) are worth considering before hand-rolling saga state machines.

## Broker notes (conceptual)

| Broker type | Model | Good for |
| --- | --- | --- |
| Log / stream (Kafka, Kinesis-style, Event Hubs) | Append-only partitioned log; consumers track offsets; replayable | High throughput, many independent consumers, replay |
| Message broker (RabbitMQ, ActiveMQ) | Queues and routing (exchanges); messages removed on ack | Work queues, flexible routing, per-message acks |
| Cloud queue (SQS, Azure Service Bus, Google Pub/Sub) | Managed queue/topic; varying ordering and dedupe features | Low ops burden; check each service's ordering, dedupe window and retention limits in its docs |

## Anti-patterns

- **Dual write** - updating the database and publishing in two steps; one will eventually fail without the other.
- **Non-idempotent consumers** - `balance = balance + amount` on every delivery.
- **Global ordering assumptions** - expecting topic-wide order from a partitioned system.
- **Breaking schema changes** - renaming or removing a field consumers read, deployed in one go.
- **Leaking internals** - publishing ORM entities or table rows as events; every schema change becomes a cross-team break.
- **DLQ as a black hole** - messages go there and nobody is alerted or owns them.
- **Event chains nobody can trace** - no correlation IDs; a failed flow can't be followed across services.
- **Events for request/response** - using two topics to fake a synchronous call; use an API.

## Done when

- Every event has a named type in domain language, a versioned schema, a standard envelope and a documented ordering key.
- Producers publish through an outbox or an equivalently atomic mechanism.
- Every consumer is idempotent, and a duplicate-delivery test proves it.
- Retry policy, DLQ, alerting, owner and replay procedure exist for every consumer.
- Schema changes follow the compatibility rules and are checked in CI or by the registry.
- Lag, DLQ depth and end-to-end latency are monitored with alerts.

## References

- [references/schema-evolution.md](references/schema-evolution.md) - read before changing any event schema or choosing a registry compatibility mode.
