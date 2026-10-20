---
name: dotnet-architecture-selection
description: ".NET için Monolitik, Clean, Vertical Slice, CQRS, Mikroservisler vb. mimari seçer; yeni çözüm başlatırken veya mimari değişikliği gerekçelendirirken kullan."
---

# .NET Core — Architecture Selection

## Overview

There is no one-size-fits-all architecture; choose the one that fits your team, domain, and
long-term goals. This skill helps pick — and combine — the major .NET architecture styles.
For deep design work, hand off to the `dotnet-backend-architect` agent.

## Decision shortcut

1. **Small app / MVP / prototype, one team** → start **Monolithic** (or layered).
2. **Clear separation needed, single deployable** → **N-Tier** or **Clean**.
3. **Long-lived, business-rule-heavy, must stay testable** → **Clean (+ Vertical Slice)**.
4. **Feature-team velocity, low cross-feature coupling** → **Vertical Slice (+ CQRS)**.
5. **Independent scaling/deploy of parts, mature org** → **Microservices**.
6. **Asymmetric read/write load or complex domains** → **CQRS** (within any of the above).
7. **Real-time, decoupled integration, audit/replay** → **Event-Driven (+ Event Sourcing)**.

> Defaults are combinable. A common high-quality .NET default is **Clean Architecture +
> Vertical Slice + CQRS** (the project-template's stack): Clean for dependency direction,
> Vertical Slice for feature cohesion, CQRS for read/write clarity.

## The seven styles

### 1. Monolithic
Single codebase, single deployable; components tightly coupled.
**Pros:** easy to develop/deploy, simple to test, good performance (in-process calls).
**Cons:** hard to scale selectively, tight coupling, technology lock-in.
**Best for:** small apps, MVPs, prototypes, simple domains.

### 2. N-Tier
Layers: Presentation → Business Logic → Data Access.
**Pros:** separation of concerns, organized, maintainable.
**Cons:** still tightly coupled; a change in one layer can ripple.
**Best for:** enterprise apps needing clear layer separation.

### 3. Clean (Onion / Hexagonal)
Dependency rule points inward: **WebApi → Infrastructure → Application → Domain**. Domain has
no outward dependencies; UI/frameworks live at the edge.
**Pros:** highly maintainable, testable, independent of UI/DB/frameworks.
**Cons:** more initial setup, steeper learning curve.
**Best for:** complex, long-term projects that must stay testable.

### 4. Vertical Slice
Organize by **feature** (slice) rather than technical layer; each feature is end-to-end
(Command/Query + Handler + Validator + Endpoint).
**Pros:** high cohesion, low coupling between features, faster feature development, easy to
scale by feature.
**Cons:** requires good team discipline to keep slices consistent.
**Best for:** modern APIs, feature-team-oriented development.

### 5. Microservices
Small, independent services communicating over the network.
**Pros:** independent deployment, scalability, tech flexibility, fault isolation.
**Cons:** operational/design complexity, network latency, distributed-data challenges.
**Best for:** large-scale systems with multiple teams and high scalability needs.

### 6. CQRS (Command Query Responsibility Segregation)
Separate the **write** model (commands) from the **read** model (queries); optionally separate
stores.
**Pros:** optimized/scalable reads & writes, better separation.
**Cons:** more complex, data synchronization between models.
**Best for:** high read/write asymmetry, reporting, analytics, complex domains.

### 7. Event-Driven (EDA)
Components communicate by **producing** and **consuming** events (Producer → Event Broker →
Consumer).
**Pros:** loose coupling, scalable, real-time processing, resilient.
**Cons:** eventual consistency, harder to debug/trace.
**Best for:** real-time systems, integration between services, IoT/stream processing.

## How to choose (checklist)

- **Team size & maturity** — microservices tax small teams; monolith slows huge ones.
- **Domain complexity** — rich business rules favor Clean; simple CRUD favors N-Tier/monolith.
- **Scaling profile** — selective scaling → services/CQRS; uniform load → monolith scales fine.
- **Change frequency by feature** → Vertical Slice; by layer → N-Tier/Clean.
- **Consistency needs** — strong → single store; tolerant of eventual → EDA/CQRS.
- Prefer the **simplest** style that fits; combine patterns rather than over-architecting.

## Gotchas

- **Microservices too early** — distributed complexity (network, data consistency, ops) sinks small teams.
- **CQRS on simple CRUD** — two models + sync overhead with no read/write asymmetry to justify it.
- **Clean Architecture on a throwaway** — ceremony and layers that a small app/MVP doesn't need.
- **Inconsistent slices** — Vertical Slice without discipline drifts into duplicated, divergent patterns.
- **Anemic domain** — entities as data bags with logic in services defeats Clean/DDD intent.
- **Over-combining** — stacking every pattern "to be safe"; combine only what the problem demands.

## Related

- Deep .NET design & implementation: `dotnet-backend-architect` agent.
- ASP.NET Core app-model & pipeline: `dev-aspnet-core`.
- Scaling these architectures by user stage: `dev-system-design-scaling`.
- Class-level design within a slice: `dev-low-level-design`.
