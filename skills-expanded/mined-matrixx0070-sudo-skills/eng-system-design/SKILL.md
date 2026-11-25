---
name: eng-system-design
version: 1.0.0
description: Design a service, API, or data model with numeric requirements, clear boundaries, explicit interfaces, and an honest scaling and failure story.
author: matrixx0070
tags: [system-design, api-design, data-modeling, scaling, architecture, reliability]
capabilities: []
---

## When to use

When you must design a new service, a significant API, or a data model — or evaluate one someone else proposed. Anchor everything in real requirements, not resume-driven complexity.

**Not for:** trivial CRUD endpoints, one-off scripts, or premature scaling of a system with no traffic. If load fits in a single node with headroom, say so and stop.

## Method

1. **Requirements first, with numbers.** List functional needs and non-functional targets: expected QPS, data volume, read/write ratio, latency budget (p50/p99), consistency needs, availability target. Estimate the numbers — don't hand-wave.
2. **Define boundaries.** Decide what this component owns and what it delegates. Draw seams so responsibilities don't leak across them.
3. **Design the interface before internals.** Specify the API contract — resources/operations, request/response shapes, idempotency, pagination, versioning, error semantics.
4. **Model the data to fit access patterns**, not fashion. Define schema, keys/indexes, and growth. If reads dominate and joins are hot, denormalize and say what you traded; if writes dominate, protect write throughput.
5. **Address scale and failure.** Identify the bottleneck; plan caching, partitioning, async/queue work, and backpressure. For each dependency, state what happens when it is slow or down — degrade, queue, or fail closed.
6. **If a requirement number is unknown, flag it as an open question** rather than designing for an imagined peak. State trade-offs and the parts you're least sure about.

## Example

```
Requirements: URL shortener, 1k writes/s, 50k reads/s, 500M links,
  read p99 < 50ms, writes can be eventually consistent.
Boundary: owns short-code issuance + redirect; delegates auth to gateway.
API: POST /links {url} -> {code}; GET /{code} -> 302 (idempotent).
Data: KV store keyed by code (base62 counter); read-heavy -> cache hot codes.
Scale/failure: CDN + read cache absorbs reads; if store is down, serve
  cached redirects and 503 new writes (fail closed on issuance).
Open question: expiry/TTL policy unspecified — confirm before schema freeze.
```

## Pitfalls

- **Designing for scale you don't have** — microservices and sharding for 10 QPS.
- **Interface built after internals**, leaking storage details into the API contract.
- **No failure story** — "the DB is always up" is not a plan.
- **Requirements as adjectives** ("fast", "scalable") with no QPS, latency, or volume numbers.

## Output format

```
Requirements: <functional + non-functional, with numbers>
Components & boundaries: <text diagram; who owns what>
API contract: <operations, request/response shapes, idempotency, versioning, errors>
Data model: <schema, keys, indexes, growth, normalization trade-off>
Scaling & failure: <bottleneck, caching, partitioning, per-dependency degradation>
Trade-offs & open questions: <what you gave up; unknowns to confirm>
```
