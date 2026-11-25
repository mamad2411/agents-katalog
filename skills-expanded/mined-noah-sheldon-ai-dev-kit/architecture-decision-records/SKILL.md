---
name: architecture-decision-records
description: ADR process — template, lifecycle (proposed → accepted → deprecated), storage convention, when to create ADRs, referencing ADRs in PRs and plans, ADR maintenance.
origin: AI Dev Kit
---

# Architecture Decision Records (ADRs)

Capture significant architectural decisions in lightweight, version-controlled documents
that explain the context, alternatives, consequences, and status of each choice.

## When to Use

- Making a decision that affects system architecture, technology selection, or team workflow.
- A choice has non-obvious trade-offs that future maintainers need to understand.
- Reversing or superseding a prior architectural decision.
- Onboarding new engineers who need context for "why was it built this way?"
- Documenting compliance-related architecture choices (data residency, encryption standards).

## Core Concepts

### 1. ADR Template

Every ADR follows this structure in `docs/adr/NNNN-title.md`:

```markdown
# ADR-NNNN: Title

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD
**Author:** @username
**Reviewers:** @reviewer1, @reviewer2

## Context

What is the issue that we're seeing that is motivating this decision?
What are the constraints, forces, and stakeholders involved?
Include relevant data, metrics, or incidents that frame the problem.

## Decision

What is the change that we're proposing?
State the decision clearly and concisely in imperative form.
Be specific enough that a reviewer can verify compliance.

## Alternatives Considered

### Alternative 1: [Name]
- **Description:** What is it?
- **Pros:** Why consider it?
- **Cons:** Why reject it?

### Alternative 2: [Name]
- **Description:** What is it?
- **Pros:** Why consider it?
- **Cons:** Why reject it?

## Consequences

What becomes easier or more difficult to do because of this change?
List both positive and negative outcomes.
Include migration effort, cost implications, and operational impact.

## References

- Links to related ADRs, RFCs, PRs, or external resources.
```

### 2. ADR Lifecycle

```
Proposed → [Discussion] → Accepted → [Implementation] → Active
                                                ↓
                                    Superseded by ADR-NNNN
                                                or
                                       Deprecated
```

| Status | Meaning | Actions Allowed |
|---|---|---|
| **Proposed** | Under discussion, not yet binding | Anyone can comment, author updates |
| **Accepted** | Decision is made, implementation begins | Implement per decision; amendments via new ADR |
| **Active** | Implemented and in production | Follow the decision; no changes without new ADR |
| **Deprecated** | No longer recommended for new work | Migrate away; superseding ADR references old one |
| **Superseded** | Replaced by a newer ADR | Follow the new ADR; old one is archival |

### 3. Storage Convention

```
docs/adr/
├── 0001-use-postgres-as-primary-db.md
├── 0002-adopt-fastapi-for-new-services.md
├── 0003-event-driven-communication-between-services.md
├── 0004-migrate-to-aws-graviton-instances.md
└── README.md              ← Index of all ADRs with status
```

**Numbering rules:**
- Sequential, zero-padded to 4 digits (0001, 0002, ...)
- Never reuse a number; never delete an ADR
- Superseded ADRs stay in place with a link to the replacement

**README index:**

```markdown
# Architecture Decision Records

| # | Title | Status | Date |
|---|-------|--------|------|
| 0001 | Use PostgreSQL as Primary DB | Active | 2025-01-15 |
| 0002 | Adopt FastAPI for New Services | Active | 2025-02-03 |
| 0003 | Event-Driven Communication | Accepted | 2025-03-10 |
| 0004 | Migrate to AWS Graviton Instances | Proposed | 2025-04-01 |
```

### 4. When to Create an ADR

**Create an ADR when:**
- Choosing between two or more viable technologies, frameworks, or patterns
- Establishing a convention that will affect multiple teams or services
- Making a decision with long-lasting consequences (>6 months)
- A decision has significant cost, security, or compliance implications
- Reversing a prior decision that was documented in an ADR

**Do NOT create an ADR when:**
- The decision is trivial or reversible with minimal effort
- It's a implementation detail within an established pattern
- The choice is dictated by an external requirement (e.g., "client requires OAuth2")
- It's a temporary experiment or proof of concept

