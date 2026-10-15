---
name: kotlin-springboot-hexagonal
description: >
  Architecture guide for Kotlin + Spring Boot projects using hexagonal (ports & adapters) architecture
  with a modular monolith structure. Use this skill whenever creating new features, modules, use cases,
  domain entities, controllers, repositories, or any code that needs to follow the project's layered
  architecture. Also use when the user asks about project structure, where to place new code, how to
  wire dependencies between layers, or how to implement CQRS-style patterns. Trigger on mentions of
  "new feature", "new use case", "new entity", "new endpoint", "add API", "new module", "architecture",
  "hexagonal", "ports and adapters", or any request to scaffold or generate code following project conventions.
---

# Kotlin + Spring Boot Hexagonal Architecture Guide

This skill defines the architectural conventions for a Kotlin Spring Boot modular monolith using hexagonal architecture (ports & adapters). Follow these patterns when creating or modifying any code.

## Module Structure

The project is organized into strict layers with unidirectional dependencies:

```
presentation (REST)  →  application (Use Cases)  →  domain (Models)  →  support (Shared Kernel)
```

| Layer | Responsibility | May Depend On |
|-------|---------------|---------------|
| `presentation` | REST controllers, request/response DTOs, security adapters, Spring config. There can be multiple presentation modules (e.g., `*-api`, `*-admin`) sharing the same application layer. | `application`, `support` |
| `application` | Use case interfaces (ports/in), service implementations, port/out interfaces | `domain`, `support` |
| `domain` | Entities, value objects, domain exceptions, repository interfaces & implementations | `support` |
| `support` | Base exception hierarchy, error codes, shared enums, cross-cutting types | _(none)_ |
| `infrastructure/*` | External system adapters (Redis, messaging, etc.) | `domain`, `support` |

**Critical rule**: Presentation modules never import `domain` directly. All domain concepts are accessed through `application` layer DTOs (Command, Query, Result).

## Creating a New Feature — Step by Step

When adding a new feature (e.g., "bookmark a post"), work bottom-up through the layers:

### 1. Domain Layer — Entity & Repository

If the feature requires a new entity, create it in `domain/src/main/kotlin/{base-package}/domain/{aggregate}/`.

For detailed entity patterns, value objects, repository conventions, and domain service patterns, see `references/domain-patterns.md`.

### 2. Application Layer — Use Case & Service

Create the use case interface, DTOs, and service implementation in `application/src/main/kotlin/{base-package}/application/{feature}/`.

For the full use case structure (Command/Query/Result naming, port/in and port/out organization, service patterns), see `references/application-patterns.md`.

### 3. Presentation Layer — Controller & DTOs

Create the controller, request/response DTOs in the target presentation module: `{presentation-module}/src/main/kotlin/{base-package}/{presentation}/...`.

For controller patterns (Request→Command mapping, Response construction, ApiResponse wrapping), see `references/presentation-patterns.md`.

### 4. Shared Types — Support Module

If the feature introduces new enums or exception types shared across layers, add them to `support/src/main/kotlin/{base-package}/support/`.

For the exception hierarchy and shared type conventions, see `references/support-patterns.md`.

## Quick Reference: File Placement

When you need to create a new file, use this table to determine the correct location:

