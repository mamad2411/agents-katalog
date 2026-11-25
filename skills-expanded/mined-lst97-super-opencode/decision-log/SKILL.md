---
name: decision-log
description: Architecture Decision Record (ADR) creation, tracking, and management for informed technical choices.
---

# Decision Log Skill

## Purpose

To transform **implicit decisions** into **explicit records**. This skill ensures every significant technical choice is documented with context, alternatives, and consequences—preventing "tribal knowledge" loss and enabling future maintainers to understand the "why" behind the "what."

**ROI Metric**: Spending 10 minutes documenting a decision saves hours of debate and prevents costly reversals months later.

## When to Use

- **Trigger**: When `architect` recommends a technology, pattern, or structural change.
- **Trigger**: When a decision has >1 viable alternative.
- **Trigger**: When a decision is hard to reverse (high consequence).
- **Trigger**: When `pm-agent` flags a decision as "architecturally significant."

## The ADR Protocol (The 5-Step Process)

### 1. Recognition (Is This Significant?)

**Ask**: Does this decision impact any of the following?
- Technology stack (language, framework, database)
- Architecture style (microservices vs monolith, REST vs GraphQL)
- Infrastructure (cloud provider, containerization, serverless)
- Security model (auth strategy, encryption approach)
- Data strategy (storage, caching, messaging)
- Team workflow (CI/CD, branching strategy, code review)

**If YES** → Create an ADR  
**If NO** → Document briefly in code comments

### 2. Context (Why Are We Doing This?)

Document the forces at play:
- Business requirements (scale, compliance, time-to-market)
- Technical constraints (legacy systems, team expertise)
- Quality attributes (performance, security, maintainability)

### 3. Decision (What Did We Choose?)

State the decision clearly:
- Chosen option with version/variant
- Configuration details
- Scope (what's in, what's out)

### 4. Alternatives (What Else Did We Consider?)

Document at least 2-3 alternatives:
- Option name and brief description
- Pros and cons
- Why it was rejected (be honest: "team familiarity," "cost," "risk")

### 5. Consequences (What Happens Now?)

List the implications:
- **Positive**: Benefits we gain
- **Negative**: Trade-offs we accept
- **Neutral**: Changes to workflows or expectations
- **Risks**: What could go wrong
- **Migration**: Path from current state to new state

## ADR Template

```markdown
# ADR-[NUMBER]: [Short Title]

## Status
- Proposed
- Accepted
- Deprecated (replaced by ADR-XXX)
- Superseded by ADR-XXX

## Context

[The problem statement. What is the issue we're addressing? What forces are at play?]

[Example: We need to choose a database for our user service. The service must handle 10k writes/second with ACID compliance. Team has Postgres expertise but limited NoSQL experience.]

## Decision

**We will use [TECHNOLOGY/Approach] version [X.Y]**

[Clear, concise statement of the decision.]

### Configuration
- Setting A: Value
- Setting B: Value

### Scope
- **In Scope**: User data, session storage
- **Out of Scope**: Analytics data (see ADR-015)

## Alternatives Considered

### Option 1: [Name]
[Description]

**Pros:**
- Benefit A
- Benefit B

**Cons:**
- Drawback A
- Drawback B

**Decision**: Rejected because [specific reason].

### Option 2: [Name]
[Description]

**Pros:**
- Benefit A
- Benefit B

**Cons:**
- Drawback A
- Drawback B

**Decision**: Rejected because [specific reason].

### Option 3: Status Quo (Do Nothing)
**Decision**: Rejected because [specific reason].

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative / Trade-offs
- [Trade-off 1]
- [Trade-off 2]

### Neutral
- [Change 1]

### Risks
- [Risk 1] → Mitigation: [strategy]
- [Risk 2] → Mitigation: [strategy]

### Migration Path
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Related Decisions
- Relates to ADR-XXX
- Depends on ADR-YYY
- Supersedes ADR-ZZZ

## Notes
- **Decision Date**: YYYY-MM-DD
- **Decision Makers**: [Name], [Name]
- **Stakeholders Consulted**: [Team/Individual]
```

## Execution Template

*Use this when documenting a decision.*

```markdown
## 📝 Decision Documentation

### 1. Decision Summary
- **Topic**: [What are we deciding?]
- **Significance**: High/Medium/Low
- **Reversibility**: Easy/Moderate/Difficult

### 2. Context & Forces
- Business driver: [What business need drives this?]
- Technical driver: [What technical need drives this?]
- Constraints: [Time, budget, expertise, legacy]

### 3. Options Analysis

| Option | Pros | Cons | Score (1-10) |
|:-------|:-----|:-----|:------------:|
| Option A | Fast, proven | Expensive | 7 |
| Option B | Cheap, flexible | Unproven | 6 |
| Option C | [Status Quo] | Technical debt | 4 |

### 4. Recommendation
**Chosen**: Option A  
**Rationale**: Best balance of speed and reliability given Q2 deadline. Cost acceptable.

### 5. ADR Status
- [ ] Draft created
- [ ] Reviewed by architect
- [ ] Reviewed by team
- [ ] Accepted
- [ ] Documented in `docs/adr/`
```

## ADR Index Maintenance

Maintain an index file for discoverability:

```markdown
# Architecture Decision Records

## Active Decisions
| ADR | Title | Date | Status |
|:----|:------|:-----|:------:|
| 001 | Use PostgreSQL for Core Data | 2026-01-15 | Accepted |
| 002 | Adopt Next.js App Router | 2026-01-20 | Accepted |
| 003 | Implement JWT Authentication | 2026-01-25 | Accepted |

## Deprecated/Superseded
| ADR | Title | Date | Status |
|:----|:------|:-----|:------:|
| 000 | Use MongoDB (pilot) | 2026-01-10 | Superseded by ADR-001 |
```

## Integration with Agents

- **`architect`**: Primary user—creates ADRs for all architectural decisions.
- **`pm-agent`**: Reviews ADRs for impact on timelines and resources.
- **`backend` / `frontend`**: Reference ADRs when implementing to understand constraints.
- **`writer`**: Updates ADRs with implementation details and outcomes.

## Storage Location

```
docs/
└── adr/
    ├── README.md           # Index of all ADRs
    ├── 001-use-postgres.md
    ├── 002-nextjs-app-router.md
    └── 003-jwt-auth.md
```

Or in `.opencode/memory/adr/` for agent-centric projects.
