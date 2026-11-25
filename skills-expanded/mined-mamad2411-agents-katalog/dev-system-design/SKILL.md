---
name: dev-system-design
description: Guides the agent through high-level system design — component decomposition, scalability, data stores, communication patterns, and trade-off analysis. Used during US execution when a feature requires significant architectural decisions.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Senior Staff Engineer / System Architect**. Your primary job is to make the right trade-offs for the given scale and constraints — not to produce the most sophisticated design. Do NOT spawn a subagent for this.

Design the system/subsystem for: $ARGUMENTS

> **Scope distinction:** [`plan-architecture-agent`](../plan-architecture-agent/SKILL.md) produces the *project-wide* `docs/SYSTEM_ARCHITECTURE.md` during bootstrap. This skill is used *within* a feature/US execution when a significant architectural decision must be made (new service, new data tier, cross-component boundary). Its output is a design note in `docs/design-docs/<feature_id>/system-design.md`.

> **Apply the shared [engineering principles](../../resources/engineering-principles.md) throughout**, especially §2 (architecture before code) and §3 (design patterns deliberately).

---

## Step 0: Frame the Problem
Before drawing any diagram or picking any technology, write brief answers to these four questions:
1. **What problem does this solve?** (user-visible behavior from the US)
2. **What is the expected scale?** (requests/sec, data volume, number of users — use real numbers or documented estimates)
3. **What are the non-functional requirements?** (latency target, availability SLA, consistency requirement, compliance)
4. **What already exists?** (read `docs/SYSTEM_ARCHITECTURE.md` and list the components this new piece must integrate with)

Do not proceed until these are written.

---

## Step 1: Decompose into Components
Break the system into logical components (services, modules, or layers) and define each component's **single responsibility**:

| Component | Responsibility | Owns | Exposes |
|---|---|---|---|
| `user-service` | Auth, profile management | `users` table | REST `/users`, gRPC UserService |
| `order-service` | Order lifecycle | `orders` table | REST `/orders`, publishes `order.placed` event |

Rules:
- **High cohesion, loose coupling**: each component owns its data; no component reads another's DB directly.
- **One reason to change**: if a component changes for two unrelated reasons, split it.
- **Don't over-decompose prematurely**: start with the fewest components that satisfy the requirements. Split only when there is a concrete reason (independent scaling, team boundary, different tech requirement).

---

## Step 2: Choose Communication Patterns
For each interaction between components, choose the appropriate pattern and justify the choice:

| Pattern | When to use | When NOT to use |
|---|---|---|
| **Synchronous REST / gRPC** | Caller needs an immediate response (read data, validate, return result) | When the caller can tolerate latency or doesn't need the result |
| **Async messaging / pub-sub** | Fire-and-forget; fan-out to multiple consumers; decouple producer from consumer availability | When strong consistency or immediate response is required |
| **Event streaming (Kafka/Kinesis)** | High-volume ordered events; replay; audit log; multiple independent consumers | Simple point-to-point low-volume tasks |
| **GraphQL** | Client-driven flexible queries; aggregating multiple backend sources | Internal service-to-service calls |
| **BFF (Backend for Frontend)** | When FE needs a different shape/aggregation than the core APIs provide | Simple apps with one client type |

Document each connection in the design note with: direction, protocol, sync/async, and retry policy.

---

## Step 3: Data Storage Decisions
For each data store, justify the choice against the access pattern:

| Store type | Best for | Avoid when |
|---|---|---|
| **Relational DB (PostgreSQL)** | Structured data, ACID transactions, complex joins, audit trails | Need schema-less flexibility or massive horizontal write scale |
| **Document DB (MongoDB)** | Schema-flexible, hierarchical/nested data, rapid iteration | Strong relational constraints, complex aggregations |
| **Key-Value (Redis)** | Session storage, rate limiting, leaderboards, pub-sub, cache | Primary source of truth for critical data |
| **Time-series (InfluxDB, TimescaleDB)** | Metrics, IoT, telemetry, anything with a timestamp as the primary key | Non-temporal relational data |
| **Search (Elasticsearch, Typesense)** | Full-text search, faceted filtering, fuzzy matching | Primary transactional store |
| **Object storage (S3)** | Blobs, files, media, backups | Small structured records, low-latency lookups |

**Data ownership rule**: each service owns exactly one primary data store. No sharing.

---

## Step 4: Scalability & Reliability Patterns
Address the non-functional requirements from Step 0 with explicit patterns:

### Scalability
- **Horizontal scaling**: Stateless services scale out. Move state to the data tier (DB, cache, object store).
- **Caching strategy**: Define what to cache, TTL, and invalidation strategy. Layer: CDN → API gateway → application cache → DB query cache.
- **Database scaling**: Read replicas for read-heavy workloads. Sharding for write-heavy workloads (last resort — adds significant complexity).
- **Async offloading**: Move heavy/slow work (email, PDF generation, ML inference) to background queues.

### Reliability
- **Idempotency**: All state-mutating operations must be safe to retry. Use idempotency keys for payments and critical writes.
- **Circuit breaker**: Wrap calls to external services. Fail fast rather than cascade-fail.
- **Retry with backoff**: Exponential backoff + jitter for transient failures. Define max retry count and DLQ strategy.
- **Health checks & readiness probes**: Every service exposes `/healthz` (liveness) and `/readyz` (readiness).
- **Graceful degradation**: Define what happens when each dependency is unavailable. Prefer degraded functionality over total failure.

### CAP Theorem — pick your trade-off explicitly:
- **CP** (Consistent + Partition-tolerant): correct even if some nodes are unreachable. Accepts unavailability. Right for: financial data, inventory.
- **AP** (Available + Partition-tolerant): always responds, may return stale data. Right for: user profile reads, catalog search.
- Never claim CA in a distributed system — partition tolerance is not optional.

---

## Step 5: Security Boundaries
- **AuthN/AuthZ at the gateway**: Validate JWTs / session tokens at the API gateway or BFF. Internal service-to-service calls use mTLS or signed headers — never re-validate user identity in every microservice.
- **Zero-trust internal network**: Do not assume internal traffic is trusted. Sign inter-service requests.
- **PII data isolation**: Services that store PII must document it. Apply field-level encryption for SSN, credit card, health data.
- **Secret management**: No secrets in code, environment variables, or config files committed to git. Use Vault, AWS Secrets Manager, or equivalent.

---

## Step 6: Observability Plan
For every new component, define before it ships:
1. **Logs**: structured JSON, correlation ID (trace ID) propagated through every call.
2. **Metrics**: RED (Rate, Errors, Duration) per endpoint; business KPIs per domain event.
3. **Traces**: distributed tracing spans across service boundaries (OpenTelemetry).
4. **Alerts**: define the SLO → define the alert threshold → assign the on-call runbook.

---

## Step 7: Output — Design Note
Write `docs/design-docs/<feature_id>/system-design.md` with:
- **Context**: what problem, what scale, what constraints.
- **Decision**: chosen design, components, communication, data stores.
- **Alternatives considered**: what else was evaluated and why it was rejected.
- **Trade-offs accepted**: what this design gives up and why that's acceptable.
- **Open questions**: decisions deferred to implementation (link to child tasks).

Do NOT implement code in this skill. The output is the design note. Hand off to [`dev-be-developer`](../dev-be-developer/SKILL.md), [`dev-go-developer`](../dev-go-developer/SKILL.md), or the appropriate coding skill with a pointer to this note.
