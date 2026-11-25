---
name: fastapi-scaffolder
audience: team
description: >
  Scaffolds FastAPI endpoints with OpenAPI documentation, Pydantic v2 request/response models,
  JWT authentication, rate limiting, and health checks. Python analog of minimal-api-scaffolder.
  Use when creating REST APIs, adding endpoints, setting up FastAPI projects, or configuring API
  infrastructure.
---

# FastAPI Scaffolder

> "An API is a contract — make it explicit, versioned, and documented. Security by default means the
> insecure path requires more work than the secure path."

## Core Philosophy

FastAPI has OpenAPI documentation built in — but built-in is not automatic. Every endpoint needs
explicit metadata (`summary`, `description`, `response_model`, `responses`) to produce docs useful to
consumers; an endpoint without metadata is a black box. Security by default means every router
requires authentication unless an endpoint explicitly, intentionally opts out — an unauthenticated
endpoint is a deliberate decision, not an oversight.

**Non-Negotiable Constraints:**
1. OPENAPI-FIRST — every endpoint has `summary`, `description`, `response_model`, and a `responses` dict.
2. VERSIONING FROM DAY ONE — `/api/v1/` prefix via `APIRouter(prefix="/api/v1")`; changing it later is breaking.
3. SECURITY BY DEFAULT — `Depends(get_current_user)` at router level; anonymous access is an explicit opt-out.
4. PYDANTIC V2 MODELS — all request/response types are `BaseModel` subclasses; no bare `dict`/`Any` returns.
5. TYPED RESPONSES — explicit `response_model=` on every route; no implicit response inference.

Full principle table, KB lookups, discipline rules, anti-patterns, and error recovery live in
`references/conventions.md`.

## Workflow

```
DETECT     Find the app entry point (main.py/app.py); check existing versioning, auth
           (get_current_user/OAuth2/HTTPBearer), and middleware (CORS) via grep.

CONFIGURE  Project-level setup: app creation, config (pydantic-settings), shared dependencies,
           exception handlers, CORS, health. (Structure in output-templates.md.)

SCAFFOLD   Create the endpoint with full OpenAPI metadata, Pydantic v2 request/response models, and
           security. (Complete scaffold in references/router-template.md.)

SECURE     Add authentication, authorization (role factories), and rate limiting (stricter on auth
           endpoints). (JWT + API-key patterns in references/security-patterns.md.)

DOCUMENT   uvicorn up; verify /openapi.json and /docs render the new endpoints with metadata.

VERIFY     App starts; /health passes; /docs renders; pytest passes; ruff check; mypy app/.
```

**Exit criteria:** router registered under `/api/v1` with router-level auth; every route has
`response_model`, `summary`, and a `responses` dict; rate limiting applied (strict on auth); health
endpoints present; app starts, `/docs` renders, tests/ruff/mypy pass.

## State Block

```
<fastapi-scaffold-state>
phase: DETECT | CONFIGURE | SCAFFOLD | SECURE | DOCUMENT | VERIFY | COMPLETE
project_structure: new | existing
versioning_configured: true | false
auth_configured: true | false
cors_configured: true | false
rate_limiting_configured: true | false
health_checks_added: true | false
openapi_complete: true | false
last_action: [description]
next_action: [description]
</fastapi-scaffold-state>
```

## Output Template

- **Endpoint scaffold checklist, project structure** — `references/output-templates.md`.
- **Complete endpoint scaffold (router, models, OpenAPI metadata)** — `references/router-template.md`.
- **JWT authentication, API key, role factory, rate limiting patterns** — `references/security-patterns.md`.
- **Principle table, KB lookups, discipline rules, anti-patterns, error recovery** — `references/conventions.md`.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `python-feature-slice` | Feature slice provides the service layer; this skill provides endpoint quality (OpenAPI, security, rate limiting). Use together for complete feature scaffolding. |
| `python-security-review` | After scaffolding, verify authentication, authorization, and input validation. |
| `alembic-migration-manager` | When new endpoints require schema changes, use it for the migration lifecycle. |
| `minimal-api-scaffolder` | Parallel skill for .NET Minimal API — same OpenAPI-first, security-by-default philosophy, different ecosystem. |
