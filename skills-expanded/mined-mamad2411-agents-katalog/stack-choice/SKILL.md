---
name: stack-choice
last_reviewed: 2026-09-06
group: Understand and design
description: >-
  Evaluate technology options against requirements, team skill, scale and total cost, and record
  why. Use when evaluating technologies, frameworks, or database trade-offs.
---

# Stack Choice

The most expensive technical debt is selecting an architectural stack that solves problems you do not yet have. Technology selection must be governed by operational Total Cost of Ownership (TCO), existing team competency, delivery velocity, and irreversible technical constraints, formally documented in an Architectural Decision Record (ADR).

## 1. The 5-Dimension Stack Evaluation Rubric

Evaluate technology candidates across five weighted criteria:

### A. Operational Total Cost of Ownership (TCO)
Calculate fully-loaded costs across 12 months:
$$\text{TCO} = \text{Infrastructure Bills (Cloud/Compute/DB)} + \text{Third-Party SaaS Licenses} + \text{Maintenance Engineering Hours} + \text{Hiring/Onboarding Cost}$$
- *Managed vs. Self-Hosted*: A managed database (e.g. AWS RDS Aurora at $150/mo) is vastly cheaper than self-hosting PostgreSQL on EC2 when factoring in engineer hours for backups, failover patching, and telemetry.
- *Vendor Lock-In Evaluation*: Distinguish between open standards with hosted vendors (PostgreSQL on Supabase/Neon/RDS) vs proprietary locked APIs (DynamoDB, Firebase).

### B. Team Skill & Onboarding Velocity
- Prioritize technologies the current engineering team already understands in depth. An unfamiliar "modern" framework introduces a 3–6 month velocity penalty while engineers learn its failure modes in production.
- Default rule: Choose "boring technology" (Dan McKinley's Innovation Tokens) for 90% of the stack, spending at most 2 innovation tokens on core product differentiators.

### C. Data Modeling & Database Trade-Off Matrix

| Architecture Pattern | Recommended Technology | When to Choose | When to Avoid |
|---|---|---|---|
| **Relational / ACID** | PostgreSQL | 90% of web apps; structured entities, foreign keys, complex joins, financial ledgers | Write-heavy telemetry ingestion >100k events/sec |
| **Document / Semi-Structured** | MongoDB / DynamoDB | Rapidly mutating schemas with isolated document access patterns | Relational reporting, multi-table transactions |
| **Local-First / Edge** | SQLite / Turso / Cloudflare D1 | Single-tenant silos, desktop apps, embedded edge devices, minimal memory footprints | Multi-region simultaneous writes without CRDTs |
| **In-Memory Cache & Queues** | Redis / Dragonfly | Session caching, token blacklists, pub/sub, rate limiters | Persistent primary data storage |

### D. Frontend & Application Framework Trade-offs
- **Next.js / SvelteKit / Nuxt**: Full-stack applications requiring SEO, authenticated dashboards, and server-side rendering (SSR).
- **Astro / Vite**: Content sites, blogs, and marketing surfaces with zero-JS baseline and client islands.
- **Go / Rust**: High-throughput microservices, network proxies, or compute-heavy background processing engines.
- **Node.js / Python**: Rapid API prototyping, data manipulation, LLM orchestrations, and large ecosystem libraries.

## 2. Architectural Decision Record (ADR) Template

Every significant stack choice must be recorded as an immutable ADR in `docs/adr/`:

```markdown
# ADR-004: Adoption of PostgreSQL with Prisma ORM

## Status
Accepted (2026-09-06)

## Context
Our application requires multi-tenant data isolation, strict transaction atomicity for billing,
and support for complex reporting queries. The team is proficient in TypeScript and SQL.

## Decision
We choose PostgreSQL 16 (hosted on AWS RDS Aurora) using Prisma ORM for schema migrations
and typed client generation.

## Consequences & Trade-offs
- Positive: Guaranteed ACID compliance; strong TypeScript type safety across queries.
- Positive: Rich ecosystem of extensions (pgvector for semantic search).
- Negative: Connection pooling requires PgBouncer / RDS Proxy for serverless execution.
- Risk Mitigation: Configure AWS RDS Proxy immediately to prevent connection exhaustion.
```

## Critical Rules
1. Every stack recommendation must explicitly quantify the trade-offs: what capabilities or operational ease is sacrificed for the chosen benefits.
2. Limit total innovation tokens to two per project; novel databases, novel runtimes, and novel deployment models should not all be adopted simultaneously.
3. Record all stack decisions in an ADR with context, alternatives considered, and failure criteria.

## Verification Checklist
- [ ] Requirements decomposed into data shape, read/write ratios, latency, and compliance constraints.
- [ ] Total Cost of Ownership (TCO) modeled across infrastructure and ongoing maintenance.
- [ ] Team skill gap assessed with realistic learning-curve latency accounted for.
- [ ] At least two viable alternatives evaluated with explicit rejection rationales.
- [ ] ADR drafted detailing context, decision, consequences, and mitigation paths.

## Anti-Patterns
- NEVER select a database or framework solely because it is trending on social media.
- NEVER adopt distributed microservices architecture when a modular monolith satisfies scale requirements.
- NEVER switch production technology without documenting a migration and rollback strategy.
