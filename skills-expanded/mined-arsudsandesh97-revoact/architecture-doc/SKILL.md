---
name: architecture-doc
description: |
  Generate a complete ARCHITECTURE.md file for any software system. Use whenever the user asks to create, write, generate, or draft an ARCHITECTURE.md — a system-wide architecture document that explains the big picture: how major components fit together, what patterns are used, infrastructure decisions, and cross-cutting concerns.

  This skill triggers when users need to document: overall system architecture, infrastructure setup, deployment architecture, architectural patterns (microservices, event-driven, layered), technology stack decisions, scalability strategy, or cross-cutting concerns (auth, logging, monitoring across the system).

  Do NOT trigger for single-feature technical designs (use Design.md skill), UI/visual design, or code-level implementation details.

---

# ARCHITECTURE.md Author Skill

You are a system architect documenting the high-level structure and decisions of a software system.

## Philosophy

An ARCHITECTURE.md is the **30,000-foot view** of your system. It answers:
- **What are the major building blocks?** (services, databases, external systems)
- **How do they communicate?** (APIs, message queues, events)
- **What patterns guide the design?** (microservices, CQRS, event sourcing)
- **Why these architectural choices?** (scalability, team structure, constraints)
- **What are the cross-cutting concerns?** (auth, logging, monitoring, deployment)

The audience is **technical stakeholders** who need to understand the system's structure before diving into feature-level design docs. It should survive for years, documenting foundational decisions that don't change often.

## Structure

An ARCHITECTURE.md has **10 core sections**:

1. **System Overview** - Bird's eye view and context
2. **Architectural Principles** - Guiding rules and philosophy
3. **System Context** - External systems and boundaries
4. **High-Level Architecture** - Major components and layers
5. **Component Deep Dive** - Detailed view of key services/modules
6. **Data Architecture** - Storage strategy and data flow
7. **Infrastructure & Deployment** - Where and how it runs
8. **Cross-Cutting Concerns** - Auth, logging, monitoring, security
9. **Key Architectural Decisions (ADRs)** - Major decisions and rationale
10. **Future Considerations** - Known limitations and evolution path

## Workflow: Interview → Draft → Validate

### Step 1: Interview the User

Gather architectural context before writing:

**Required context:**
- **What is the system?** (name, purpose, business domain)
- **System type?** (monolith, microservices, serverless, distributed)
- **Current state?** (greenfield, brownfield, migrating from legacy)
- **Scale requirements?** (users, requests/sec, data volume)
- **Team structure?** (single team, multiple squads, distributed)

**Optional but helpful:**
- **Existing architecture?** (if refactoring/documenting existing system)
- **Technology stack?** (languages, frameworks, cloud provider)
- **Regulatory requirements?** (HIPAA, PCI-DSS, GDPR)
- **Budget constraints?** (affects cloud vs on-prem, managed vs self-hosted)

If sparse info, make reasonable assumptions (note them) and proceed.

### Step 2: Build the Document Structure

```markdown
# [System Name] - Architecture Documentation

**Version:** 1.0
**Last Updated:** [Date]
**Status:** [Current | Proposed | Superseded]
**Authors:** [Names/Team]

---

## 1. System Overview

### Purpose & Scope
[2-3 paragraphs explaining what the system does, who uses it, and its business value]

### Key Characteristics
- **Type:** [Monolith | Microservices | Serverless | Hybrid]
- **Scale:** [Number of users, requests/sec, data volume]
- **Deployment:** [Cloud provider/region or on-premise]
- **Team:** [Number of engineers, teams, locations]

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Load Balancer                        │
└─────────────┬───────────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────┐        ┌─────▼────┐        ┌──────────┐
│  Web   │        │   API    │───────▶│ Database │
│  App   │◀───────│ Gateway  │        └──────────┘
└────────┘        └──────────┘
                       │
              ┌────────┴────────┐
              │                 │
        ┌─────▼─────┐    ┌─────▼──────┐
        │ Service A │    │ Service B  │
        └───────────┘    └────────────┘
```

### Technology Stack Summary
- **Frontend:** [Framework/library]
- **Backend:** [Language/framework]
- **Database:** [Type and product]
- **Infrastructure:** [Cloud provider/containers]
- **Key Libraries:** [Major dependencies]

---

## 2. Architectural Principles

These principles guide all architectural decisions:

### Principle 1: [Name]
**Statement:** [Clear, actionable principle]

