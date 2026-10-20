---
name: architecture-event-driven-cqrs
description: Use when designing async systems — events vs commands, event bus, eventual consistency, sagas, CQRS read/write split, event sourcing.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [architecture-essentials, observability-essentials]
---

# Event-Driven Architecture + CQRS

**Iron Law: events for cross-domain communication; commands for in-domain. CQRS only when read and write models genuinely diverge.**

EDA and CQRS pair well but solve different problems. Treat them separately. CQRS without event sourcing is fine. Event sourcing without CQRS is rare. **Conflating them is the most common confusion.**

## Events vs commands — the single most common confusion

|           | Command                                | Event                                    |
| --------- | -------------------------------------- | ---------------------------------------- |
| Intent    | "Do X"                                 | "X happened"                             |
| Direction | Sender → known receiver                | Emitter → 0..N subscribers               |
| Naming    | Imperative: `PlaceOrder`, `ChargeCard` | Past tense: `OrderPlaced`, `CardCharged` |
| Failure   | Sender expects success/failure         | Emitter doesn't know who's listening     |
| Coupling  | Sender knows what they want done       | Emitter only knows what happened         |

**Commands when you need a specific action. Events when you announce a fact.**

A common mistake: naming an event `ProcessPayment` (a command in disguise). When subscribers fail, the publisher doesn't know — but logically a payment needed to happen. That's a command, not an event.

## The event bus — pick the least powerful that fits

| Bus                                                       | Use when                                                     |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| **In-process** (Node EventEmitter, Python `blinker`)      | Single-process modular monolith; decoupling without ops cost |
| **Message broker** (Kafka, RabbitMQ, NATS, Redis Streams) | Cross-process, durability, fan-out at scale                  |
| **Cloud-native** (SNS/SQS, EventBridge, Pub/Sub)          | On a cloud, don't want to operate a broker                   |
| **Event store** (EventStoreDB, Kafka with retention)      | Events are the source of truth (event sourcing)              |

Kafka for a 3-service app is a battleship in a creek.

## Eventual consistency — the moment you go async

A user clicks "Place Order" → `OrderPlaced` → inventory decrements → email sent → analytics records. Between the click and the analytics row, the system is **temporarily inconsistent**.

Fine for most domains. **Not** fine if your UI promises "stock count exact right now."

Tools for living with it:

- **Read-your-writes:** optimistic local update after publishing, so user sees the change.
- **Idempotent handlers:** same event delivered twice → same outcome. Critical; every broker delivers duplicates.
- **Outbox pattern:** write domain change + outgoing event in _same DB transaction_; a relay ships the event. Solves "DB committed but event dropped." Relay options: (a) **polling worker** — `SELECT id, payload FROM outbox ORDER BY created_at FOR UPDATE SKIP LOCKED LIMIT 100`, ship to broker, delete on ack; simple, works on any DB. **Ship-then-delete leaves a window**: broker can accept while the delete fails → next poll re-publishes the same event → consumers MUST be idempotent (see below). (b) **change-data-capture** (Debezium reading Postgres WAL/MySQL binlog) — lower latency, no app-level polling, but heavy infra. Default to polling; reach for CDC when polling lag becomes the bottleneck.
- **Compensating actions** for downstream failure (see Sagas).

### At-least-once is the rule

"Exactly-once" claims usually mean "we dedupe under certain conditions." Treat every delivery as potentially duplicated.

Make handlers idempotent: track processed event IDs (`processed_events` table, event id = PK); use natural idempotency (`SET status = paid` is idempotent; `increment counter` is not); conditional writes (`UPDATE ... WHERE version = X`).

## Ordering

Brokers offer ordering within a partition/queue, not globally.

- `OrderPlaced` and `OrderCancelled` out of order → you cancel a non-existent order, silently wrong.
- **Partition by aggregate id** (`order_id`) for per-aggregate ordering.
- Don't assume global order. If your logic needs it, the design is wrong.

## Sagas (distributed workflows)

