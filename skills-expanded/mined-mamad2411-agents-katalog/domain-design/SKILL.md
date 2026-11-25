---
name: domain-design
description: Use when designing aggregates, domain events, application service boundaries, and anti-corruption layers for DDD-style .NET solutions.
---

# Domain Design

## Specialization

Design rich domain models and architecture-level boundaries for DDD-oriented .NET work without drifting into implementation-unrelated workflow or generic coding standards.

## Trigger Conditions

- Aggregate boundaries need to be identified or pressure-tested.
- A model is at risk of becoming anemic or overly service-centric.
- Domain events, ACLs, or repository ownership need a clear design decision.
- An application service boundary needs to be validated before implementation.

## Inputs

- Domain nouns, use cases, and invariants.
- Affected bounded context or feature area.
- External integration points and consistency requirements.
- Any performance, security, or transaction constraints already known.

## Required Outputs

- Aggregate and invariant design guidance.
- Domain-event and repository-boundary decisions.
- Application-service boundary recommendations.
- A concise pattern recommendation or anti-pattern warning when relevant.

## Assets

- Use [README.md](./references/README.md) for available reusable references.
- Use [aggregate-boundary-checklist.md](./references/aggregate-boundary-checklist.md) during boundary evaluation.

## Workflow

1. Capture inputs and list domain nouns, use cases, and invariants.
2. Run aggregate discovery and boundary checks using the checklist assets.
3. Evaluate event strategy, repository ownership, and service boundaries.
4. Evaluate ACL requirements for each external integration point.
5. Return decisions and recommendations using the required outputs.

## Aggregate Discovery Workflow

1. List the domain nouns and group them by invariants that must hold atomically.
2. Identify lifecycle state transitions and the commands that trigger them.
3. Confirm each invariant can be enforced inside one aggregate root; if not, propose a domain service, saga, or process manager.
4. Keep cross-aggregate references by identifier unless the user explicitly needs a different consistency model.

## Aggregate Rules

- Aggregates own transactional consistency boundaries.
- Value objects stay immutable and compare by value.
- Mutation methods should express domain intent rather than generic setters.
- Collections stay encapsulated behind intent methods.
- Optimistic concurrency should be explicit when concurrent modification matters.

## Domain Events

- Raise events only for meaningful state changes.
- Persist state before dispatching events.
- Prefer identifiers over large event payloads.
- Keep handler orchestration outside the aggregate when the flow spans multiple aggregates.

## Repository and Service Boundary Rules

- Repositories reconstruct and persist aggregates; they do not host business rules.
- Application services orchestrate one bounded operation and stay free of transport concerns.
- When a write must validate across entity boundaries atomically, prefer one stored procedure invoked through the owning repository.
- Service and repository layers should not add local `try/catch` behavior when the workspace policy routes exception handling through cross-cutting infrastructure.

## Anti-Corruption Layer Guidance

- Isolate external translation in a dedicated adapter.
- Validate inbound external data before it enters the domain model.
- Keep external terminology from leaking into aggregate APIs or value objects.

## Pattern Selection Grid

| Scenario | Preferred Pattern | Why |
|---|---|---|
| Cross-aggregate workflow | Saga or process manager | Keeps orchestration out of aggregate internals |
| Legacy or external boundary | Anti-corruption layer | Prevents foreign semantics from polluting the domain |
| Read-heavy optimization | CQRS read model | Preserves a rich write model while scaling reads |
| Significant architecture change | ADR with explicit rationale record | Captures durable rationale and trade-offs |

## Anti-Patterns

- Services holding core business logic that belongs in aggregate methods.
- Domain events emitted for trivial state changes.
- Repositories exposing infrastructure-specific types or leaking raw persistence models outward.
- External DTOs entering the domain without validation or translation.

## Done Criteria

- Aggregate boundaries and invariants are explicit.
- Repository and service ownership is clear.
- Event and ACL decisions are justified.
- Significant architecture choices include a durable rationale record when needed.
