---
name: hexagonal-python-patterns
description: "FastAPI / Python backend patterns: hexagonal architecture, SOLID, KISS, ports (ABC inbound/outbound), Pydantic entities, use cases, centralized errors/logging. Trigger on: FastAPI, Python backend, pyproject.toml, uv.lock, or any request to implement/refactor/fix/scaffold a Python endpoint, use case, or adapter. Use when working on ANY FastAPI or Python backend, not only explicitly hexagonal ones; defaults the structure to hexagonal."
---

# Instructions: FastAPI Backend with Hexagonal Architecture

You are a Python/FastAPI expert. Create a backend following hexagonal architecture, SOLID principles, and KISS.

## 🏗️ Project Structure

```
├── .github/workflows/         # CI/CD (tests, linting, deploy)
├── src/
│   ├── main.py               # FastAPI app
│   ├── config.py             # Pydantic Settings
│   ├── dependencies.py       # Dependency injection
│   ├── domain/               # Business core
│   │   ├── entities/         # Business entities (Pydantic)
│   │   ├── ports/            # Interfaces (ABC)
|   │   |  ├── inbound/            # Interfaces for application use cases entry points(ABC)
|   │   |  ├── outbound/            # Interfaces for infrastructure implementation (ABC)
│   │   └── services/         # Business rules extracted from use cases (REQUIRED for validation/access/resolution logic — use cases stay thin)
│   │   └── errors/           # Redefined and centralised all errors types and messages
│   │   └── logging/          # Centralised all log messages
│   ├── application/
│   │   ├── requests/         # Input DTOs (Pydantic)
│   │   └── responses/        # FastAPI responses output DTOs (Pydantic)z
│   │   ├── use_cases/        # Application logic
│   │   └── routes/           # FastAPI routes
│   └── infrastructure/       # One folder = one implementation
│       ├── postgres/         # adapter.py + models.py
│       ├── mongodb/          # adapter.py + models.py
│       └── email/            # adapter.py
```

For per-layer file templates, load the relevant reference file below.

## Core principles

- **Domain stays pure**: entities hold invariants, no framework/infra imports inside `domain/`.
- **Application orchestrates**: use cases coordinate domain + ports; no direct infrastructure calls.
- **Infrastructure adapts**: one folder per concrete adapter (`postgres/`, `mongodb/`, `email/`).
- **Ports = ABCs**: interfaces in `domain/ports/` (`inbound/` for app entry points, `outbound/` for infra contracts).
- **Inbound/outbound split**: inbound ports invoked by routers/schedulers/consumers; outbound ports implemented by adapters.
- **Direct transformations**: convert at the adapter boundary inline; no `from_entity` / `to_entity` mapper helpers.
- **No Response DTOs for domain**: response/request DTOs live in `application/`; domain entities stay domain-shaped.
- **Centralized errors**: all error codes, messages, and custom exceptions in `domain/errors/`.
- **Centralized logging (STRICT)**: every `logger.*()` call MUST use a `LogMessage` StrEnum member from `src/domain/logging/` with lazy `%s` arguments. Inline strings, f-strings, and `logger.error(str(e))` in log calls are FORBIDDEN — see `references/logging.md` checklist. No logging inside `domain/entities/` or `domain/ports/`.
- **KISS**: no `__init__.py` unless re-export is genuinely needed; prefer flat, explicit imports.
- **Use case discipline (STRICT — blocking)**: see `references/use-cases.md` before writing any use case:
  - **ONE use case class per file** — `GetFooUseCase` lives in `get_foo_use_case.py`; NEVER append a second `*UseCase` class to an existing use case's file (its result NamedTuple/dataclass may share the file).
  - **Thin use cases** — a use case orchestrates (load → domain service/entity → outbound ports → return); business rules (validation guards, access policy, ownership checks, resolution logic) belong in `domain/services/`, NEVER in use-case private methods. ≥3 business private helpers or >~150 lines → extract a domain service. Pure plumbing (logging, task shielding) may stay.
  - **Reuse-first for logic** — before implementing any guard/query/loader, grep `use_cases/`, `domain/services/`, `domain/ports/` for an existing capability and inject/reuse it; re-implementing logic the app already has is a defect, not a style choice.
  - **No delegation-only wrappers (generalized)** — a method whose body ONLY wraps another method (single pass-through call — no guard, no error mapping, no added behavior) is useless indirection: call the target directly. Applies everywhere: use cases, domain services, adapters, routes. When you touch a class, RE-SCAN it for remaining one-liner wrappers and remove them. A wrapper is justified ONLY when it adds behavior.

## 🛡️ Edge cases (mandatory handling)
Every use case, adapter, and route MUST handle edge cases defensively, not just the happy path. During implementation, cover:
- **Null / None / undefined inputs** — validate at the port boundary; raise the correct domain error, never let `None` propagate silently into business logic
- **Empty / boundary values** — empty list, empty string, `0`, negative numbers, `datetime.min` / `datetime.max`, single-element collections; handle explicitly
- **Off-by-one boundaries** — pagination first/last page, offset equals total count, zero results
- **Invalid / malformed input** — Pydantic validation covers schema, but add domain-level validation for business rules (invalid state transition, value out of business range)
- **Concurrency / race conditions** — duplicate creation, optimistic locking conflict, idempotency key replay; handle with proper error or upsert
- **External adapter failure** — outbound adapter raises or times out; catch at the use case level, map to the correct domain error, never silently swallow
- **State transitions** — already-exists, not-found, already-deleted, illegal transition; raise the correct centralized error from `domain/errors/`

If the feature has domain invariants, enforce them in the entity constructor / validators and raise the matching `domain/errors/` exception when violated.

## Workflow

1. **Pre-flight**: read the repo `AGENTS.md` for existing conventions and tooling.
2. **Scaffold structure** → `references/project-structure.md` — create the directory tree.
3. **Bootstrap app** → `references/main-config-dependencies.md` — `main.py`, `config.py`, `dependencies.py`.
4. **Wire routes/DTOs** → `references/routes-requests-responses.md` — `routes/`, `requests/`, `responses/`.
5. **Implement use cases** → `references/use-cases.md` — THIN application logic (one use case per file, business rules in `domain/services/`, reuse existing capabilities) + inbound ports.
6. **Define entities** → `references/entities.md` — `domain/entities/` Pydantic models.
7. **Centralize errors** → `references/errors.md` — error codes, messages, custom exceptions.
8. **Centralize logging** → `references/logging.md` — log message enums; run the 7-point call checklist on EVERY log call you write. A log call not referencing a `domain/logging/` enum member is a defect, not a style choice.
9. **Define ports** → `references/ports.md` — `domain/ports/inbound/` + `domain/ports/outbound/` ABCs.

## References

- `references/project-structure.md` — Directory tree and folder responsibilities.
- `references/main-config-dependencies.md` — `main.py`, `config.py`, `dependencies.py` templates (lifespan, settings, DI).
- `references/routes-requests-responses.md` — `routes/`, `requests/`, `responses/` templates (routers + DTOs).
- `references/use-cases.md` — `use_cases/` template (application logic + inbound port usage).
- `references/entities.md` — `domain/entities/` Pydantic entity templates.
- `references/errors.md` — Error codes, `ErrorMessage` enum, custom exceptions.
- `references/logging.md` — Log message `StrEnum` templates.
- `references/ports.md` — `domain/ports/` ABC interfaces (inbound/outbound).