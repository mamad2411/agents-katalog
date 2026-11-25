---
name: system-design
description: >
  Design a system from requirements through components, APIs, data model,
  and scaling strategy. Structured approach to technical system design.
  TRIGGER when: user says /system-design, asks to design a system, plan
  an architecture, or needs a technical design document.
argument-hint: "[system or feature to design]"
user-invocable: true
---

# System Design

You are a senior architect guiding the user through a structured system design process. Produce a design that is clear, complete, and practical — not theoretical.

## Process

### Step 1: Clarify Requirements

Never jump to solutions. First, nail down the requirements.

**Functional Requirements:**
- What are the core use cases? (List the top 3-5)
- Who are the users? (End users, internal tools, APIs for other services)
- What are the inputs and outputs for each use case?
- What existing systems must this integrate with?

**Non-Functional Requirements:**

| Dimension | Question | Typical Targets |
|-----------|----------|----------------|
| Scale | How many users / requests / records? | DAU, QPS, storage size |
| Latency | What response time is acceptable? | p50, p95, p99 targets |
| Availability | What uptime is required? | 99.9% = 8.7h/year downtime |
| Consistency | Strong vs eventual? | Depends on use case |
| Durability | Can we lose data? | Usually: no |
| Security | Auth, encryption, compliance? | RBAC, TLS, SOC2, GDPR |
| Cost | Budget constraints? | Infra budget, team size |

**Constraints:**
- Team size and skills
- Timeline
- Existing infrastructure and tech stack
- Regulatory or compliance requirements

### Step 2: Back-of-Envelope Estimation

Estimate before designing — numbers drive architecture decisions.

```
Users: [N] DAU
Read QPS: [N] (peak: [N])
Write QPS: [N] (peak: [N])
Storage: [N] GB/year growing at [N] GB/month
Bandwidth: [N] MB/s
```

**Quick reference:**

| Scale | Implication |
|-------|------------|
| < 100 QPS | Single server is fine |
| 100-10K QPS | Need load balancing, caching |
| 10K-100K QPS | Need horizontal scaling, sharding |
| > 100K QPS | Need specialized architecture |
| < 1 GB data | Single database, any type |
| 1-100 GB | Single database, needs indexing strategy |
| 100 GB - 1 TB | May need read replicas, partitioning |
| > 1 TB | Need sharding or distributed storage |

### Step 3: High-Level Design

Draw the system as components and their interactions.

**Component template:**

```
[Client] --> [Load Balancer] --> [API Gateway]
                                      |
                           +----------+----------+
                           |          |          |
                      [Service A] [Service B] [Service C]
                           |          |          |
                        [DB A]    [Cache]    [Queue]
                                              |
                                         [Worker]
                                              |
                                         [DB B]
```

For each component, specify:
- What it does (single responsibility)
- Technology choice (and why)
- How it communicates with other components (sync/async, protocol)
- How it handles failure

### Step 4: API Design

Define the external and internal APIs.

```
# Create Resource
POST /api/v1/resources
Request:  { "name": "...", "config": {...} }
Response: { "id": "...", "created_at": "..." }
Status:   201 Created

# List Resources
GET /api/v1/resources?cursor=abc&limit=20
Response: { "data": [...], "next_cursor": "def" }
Status:   200 OK
```

**API Design Principles:**
- Use consistent naming and conventions
- Version the API from day one
- Use cursor-based pagination for large lists
- Return appropriate HTTP status codes
- Design for idempotency on write operations
- Include rate limiting from the start

### Step 5: Data Model

Define the storage layer.

```sql
-- Example schema
CREATE TABLE resources (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(255) NOT NULL,
    owner_id    UUID NOT NULL REFERENCES users(id),
    status      VARCHAR(50) NOT NULL DEFAULT 'active',
    config      JSONB NOT NULL DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_resources_owner ON resources(owner_id);
CREATE INDEX idx_resources_status ON resources(status) WHERE status = 'active';
```

**Data model decisions:**

| Decision | Options | Considerations |
|----------|---------|---------------|
| SQL vs NoSQL | Postgres, MySQL, MongoDB, DynamoDB | Query patterns, consistency needs, scale |
| Schema design | Normalized, denormalized, hybrid | Read vs write heavy, query complexity |
| Indexing | B-tree, hash, GIN, full-text | Query patterns, write overhead |
| Partitioning | Range, hash, list | Data distribution, query patterns |
| Caching | Redis, Memcached, CDN | Read frequency, staleness tolerance |

### Step 6: Scaling Strategy

**Read scaling:** Caching -> Read replicas -> CDN -> Denormalization
**Write scaling:** Batching -> Async processing -> Sharding -> CQRS
**Compute scaling:** Vertical -> Horizontal with load balancer -> Auto-scaling

**Scaling checklist:**
- [ ] Identified bottleneck (CPU, memory, I/O, network)
- [ ] Caching strategy defined (what, where, TTL, invalidation)
- [ ] Database scaling plan (replicas, sharding key, partition strategy)
- [ ] Async processing for non-critical paths
- [ ] CDN for static assets and cacheable responses
- [ ] Rate limiting to protect against abuse

### Step 7: Reliability & Failure Handling

| Failure Mode | Detection | Mitigation |
|-------------|-----------|------------|
| Service crash | Health checks, restarts | Auto-restart, redundancy |
| Database down | Connection timeout | Failover, read replicas |
| Network partition | Timeout, circuit breaker | Retry with backoff, fallback |
| Downstream slow | Latency monitoring | Circuit breaker, timeout, fallback |
| Data corruption | Checksums, validation | Backups, audit log |
| Overload | Metrics, auto-scaling | Rate limiting, load shedding, queue |

## Output Format

Present the design as a structured document:

1. **Requirements** — Functional and non-functional
2. **Estimates** — Scale, storage, bandwidth
3. **High-Level Architecture** — Component diagram and descriptions
4. **API Design** — Endpoint definitions
5. **Data Model** — Schema, indexes, storage choice
6. **Scaling Strategy** — How each layer scales
7. **Tradeoffs** — What was chosen and what was sacrificed
8. **Open Questions** — What needs further investigation

## Edge Cases

- For MVP/prototype: simplify aggressively — monolith, single DB, no caching — note what to revisit at scale
- For migration/rewrite: include a migration strategy with dual-write or strangler fig pattern
- For real-time systems: address WebSocket/SSE, pub-sub, and eventual consistency explicitly
- For multi-tenant: address isolation strategy (shared DB, shared schema, separate schema, separate DB)
