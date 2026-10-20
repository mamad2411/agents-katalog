---
name: skill-knowledge-management
description: Design docs, RFC (Request for Comments) process, ADR (Architecture Decision Records), code comments (WHY not WHAT), documentation structure, knowledge discovery and search, cross-team communication. Use when documenting decisions, writing design docs, or improving knowledge sharing.
version: 1.0.0
---

# Skill: Knowledge Management

Design docs live in git. Decisions are documented. Knowledge is discoverable.

## RFC (Request for Comments)

**Before designing** (gather feedback early):

```markdown
## RFC: [Title]

### Problem
[What problem are we solving?]

### Proposed Solution
[How does this solve it?]

### Alternatives
[Other approaches and why we rejected them]

### Trade-offs
[What do we gain/lose?]

### Timeline
[When will this ship?]
```

## Design Doc

**Before implementing** (detailed specification):

```markdown
## Design Doc: [Title]

### Problem Statement
[Why are we building this?]

### Goals & Non-Goals
[What we're doing, what we're not]

### Proposed Design
[Architecture, data flow, components]

### Alternatives Considered
[Why we chose this approach]

### Trade-offs
[Maintainability vs. speed, etc.]

### Implementation Plan
[Phases, dependencies]

### Testing Strategy
[How will we verify this works?]

### Risks & Mitigation
[What could go wrong?]
```

## ADR (Architecture Decision Record)

**After deciding** (commit to git as history):

```
## ADR-0001: Microservices vs. Monolith

### Context
[Why are we deciding?]

### Decision
[What are we choosing?]

### Consequences
[What changes?]

### Alternatives Considered
[Other options]
```

## Code Comments

**DO**: Explain WHY
```python
# ✓ Explain the decision
# Retry only on transient errors (connection refused, timeout)
# Don't retry on permanent errors (auth, not found)
if isinstance(error, TransientError):
    retry()
```

**DON'T**: Explain WHAT (names say that)
```python
# ✗ Redundant, names already say this
# Set retry count to 3
retry_count = 3

# ✓ Explain why 3
# Balances latency (most transient errors recover quickly)
# with reliability (rare cascading failures)
retry_count = 3
```

---

**Status**: Ready for knowledge work  
**Best for**: Design docs, RFCs, ADRs, documentation
