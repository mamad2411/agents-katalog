---
name: python-feature-slice
audience: team
description: >
  Scaffolds feature-based Python architecture using FastAPI routers, Pydantic v2 models, and a
  service layer. Python analog of dotnet-vertical-slice — no mediator library, uses FastAPI
  Depends() for dependency injection and structural CQRS conventions. Use when creating
  feature-based Python projects, adding FastAPI features, scaffolding service layers, or
  organizing Python code by feature.
---

# Python Feature Slice Architecture

> "Organize around business capabilities, not technical layers."
> -- Sam Newman, *Building Microservices*

## Core Philosophy

Feature slice architecture organizes code by business capability, not technical layer: instead of
`controllers/`, `services/`, `repositories/`, you have `features/orders/`, `features/users/` — each a
self-contained vertical slice. In Python with FastAPI, the mediator pattern (FreeMediator in .NET) is
replaced by FastAPI's native `Depends()`; service classes are injected directly into route handlers.
CQRS separation is a structural/naming convention — `OrderReadService` vs `OrderWriteService` — not a
library contract.

**Non-Negotiable Constraints:**
1. FEATURE ISOLATION — no cross-feature imports; features communicate only through `shared/` domain models.
2. SERVICE OWNS LOGIC — routers are thin (extract → call service → return); no business logic in handlers.
3. PYDANTIC V2 EVERYWHERE — all request/response types are Pydantic models with `response_model` set; no bare `dict` returns.
4. PROTOCOL INTERFACES — `typing.Protocol` for service interfaces so tests run without concrete implementations.
5. ASYNC-FIRST — all I/O uses `async def`; no blocking calls in async context (`asyncio.to_thread()` if unavoidable).

Full principle table, KB lookups, discipline rules, anti-patterns, and error recovery live in
`references/conventions.md`.

## Workflow

```
DETECT     Identify existing structure (flat/layered/feature-based), the FastAPI entry point
           (main.py/app.py), the router registration pattern, the ORM setup, and the auth pattern.
           (grep APIRouter/include_router; find main.py/app.py.)

SCAFFOLD   Create the feature package:
             features/<name>/{__init__.py, router.py, service.py, models.py, dependencies.py}
             tests/features/<name>/{test_router.py, test_service.py}
           (File-by-file content in references/feature-folder-template.md; read/write split in cqrs-conventions.md.)

REGISTER   Wire the router: app.include_router(<name>_router, prefix="/api/v1", tags=["<name>"]).

VERIFY     uvicorn starts; /docs renders the endpoints; pytest tests/features/<name>/ passes;
           grep confirms no cross-feature imports.
```

**Exit criteria:** feature package created with thin router, Protocol-typed read/write services,
Pydantic v2 models, and tests; router registered under `/api/v1`; app starts, `/docs` renders, tests
pass, and no cross-feature imports exist.

## State Block

```
<python-feature-slice-state>
phase: DETECT | SCAFFOLD | REGISTER | VERIFY | COMPLETE
feature_name: [name]
existing_structure: flat | layered | feature-based | unknown
app_entry_point: [file path]
router_registered: true | false
tests_scaffolded: true | false
read_service_created: true | false
write_service_created: true | false
last_action: [description]
next_action: [description]
</python-feature-slice-state>
```

## Output Template

- **Scaffold checklist, feature folder structure** — `references/output-templates.md`.
- **File-by-file scaffold content (router, service, models, dependencies, tests)** — `references/feature-folder-template.md`.
- **Read/write service separation conventions** — `references/cqrs-conventions.md`.
- **Principle table, KB lookups, discipline rules, anti-patterns, error recovery** — `references/conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `fastapi-scaffolder` | Endpoint-level scaffolding (OpenAPI metadata, security, rate limiting). Use together for full endpoint quality within a feature. |
| `alembic-migration-manager` | When a feature needs schema changes, use it for the migration lifecycle. |
| `python-security-review` | After scaffolding, verify the feature's authentication, authorization, and input validation. |
| `python-architecture-checklist` | Quality gate — run after several features to verify isolation and coupling metrics. |
