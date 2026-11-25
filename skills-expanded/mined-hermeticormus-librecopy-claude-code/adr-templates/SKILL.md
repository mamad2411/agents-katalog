---
name: "adr-templates"
description: "ADR reference: what an ADR is, the status lifecycle, numbering, the index file, when to write one, Nygard, MADR, and Y-statement formats, and how ADRs relate to C4 levels. Use when setting up or maintaining an ADR log."
---

# ADR Templates

> Architecture Decision Record formats, status lifecycles, and architectural documentation patterns.

## Knowledge Base

### What is an ADR?

An Architecture Decision Record captures a single architectural decision along with its context and consequences. ADRs are:

- **Immutable**: Once accepted, an ADR is not modified. If a decision changes, a new ADR supersedes the old one.
- **Sequential**: Numbered in the order they are created.
- **Lightweight**: One page, one decision. Not a design document.
- **Permanent**: Even deprecated ADRs remain in the repository as historical records.

### ADR Status Lifecycle

```
proposed --> accepted --> [active indefinitely]
                     \--> deprecated (no longer relevant)
                     \--> superseded by ADR-XXX (replaced)
```

- **Proposed**: Under discussion. Not yet decided.
- **Accepted**: Decision made. Team is committed to this approach.
- **Deprecated**: No longer relevant (e.g., the feature was removed).
- **Superseded**: A newer ADR replaces this decision.

### ADR Numbering

Convention: `ADR-NNNN` with zero-padded numbers.

```
docs/adr/
  README.md           # Index of all ADRs
  ADR-0001-use-typescript.md
  ADR-0002-adopt-monorepo.md
  ADR-0003-use-postgresql.md
  ADR-0004-replace-rest-with-grpc.md   # supersedes ADR-0003 partially
```

### ADR Index (README.md)

```markdown
# Architecture Decision Records

| Number | Title | Status | Date |
|--------|-------|--------|------|
| [ADR-0001](ADR-0001-use-typescript.md) | Use TypeScript for all services | Accepted | 2025-01-10 |
| [ADR-0002](ADR-0002-adopt-monorepo.md) | Adopt monorepo with Turborepo | Accepted | 2025-01-15 |
| [ADR-0003](ADR-0003-use-postgresql.md) | Use PostgreSQL as primary datastore | Accepted | 2025-02-01 |
| [ADR-0004](ADR-0004-replace-rest-with-grpc.md) | Replace REST with gRPC for internal services | Proposed | 2025-03-01 |
```

### When to Write an ADR

Write an ADR when:
- Choosing a technology (language, framework, database, cloud service)
- Choosing an architectural pattern (monolith, microservices, event-driven)
- Establishing a convention (branching strategy, API versioning, error handling)
- Making a decision that is costly to reverse
- Making a decision that the team disagreed about (the ADR records the resolution)

Do NOT write an ADR for:
- Trivial choices ("use prettier for formatting")
- Temporary decisions ("use mock data until API is ready")
- Business decisions (those go in product docs)

### ADR Format Variants

**Nygard Format (minimal):**
```markdown
# Title
## Status
## Context
## Decision
## Consequences
```

**MADR Format (recommended, used by this plugin):**
```markdown
# Title
- Status, Date, Deciders
## Context and Problem Statement
## Decision Drivers
## Considered Options
## Decision Outcome
### Consequences
## Options Analysis
## Related Decisions
## Notes
```

**Y-Statement Format (for the decision line):**
```
In the context of {context},
facing {concern},
we decided for {option},
to achieve {quality},
accepting {downside}.
```

Example: "In the context of choosing a primary datastore, facing the need for ACID transactions and complex joins, we decided for PostgreSQL, to achieve data consistency and query flexibility, accepting that horizontal scaling will require read replicas."

### Architecture Documentation Levels (C4 Model)

| Level | What it Shows | Audience | Update Frequency |
|-------|---------------|----------|-----------------|
| **Context** (L1) | System + external actors | Everyone | Rarely |
| **Container** (L2) | Deployable units | Developers, DevOps | When adding services |
| **Component** (L3) | Internal structure of one container | Developers | When refactoring |
| **Code** (L4) | Classes and functions | Not usually documented | Auto-generated if needed |

## Patterns

1. **One Decision Per ADR**: Do not combine "Use PostgreSQL" and "Use Redis for caching" into one ADR. They are separate decisions with separate contexts.
2. **Link Superseding ADRs**: When ADR-012 supersedes ADR-005, update ADR-005's status to "Superseded by ADR-012" and link it.
3. **Include Rejected Options**: Future developers need to know what was considered AND rejected, so they do not re-propose it.
4. **Date Everything**: ADR decisions are anchored in time. The constraints that drove a decision in 2023 may not apply in 2025.
5. **Keep It Short**: If an ADR exceeds 2 pages, either split the decision or move detailed analysis to an appendix.

## Anti-Patterns

1. **ADR Graveyard**: Writing ADRs that nobody reads. Link to relevant ADRs from code comments and PR descriptions.
2. **Editing Accepted ADRs**: Modifying accepted ADRs to reflect current reality. Create a new ADR instead.
3. **Retroactive ADRs Without Admitting It**: Writing an ADR for a decision made 6 months ago as if it were current. Note "Recorded retroactively" in the status.
4. **No Options Considered**: An ADR that only describes the chosen option. Without alternatives, it is not a decision record; it is a description.
5. **Vague Consequences**: "This might have performance implications." Be specific: "Read queries on the orders table will require an index scan above 10M rows."

## References

- [MADR - Markdown Any Decision Records](https://adr.github.io/madr/)
- [Michael Nygard's ADR Blog Post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub Organization](https://adr.github.io/)
- [C4 Model](https://c4model.com/)
- [arc42 Architecture Documentation](https://arc42.org/)
