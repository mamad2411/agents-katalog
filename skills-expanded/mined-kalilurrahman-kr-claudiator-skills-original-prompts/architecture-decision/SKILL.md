---
name: architecture-decision
description: Document architecture decisions with ADRs (Architecture Decision Records). Outputs decision context, options, trade-offs, and rationale.
argument-hint: [decision type, stakeholders, constraints]
allowed-tools: Read, Write, Bash
---

# Architecture Decision Records (ADRs)

Document architectural decisions with structured records. Not informal notes — formal ADRs with context, options, consequences, and rationale that survive team changes.

## Process

1. **Identify decision.** Database choice, API pattern, deployment strategy.
2. **Gather context.** Requirements, constraints, stakeholders.
3. **List options.** 3-5 alternatives with pros/cons.
4. **Evaluate trade-offs.** Performance, cost, complexity, maintainability.
5. **Make decision.** Choose option with reasoning.
6. **Document consequences.** Positive, negative, and neutral impacts.
7. **Version control.** Store ADRs in repo, immutable once decided.

## Output Format

### ADR: [Decision Title]

**Status:** Accepted  
**Date:** 2024-01-15  
**Decision:** PostgreSQL for primary database  
**Alternatives:** MySQL, MongoDB  
**Context:** Need ACID, relational data, complex queries

---

## ADR Template

```markdown
# ADR-001: Choose Database for User Data

**Status:** Accepted  
**Date:** 2024-01-15  
**Deciders:** Engineering Team, CTO  
**Consulted:** Product, Data Science

## Context

We need to select a database for storing user data, orders, and analytics.

**Requirements:**
- ACID transactions (payment processing)
- Complex joins (reporting queries)
- 100k writes/day, 1M reads/day
- Budget: $500/month

**Constraints:**
- Team familiar with SQL
- Must run on AWS
- 99.9% availability SLA

## Decision

We will use **PostgreSQL** (RDS) for the primary database.

## Alternatives Considered

### Option 1: PostgreSQL (Chosen)
**Pros:**
- Strong ACID guarantees
- Excellent SQL support with complex queries
- JSON support for semi-structured data
- Mature ecosystem, good tooling
- Team expertise in SQL

**Cons:**
- Vertical scaling limits
- Slower writes than NoSQL
- More expensive than MySQL

**Estimated Cost:** $450/month (db.m5.large)

### Option 2: MySQL
**Pros:**
- Lower cost ($350/month)
- Good read performance
- Team knows SQL

**Cons:**
- Weaker transactional guarantees
- Less advanced query planner
- Limited JSON support

### Option 3: MongoDB
**Pros:**
- Horizontal scaling
- Flexible schema
- Fast writes

**Cons:**
- No ACID across documents
- Team has no NoSQL experience
- Join operations limited
- Higher cost ($600/month)

## Consequences

### Positive
- ACID transactions prevent payment inconsistencies
- Complex reporting queries are efficient
- Team productive immediately (no learning curve)
- JSON columns allow schema flexibility where needed

### Negative
- Vertical scaling limit at ~50k writes/second
- Will need read replicas if read traffic grows 10x
- More expensive than MySQL

### Neutral
- Standard SQL database, not differentiated
- Vendor lock-in to PostgreSQL dialect (minimal)

## Follow-Up Actions
- [ ] Set up RDS with Multi-AZ
- [ ] Configure automated backups (7-day retention)
- [ ] Set up read replica for analytics queries
- [ ] Document schema migration process
- [ ] Add connection pooling (PgBouncer)

## References
- PostgreSQL vs MySQL comparison: https://...
- RDS pricing calculator: https://...
- Team SQL expertise survey results
```

---

## ADR Index Structure

```
docs/adr/
├── README.md              # Index of all ADRs
├── 0001-use-postgresql.md
├── 0002-rest-over-graphql.md
├── 0003-kubernetes-deployment.md
├── 0004-event-sourcing-for-orders.md
└── 0005-oauth-for-authentication.md
```