**Rationale:** [Why this matters for our system]

**Implications:**
- [How this affects design decisions]
- [What we do/don't do because of this]

**Example:** [Concrete example in our system]

---

### Principle 2: [Name]
[Same structure for 3-5 key principles]

**Common Principles to Consider:**
- **Simplicity over cleverness** - Prefer boring, proven solutions
- **Fail gracefully** - Design for partial failures
- **Statelessness** - Services don't hold session state
- **Idempotency** - Operations can be safely retried
- **Eventual consistency** - Accept temporary inconsistency for availability
- **Security by default** - Security is not optional
- **Observability first** - If you can't measure it, you can't fix it

---

## 3. System Context

### System Boundary

```
                     ┌──────────────────┐
   External Users ──▶│   Our System     │
                     │                  │
                     │  ┌────────────┐  │
   Internal Users ──▶│  │  Core App  │  │──▶ Payment Gateway
                     │  └────────────┘  │
                     │                  │
   Mobile Apps ─────▶│                  │──▶ Email Service
                     └──────────────────┘
                              │
                              ▼
                        Analytics Platform
```

### External Dependencies

#### Dependency 1: [Service Name]
- **Type:** [Third-party API | Internal service | Cloud service]
- **Purpose:** [What we use it for]
- **Integration:** [REST API | SDK | Message queue]
- **Criticality:** [Critical | Important | Optional]
- **SLA:** [Uptime guarantee]
- **Failure Mode:** [What happens if it's down]
- **Fallback:** [How we handle outages]

[Repeat for each external dependency]

### System Interfaces

**Inbound:**
- Users via web browser (HTTPS)
- Mobile apps via REST API
- Admin portal (internal network)
- Scheduled jobs (cron/Lambda triggers)

**Outbound:**
- External APIs (payment, auth, email)
- Data warehouse (nightly ETL)
- Monitoring systems (metrics, logs)

---

## 4. High-Level Architecture

### Architectural Style
[Describe the overall pattern: layered monolith, microservices, event-driven, etc.]

**We chose [pattern] because:**
- Reason 1 (e.g., team size, scaling needs)
- Reason 2 (e.g., independent deployment)
- Reason 3 (e.g., technology diversity)

### Logical Architecture (Layers)

```
┌─────────────────────────────────────────┐
│        Presentation Layer               │
│  (Web UI, Mobile Apps, APIs)            │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│        Application Layer                │
│  (Business Logic, Workflows)            │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│        Domain Layer                     │
│  (Core Business Rules, Entities)        │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│        Data Layer                       │
│  (Repositories, Database Access)        │
└─────────────────────────────────────────┘
```

**Layer Responsibilities:**
- **Presentation:** User interaction, input validation, response formatting
- **Application:** Orchestration, use cases, application workflows
- **Domain:** Business rules, core logic, domain entities
- **Data:** Persistence, queries, data access patterns

**Communication Rules:**
- Each layer only talks to the layer directly below
- No skipping layers (Presentation cannot directly access Data)
- Domain layer has no knowledge of Presentation or Data

### Physical Architecture (Deployment)

```
┌─────────────────────────────────────────────────────┐
│                  CDN (Static Assets)                 │
└─────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────┐
│              Load Balancer (ALB)                      │
└────────────┬─────────────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼──────┐    ┌────▼────────┐
│ Web      │    │  API        │
│ Servers  │    │  Servers    │
│ (3x ECS) │    │  (5x ECS)   │
└──────────┘    └─────┬───────┘
                      │
           ┌──────────┴───────────┐
           │                      │
    ┌──────▼──────┐      ┌───────▼────────┐
    │  Primary DB │      │  Message Queue │
    │ (RDS Multi-AZ)     │  (SQS/RabbitMQ)│
    └─────────────┘      └────────────────┘
           │
    ┌──────▼──────┐
    │  Read       │
    │  Replicas   │
    │  (2x)       │
    └─────────────┘
```

---

## 5. Component Deep Dive

### Component 1: [Service/Module Name]

**Purpose:** [What this component does in 1-2 sentences]

**Responsibilities:**
- Responsibility 1
- Responsibility 2
- Responsibility 3

**Technology:**
- Language: [Python, Java, Node.js, etc.]
- Framework: [Express, Spring Boot, FastAPI]
- Key Libraries: [List major dependencies]

**Interfaces:**
- **Exposes:** REST API at `/api/v1/[domain]`
- **Consumes:** [Other services it depends on]
- **Events:** [Messages it publishes/subscribes to]

**Data Storage:**
- **Database:** PostgreSQL table `[name]`
- **Cache:** Redis keys `[pattern]`
- **Files:** S3 bucket `[name]`

**Scaling:**
- **Horizontal:** Auto-scales 2-10 instances based on CPU
- **Bottleneck:** Database writes (mitigated by write-through cache)
- **Limits:** 1000 requests/second per instance

**Failure Modes:**
- **If down:** [Impact on system, fallback behavior]
- **Circuit breaker:** Opens after 5 failures, half-open after 30s

**Monitoring:**
- **Metrics:** Request rate, error rate, latency (p50/p95/p99)
- **Logs:** Structured JSON to CloudWatch
- **Alerts:** Error rate >5% for 5 minutes

---

### Component 2: [Service/Module Name]
[Same structure for each major component]

---

## 6. Data Architecture

### Data Storage Strategy

**Database Per Service Pattern:** Each microservice owns its data

```
┌────────────┐         ┌────────────┐         ┌────────────┐
│ Service A  │         │ Service B  │         │ Service C  │
└──────┬─────┘         └──────┬─────┘         └──────┬─────┘
       │                      │                      │
┌──────▼─────┐         ┌──────▼─────┐         ┌──────▼─────┐
│  DB A      │         │  DB B      │         │  DB C      │
│ (Postgres) │         │ (MongoDB)  │         │ (Redis)    │
└────────────┘         └────────────┘         └────────────┘
```

**Rationale:**
- Loose coupling (services can't share databases)
- Independent scaling
- Technology diversity (pick right tool for each job)

**Trade-off:**
- Cross-service queries require API calls or event sourcing
- Data consistency managed via eventual consistency patterns

### Primary Data Stores

#### Store 1: [Name and Type]
- **Type:** [Relational | Document | Key-Value | Graph]
- **Product:** [PostgreSQL, MongoDB, Redis, etc.]
- **Purpose:** [What data lives here]
- **Schema:** [High-level schema description or link]
- **Size:** [Current: Xgb, Projected 1 year: Ygb]
- **Access Pattern:** [Read-heavy, write-heavy, balanced]
- **Consistency Model:** [Strong | Eventual]
- **Backup:** [Strategy and RPO/RTO]

[Repeat for each data store]

### Caching Strategy

**Layers:**
1. **CDN Cache** (CloudFront) - Static assets, 24hr TTL
2. **API Gateway Cache** - GET responses, 5min TTL
3. **Application Cache** (Redis) - Database query results, session data
4. **Database Query Cache** - Postgres built-in cache

**Cache Invalidation:**
- **Time-based:** TTL expiry
- **Event-based:** Invalidate on writes via pub/sub
- **Manual:** Admin API for emergency cache clearing

### Data Flow

**Write Path:**
```
User Request → API → Service → Database → Event Published → Analytics
```

**Read Path:**
```
User Request → API → Cache (hit) → Return
                   ↓ (miss)
                Database → Update Cache → Return
```

---

## 7. Infrastructure & Deployment

### Cloud Architecture

**Provider:** AWS (Primary) + Cloudflare (CDN)

**Regions:**
- **Primary:** us-east-1 (N. Virginia)
- **Secondary:** eu-west-1 (Ireland) - Disaster recovery
- **Multi-region:** Not yet, planned for Phase 3

**Availability Zones:**
- Deployed across 3 AZs in primary region
- Load balanced across all AZs
- Database Multi-AZ failover enabled

### Compute

**Container Platform:** AWS ECS (Fargate)

**Container Strategy:**
- All services containerized (Docker)
- Base images: Alpine Linux (minimal size)
- Image registry: ECR
- CI/CD builds on every merge to main

**Scaling:**
- **Auto-scaling:** CPU >70% or requests >80% capacity
- **Min instances:** 2 per service (high availability)
- **Max instances:** 20 per service (cost control)

### Networking

**VPC Architecture:**
```
┌─────────────────────── VPC ──────────────────────────┐
│                                                       │
│  ┌───────────────── Public Subnet ────────────────┐  │
│  │  Load Balancer (Internet-facing)               │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
│  ┌───────────────── Private Subnet ───────────────┐  │
│  │  Application Servers (ECS Tasks)               │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
│  ┌───────────────── Database Subnet ──────────────┐  │
│  │  RDS (No internet access)                      │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**Security Groups:**
- Load Balancer: Allow 80/443 from internet
- App Servers: Allow traffic only from LB
- Database: Allow 5432 only from App Servers

### Deployment Strategy

**Blue-Green Deployment:**
1. Deploy new version (Green) alongside current (Blue)
2. Run smoke tests on Green
3. Shift 10% traffic to Green (canary)
4. Monitor error rates for 10 minutes
5. If healthy, shift 100% traffic to Green
6. Keep Blue running for 1 hour (rollback window)
7. Terminate Blue

**Rollback:**
- Automated rollback if error rate >5%
- Manual rollback command available (< 2 minutes)

**Deployment Frequency:** Multiple times per day

### Infrastructure as Code

**Tool:** Terraform

**Structure:**
```
infrastructure/
├── modules/
│   ├── ecs/
│   ├── rds/
│   └── vpc/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── global/
```

**Change Process:**
1. Create Terraform plan
2. Review in PR
3. Apply via CI/CD pipeline
4. Changes tracked in version control

---

## 8. Cross-Cutting Concerns

### Authentication & Authorization

**Authentication:** OAuth 2.0 + JWT

**Flow:**
1. User logs in → Auth service validates credentials
2. Auth service issues JWT (1-hour expiry)
3. Client includes JWT in Authorization header
4. API Gateway validates JWT signature
5. Service extracts user ID from JWT claims

**Authorization:** Role-Based Access Control (RBAC)

**Roles:**
- `admin` - Full system access
- `user` - Standard user permissions
- `readonly` - Read-only access

**Implementation:**
- Roles stored in JWT claims
- Each endpoint checks required role
- Centralized permission service for complex rules

### Logging

**Strategy:** Structured logging (JSON format)

**Log Levels:**
- ERROR: Production issues requiring immediate attention
- WARN: Potential issues (rate limits, retries)
- INFO: Normal operations (requests, transactions)
- DEBUG: Detailed diagnostics (dev/staging only)

**Log Aggregation:**
- All services → CloudWatch Logs
- Retention: 30 days
- Search/query via CloudWatch Insights
- Critical errors forwarded to PagerDuty

**Required Fields:**
```json
{
  "timestamp": "ISO8601",
  "level": "ERROR",
  "service": "user-service",
  "request_id": "uuid",
  "user_id": "uuid",
  "message": "description",
  "context": { "key": "value" }
}
```

### Monitoring & Observability

**Metrics:** Prometheus + Grafana

**Key Metrics:**
- **RED Method:** Rate, Errors, Duration
  - Request rate per service
  - Error rate (4xx, 5xx)
  - Response time (p50, p95, p99)
- **USE Method:** Utilization, Saturation, Errors
  - CPU/memory utilization
  - Queue depth
  - Error counts

**Distributed Tracing:** AWS X-Ray

**Alerts:**
- Error rate >5% for 5 minutes → PagerDuty
- p95 latency >1s for 10 minutes → Slack
- Database connections >80% → PagerDuty

### Security

**Principles:**
- Defense in depth (multiple security layers)
- Principle of least privilege
- Encrypt everything (in transit and at rest)
- Zero trust networking

**Implementation:**
- **Network:** VPC isolation, security groups, no public databases
- **Encryption:** TLS 1.3 for transit, AES-256 for at rest
- **Secrets:** AWS Secrets Manager (rotated every 90 days)
- **Vulnerability Scanning:** Snyk on every build
- **Penetration Testing:** Annual third-party audit

### Error Handling

**Strategy:** Fail fast, fail safe

**Patterns:**
- **Retry with exponential backoff** - Transient failures
- **Circuit breaker** - Prevent cascading failures
- **Fallback** - Degrade gracefully (cached data, default values)
- **Timeout** - All external calls have deadlines

**Error Responses:**
```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "User-friendly message",
    "details": { "field": "email", "issue": "invalid format" },
    "request_id": "uuid"
  }
}
```

### Performance

**Targets:**
- API response time: p95 < 500ms
- Page load time: <2 seconds
- Database queries: <100ms
- Message processing: <1 second

**Optimization Strategies:**
- Database indexing on hot paths
- Redis caching for read-heavy queries
- CDN for static assets
- Connection pooling
- Async processing for slow operations

---

## 9. Key Architectural Decisions (ADRs)

### ADR-001: Microservices over Monolith

**Date:** 2026-01-15

**Status:** Accepted

**Context:**
We need to decide between a monolithic architecture and microservices for our new platform. Team is growing to 25 engineers across 5 squads.

**Decision:**
Adopt microservices architecture with domain-driven design boundaries.

**Rationale:**
- **Team scalability:** Independent teams can work on separate services
- **Deployment:** Services can be deployed independently
- **Technology diversity:** Choose best tool per service
- **Fault isolation:** One service failure doesn't crash the system

**Consequences:**
- **Pros:** Faster development, better scalability, technology flexibility
- **Cons:** Increased operational complexity, distributed system challenges
- **Mitigations:** Invest in observability, standardize deployment pipelines

**Alternatives Considered:**
- **Modular Monolith:** Easier ops but team coordination bottleneck
- **Serverless:** Lower ops but cold starts and vendor lock-in

---

### ADR-002: PostgreSQL over MongoDB

**Date:** 2026-02-20

**Status:** Accepted

**Context:**
Need to choose primary database for transactional data.

**Decision:**
Use PostgreSQL as primary database.

**Rationale:**
- ACID transactions critical for financial data
- Complex queries require relational model
- Team has deep PostgreSQL expertise
- JSONB support provides schema flexibility when needed

**Consequences:**
- Strong consistency guarantees
- Proven scalability path (read replicas, partitioning)
- Trade-off: Slightly more rigid schema than document DB

---

[Continue with 3-5 major architectural decisions]

---

## 10. Future Considerations

### Known Limitations

**Current Architecture Limitations:**
1. **Single region:** No multi-region support yet (latency for global users)
2. **Synchronous APIs:** All inter-service communication is synchronous (coupling)
3. **Manual scaling decisions:** Auto-scaling rules are conservative
4. **Limited caching:** Only database query cache, no distributed cache mesh

**Technical Debt:**
1. Legacy authentication system (migrating to OAuth)
2. Inconsistent error handling across services
3. Missing distributed tracing in older services

### Planned Evolution

**Phase 2: Scale & Resilience (Q4 2026)**
- Introduce event-driven architecture (Kafka/SQS)
- Implement CQRS for read-heavy services
- Add API rate limiting and quotas
- Distributed caching layer (Redis Cluster)

**Phase 3: Global Expansion (Q1 2027)**
- Multi-region deployment
- Edge computing for low-latency APIs
- CDN for dynamic content
- Geo-distributed databases

**Phase 4: Advanced Features (Q2 2027)**
- Real-time collaboration (WebSockets)
- Machine learning inference pipeline
- Data lake for analytics
- Advanced observability (OpenTelemetry)

### Scalability Roadmap

**Current Capacity:** 10,000 concurrent users, 100K requests/hour

**Scaling Targets:**

| Milestone | Users | Requests/Hour | Changes Required |
|-----------|-------|---------------|------------------|
| Current | 10K | 100K | None (baseline) |
| 6 months | 50K | 500K | Add read replicas, Redis cluster |
| 1 year | 200K | 2M | Multi-region, CDN for dynamic content |
| 2 years | 1M | 10M | Shard databases, edge computing |

**Bottlenecks to Address:**
1. Database writes (solution: write-through cache, async processing)
2. API Gateway (solution: horizontal scaling, edge deployment)
3. Session storage (solution: distributed session store)

---

## 11. Appendix

### Glossary

- **ADR:** Architecture Decision Record
- **CQRS:** Command Query Responsibility Segregation
- **RTO:** Recovery Time Objective (max downtime)
- **RPO:** Recovery Point Objective (max data loss)
- **Circuit Breaker:** Pattern to prevent cascading failures
- **Blue-Green Deployment:** Zero-downtime deployment strategy

### References

- [System Design Primer](internal-wiki/design-primer)
- [AWS Well-Architected Framework](aws-link)
- [Microservices Patterns](book-link)
- [API Design Guidelines](internal-wiki/api-standards)

### Review History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-10 | Arch Team | Initial architecture |
| 1.1 | 2026-03-15 | Arch Team | Added microservices details |
| 1.2 | 2026-07-22 | Arch Team | Updated scaling section |

---

## Maintenance

**This document should be updated when:**
- Major architectural changes are made
- New services/components are added
- Infrastructure changes (cloud provider, deployment model)
- Significant technology stack changes
- After quarterly architecture review

**Review Schedule:** Quarterly (every 3 months)
**Document Owner:** Architecture Team
```

---

## Best Practices

### 1. **Focus on "Why" Not Just "What"**
   - Don't just list components, explain the reasoning
   - Show trade-offs and alternatives considered
   - Link decisions to business/technical constraints

### 2. **Use Diagrams Liberally**
   - ASCII diagrams are fine and version-control friendly
   - Show different views: logical, physical, data flow
   - Keep diagrams simple (max 7±2 boxes per diagram)

### 3. **Document Cross-Cutting Concerns**
   - Security, logging, monitoring apply to all components
   - Define once, reference everywhere
   - Provide concrete examples

### 4. **Make It Living Documentation**
   - Include review schedule
   - Track version history
   - Note document owner
   - Update when architecture changes

### 5. **Balance Detail and Readability**
   - High-level overview first
   - Deep dive sections for critical components
   - Link to other docs for full details
   - Use tables for comparison/summary

### 6. **Include ADRs (Architecture Decision Records)**
   - Document significant decisions
   - Capture context at decision time
   - Show alternatives considered
   - Note consequences and trade-offs

### 7. **Address the Future**
   - Known limitations section
   - Scalability roadmap
   - Planned evolution
   - Technical debt acknowledgment

---

## Conversation Flow

When the user asks for an ARCHITECTURE.md:

**1. Understand Current State**
Ask: "Are you documenting an existing system or designing a new one?"

**2. Gather Context**
- "What's the system's purpose and scale?"
- "What's the current architecture (if any)?"
- "What are the main challenges or goals?"

**3. Clarify Scope**
Ask: "Should this cover the entire system or a specific subsystem?"

**4. Generate the Architecture Doc**
- Start with System Overview and Context
- Build High-Level Architecture diagram
- Detail major components
- Document data architecture
- Cover infrastructure and deployment
- Address cross-cutting concerns
- Include key decisions (ADRs)
- Add future considerations

**5. Use Placeholders for Unknowns**
Mark uncertain sections with `[TBD: reason]` or `[Decision pending: question]`

**6. Save and Suggest Next Steps**
Save as `ARCHITECTURE.md` and suggest: "Want me to create Design.md for specific features next?"

---

## Tips by System Type

### For Microservices
- Document service boundaries clearly
- Show inter-service communication patterns
- Include service mesh / API gateway details
- Address data consistency strategies

### For Monoliths
- Show internal module/layer structure
- Document deployment model
- Include scaling strategy (vertical vs horizontal)
- Address modularity and coupling

### For Serverless
- Document function boundaries
- Show event flow and triggers
- Include cold start mitigation
- Address state management

### For Event-Driven
- Document event schemas
- Show event flow diagrams
- Include consistency patterns
- Address message ordering/idempotency

---

## Common Mistakes to Avoid

❌ **Too Much Detail**
   - Architecture is high-level; save implementation for Design.md
   - Don't list every API endpoint or database column

❌ **Missing "Why"**
   - Don't just say "we use microservices"
   - Explain why microservices vs alternatives

❌ **No Diagrams**
   - Architecture is visual; text alone is hard to grasp
   - Include at least 3-4 diagrams

❌ **Ignoring Non-Functional Requirements**
   - Document security, performance, scalability
   - These are architectural concerns

❌ **Stale Documentation**
   - Include review schedule and version history
   - Note when architecture changes

❌ **No Decision Records**
   - Future engineers need to know why decisions were made
   - Document alternatives considered

---

## Output Instructions

When generating an ARCHITECTURE.md:

1. **Interview for context** (system type, scale, constraints)
2. **Start with overview** (purpose, diagram, tech stack)
3. **Document principles** (guiding rules for decisions)
4. **Show structure** (logical and physical architecture)
5. **Detail components** (major services/modules)
6. **Include diagrams** (use ASCII art)
7. **Cover cross-cutting** (auth, logging, monitoring, security)
8. **Document decisions** (ADRs with rationale)
9. **Address future** (limitations, evolution, scalability)
10. **Save as `ARCHITECTURE.md`** in working directory

---

## Follow-Up Documents

After creating ARCHITECTURE.md, suggest:
- **Design.md** - Feature-level technical design
- **ADR-###.md** - Detailed decision records
- **Infrastructure.md** - Deployment and ops details
- **Security.md** - In-depth security documentation
