---
name: system-design
description: Use this skill when designing large-scale systems, choosing between architectural patterns, evaluating trade-offs, designing for scalability and reliability, or preparing for system design interviews. Trigger on keywords: system design, architecture, scalability, microservices, monolith, distributed system, design trade-offs, high availability, load balancing, caching strategy, database selection.
---

# System Design

## Design Process (Always Follow This Order)

1. **Clarify requirements** — functional AND non-functional
2. **Estimate scale** — users, requests/sec, data volume, read/write ratio
3. **Define the API** — what does the system expose?
4. **Design the data model** — what data, how stored, how accessed?
5. **High-level architecture** — major components and their relationships
6. **Deep dive** — zoom into the hardest or most critical parts
7. **Identify bottlenecks** — and how to address them

---

## Requirements Clarification

Before designing anything, answer:

**Functional:** What does the system do?
**Scale:** How many users? Requests/sec? Data volume? Growth rate?
**Availability:** What's the acceptable downtime? (99.9% = 8.7h/yr, 99.99% = 52m/yr)
**Latency:** What's the acceptable response time? (p99)
**Consistency:** Strong vs eventual consistency? (CAP theorem)
**Read/Write ratio:** Read-heavy? Write-heavy? Mixed?
**Geography:** Single region? Global? Data sovereignty requirements?

---

## Scalability Patterns

### Horizontal vs Vertical Scaling
| | Vertical | Horizontal |
|---|---|---|
| Method | Bigger machine | More machines |
| Limit | Hardware ceiling | Theoretically unlimited |
| Cost | Expensive | More cost-efficient |
| Downtime | Required | Zero downtime possible |
| Complexity | Simple | Requires load balancing, distributed design |

**Default: design for horizontal scaling from the start.**

### Load Balancing
- **Round Robin** — equal distribution, simple, doesn't account for load
- **Least Connections** — routes to server with fewest active connections
- **Consistent Hashing** — for distributed caches, minimizes redistribution on scaling

### Caching Strategy
| Layer | Tool | What to Cache |
|---|---|---|
| CDN | Cloudflare, CloudFront | Static assets, public API responses |
| Application | Redis, Memcached | Session data, computed results, DB query results |
| Database | Query cache, materialized views | Expensive aggregations |

**Cache Invalidation Strategies:**
- **TTL (Time-to-Live)** — expire after N seconds. Simple, may serve stale data.
- **Write-through** — update cache on every write. Strong consistency, slower writes.
- **Write-behind** — async cache update after write. Fast writes, eventual consistency.
- **Cache-aside** — app manages cache explicitly. Most flexible.

---

## Data Architecture

### SQL vs NoSQL Decision
| Use SQL When | Use NoSQL When |
|---|---|
| Data is relational | Data is unstructured or variable schema |
| ACID transactions required | Horizontal scaling is priority |
| Complex queries and joins | High write throughput needed |
| Data integrity is critical | Eventual consistency is acceptable |

### Database Sharding
Partition data across multiple databases:
- **Horizontal sharding** — split rows (e.g., users A-M on DB1, N-Z on DB2)
- **Vertical sharding** — split tables by feature (users DB, orders DB, payments DB)
- **Hash-based** — shard key hashed to determine partition

### Read Replicas
- Primary handles writes
- Replicas handle reads
- Good for read-heavy workloads (social feeds, analytics)
- Trade-off: replication lag = eventual consistency

---

## Architecture Patterns

### Monolith vs Microservices

| | Monolith | Microservices |
|---|---|---|
| Complexity | Low (operational), High (code over time) | High (operational), Lower (per service) |
| Deployment | Simple, all-or-nothing | Complex, independent per service |
| Scaling | Scale everything together | Scale services independently |
| Team size | Small teams, early stage | Larger teams, mature product |
| Start with | ✓ Yes | Only when monolith pain is real |

**Rule:** Start monolith, extract services when you feel the pain. Premature microservices is a common mistake.

### Event-Driven Architecture
Use when:
- Services need to be decoupled
- High throughput, async processing
- Audit trail / event sourcing needed

Tools: Kafka (high throughput), RabbitMQ (complex routing), AWS SQS (simple, managed)

### CQRS (Command Query Responsibility Segregation)
Separate read and write models:
- **Write model** — optimized for consistency and transactions
- **Read model** — optimized for query performance (denormalized, pre-computed)

Good for: high read/write ratio disparity, complex domain logic

---

## Common System Design Components

### API Gateway
- Single entry point for all clients
- Handles auth, rate limiting, SSL termination, routing
- Tools: AWS API Gateway, Kong, Nginx

### Message Queue
- Decouples producers from consumers
- Enables async processing, load leveling
- Provides buffer for traffic spikes

### CDN (Content Delivery Network)
- Serve static assets from edge locations close to users
- Reduce latency, reduce origin server load
- Cache invalidation is the hard part

### Search
- Don't use your primary DB for full-text search
- Elasticsearch / OpenSearch for complex text search
- Typesense for simpler, faster search

---

## Non-Functional Requirements Cheatsheet

| Requirement | Pattern |
|---|---|
| High Availability | Redundancy, failover, multi-region |
| Low Latency | CDN, caching, read replicas, edge computing |
| High Throughput | Horizontal scaling, async processing, queues |
| Consistency | ACID transactions, consensus protocols (Raft, Paxos) |
| Durability | Replication, backups, write-ahead logs |
| Security | Auth, encryption at rest + transit, least privilege |

---

## Trade-Off Framework

For every design decision, explicitly state the trade-off:

```
Decision: [what you chose]
Why: [what problem it solves]
Trade-off: [what you give up]
Alternative: [what you considered]
When to reconsider: [conditions that would change this decision]
```

---

## Back-of-Envelope Estimation

Useful numbers:
- 1M users × 10 req/day = ~120 requests/second
- 1KB × 1M requests/day = ~1GB/day of data
- SSD read: ~0.1ms | Network: ~1ms | HDD: ~10ms
- Single server handles ~10K-50K requests/sec (depends on complexity)
- RAM: 1 server ≈ 64-256GB | Typical process ≈ 100MB-1GB
