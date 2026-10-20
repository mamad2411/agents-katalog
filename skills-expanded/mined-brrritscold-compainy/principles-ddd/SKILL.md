---
name: principles-ddd
description: Applies Domain-Driven Design discipline. Invoked when an engineer is modeling a domain, designing bounded contexts, considering aggregates, value objects, domain events, or any DDD pattern. Governs when strategic DDD is mandatory and when tactical patterns earn their place vs. add ceremony.
---

# DDD Principle

Strategic DDD always. Tactical patterns earn their place — reach for them when invariants/consistency/complexity demand, never as ritual. KISS/YAGNI break ties.

## Lean here (strategic)

**Ubiquitous language.**
Name types, methods, and modules after the domain concept. When the code and the business conversation use different words, translation errors compound. Pick one vocabulary and enforce it in code.

**Bounded contexts = module boundaries.**
A bounded context is a seam where a model has consistent meaning. Map it directly to a module, package, or service boundary. Resist the urge to share models across contexts — shared models become a coupling trap. Use explicit translation at the boundary instead.

**Pure domain, separated from infra.**
Domain logic must not import I/O, frameworks, or third-party services. Keep it pure: inputs and outputs are domain types, side-effects happen outside. This pairs naturally with Dependency Inversion — see `principles-pragmatic-solid`.

## Tactical patterns are tools

**Value Objects — only when the invariant justifies it.**
Use a Value Object (`Money`, `Email`, `DateRange`) when the concept carries validation, invariants, or equality-by-value that primitive types cannot express. Do not wrap every primitive. `userId: string` is fine; `UserId` is only worth it if the type enforces a format or participates in domain logic.

**Aggregates — only in genuine multi-entity consistency domains.**
An Aggregate boundary exists to enforce a consistency rule that spans multiple entities within one transaction. If you have a single entity with CRUD operations, use an entity + repository — there is no Aggregate problem to solve. Reach for Aggregate roots only when concurrent writes to a cluster of objects would produce invalid state.

**Domain events — only to decouple reactions.**
A domain event (`OrderPlaced`, `PaymentFailed`) makes sense when multiple downstream reactions must happen without the domain core knowing about them. Do not introduce events to communicate within a single bounded context; a direct method call is simpler and easier to trace.

## Cross-references

- `principles-pragmatic-solid` — Dependency Inversion enforces the infra/domain separation that strategic DDD demands.
- `principles-dry-kiss` — YAGNI is the tiebreaker when a tactical pattern is "nice to have" but the problem doesn't demand it yet.
- `principles-tdd` — a pure domain model with no infra dependencies is trivially unit-testable; tactical patterns that add complexity must justify themselves against testability cost.