When a workflow spans services without distributed transactions (which don't really work at scale):

| Style                                                | Pros                                  | Cons                        |
| ---------------------------------------------------- | ------------------------------------- | --------------------------- |
| **Choreography** — each service reacts and emits     | Simpler, no central coordinator       | Hard to follow at scale     |
| **Orchestration** — saga orchestrator sends commands | Visible, single point of choreography | New single point of failure |

Each step has a **compensating action**: `BookFlight` → `BookHotel` → `BookCar`. Car fails → cancel hotel, cancel flight.

Compensations aren't always trivial. "Uncharge credit card; pretend it never happened" doesn't exist; "issue refund" does, and it's itself async. Plan for it.

## CQRS — separate read and write models

|          | Write side                                | Read side                                                  |
| -------- | ----------------------------------------- | ---------------------------------------------------------- |
| Receives | `PlaceOrderCommand`, `CancelOrderCommand` | `GetOrderById`, `ListOrdersForCustomer`                    |
| Returns  | success/failure/id — _not_ the new state  | DTO shaped for the consumer                                |
| Storage  | Normalized, transactional                 | Denormalized; could be same DB, replica, or different tech |
| Owns     | Invariants, validation                    | Reflection only — no invariants                            |

After a write commits, the read model updates. Three strategies:

| Sync mode                                                          | Trade-off                                                                               |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| **Synchronous projection** (same transaction)                      | Simple, strongly consistent; only works when stores share DB                            |
| **Async via events** (`OrderPlaced` → projector writes read model) | Eventually consistent; allows different read store (Elasticsearch read, Postgres write) |
| **On-demand** (compute lazily)                                     | Slow for popular reads; fine for rare ones                                              |

Most systems mix all three.

### Read model design

**Purpose-built for the screen/endpoint that consumes them.**

- One read model per query, ideally.
- Denormalize freely — joins precomputed, derived fields stored.
- Cheap to throw away and rebuild from events.

A read model with 12 joins to answer one screen is missing the point. Build a table whose rows _are_ the screen.

### Light CQRS (without event sourcing)

Just code organization:

- `OrderCommands.place_order(cmd) -> Result`
- `OrderQueries.list_for_customer(id) -> list[OrderListView]`

Both might read/write the same DB, but write side touches `orders` + `order_lines`; read side has an `order_view` table or materialized view. **Mostly discipline + naming.** Pays off in even modest systems.

### CQRS + event sourcing

Persist the sequence of events that produced state, not the current state. Read models are projections over the event log.

Event sourcing is a serious commitment — schema versioning, replay infra, projector management. Use **only** when:

- Audit + history are first-class (financial, regulated, healthcare).
- You need to build _arbitrary new views_ over historical data without re-fetching from external systems.
- The domain is genuinely event-shaped ("things that happen") not entity-shaped ("things that exist").

**PII + right-to-erasure conflict.** Event logs are append-only by design. GDPR/CCPA right-to-erasure lets a user demand removal of personal data. These fight each other. Two workable strategies: (a) **crypto-shredding** — store PII inside events encrypted with a per-subject key in a separate, deletable keystore; on erasure, drop the key (ciphertext remains, unrecoverable). Use **AEAD** (AES-GCM or ChaCha20-Poly1305) with a fresh random nonce per encryption — unauthenticated modes (CBC) let attackers tamper with PII fields; nonce reuse under AES-GCM breaks confidentiality. Rotate per-subject keys periodically and store them in an HSM/KMS, not a plain DB table. (b) **PII-out-of-events** — events carry only `customer_id`; PII lives in a regular CRUD table you `DELETE` from. Design for erasure on day 1; retrofitting is brutal. Replay re-emits events, so every downstream projection store (search indexes, warehouses, caches) needs its own erasure procedure and projectors must treat decryption failure as "subject erased, skip/tombstone," not crash. Erasure at source does NOT cascade automatically.

## When CQRS pays vs is overkill

| Pays when                                                   | Overkill when                             |
| ----------------------------------------------------------- | ----------------------------------------- |
| 1000× more reads than writes                                | CRUD app, one screen per entity           |
| Read shapes wildly different (customer / admin / analytics) | Low volume                                |
| Write logic is rich (lots of invariants)                    | Team unfamiliar with eventual consistency |
| Multiple read stores (search, cache, warehouse)             | Tight deadlines + uncertain domain        |

A useful smell for adopting CQRS: one screen needs five joins, the next needs three different joins on the same tables, indexes nobody else uses keep piling up.

## When async beats sync

- **Different rates/loads** — producer spikes, consumer processes steadily.
- **Multiple consumers** for the same fact (analytics + inventory + notifications + audit).
- **Decoupled deploys** — producer ships without coordinating with consumers.
- **Long-running work** that shouldn't block a user request.
- **Resilience** — consumer down → events queue up; sync RPC fails real-time.

## When sync is better

- **Strong consistency required** ("after this call, new state immediately visible").
- **User is waiting for the result.** They want the answer.
- **Tiny system** with one producer / one consumer.
- **Debugging is harder async.** Stack trace beats distributed log correlation.

## Anti-patterns

- Events for synchronous workflows (the user is waiting)
- CQRS as a default (one entity → one model, just use it)
- Event sourcing without audit/history requirements
- "Command disguised as event" (`ProcessPaymentRequested`)
- Producer writes to DB then event publish fails (use outbox)
- Handler not idempotent → duplicate causes double-charge
- "We're doing CQRS so we need event sourcing" — no
- One God read model serving every endpoint
- Read model used to enforce invariants
- Commands return the new state (return success/failure/id only)
- Schema change breaks consumers (version events, V1/V2 during transition)
- Replay rebuilds the world wrong because handlers had side effects (handlers must be pure)
- Debugging by `tail -f` (add correlation IDs, OpenTelemetry)

## Hand-off

For module boundaries that emit events, hexagonal isolation, and the foundational architecture choices: `Skill(architecture-essentials)`. For distributed tracing across event boundaries: `Skill(observability-essentials)`.
