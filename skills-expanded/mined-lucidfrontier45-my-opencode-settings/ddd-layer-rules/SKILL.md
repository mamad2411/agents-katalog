---
name: ddd-layer-rules
description: >-
  Guide for projects using a DDD-like layered architecture with Domain, Use Case, Infrastructure, Entrypoint, and Shared layers.
  Use this skill whenever the user mentions DDD, domain-driven design, layered architecture, hexagonal architecture,
  clean architecture, or when the existing project has directories like domain/, usecase/, infrastructure/, entrypoint/,
  and common/. Also trigger when the user asks where to place new code, how to organize files, what dependency rules
  apply, or how to refactor across these layers — even if they don't explicitly name "DDD" or "layers."
  This skill is language-agnostic and applies to any project following this pattern.
---

# DDD-like Layer Architecture Rules

This project uses a Domain-Driven Design-like layered architecture. The goal is to keep business logic isolated from infrastructure concerns, making the code testable, maintainable, and adaptable to change.

## The Five Layers

### Domain Layer (`domain/`)
Core business logic and entities. This is the heart of the application — it should contain nothing but pure business concepts.

**What goes here:**
- Entity structs/classes representing business objects
- Value objects
- Domain services (business logic that doesn't fit on an entity)
- Repository interfaces (not implementations)
- Domain events
- Business rule validation

**Why this matters:** When domain logic is mixed with database or framework code, you can't test business rules without spinning up a database. Keeping the domain pure means you can unit test your most important logic instantly.

### Use Case Layer (`usecase/`)
Application-specific business rules that orchestrate the domain layer.

**What goes here:**
- Interactors or use case classes
- Input/output data structures (DTOs) for each use case
- Business workflow orchestration

**Typical flow:**
1. Receives input as function/method arguments from the entry point layer
2. Uses repository interfaces or domain services from the domain layer to fetch, manipulate, and persist data
3. Returns output as return values back to the entry point layer

**Why this matters:** Use cases are the "script" of the application. They should read like a story of what happens step by step, without getting bogged down in database queries or HTTP concerns.

### Infrastructure Layer (`infrastructure/`)
External services, databases, frameworks, and technical capabilities.

**What goes here:**
- Repository implementations (database access)
- External API clients
- Message queue producers/consumers
- File storage implementations
- Framework-specific configuration
- All concrete implementations of domain interfaces

**Why this matters:** Infrastructure is a detail that can be swapped. By keeping implementations separate, you can change databases, cloud providers, or external services without touching business logic.

### Entrypoint Layer (`entrypoint/`)
API endpoints, CLI interfaces, event consumers, and user interactions.

**What goes here:**
- HTTP handlers / controllers
- CLI command definitions
- Background worker entry points
- Request/response serialization
- Input validation (structural — business validation goes in the domain)
- Middleware (auth, logging, CORS)
- Dependency wiring / composition root — creating concrete instances of infrastructure implementations and injecting them into use cases

**Why this matters:** This layer translates between the outside world and your application. It should be thin — just enough to parse input and format output, delegating everything else to use cases.

The entrypoint layer also serves as the **composition root** — the only place where concrete types are instantiated and wired together. Interfaces are defined in the domain, implementations live in infrastructure, but the act of connecting them (creating a PostgresOrderRepository and injecting it into CreateOrderUseCase) happens in entrypoint. This keeps every other layer agnostic about which specific implementations are in use and makes swapping implementations trivial.

### Shared Layer (`common/`)
Common utilities, constants, and helper functions that any layer can use.

**What goes here:**
- Type aliases and shared constants
- Utility functions (string manipulation, date formatting)
- Custom error types used across layers
- Logging helpers
- Configuration loading

**Why this matters:** Centralizing shared code prevents circular dependencies and duplication. However, avoid letting this become a dumping ground — if something belongs to a specific layer, put it there.

## Dependency Rules

These rules define which layers can depend on which. Think of them as a directed acyclic graph — following them prevents the tangled mess that makes projects hard to change.

```
entrypoint → usecase → domain
entrypoint → infrastructure
    ↑            ↓
    └── common ──┘
          ↑
    (no downward dependency)
```

- **Domain Layer** should not depend on any other layer.
  - *Exception:* Structs can have tags of external libraries (e.g., JSON serialization tags, ORM column tags) but should not import or use any external packages directly in domain logic.
- **Use Case Layer** can depend on the Domain Layer but not on Infrastructure or Entrypoint Layers.
- **Infrastructure Layer** can depend on Domain and Use Case Layers but not on Entrypoint Layer.
- **Entrypoint Layer** can depend on all other layers.
- **Shared Layer** can be used by any layer but should not depend on any specific layer.

### How to apply these rules

When generating or reviewing code, ask yourself:

1. **Which layer does this belong to?** If it's a business concept, it's domain. If it's a database call, it's infrastructure. If it's orchestrating a workflow, it's a use case. If it's handling HTTP or CLI input/output, it's entrypoint.

2. **Does this violate a dependency direction?** Look at the imports/requires/uses of the file. If a domain file imports something from infrastructure, that's a violation. If a use case imports an HTTP handler, that's a violation.

3. **Can this be expressed as an interface in the domain?** If infrastructure depends on domain concepts, that's fine. If domain needs to call infrastructure, define an interface in the domain layer and implement it in infrastructure. This is the Dependency Inversion Principle in action.

4. **Is this leaking abstractions?** Don't pass HTTP request objects, database connections, or framework types through domain or use case layers. Define simple input/output types in the use case layer.

5. **Where are instances created and wired?** If you're writing `new PostgresOrderRepository()` or equivalent, it should be in the entrypoint layer. Use cases should receive their dependencies (via constructors, function arguments, or DI) — they should never instantiate infrastructure. This is the composition root pattern: interfaces in domain, implementations in infrastructure, instantiation and wiring in entrypoint.

### Concrete examples

**Correct:**
- `domain/order.go` defines an `Order` struct and an `OrderRepository` interface
- `usecase/create_order.go` uses `OrderRepository` interface to implement order creation workflow
- `infrastructure/postgres_order_repo.go` implements `OrderRepository` using a PostgreSQL driver
- `entrypoint/http/handler.go` calls the use case with parsed HTTP request data
- `common/errors.go` defines shared error types used across layers
- `entrypoint/main.go` (or `entrypoint/wire.go`) creates `PostgresOrderRepository` and injects it into `CreateOrderUseCase`, then passes the use case to the HTTP handler

**Incorrect:**
- `domain/order.go` imports a database driver directly — domain should not depend on infrastructure
- `usecase/create_order.go` takes an `http.Request` as input — use case should not know about HTTP
- `usecase/create_order.go` calls `new(PostgresOrderRepository)` directly — use cases should receive dependencies, not instantiate them
- `infrastructure/postgres_order_repo.go` imports HTTP-related types — infrastructure should not depend on entrypoint
- `domain/order.go` imports from `common/` utility that itself depends on infrastructure — shared should not depend on specific layers

## Language-specific notes

While these rules are language-agnostic, here are considerations for specific languages:

- **Go**: Use interfaces in domain, concrete structs in infrastructure. JSON/GORM tags on domain structs are acceptable exceptions. Wire dependencies in `entrypoint/main.go` or using a DI tool like Google Wire.
- **Java/Kotlin**: Define interfaces in domain module, implementations in infrastructure module. Use dependency injection frameworks at the entrypoint layer.
- **Python**: Abstract base classes or protocols in domain, concrete implementations in infrastructure.
- **TypeScript/JavaScript**: Interfaces or type definitions in domain, implementations in infrastructure. Use dependency injection or module boundaries.
- **Rust**: Traits in domain, implementations in infrastructure. Crate-level visibility to enforce boundaries.

## When to be flexible

Architecture rules serve the code, not the other way around. Reasonable exceptions include:

- **Cross-cutting concerns**: Logging, metrics, and tracing often cut across layers. Route them through the shared layer or inject them via interfaces.
- **Prototyping**: In early stages, it's fine to flatten the structure and refactor later — as long as the team understands the target architecture.
- **Framework conventions**: Some frameworks (e.g., Rails, Django) have their own conventions. When using such frameworks, adapt these rules to fit within the framework's structure rather than fighting it.

The goal is not purity — it's maintainability. If a rule is making the code harder to maintain instead of easier, reassess.
