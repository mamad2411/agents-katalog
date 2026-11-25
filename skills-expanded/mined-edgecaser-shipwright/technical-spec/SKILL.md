---
name: technical-spec
description: "Translates product requirements (PRDs, user stories) into engineering-ready technical specifications. Covers system architecture decisions, API contracts, data models, non-functional requirements, and migration plans. Bridges the gap between \"what to build\" (PM) and \"how to build it\" (engineering)."
category: technical
default_depth: standard
---

# Technical Spec Writing

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Translates product requirements (PRDs, user stories) into engineering-ready technical specifications. Covers system architecture decisions, API contracts, data models, non-functional requirements, and migration plans. Bridges the gap between "what to build" (PM) and "how to build it" (engineering).

## When to Use

- After a PRD is approved and before engineering estimation begins
- When a feature requires significant architectural decisions
- When multiple engineering teams need to coordinate on an implementation
- As a PM who wants to speak engineering's language and earn technical credibility

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Small feature or isolated backend change | Context & Motivation + System Architecture + API Contract |
| **Standard** | Typical feature spanning multiple components | All sections |
| **Deep** | Platform migration, new system, or multi-team coordination | All sections + load test plan, detailed ADRs per component, cross-service sequence diagrams, rollback rehearsal script |

**Omit rules:** At Light depth, condense non-functional requirements and rollout detail. Retain material security, migration and rollback considerations alongside context, architecture and API contract. Mark irrelevant items N/A with rationale.

## Framework

### Step 1: Context & Motivation (Engineering Perspective)

```markdown
# Technical Specification: [Feature Name]

## Metadata
- PRD Reference: [link to PRD]
- Author: [PM + Tech Lead]
- Reviewers: [engineering, security, infra]
- Status: [Draft / In Review / Approved]
- Last updated: [date]

## Context
**What we're building:** [1-2 sentences, from the PRD]
**Why (business):** [Key metric we're moving and by how much]
**Why (technical):** [Technical motivation, e.g., "Current system can't support X"]

## Scope
**In scope:** [Specific capabilities this spec covers]
**Out of scope:** [What's explicitly NOT covered, defer to future specs]
**Assumptions:** [Technical assumptions we're making]

## Codebase Notes
**Codebase available:** [Yes: path or repo / No]
**Files and modules inspected:** [list, or "none, no codebase access"]
**Patterns in use:** [framework, persistence layer, auth model, error handling, naming conventions]
**Reusable components:** [what already exists that this feature should build on]
**Conflicts with the PRD:** [anything the PRD assumes that the system does not do today]
```

**Read before you design.** If a codebase is available, read the modules this feature touches before drafting Steps 2 through 4, and fill in Codebase Notes from what you actually read. If no codebase is available, write `Codebase available: No` and label the Architecture, API Contract and Data Model sections `Hypothesis: written without codebase access`. A spec written blind is a set of questions for the tech lead, not a plan.

### Step 2: System Architecture

```markdown
## Architecture

### High-Level Design
[Describe the architecture at a block-diagram level]

```
[Client] → [API Gateway] → [Service A] → [Database]
                         → [Service B] → [Message Queue] → [Worker]
```

### Components Affected
| Component | Change Type | Description |
|---|---|---|
| [Service A] | Modify | [What changes and why] |
| [Service B] | New | [New service needed for X] |
| [Database] | Schema change | [New tables/columns] |
| [Client] | UI update | [New screens/flows] |

### Architecture Decision Records (ADRs)
For each significant choice:

#### ADR 1: [Decision Title, e.g., "Use event-driven architecture for notifications"]
- **Context:** [Why this decision was needed]
- **Options considered:**
  - Option A: [Description], Pros: [x] / Cons: [y]
  - Option B: [Description], Pros: [x] / Cons: [y]
- **Decision:** [What we chose]
- **Rationale:** [Why, trade-off analysis]
- **Consequences:** [What this commits us to]
```

