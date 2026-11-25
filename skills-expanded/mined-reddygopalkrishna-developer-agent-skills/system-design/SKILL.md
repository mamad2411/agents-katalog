---
name: system-design
description: Designs software systems from requirements to a reviewed architecture - functional and non-functional requirements, back-of-envelope capacity estimates, components, data storage and consistency choices, sync vs async, failure modes, and an explicit tradeoff table. Use when designing a new service or feature with scale, availability or latency needs, choosing a database or queue, reviewing an architecture, or answering "how should we build X". Not for code-level design inside one module.
license: MIT
---

# System Design

Design from numbers and failure modes, not from favourite technologies. Every component in the design must be justified by a requirement, and every requirement that matters must have a number. The output is a design whose tradeoffs are written down, so reviewers can disagree with a specific decision rather than a vibe.

## When to use

- A new service, feature or integration with real scale, latency, availability or data-durability needs.
- Choosing storage, a queue, a cache, or a sync/async boundary.
- Reviewing an existing architecture or explaining why it is struggling.

Not for: class/function structure inside one codebase (see the legacy-refactoring or domain-driven-design skills), or writing the final document (see the design-docs skill, which this skill feeds).

## Workflow

1. **Clarify functional requirements.** List the core use cases as verbs ("user uploads a file", "admin exports a report"). Mark which are in scope for v1. Ask the user rather than assume.
2. **Pin non-functional requirements with numbers.** Fill the table below. If the user doesn't know, propose a number and label it an assumption.
3. **Estimate load** (back-of-envelope, see the worked example). Requests per second at average and peak, read/write ratio, data size per record, total storage over the retention period, bandwidth. Read [references/estimation.md](references/estimation.md) for latency orders of magnitude and conversion shortcuts.
4. **Define the API and data model first.** Key operations with inputs/outputs; main entities, their relationships, access patterns (which queries, how often, with which keys). Access patterns drive storage choice.
5. **Sketch the simplest architecture that meets the numbers.** Usually: clients, load balancer, stateless service, one relational database. Add a component only when a requirement forces it, and write down which one.
6. **Choose storage per access pattern** using the storage table. Decide consistency needs per operation, not per system.
7. **Decide sync vs async** for each interaction (table below). Put queues where work can be deferred, where producers and consumers scale differently, or where a downstream failure must not fail the user request.
8. **Walk through failure modes.** For every component and dependency: what happens when it is slow, down, or returns bad data? Remove single points of failure that the availability target cannot tolerate. See the resilience-patterns skill for timeouts, retries and circuit breakers.
9. **Cover cross-cutting concerns:** authentication and authorization, data privacy and retention, observability (see the observability skill), deployment and migration path, cost.
10. **Write the tradeoff table** (format below) and hand off to the design-docs skill for the written proposal. Include rejected alternatives and why.

## Non-functional requirements

| Property | Question | Example answer |
| --- | --- | --- |
| Scale | Users, requests/s at peak, data volume, growth per year | 2M DAU, 3k req/s peak, 1 TB/year |
| Latency | Target percentile for key operations | p99 read under 200 ms, p99 write under 500 ms |
| Availability | Target and allowed downtime | 99.9% monthly (about 43 min/month) |
| Durability | Can any acknowledged write be lost? RPO / RTO | RPO 0 for payments, 1 h for analytics; RTO 30 min |
| Consistency | Must readers see the latest write? Where is stale data acceptable? | Balance must be strongly consistent; feed may lag 10 s |
| Security / compliance | Data classes, residency, audit | PII, EU residency, audit log for admin actions |
| Cost | Budget or cost per unit | under $0.001 per request |

## Worked estimate

Notification service, 10M daily active users, 5 notifications per user per day:

- Writes: 10M x 5 = 50M/day. 50M / 86,400 s is about 580/s average. Peak at 5x is about 3,000/s.
- Reads: users open the inbox 3 times a day, 30M reads/day, about 350/s average, about 1,750/s peak.
- Storage: 500 bytes per notification x 50M = 25 GB/day. 30-day retention = 750 GB. With 3 replicas, about 2.25 TB.
- Conclusion: one well-indexed relational cluster or a key-value store handles this; partition by user ID if a single node can't take the write rate. No need for anything exotic.

Always state the conclusion the numbers lead to. Estimates are for choosing the order of magnitude, not exact sizing.

## Storage choices

