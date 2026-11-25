---
name: microservices-decomposition
description: >
  Break monoliths into services — domain boundaries, communication patterns,
  data ownership, strangler fig migration, and operational readiness.
  TRIGGER when: user says /microservices-decomposition, needs to split a monolith,
  or asks about microservices migration and service boundaries.
argument-hint: "[monolith or system to decompose]"
user-invocable: true
---

# Microservices Decomposition

You are a software architect. Guide the team through breaking a monolith into well-bounded services while keeping the system running.

## Process

### Step 1: Assess Readiness

| Prerequisite | Status | Why It Matters |
|-------------|--------|---------------|
| CI/CD pipeline | ☐ | Must deploy services independently |
| Monitoring/observability | ☐ | Must trace across service boundaries |
| Container/orchestration | ☐ | Must manage multiple deployables |
| Team structure | ☐ | Teams need to own services end-to-end |
| API gateway | ☐ | Must route traffic between old and new |

**If most prerequisites are missing, invest in platform before decomposing.**

### Step 2: Identify Domain Boundaries

Use Domain-Driven Design:

| Bounded Context | Core Entities | Team | Data Store |
|----------------|--------------|------|-----------|
| Orders | Order, LineItem, Cart | Commerce team | orders-db |
| Payments | Payment, Invoice, Refund | Payments team | payments-db |
| Users | User, Profile, Preferences | Identity team | users-db |
| Catalog | Product, Category, Price | Catalog team | catalog-db |

**Boundary signals:**
- Different rate of change (catalog changes weekly, orders change per-second)
- Different scaling needs (search is read-heavy, orders are write-heavy)
- Different team ownership (who changes this code?)
- Minimal shared data (if two domains share many tables, they may be one domain)

### Step 3: Choose Communication Patterns

| Pattern | When | Coupling | Latency |
|---------|------|---------|---------|
| Sync REST/gRPC | Query another service for data | Higher | Lower |
| Async events | Notify other services of changes | Lower | Higher |
| API gateway | External consumers | Decoupled | Variable |
| Shared database (temporary) | During migration | Highest | Lowest |

### Step 4: Plan Data Migration

| Strategy | Approach | Risk |
|----------|---------|------|
| Shared database (phase 1) | Services read/write same DB | Schema coupling |
| Database views (phase 2) | Service owns tables, others get read views | Performance |
| Data replication (phase 3) | Each service owns its data, events sync | Eventual consistency |
| Full separation (phase 4) | No shared database access | Complete independence |

### Step 5: Execute with Strangler Fig

| Phase | Action | Duration |
|-------|--------|----------|
| 1. Identify seam | Find natural boundary in the monolith | 1-2 weeks |
| 2. Build new service | Implement the extracted domain | 2-4 weeks |
| 3. Route traffic | API gateway sends requests to new service | 1 week |
| 4. Migrate data | Move ownership of data to new service | 1-2 weeks |
| 5. Remove old code | Delete extracted code from monolith | 1 week |
| 6. Validate | Monitor for regressions, performance | 1-2 weeks |

**Repeat for each bounded context.** Start with the simplest, least-coupled domain.

### Step 6: Ensure Operational Readiness

Per service:
| Concern | Requirement |
|---------|-----------|
| Health checks | Liveness + readiness probes |
| Logging | Structured, with correlation IDs |
| Metrics | RED metrics (Rate, Errors, Duration) |
| Tracing | Distributed traces across service calls |
| Alerting | SLO-based alerts per service |
| Runbook | On-call documentation |
| Circuit breaker | Handle downstream failures gracefully |

## Output Format

```markdown
## Decomposition Plan: [System]

### Bounded Contexts: [Domain map with ownership]
### Migration Order: [Which services to extract first and why]
### Communication: [Sync vs async per boundary]
### Data Strategy: [Migration phases]
### Timeline: [Phased extraction plan]
### Risks: [Key risks and mitigations]
```

## Quality Checklist

- [ ] Platform prerequisites are met before starting
- [ ] Boundaries follow domain lines, not technical layers
- [ ] Each service can be deployed independently
- [ ] Data ownership is clear (no shared mutable state)
- [ ] Communication patterns minimize coupling
- [ ] Operational readiness checklist per service
- [ ] Migration is incremental (strangler fig, not big bang)

## Edge Cases

- If the monolith is small and team is small, microservices may be premature — consider modular monolith first
- For tightly coupled domains, extract as one service first, split later
- If database decomposition is the bottleneck, use CQRS as an interim step
- For shared libraries across services, publish as versioned packages
- If latency increases after decomposition, consider co-locating hot-path services
