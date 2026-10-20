---
name: cqrs-design
description: Separate command and query models with explicit projections and eventual-consistency budgets. Use when read and write patterns diverge sharply, or when audit, replay, and independent scaling justify the extra moving parts.
---

# CQRS Design

CQRS splits the system into a write side that protects invariants and a read side optimized for queries. It pays off when reads and writes have very different shapes, scaling needs, or consistency requirements - and is overkill almost everywhere else.

## Stack Baseline (2026)

| Concern | Recommended |
| --- | --- |
| Write store | Postgres 17, EventStoreDB 24, Marten, Axon Server 4 |
| Event log | Kafka 3.7, EventBridge, NATS JetStream 2.10 |
| Read stores | Postgres read replicas, Elasticsearch 8 / OpenSearch 2.13, Redis 7.4, Materialize, ClickHouse 24 |
| Projections | Kafka Streams, Flink 1.20, Debezium 2.x, Marten projections, Axon Tracking Processors |
| Frameworks | Axon Framework, Marten, EventFlow, Equinox (F#), NestJS CQRS module |
| Consistency | Read-your-writes via session pinning, version stamps, or wait-for-projection tokens |
| Observability | OTel traces from command to projection; per-projection lag SLOs |

## When to Use
- Reads outnumber writes by 100x+ and need denormalized shapes (search, dashboards).
- Multiple read models serve different consumers (mobile, analytics, search).
- Audit and replay require an event log as the source of truth.
- The domain has rich invariants that benefit from explicit aggregates (often paired with DDD).

## Prerequisites
- Domain model with clear aggregates and command boundaries.
- A reliable event log or CDC pipeline with ordering guarantees per aggregate.
- Operational maturity for at least two stores (write + one read) and projection lag monitoring.
- UX agreement on staleness windows and read-your-writes behavior.

## Instructions

1. **Justify the split**: Document the divergence (query shapes, scale ratio, audit needs). If a read replica or materialized view solves it, prefer that. Apply CQRS where the divergence is structural.

2. **Model commands and events explicitly**: Commands are imperative (`PlaceOrder`), events are past-tense facts (`OrderPlaced`). Aggregates accept commands, validate invariants, and emit events.

   ```mermaid
   flowchart LR
     U[User] -->|Command| API[Command API]
     API --> AGG[Aggregate]
     AGG -->|Events| LOG[(Event Log)]
     LOG --> P1[Projection: OrderSummary]
     LOG --> P2[Projection: SearchIndex]
     LOG --> P3[Projection: Analytics]
     P1 --> Q[Query API]
     P2 --> Q
   ```

3. **Design one read model per use case**: Resist a universal read model. A search index, a dashboard rollup, and a customer order list are three projections, each tuned to its query.

4. **Build idempotent projections**: Track `(projection_name, last_event_id)`; updates must be idempotent so replays from offset N rebuild deterministically.

   ```sql
   CREATE TABLE order_summary (
     order_id uuid PRIMARY KEY,
     customer_id uuid NOT NULL,
     total_cents bigint NOT NULL,
     status text NOT NULL,
     last_event_id uuid NOT NULL,
     updated_at timestamptz NOT NULL
   );
   -- upsert keyed by order_id; ignore if last_event_id is older
   ```

5. **Define an eventual-consistency budget**: e.g. "99% of orders visible in OrderSummary within 1s; 99.9% within 5s". Show staleness in UI when exceeded; offer read-your-writes via aggregate-version tokens returned from commands.

6. **Plan for replay and schema change**: Treat projections as derived data. New projection = replay log; schema change = run new projection in parallel, switch reads, drop old.

7. **Operate with lag SLOs**: Per-projection lag and error rate dashboards; alert on lag burn-rate; auto-pause projections on schema-incompatible events.

## Common Pitfalls

| Pitfall | Why it bites | Mitigation |
| --- | --- | --- |
| CQRS for CRUD | Pure overhead, no payoff | Use plain CRUD; reach for CQRS only on real divergence |
| One giant read model | All the cost of denormalization, none of the focus | One projection per query family |
| Non-idempotent projections | Replays corrupt data | Upsert by key + last_event_id; deterministic handlers |
| Hidden eventual consistency in UX | Users see stale data and complain | Publish a budget; show "updating..." state; provide RYW token |
| Coupling commands to read schema | Every UI change forces command refactor | Keep aggregates pure; evolve projections independently |
| No replay tooling | Schema changes become incidents | Build replay-from-offset and parallel-projection ops from day one |

## Output Format

Deliver a CQRS design doc: justification and scope, command and event catalog, aggregates with invariants, list of read models with owner and query, projection deployment and replay plan, eventual-consistency budget and UX rules, observability schema, and rollback plan.

## Authoritative References

- [Martin Fowler - CQRS](https://martinfowler.com/bliki/CQRS.html)
- [Greg Young - CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
- [microservices.io - Pattern: CQRS](https://microservices.io/patterns/data/cqrs.html)
- [Axon Framework documentation](https://docs.axoniq.io/)
- [Marten documentation](https://martendb.io/)
- [EventStoreDB documentation](https://developers.eventstore.com/)
- [Designing Data-Intensive Applications - Stream Processing](https://dataintensive.net/)
