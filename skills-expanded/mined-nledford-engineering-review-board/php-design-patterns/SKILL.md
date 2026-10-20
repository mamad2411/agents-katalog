---
name: php-design-patterns
description: PHP-native design-pattern guidance. Use when choosing or reviewing value objects, readonly DTOs, enums, factories, interfaces, dependency injection, adapters, repositories, application services, presenters, middleware, property hooks, or resource ownership in PHP. Do not use for ordinary PHP implementation, test-lane execution, or smell-focused review; use php-engineering, php-testing-quality, or php-antipatterns instead.
---

# PHP Design Patterns

## Use When

Use for deliberate PHP pattern selection or review where types, ownership, and boundaries affect maintainability. Use [`php-engineering`](../php-engineering/SKILL.md) to implement the chosen design, [`php-testing-quality`](../php-testing-quality/SKILL.md) for test execution, and [`php-antipatterns`](../php-antipatterns/SKILL.md) for smell-focused review.

## Selection Rules

Choose the smallest pattern that encodes an actual invariant, ownership boundary, or substitution seam. Prefer concrete collaborators until multiple implementations or an external boundary justify an interface. Do not introduce a pattern only to mirror framework vocabulary.

## Patterns To Prefer

- Value objects and readonly DTOs for validated, immutable concepts; use enums plus `match` for finite states.
- Named constructors or factories when creation has validation, normalization, or multiple meaningful entry paths.
- Small behavior-oriented interfaces and constructor dependency injection at external boundaries.
- Functional core/imperative shell for pure policy separated from I/O.
- Adapters for host, framework, filesystem, HTTP, or vendor APIs; domain-specific repositories only where collection-like persistence behavior belongs to the domain.
- Application services or commands for use-case coordination; presenters/view models for render-ready data; middleware for cross-cutting request flow.
- Deterministic resource and transaction ownership: one owner opens, commits/rolls back, and cleans up.

## Property Hooks And Encapsulation

Property hooks suit local property invariants, normalization, or computed views. Keep hooks deterministic and local. Do not perform service lookup, database/network I/O, logging, or surprising mutation in a hook; use a method or application service when work has observable behavior.

## Architecture And Methods

Keep domain behavior near the values it protects. Let controllers, handlers, and templates adapt inputs and outputs rather than carry policy. Prefer explicit method names for state transitions and return domain values or explicit result/error contracts.

## Testing Seams

Test pure policy directly. Substitute external adapters at ports, not arbitrary internals. Verify transactions, retries, and resource cleanup at integration boundaries where their observable contracts exist.

## Review Checklist

- Does the pattern encode a named invariant or external boundary?
- Are interfaces small and owned by their consumer?
- Is construction valid by default and state transition explicit?
- Is I/O outside value objects, property hooks, and pure policy?
- Is resource and transaction ownership singular and testable?

## Common Mistakes

Avoid service bags, generic repository wrappers, inheritance trees used only for reuse, DTOs that leak framework types, hooks with side effects, and abstraction before multiple real callers require it.
