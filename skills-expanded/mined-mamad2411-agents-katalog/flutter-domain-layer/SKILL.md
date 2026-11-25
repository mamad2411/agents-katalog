---
name: flutter-domain-layer
description: "**WORKFLOW SKILL** — Minimal guidance for the domain layer in Flutter Clean Architecture (use `equatable`, `call()` pattern)."
---

# Flutter Domain Layer (summary)

Purpose: Minimal, opinionated guidance and templates for the domain/core layer.

Essentials
- Entities: immutable models and value objects (use `equatable` for equality).
- Repositories: abstract interfaces (ports) implemented by the data layer.
- Use cases: interactors exposing a `call()` method.
- Domain exceptions: typed domain errors; map infra errors in the data layer.

Structure
- Suggested layout: `lib/domain/entities/`, `lib/domain/repositories/`, `lib/domain/usecases/`, `lib/domain/exceptions.dart`
- Keep domain pure (no Dio or data imports).

Details and examples moved to reference docs:
- `references/entities.md`
- `references/repositories.md`
- `references/usecases.md`
- `references/exceptions.md`
- `templates/` — code templates (entity, repository, use case, exceptions)

Quick prompts
- "Scaffold `User` entity (Equatable), `UserRepository` interface, `GetUser` use case, and domain exceptions."
- "Create a `GetUser` unit test using a fake repository."