### README.md (Index)
```markdown
# Architecture Decision Records

## Active Decisions
- [ADR-001](0001-use-postgresql.md) - PostgreSQL for primary database
- [ADR-002](0002-rest-over-graphql.md) - REST API over GraphQL
- [ADR-003](0003-kubernetes-deployment.md) - Kubernetes for deployment

## Superseded Decisions
- [ADR-004](0004-mongodb-for-analytics.md) - ~~MongoDB for analytics~~ → Replaced by ADR-010

## Rejected Decisions
- [ADR-007](0007-blockchain-for-audit.md) - Blockchain for audit trail (Rejected)
```

---

## Decision Status

```
Proposed → Under Review → Accepted → Superseded/Deprecated
                       ↘ Rejected
```

**Proposed:** Decision draft, seeking feedback  
**Under Review:** Active discussion  
**Accepted:** Implemented, current state  
**Rejected:** Considered but not chosen  
**Superseded:** Replaced by newer decision (link to new ADR)  
**Deprecated:** Still in use but planned for removal

---

## Common ADR Patterns

### Technology Choice
```markdown
# ADR-N: Choose [Technology]

**Context:** What problem needs solving?

**Decision:** Technology X

**Alternatives:**
- Technology Y
- Technology Z

**Trade-offs:**
- Performance vs Simplicity
- Cost vs Scalability
```

### Architectural Pattern
```markdown
# ADR-N: Use [Pattern] for [Component]

**Context:** Current architecture pain points

**Decision:** Implement [pattern]

**Consequences:**
- Increased complexity in [area]
- Better scalability for [use case]
```

### Build vs Buy
```markdown
# ADR-N: Build/Buy [Solution]

**Context:** Need [capability]

**Decision:** Build in-house / Buy [vendor]

**Cost Analysis:**
- Build: $X upfront, $Y maintenance
- Buy: $Z/month, $W integration
```

---

## Example ADRs

### ADR-002: REST API Over GraphQL

```markdown
# ADR-002: Use REST API Instead of GraphQL

**Status:** Accepted  
**Date:** 2024-01-20  
**Deciders:** Engineering Team

## Context

We need an API for mobile and web clients to access user data, products, and orders.

**Requirements:**
- Support iOS, Android, Web clients
- Simple CRUD operations (90% of use cases)
- Caching via CDN
- Team has no GraphQL experience

## Decision

Use **REST API** with JSON responses.

## Alternatives Considered

### Option 1: REST (Chosen)
**Pros:**
- Team knows REST well
- Simple to cache (HTTP caching)
- Mature tooling (Swagger, Postman)
- Easy to version (/v1/, /v2/)

**Cons:**
- Over-fetching (clients get extra fields)
- Multiple requests for related data
- No real-time subscriptions

### Option 2: GraphQL
**Pros:**
- Clients request exact fields needed
- Single request for nested data
- Strong typing with schema

**Cons:**
- Team learning curve (2-3 months)
- Harder to cache (POST requests)
- N+1 query problem requires DataLoader
- Security challenges (query depth, complexity)

## Consequences

### Positive
- Fast development (team productive day 1)
- CDN caching reduces server load
- Simple to understand and debug

### Negative
- Mobile apps fetch extra data (20% overhead)
- Dashboard needs 3 API calls instead of 1
- Real-time features need separate WebSocket

### Mitigations
- Add `?fields=` query param for sparse fieldsets
- Implement GraphQL in future if needs change (ADR-015)
- Use Server-Sent Events for real-time updates
```

---

### ADR-003: Microservices vs Monolith

```markdown
# ADR-003: Start with Modular Monolith

**Status:** Accepted  
**Date:** 2024-02-01

## Context

Early-stage startup, 5 engineers, unclear product-market fit.

## Decision

Build **modular monolith** with clear module boundaries, plan for future microservices split.

## Rationale

**Monolith Advantages (Now):**
- Single deployment (fast iterations)
- Easier debugging (single codebase)
- No distributed system complexity
- Faster development for small team

**Modular Design (Future-Proof):**
- Clear module boundaries (users, orders, payments)
- Independent databases per module
- API contracts between modules
- Easy to extract services later

**Microservices (Later):**
- When team > 20 engineers
- When scaling requirements diverge
- When deployment independence needed

## Success Metrics
- Deploy 10x/day (monolith)
- Extract first service within 12 months if needed
```

---

### ADR-004: Event Sourcing for Orders

