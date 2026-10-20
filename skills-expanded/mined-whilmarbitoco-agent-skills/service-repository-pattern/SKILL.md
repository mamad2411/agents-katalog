---
name: service-repository-pattern
description: >
  Extends agent's knowledge of Service + Repository pattern in Java 21.
  Use when implementing business logic and data access with clean boundaries,
  testable units, and Ebean ORM or JDBC backends.
compatibility: Java 21+
metadata:
  domain: architecture
  level: beginner
  stack: [java-21, ebean-15, sqlite, slf4j]
  version: "1.0.0"
---

# Service + Repository Pattern

Two-layer business/data split. Service owns transactions and rules; Repository owns queries.

## Repository

- Wraps Ebean / JDBC calls. Returns domain objects or `Optional`.
- No business logic — only CRUD, finders, and simple aggregations.
- Interface + implementation split for testability.

## Service

- One public method per use case.
- Calls one or more repositories inside a single transaction.
- Validates input, enforces invariants, publishes domain events.
- Constructor-injected with repositories and event publishers.

## Rules

- Service methods are the transaction boundary (`@Transactional` or Ebean `beginTransaction`).
- Repos never call other repos — fan-out happens in the Service.
- Return domain objects from repos; return DTOs or records from services to callers.
- Use `Optional` for single-result finders; never return `null`.
- Parameterized logging only — no string concatenation.

## See also

- layered-architecture — where these layers sit
- domain-driven-structure-lite — richer domain model variant