| What you're creating | Module | Path |
|---------------------|--------|------|
| Entity class | `domain` | `domain/.../domain/{aggregate}/{Entity}.kt` |
| Value object | `domain` | `domain/.../domain/{aggregate}/vo/{ValueObject}.kt` |
| Domain exception | `domain` | `domain/.../domain/{aggregate}/exception/{Exception}.kt` |
| Command repository (interface) | `domain` | `domain/.../domain/{aggregate}/repository/{Entity}CommandRepository.kt` |
| Command repository (impl) | `domain` | `domain/.../domain/{aggregate}/repository/{Entity}CommandRepositoryImpl.kt` |
| Query repository (interface) | `domain` | `domain/.../domain/{aggregate}/repository/{Entity}QueryRepository.kt` |
| Query repository (impl) | `domain` | `domain/.../domain/{aggregate}/repository/{Entity}QueryRepositoryImpl.kt` |
| Domain service | `domain` | `domain/.../domain/{aggregate}/{Entity}DomainService.kt` |
| Use case interface | `application` | `application/.../application/{feature}/port/in/{Action}UseCase.kt` |
| Command DTO | `application` | `application/.../application/{feature}/port/in/command/{Action}Command.kt` |
| Query DTO | `application` | `application/.../application/{feature}/port/in/query/{Entity}Query.kt` |
| Result DTO | `application` | `application/.../application/{feature}/port/in/result/{Entity}Result.kt` |
| Port/out interface | `application` | `application/.../application/{feature}/port/out/{Capability}Port.kt` |
| Service implementation | `application` | `application/.../application/{feature}/{Action}Service.kt` |
| Controller | `presentation` | `{presentation-module}/.../api/{feature}/{Feature}Controller.kt` |
| Request DTO | `presentation` | `{presentation-module}/.../api/{feature}/request/{Action}Request.kt` |
| Response DTO | `presentation` | `{presentation-module}/.../api/{feature}/response/{Entity}Response.kt` |
| Port/out adapter | `presentation` | `{presentation-module}/.../api/common/{concern}/{Adapter}.kt` |
| Shared enum | `support` | `support/.../support/type/{TypeName}.kt` |
| Shared exception | `support` | `support/.../support/exception/{Exception}.kt` |

> `{base-package}` and `{presentation-module}` are placeholders — resolve them from the actual project structure (e.g., by inspecting existing packages or `build.gradle.kts`). A project may have multiple presentation modules (e.g., `*-api` for public, `*-admin` for back-office).

## Key Conventions Summary

### DTO Naming

| Kind | Suffix | Location | Example |
|------|--------|----------|---------|
| Write/action input | `Command` | `port/in/command/` | `CreatePostCommand` |
| Read/query input | `Query` | `port/in/query/` | `PostsQuery` |
| Use case output | `Result` | `port/in/result/` | `PostDetailResult` |
| API input | `Request` | `api/{feature}/request/` | `CreatePostRequest` |
| API output | `Response` | `api/{feature}/response/` | `PostResponse` |

### Use Case Rules

- One use case = one action = one `operator fun invoke` method
- Interface in `port/in/`, implementation as `@Service` class
- Command for writes, Query for reads — never mix
- Result types returned from use cases, never domain entities

### Controller Rules

- Request → Command/Query mapping via **private extension functions** inside the controller
- Result → Response mapping via **private extension functions** inside the controller
- All responses wrapped in `ApiResponse`


### Repository Rules

- Split into CommandRepository (writes) and QueryRepository (reads)
- Interface defined in `domain/{aggregate}/repository/`
- Implementation using `SimpleJpaRepository` (command) or `JPAQueryFactory` (query)
- Both interface and impl live in the domain module

### Transaction Rules

- `@Transactional` on service methods that write
- `@Transactional(readOnly = true)` on service methods that only read
- Transaction boundaries at the application service layer, never at controller or domain

### Kotlin Idioms

- `data class` for DTOs, `@JvmInline value class` for value objects
- `private set` on mutable entity fields — mutations only through domain methods
- `companion object { fun create(...) }` factory methods on entities
- Expression bodies for single-expression functions
- `val` over `var`, immutable collections at public boundaries
- Named arguments and trailing lambdas for clarity

## Agents

This skill includes specialized agents for common workflows. Read the agent instructions before delegating:

- `agents/feature-scaffold.md` — Scaffolds a complete vertical slice (entity → repository → use case → controller) for a new feature. Use when adding a new feature that spans all layers.
- `agents/architecture-reviewer.md` — Reviews code for hexagonal architecture compliance, naming convention violations, and layer dependency issues. Use after scaffolding or before PRs.