```markdown
# ADR-004: Use Event Sourcing for Order Processing

**Status:** Accepted  
**Date:** 2024-03-01

## Context

Order workflow has many state transitions:
Created → Paid → Confirmed → Shipped → Delivered → Returned

Need full audit trail for compliance and customer support.

## Decision

Implement **event sourcing** for orders.

## Design

**Event Store:**
```
orders_events
- event_id (UUID)
- order_id
- event_type (OrderCreated, OrderPaid, OrderShipped)
- event_data (JSON)
- timestamp
```

**Current State (Projection):**
```
orders
- order_id
- status
- total_amount
- last_updated
```

## Consequences

### Positive
- Complete audit trail (who did what when)
- Can replay events to rebuild state
- Time-travel queries ("what was order state on Jan 15?")
- Easy to add new projections

### Negative
- More complex than CRUD
- Event schema evolution requires care
- Two tables instead of one (events + projection)
- Team learning curve

### Trade-offs Accepted
- Complexity worth it for compliance requirements
- Event replay enables powerful analytics
```

---

## Decision-Making Framework

### 1. Gather Context
```
- What problem are we solving?
- What are the requirements?
- What are the constraints (time, budget, team)?
- What are the non-negotiables?
```

### 2. List Options (3-5)
```
Option A: [Current approach or obvious choice]
Option B: [Alternative 1]
Option C: [Alternative 2]
```

### 3. Evaluate Trade-offs
```
Dimensions to consider:
- Performance
- Cost (upfront + ongoing)
- Complexity
- Maintainability
- Team expertise
- Vendor lock-in
- Time to implement
```

### 4. Make Decision
```
Choose option with best trade-offs for current context.
Document why other options rejected.
```

---

## ADR Anti-Patterns

### ❌ Too Vague
```markdown
## Decision
Use the best database.
```
**Problem:** No specifics, can't evaluate later

### ✅ Specific
```markdown
## Decision
Use PostgreSQL 15 on AWS RDS (db.m5.large) for user data.
```

---

### ❌ No Alternatives
```markdown
## Decision
We chose PostgreSQL.
```
**Problem:** Can't see what was considered

### ✅ Multiple Options
```markdown
## Alternatives Considered
1. PostgreSQL (chosen)
2. MySQL
3. MongoDB

[Detailed pros/cons for each]
```

---

### ❌ Missing Consequences
```markdown
## Decision
Use microservices.
```
**Problem:** No discussion of trade-offs

### ✅ Honest Consequences
```markdown
## Consequences

Positive:
- Independent deployments

Negative:
- 3x operational complexity
- Network latency between services
- Debugging harder

We accept these trade-offs because [reason].
```

---

## When to Write an ADR

**Yes:**
- Technology choices (database, language, framework)
- Architectural patterns (monolith vs microservices)
- API design (REST vs GraphQL)
- Deployment strategy (Kubernetes vs serverless)
- Security model (OAuth vs sessions)
- Data model changes (SQL vs NoSQL)

**No:**
- Implementation details (variable naming)
- Code style (tabs vs spaces → linter config)
- Library version updates (routine maintenance)
- Bug fixes (use commit messages)

---

## ADR Tools

### Manual (Markdown)
```bash
# Create new ADR
./adr-tools new "Use PostgreSQL for primary database"
# Creates docs/adr/0001-use-postgresql-for-primary-database.md
```

### adr-tools (CLI)
```bash
npm install -g adr-log

adr new "Choose deployment platform"
adr list
adr generate toc
```

### Log4brains (Web UI)
```bash
npx log4brains init
npx log4brains preview
```

## Rules

- ADRs are immutable once accepted — capture decision at point in time, don't rewrite history.
- Every significant architectural decision needs an ADR — if it affects future development, document it.
- Include 3-5 alternatives with honest pros/cons — shows due diligence, not rubber-stamping.
- Document consequences, both positive and negative — acknowledges trade-offs accepted.
- Store ADRs in version control — part of codebase, not separate wiki.
- Number ADRs sequentially — 0001, 0002, etc., preserves decision timeline.
- Write in present tense ("we choose") not past — ADR represents decision moment.
- Supersede, don't delete old ADRs — link old to new, maintain decision history.
- Decision-makers listed in ADR — accountability and context for future teams.
- Review ADRs during onboarding — fastest way to understand system evolution.
