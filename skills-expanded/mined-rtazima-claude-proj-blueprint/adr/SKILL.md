---
name: adr
description: Create Architecture Decision Records. Activated when the user mentions ADR, architectural decision, or technical trade-off.
allowed tools: Read, Write, Glob
---

# Architecture Decision Records

## Template
Create in `docs/architecture/adr-NNN-title.md`:

```markdown
# ADR-NNN: Decision Title

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## Context
What motivated this decision? What problem are we solving?

## Decision
What we decided to do and why.

## Alternatives considered
1. **Alternative A** — pros and cons
2. **Alternative B** — pros and cons

## Consequences
- Positive: ...
- Negative: ...
- Risks: ...

## Impact on specs
[SPEC] List affected specs:
- Compliance: [impact]
- Security: [impact]
- Scalability: [impact]
- [others]

## References
- PRD: `docs/product/xxx.md`
- Design: [link]
```

## Rules
- Number sequentially (check last number with `ls docs/architecture/`)
- Accepted ADRs are immutable — create a new ADR to supersede
- Always link to the PRD that motivated the decision