### Step 3: API Contract

```markdown
## API Design

### New Endpoints

#### POST /api/v2/[resource]
**Purpose:** [What this endpoint does]
**Authentication:** [Required, Bearer token / API key / etc.]
**Rate limit:** [N requests per minute]

**Request:**
```json
{
  "field_1": "string (required), description",
  "field_2": 123,              // integer (optional), description
  "field_3": {                 // object (required)
    "nested_field": "string"
  }
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "field_1": "string",
  "created_at": "2026-01-15T10:30:00Z",
  "status": "active"
}
```

**Error Responses:**
| Code | Condition | Response Body |
|---|---|---|
| 400 | Invalid input | `{ "error": "validation_error", "details": [...] }` |
| 401 | Not authenticated | `{ "error": "unauthorized" }` |
| 403 | Not authorized | `{ "error": "forbidden" }` |
| 404 | Resource not found | `{ "error": "not_found" }` |
| 429 | Rate limited | `{ "error": "rate_limited", "retry_after": 60 }` |

### Modified Endpoints
| Endpoint | Change | Backward Compatible? |
|---|---|---|
| [existing endpoint] | [what changes] | [Yes / No, if no, migration plan required] |
```

### Step 4: Data Model

```markdown
## Data Model

### New Tables / Collections

#### [table_name]
| Column | Type | Nullable | Default | Description |
|---|---|---|---|---|
| id | UUID | No | gen_random_uuid() | Primary key |
| [field] | VARCHAR(255) | No | | [description] |
| [field] | INTEGER | Yes | 0 | [description] |
| created_at | TIMESTAMP | No | NOW() | Record creation time |
| updated_at | TIMESTAMP | No | NOW() | Last modification time |

**Indexes:**
- `idx_[table]_[column]` on [column], for [query pattern]
- `idx_[table]_[col1]_[col2]` on ([col1], [col2]), for [query pattern]

**Relationships:**
- [table_name].[field] → [other_table].id (foreign key)

### Schema Migrations
| Migration | Description | Reversible? | Estimated Duration |
|---|---|---|---|
| [001_add_table_x] | Creates [table] | Yes | [seconds/minutes] |
| [002_add_column_y] | Adds [column] to [table] | Yes | [time, data volume] |

### Data Volume Estimates
| Table | Expected Rows (Year 1) | Growth Rate | Storage Estimate |
|---|---|---|---|
| [table] | [N] | [X]/month | [GB] |
```

### Step 5: Non-Functional Requirements

```markdown
## Non-Functional Requirements

### Performance
| Metric | Requirement | Measurement Method |
|---|---|---|
| API response time (p95) | < [N]ms | [APM tool] |
| Page load time (p95) | < [N]s | [RUM / Lighthouse] |
| Throughput | [N] requests/second | [Load testing] |
| Database query time (p95) | < [N]ms | [Query monitoring] |

### Scalability
- Must support [N] concurrent users
- Must handle [N] [operations] per [time period]
- Horizontal scaling strategy: [approach]

### Security
- [ ] Authentication: [method]
- [ ] Authorization: [RBAC / ABAC, describe permission model]
- [ ] Data encryption: At rest [method] / In transit [TLS version]
- [ ] PII handling: [what PII is involved, how it's protected]
- [ ] Audit logging: [what actions are logged]

### Reliability
- Availability target: [99.9% / 99.95% / etc.]
- Failover strategy: [approach]
- Data backup: [frequency, retention]
- Disaster recovery: [RTO and RPO targets]

### Observability
- Logging: [What's logged, at what level]
- Metrics: [Key metrics to instrument]
- Alerting: [Conditions that trigger alerts]
- Dashboards: [What dashboards need updating]
```

### Step 6: Rollout & Migration

