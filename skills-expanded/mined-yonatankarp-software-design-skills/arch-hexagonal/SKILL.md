---
name: arch-hexagonal
description: Use when isolating domain logic from frameworks and external systems — phrases like "hexagonal architecture", "ports and adapters", "clean architecture", "onion architecture", "dependency inversion at the architecture level", "domain should not know about Spring", "the framework is leaking into my model", "input ports", "output ports", "primary vs secondary adapters". Defines the Ports & Adapters style: the domain at the centre, ports as interfaces, adapters as the technology-specific implementations.
---

## One-line summary

Place the domain at the centre. Define *ports* — abstract interfaces the domain owns — for everything outside (HTTP, databases, message brokers). Plug *adapters* into those ports. Dependencies point inward; the domain depends on nothing.

## When to use this skill

- The domain is complex and you want it testable in isolation from frameworks.
- You expect to swap infrastructure (database, message broker, HTTP framework) over the system's life.
- The domain logic must survive multiple delivery mechanisms (REST API, message handler, scheduled job all calling the same domain).
- DDD codebase that wants a clear technical architecture (`arch-hexagonal` is the conventional architectural shape for DDD).

## When NOT to use this skill

- Simple CRUD with no real domain logic — layered architecture (`arch-layered`) is enough. Hexagonal's ceremony costs more than it saves.
- Tiny scripts or short-lived prototypes.
- Teams unfamiliar with dependency inversion who would build "fake hexagonal" — folders renamed without actually inverting the dependency direction.

## Core content

The three pieces:

- **Domain (core).** Pure business logic. Knows nothing about Spring, JPA, HTTP, Kafka. Defines interfaces (*ports*) it needs the outside world to satisfy. Imports nothing from infrastructure.
- **Ports.** Interfaces owned by the domain that describe what it needs:
  - **Input ports** (driving / primary) — invoked by the outside world to ask the domain to do work (use-case interfaces).
  - **Output ports** (driven / secondary) — used by the domain to reach out (repository interfaces, notification senders, time providers).
- **Adapters.** Concrete implementations:
  - **Input adapters** call input ports (an HTTP controller, a message-queue consumer, a CLI handler).
  - **Output adapters** implement output ports (a JPA repository, a Kafka publisher, a system-clock implementation).

The **dependency rule**: code inside the domain hexagon cannot import anything outside it. Code in adapters can import the domain. Wiring is done at the composition root (often a Spring config or the `main` function).

**Why it's worth it.** Tests for the domain run instantly with in-memory adapters. Changing the database doesn't touch the domain. A second delivery mechanism (message handler vs REST) reuses the same use cases. The model survives even when half the infrastructure is replaced.

**Variants.** "Onion architecture" and "Clean Architecture" (Uncle Bob) are the same idea with different vocabulary and a few extra layers. The core insight — dependencies point inward toward the domain — is identical.

## Decision heuristics

- Always pair with DDD (or at least a real domain model). Hexagonal without a domain model is hexagonal-flavoured CRUD.
- Domain code does not depend on Spring annotations, JPA annotations, framework types, or library classes other than the standard library. If `import org.springframework.…` appears in domain code, it's no longer hexagonal.
- Ports live in the domain module. Adapters live in an infrastructure module. The build system enforces the direction.
- Be wary of inventing more than the necessary number of ports — every interface is a cost.

## Anti-patterns

- **Hexagonal in name only.** Folders renamed `domain/` and `infrastructure/` but the domain still imports Spring or JPA. Cargo cult.
- **Anemic ports.** Output ports that are 1:1 with JPA's `JpaRepository` interface — the abstraction adds no abstraction.
- **God adapter.** One adapter implementing six ports. Split by responsibility.
- **Bidirectional dependency at the seam.** The domain importing an adapter type by name. Defeats inversion.
- **Adapter doing business logic.** Logic that belongs in the domain leaking into the controller or the repository implementation.

## See also

- `arch-layered` — the alternative shape; simpler, no inversion.
- `arch-solid` — Dependency Inversion Principle is the foundational idea.
- `ddd-context-mapping` — Anticorruption Layer at a context boundary is a domain-side port + adapter.
- `ddd-repository` — DDD repositories are output ports in hexagonal terms.
- `arch-fitness-functions` — enforcing the dependency direction in CI.

## References

- Alistair Cockburn, *Hexagonal Architecture* (2005 original essay).
- Tom Hombergs, *Get Your Hands Dirty on Clean Architecture* — practical hexagonal-with-Java reference.
- Robert C. Martin, *Clean Architecture* (Pearson, 2017) — the "Clean Architecture" variant.
- Davi Vieira, *Designing Hexagonal Architecture with Java* (Packt) — domain / application / framework hexagon vocabulary.