| Need | Default choice | Consider instead when |
| --- | --- | --- |
| Transactions, relations, ad-hoc queries | Relational (PostgreSQL, MySQL, SQL Server) | Write rate or data size exceeds what one primary plus partitioning can handle |
| Lookups by key at very high rate | Key-value (Redis for cache/ephemeral; DynamoDB, Cassandra-style stores for durable) | You need multi-key transactions or ad-hoc queries |
| Flexible documents read as a whole | Document store, or JSON columns in relational | Strong relational integrity between documents |
| Full-text search, faceting | Search engine (OpenSearch/Elasticsearch, or built-in full-text search of the DB for small scale) | Never as the system of record; index from the primary store |
| Time-ordered metrics/events | Time-series database or columnar store | Low volume: a relational table with time partitioning |
| Analytics over large history | Columnar warehouse / lakehouse | Small data: read replica plus SQL |
| Files, media, backups | Object storage | Never store large blobs in the primary database |
| Event log / stream | Kafka-style log or managed stream | Simple work queue: a queue service is simpler |

Start with one relational database unless the numbers rule it out. Each extra store adds consistency, backup, security and on-call cost.

## Consistency and partitioning

- Decide per operation: strong consistency (money, inventory, uniqueness), read-your-writes (user sees their own update), eventual (feeds, counters, search).
- Read replicas lag. Route reads that must see a just-made write to the primary, or use a session token/version check.
- Partition (shard) by the key most queries filter on (often tenant or user ID). Hash partitioning spreads load; range partitioning keeps ranges queryable but creates hot spots on sequential keys.
- Look for hot keys (a celebrity user, a global counter) and plan for them: split counters, cache, or a dedicated partition.
- Cross-partition transactions are expensive. Design aggregates so most writes touch one partition (see the domain-driven-design skill).

## Sync vs async

| Use synchronous request/response when | Use asynchronous (queue/event) when |
| --- | --- |
| The caller needs the result to continue | The work can complete after the user gets a response |
| The operation is fast and the dependency is reliable | The dependency is slow, flaky or rate-limited |
| Strong consistency is required now | Producers and consumers scale or fail independently |
| Simplicity matters more than decoupling | Many consumers react to the same fact (fan-out) |

Async adds: at-least-once delivery, idempotent consumers, ordering questions, dead-letter handling, and lag monitoring. See the event-driven-architecture skill.

## Caching

Add a cache only for a measured read hotspot or a latency target the store can't meet. Decide up front: what key, what TTL, how it is invalidated, and what happens on a cache miss storm. See the caching-strategies skill.

## Failure-mode checklist

- [ ] Every component has a stated behaviour when a dependency is slow or down (timeout, fallback, error).
- [ ] No single point of failure the availability target can't tolerate (single DB primary without failover, one AZ, one region, a single cron host).
- [ ] Retries are bounded, with backoff and jitter, and only on idempotent operations.
- [ ] Overload behaviour is defined: rate limits, load shedding, queue limits.
- [ ] Backups exist, restores are tested, and RPO/RTO are achievable with them.
- [ ] Data migrations and deploys can roll back or roll forward safely (see the database-migrations skill).
- [ ] Multi-region decision is explicit: single region, active-passive (failover) or active-active (conflict handling needed). Don't add regions without an availability or residency requirement.

## Tradeoff table (output format)

| Decision | Chosen | Alternatives | Why | Cost / risk accepted |
| --- | --- | --- | --- | --- |
| Primary store | PostgreSQL | DynamoDB | Transactions across order and payment rows; team expertise | Manual sharding needed beyond ~10x growth |
| Notification delivery | Queue + workers | Synchronous send in request | Provider latency and outages must not affect checkout | At-least-once delivery; consumers must dedupe |

## Anti-patterns

- **Technology first** - "we'll use Kafka and microservices" before any requirement or number exists.
- **Premature distribution** - microservices, multiple databases or multi-region for a load one server handles.
- **Unstated assumptions** - designs that silently assume low traffic, a single tenant, or unlimited budget.
- **Ignoring the data model** - boxes and arrows with no access patterns; the database choice is then a guess.
- **Happy-path diagrams** - no answer to "what happens when this is down?".
- **Averages only** - sizing for average load and missing peak, or reporting mean latency instead of p99.
- **Search or cache as source of truth** - they will lose or stale data; the primary store must be authoritative.

## Done when

- Functional scope and every relevant non-functional requirement have explicit numbers or labelled assumptions.
- Load, storage and bandwidth estimates exist and lead to stated conclusions.
- API, data model and access patterns are defined; each storage choice maps to an access pattern.
- Every component is justified by a requirement; failure behaviour is defined for each dependency.
- The tradeoff table lists chosen options, alternatives, reasons and accepted risks, ready for the design-docs skill.

## References

- [references/estimation.md](references/estimation.md) - read when doing step 3: latency orders of magnitude, availability math, unit shortcuts.