```markdown
## Rollout Plan

### Feature Flags
| Flag | Description | Default | Rollout Plan |
|---|---|---|---|
| [flag_name] | [what it controls] | Off | Internal → 10% → 50% → 100% |

### Migration Steps
1. [ ] Deploy database migrations (backward-compatible)
2. [ ] Deploy service changes behind feature flag (off)
3. [ ] Enable for internal users / dogfood
4. [ ] Enable for [X]% of users, monitor for [N] days
5. [ ] Ramp to 100%
6. [ ] Remove feature flag and old code paths

### Rollback Plan
- **Trigger:** [What metric or alert triggers rollback]
- **Steps:** [How to roll back safely]
- **Data implications:** [What happens to data created during the rollout]

### Testing Requirements
- [ ] Unit tests for [components]
- [ ] Integration tests for [API contracts]
- [ ] Load test to [N] concurrent users
- [ ] Security review for [auth, PII handling]
- [ ] Accessibility audit
```

## Minimum Evidence Bar

**Required inputs:** An approved PRD or equivalent product brief with defined scope, target users, and success metrics. Access to the current system architecture (or confirmation this is greenfield).

**Acceptable evidence:** PRD, system architecture diagrams, existing API documentation, performance benchmarks, engineering team input on feasibility, and schema or data model context.

**Insufficient evidence:** If no PRD or product brief exists, stop and recommend running the PRD skill before attempting this skill. If no engineering input is available, state "Architecture decisions are PM hypotheses only" and flag for tech lead review. If a codebase is available and was not read, the spec is not ready; read it first.

**Hypotheses vs. findings:**
- **Findings:** Components affected, API contract schemas, data model structure (must reflect current system state or confirmed engineering decisions)
- **Hypotheses:** Performance targets, data volume estimates, rollout ramp percentages (must be labeled as projections pending load testing or production validation)

## Output Format

Produce a Technical Specification with:
1. **Context & Scope**, what, why, boundaries
2. **Architecture**, system design with ADRs for key decisions
3. **API Contract**, endpoints, request/response schemas, errors
4. **Data Model**, tables, relationships, migrations
5. **Non-Functional Requirements**, performance, security, reliability
6. **Rollout Plan**, feature flags, migration, rollback

**Shipwright Signature (required closing):**
7. **Decision Frame**, recommended architecture approach, trade-off, confidence with evidence quality, owner, decision date, revisit trigger
8. **Unknowns & Evidence Gaps**, unvalidated performance targets, missing data volume estimates, untested migration paths
9. **Pass/Fail Readiness**, PASS for engineering approval if the tech lead has reviewed the architecture, the API contract matches PRD requirements, and material security/rollback issues are resolved. FAIL for approval if review is missing, alternatives are unexamined, or material rollback needs are unanswered. A useful draft may be delivered with explicit blockers at any depth.
10. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Writing implementation details in the PRD**, The PRD says "what"; the tech spec says "how"
- **No ADRs**, If you chose approach A over B, document why; future engineers will thank you
- **Forgetting non-functionals**, Performance, security, and observability are requirements, not nice-to-haves
- **No rollback plan**, Every deployment should be reversible
- **PM writes tech spec alone**, Co-author with the tech lead; the PM ensures requirements fidelity, the engineer ensures technical feasibility
- **Writing the spec blind**, Architecture, data model and API sections written without reading the codebase describe an imagined system; read the relevant modules first, or label the sections as hypotheses

## Weak vs. Strong Output

**Weak:**
> "ADR: We will use a message queue for async processing."

No alternatives considered, no trade-off analysis, no consequences stated, this is a statement, not a decision record.

**Strong:**
> "ADR: Use RabbitMQ over SQS for notification processing. SQS is simpler but lacks routing key support needed for per-tenant delivery rules. RabbitMQ adds operational overhead (cluster management) but supports the fan-out pattern required by 3 of 4 notification types. Consequence: team must maintain RabbitMQ infrastructure or migrate to managed CloudAMQP ($200/mo at projected volume)."

Names alternatives, explains the deciding factor, and quantifies the operational consequence.