### 5. Referencing ADRs in PRs and Plans

**In PR descriptions:**

```markdown
## Architecture

- This PR implements ADR-0003 (Event-Driven Communication)
- Changes the notification service to publish to SQS instead of direct HTTP calls
- See `docs/adr/0003-event-driven-communication-between-services.md` for context
```

**In implementation plans:**

```markdown
### Decision Reference

Per ADR-0002, all new services must use FastAPI with:
- SQLAlchemy async ORM
- Pydantic v2 request/response models
- Structured logging with correlation IDs

This plan follows those conventions.
```

**In code comments (for traceability):**

```python
# ADR-0003: All inter-service communication uses SQS, not direct HTTP
# See: docs/adr/0003-event-driven-communication-between-services.md
async def publish_notification(event: NotificationEvent) -> None:
    await sqs_client.send_message(
        QueueUrl=settings.notification_queue_url,
        MessageBody=event.model_dump_json(),
    )
```

### 6. ADR Maintenance

**Quarterly review checklist:**
- [ ] Scan all `Proposed` ADRs — move to `Accepted` or `Deprecated`
- [ ] Verify `Active` ADRs are still followed in the codebase
- [ ] Identify ADRs that should be `Superseded` by newer decisions
- [ ] Update the `docs/adr/README.md` index
- [ ] Link any orphaned ADRs to related PRs and issues

**Deprecation process:**

```markdown
# ADR-0002: Adopt FastAPI for New Services

**Status:** Superseded by ADR-0015
**Date:** 2025-02-03
**Superseded Date:** 2026-03-01

## Supersession Notice

This ADR is superseded by [ADR-0015: Unified Python Service Framework](./0015-unified-python-framework.md).
The decision to standardize on a broader framework supersedes the FastAPI-specific guidance.
Existing FastAPI services remain supported; new services should follow ADR-0015.
```

### 7. ADR-Driven Development Workflow

```
1. Identify architectural decision point
2. Draft ADR in docs/adr/NNNN-title.md with status: Proposed
3. Share with team for async review (GitHub PR or shared doc)
4. Discuss alternatives, update based on feedback
5. Merge ADR → status: Accepted
6. Implement the decision (reference ADR in PR)
7. After implementation → status: Active
8. Revisit quarterly; deprecate or supersede as needed
```

## Anti-Patterns

- **Writing ADRs after the fact** — ADRs are decision records, not documentation of what already happened
- **Vague context section** — If a future reader can't understand why the decision was made, the ADR failed
- **No alternatives considered** — Every ADR must document at least 2 alternatives with pros/cons
- **Orphaned ADRs** — ADRs not referenced in code, PRs, or plans become dead documentation
- **Over-documenting trivial choices** — "We chose black over autopep8" does not need an ADR
- **Mutable ADRs** — Never edit an accepted ADR; write a new one to supersede or amend
- **Ignoring consequences** — Skipping the consequences section leaves teams unprepared for trade-offs

## Best Practices

1. **Write ADRs at decision time**, not during implementation or after deployment.
2. **Keep them short** — 1-2 pages max; if longer, split into multiple ADRs.
3. **Include data** — Metrics, benchmarks, and incident reports in the Context section.
4. **Reference ADRs everywhere** — PR descriptions, plans, code comments, runbooks.
5. **Maintain the index** — `docs/adr/README.md` must be current for ADRs to be discoverable.
6. **Use status transitions deliberately** — Proposed → Accepted → Active is a one-way flow.
7. **Review quarterly** — Assign an owner to scan and update ADR statuses each quarter.
8. **Link, don't duplicate** — Reference related ADRs instead of repeating context.
9. **Make consequences explicit** — List what becomes harder, what costs increase, what skills are needed.
10. **Treat ADRs as living documents** — Supersede, don't delete; deprecate, don't ignore.

## Related Skills

- `skill-authoring` — Creating reusable skill documents with similar structure
- `codebase-onboarding` — ADRs are critical onboarding artifacts for new engineers
- `code-review` — Reviewers should check that implementations follow accepted ADRs
- `documentation-lookup` — ADRs are part of the canonical documentation corpus
