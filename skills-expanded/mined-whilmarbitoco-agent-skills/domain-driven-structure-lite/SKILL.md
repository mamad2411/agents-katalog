---
name: domain-driven-structure-lite
description: >
  Extends agent's knowledge of lightweight DDD structure for Java 21 apps.
  Use when the domain logic is complex enough to warrant aggregates, value
  objects, and domain events, but a full DDD tactical pattern set is overkill.
compatibility: Java 21+
metadata:
  domain: architecture
  level: advanced
  stack: [java-21, ebean-15, slf4j]
  version: "1.0.0"
---

# Domain-Driven Structure (Lite)

A pragmatic subset of DDD tactical patterns. Enough structure to model complex domains without ceremony.

## Building Blocks

| Block | Java construct | Purpose |
|-------|---------------|---------|
| Value Object | `record` | Immutable, compared by fields |
| Entity | Class with `id` | Mutable identity, lifecycle |
| Aggregate Root | Entity + invariants | Consistency boundary |
| Domain Event | `record` | Something happened in the domain |
| Domain Service | Class | Logic that doesn't belong to one entity |

## Rules

- Value objects are `record` — auto `equals`/`hashCode`, immutable.
- Aggregates enforce invariants in methods, not setters.
- Domain events are raised inside aggregate methods, collected by the service layer.
- Repositories persist whole aggregates — no partial saves.
- Domain services are stateless; they receive aggregates via constructor or method args.
- No anemic domain model — entities have behavior, not just getters/setters.

## Package layout

```
domain/
├── order/
│   ├── Order.java              aggregate root
│   ├── OrderLine.java          entity
│   ├── Money.java              value object (record)
│   ├── OrderPlaced.java        domain event (record)
│   ├── OrderRepository.java    interface
│   └── PricingService.java     domain service
```

## See also

- feature-based-packaging — aligns naturally with DDD boundaries
- service-repository-pattern — application service layer sits above domain
