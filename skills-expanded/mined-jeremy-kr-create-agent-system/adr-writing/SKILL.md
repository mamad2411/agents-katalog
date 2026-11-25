---
name: adr-writing
description: "ADR (Architecture Decision Record) writing guide. Use when documenting architecture decisions."
---

# ADR Writing Guide

## Required Structure
All ADRs must follow this structure:

```markdown
# ADR-{number}: {Title}

## Status
Proposed | Accepted | Amended | Deprecated

## Context
Why is this decision needed? Current situation and constraints.

## Decision
What was chosen?

## Alternatives Considered
| Alternative | Pros | Cons | Rejection Reason |
|------------|------|------|-----------------|
| A | ... | ... | ... |
| B | ... | ... | ... |

## Consequences
- (+) Positive outcomes
- (-) Negative outcomes / trade-offs
```

## Amendment (for changes after spec finalization)
When a CR (Change Request) is approved, add an Amendment to the existing ADR:
```markdown
## Amendment (CR-{number}, {date})
- Change: ...
- Reason: ...
- Impact scope: ...
```
