---
name: architectural-decision-records
version: "0.1"
description: >
  [STUB - Not implemented] Lightweight architectural decision tracking in Markdown (ADR) format.
  PROACTIVELY activate for: [TODO: Define on implementation].
  Triggers: [TODO: Define on implementation]
core-integration:
  techniques:
    primary: ["[TODO]"]
    secondary: []
  contracts:
    input: "[TODO]"
    output: "[TODO]"
  patterns: "[TODO]"
  rubrics: "[TODO]"
---

# Architectural Decision Records

> **STUB: This skill is not yet implemented**
>
> This placeholder preserves the documented plugin structure.
> See parent plugin README for planned capabilities.

## Planned Capabilities

- ADR template generation
- Decision status tracking (Proposed, Accepted, Deprecated, Superseded)
- Cross-referencing between related decisions
- Impact analysis documentation
- Decision review workflows

## ADR Template

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
Need scalable relational database with ACID guarantees

## Decision
Use PostgreSQL 15+ for primary data storage

## Consequences
+ Strong ACID compliance
+ Rich ecosystem
- Higher operational complexity than NoSQL
```

## Implementation Status

- [ ] Core implementation
- [ ] References documentation
- [ ] Output templates
- [ ] Integration tests
