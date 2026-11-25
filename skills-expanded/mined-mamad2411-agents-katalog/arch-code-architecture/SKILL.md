---
name: arch-code-architecture
description: Design, evaluate and document software architecture end-to-end. Covers
  system design from requirements to C4 diagrams, pattern selection, hexagonal/ports-and-adapters
  structure, API design, adversarial architecture critique, and feature-level architecture.
  Use for greenfield design, re-architecture, technology selection, architecture review
  of proposals/ADRs, and feature blueprinting.
---

# Architecture & System Design (composite skill)

Design, evaluate and document software architecture. Composed from: system-architect,
hexagonal-architecture, api-design, architecture-review, architecture-critic,
feature-code-architect, feature-dev.

## When to activate

- New project or greenfield system design
- Major refactoring or re-architecture initiative
- Technology selection or migration evaluation
- Architecture review of a proposal, draft spec, or ADR
- Feature architecture: blueprint of files/components before implementation
- System design interview preparation

## A. Design process (from requirements to architecture)

### Phase 1 — Requirements & constraints
- **Business objectives**: problem solved, success criteria.
- **Functional requirements**: core capabilities.
- **Non-functional requirements** (the architect's domain): scalability, availability
  (SLA, RTO/RPO), latency (P50/P95/P99), security, cost, maintainability.
- **Constraints**: existing systems, team skills, budget, timeline, regulatory.

### Phase 2 — High-level architecture
- **System context (L1)**: inside vs outside.
- **Container view (L2)**: applications, services, databases, queues.
- **Technology selection** (weighted: team expertise 30%, ops maturity 25%, ecosystem
  20%, performance 15%, license/cost 10%; shortlist 3–5; document as ADR; validate high-risk with PoC).
- **Integration patterns**: sync vs async, event-driven vs request-response.
- **Data flow** end-to-end.

### Phase 3 — Component design
For each major component: API boundaries/contracts, data model + storage + caching,
internal architecture, failure modes, observability.

### Phase 4 — Cross-cutting concerns
AuthN/AuthZ, observability (traces/logs/metrics), deployment (CI/CD, canary/blue-green),
security (encryption, secrets, network zones), disaster recovery.

### Phase 5 — Evaluation
Trade-off analysis (explicit gains/losses per decision), risk assessment, review vs
NFRs, lightweight ATAM.

## B. Pattern selection (decision matrix)

| Pattern | Best for | When NOT to use |
|---|---|---|
| Modular monolith | Small teams, early stage | Independent scaling needed |
| Layered (n-tier) | CRUD apps | Complex domain (use hexagonal) |
| Hexagonal (Ports & Adapters) | Domain-driven, testability | Simple CRUD, small projects |
| Clean architecture | Large codebases, framework independence | Simple apps, framework coupling fine |
| Microservices | Large team, independent deploy | Small team, network overhead |
| Event-driven | Async, real-time, decoupling | Simple request-response, strong consistency |
| CQRS | Read/write disparity | Simple CRUD |
| Event sourcing | Audit trail, temporal queries | Simple state, storage cost |
| Saga | Distributed transactions | Single-service |
| Strangler fig | Legacy migration | Greenfield |

## C. Hexagonal (ports & adapters) structure

- **Domain model** — business rules, no framework imports.
- **Use cases (application layer)** — orchestrate domain.
- **Inbound/outbound ports** — contracts.
- **Adapters** — implementations (HTTP, DB, queue).
- **Composition root** — single wiring.

Dependency always inward: Adapters → Application → Domain. Anti-patterns: domain
importing ORM/HTTP types, use cases reading HTTP objects, returning DB rows directly,
adapters calling each other.

## D. API design

- Resource naming (nouns, plural, hierarchy), correct status codes.
- Pagination/filtering/sorting, error responses, versioning, rate limits.
- Contract-first with examples; validate request/response shapes.

## E. Architecture review (quality gates)

Apply these gates to any proposal or design:

1. **Concept integrity** — boundaries explicit, no purposeless components.
2. **Separation of concerns** — domain isolated from transport/UI/infra.
3. **Coupling & cohesion** — intentional minimal coupling, no parasitic links.
4. **Data & control flow** — single source of truth, no circular flows.
5. **Failure semantics** — known failure modes, defined degradation.
6. **Operability** — health checks, metrics, logs, runbook.
7. **Scalability envelope** — hot paths, capacity assumptions explicit.
8. **Security & trust boundaries** — explicit at process/network/storage.
9. **Evolvability** — localized change impact, versioning, migration paths.
10. **Spec-to-code alignment** — docs/ADRs agree with implementation.

### Adversarial critique (architecture-critic lens)
For proposals: does every service boundary map to a real domain seam? What's the
simplest design meeting requirements? Which NFRs are unstated and accidentally
violated? What's the data migration story? Trace one failure mode end-to-end.
For code: idiomatic for the target stack? Error handling meaningful or ceremonial?
Abstractions with one impl and no second use? Does the test suite pin behavior?

### Output contract (review)
1. Findings (sorted by severity: Blocker/High/Medium/Nit) → 2. Impact →
3. Evidence (files/specs) → 4. Decision options with trade-offs → 5. Recommendation
with rationale and rollback → 6. Validation plan. End with "If I could only change
one thing, it would be ___."

## F. Feature architecture

- Trace the codebase for the feature area first (dependencies, patterns, abstractions).
- Clarify underspecified details (edge cases, error handling, integration points,
  backward compat, performance) before designing.
- Draft 2–3 approaches: minimal changes, clean architecture, pragmatic balance.
- Produce a blueprint: files to create/modify, component designs, data flows,
  build sequence, executable acceptance criteria.

## Output format (architecture doc)

```
# Architecture: <name>
## Context (L1)      — one paragraph + diagram reference
## Containers (L2)   — key containers and interactions
## Architectural Decisions — ADR list with rationale
## Key Trade-offs    — chosen/rejected/rationale
## Risk Register     — likelihood/impact/mitigation
## Technology Stack  — choices with justification
```

## Related skills
- `arch-code-review` — code-level review (post-design)
- `arch-code-quality` — conventions, patterns, standards
- `arch-refactoring` — modernization of existing/legacy systems
