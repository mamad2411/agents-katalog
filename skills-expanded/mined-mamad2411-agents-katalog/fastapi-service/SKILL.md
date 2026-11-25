---
name: fastapi-service
description: Use when writing or modifying Python FastAPI service code in this repository, including routes, DTOs, Pydantic models, async request handling, middleware, dependency extraction, svcs dependency access, error handling, validation, tests, and API performance concerns.
---

# FastAPI Service

Use this skill to keep API and service code aligned with this repo's Python/FastAPI conventions instead of generic internet defaults.

## Project Fit

- Runtime: Python 3.12.
- Web framework: FastAPI.
- Validation and response models: Pydantic v2-style models.
- Dependency management: FastAPI `Depends` for request/route concerns; `svcs` registries and registrars for application/infrastructure dependencies.
- Persistence: Piccolo/PostgreSQL and async database boundaries where applicable.
- Logging/observability: structured logging, request context, middleware, and telemetry hooks.

## FastAPI Boundaries

- Keep HTTP concerns in `llm_agent/llm_agent/api/http/`: route definitions, DTOs, mappers, middleware, status codes, and request context extraction.
- Prefer declarative route definitions with explicit `response_model`, summaries, and useful response metadata for public endpoints.
- Use Pydantic models for input/output validation. Do not pass raw dictionaries across boundaries when a typed model, dataclass, or domain object would clarify intent.
- Use `HTTPException` for expected HTTP-facing failures. Translate domain exceptions at the route boundary.
- Keep route handlers thin: validate/extract request data, call a service, map the result to a DTO.
- Prefer `lifespan` and the existing `svcs.fastapi.lifespan` pattern for startup/shutdown work. Do not add new `@app.on_event` handlers.

## Python Style

- Use `def` for pure synchronous functions and `async def` for I/O-bound operations.
- Type all public function signatures, service methods, route dependencies, DTO mappers, and test helpers.
- Prefer module-level named routers, dependencies, mappers, and utility functions.
- Prefer small, composable functions over duplicated branches.
- Use descriptive snake_case names, especially boolean names with `is_`, `has_`, `can_`, or `should_`.
- Prefer object-in/object-out APIs for complex calls: accept a typed request/config object and return a typed result object.
- Avoid forcing a functional rewrite where existing classes intentionally model service boundaries, registrars, or lifecycle-owned dependencies.

## Error Handling

- Put guard clauses and edge-case handling near the top of functions.
- Avoid deeply nested `if`/`else` blocks when early returns or exception translation make control flow clearer.
- Use domain-specific exceptions for business failures and translate them once at the API boundary.
- Log unexpected failures with useful context, but do not log raw tokens, secrets, or sensitive request bodies.
- Keep client-facing error messages stable and useful without leaking internals.

## Async And Performance

- Do not perform blocking I/O in request handlers or async service methods.
- Use async database and external API calls.
- Avoid unbounded fan-out, unbounded background tasks, or fire-and-forget work without lifecycle ownership.
- For large or frequently accessed responses, consider pagination, lazy loading, caching, or projection/read-model patterns before returning large payloads.
- Preserve observability for latency, throughput, queue depth, worker progress, and failure modes when touching hot paths.

## svcs And Registrar Pattern

- Before changing DI wiring, registrars, FastAPI lifespan setup, or `svcs` route dependencies, read `docs/patterns/svcs_notes.md`.
- Use FastAPI dependencies for request-local extraction, such as path/query/body values, request context, or route-local service assembly.
- Use `svcs.Registry` and registrar classes for reusable application/infrastructure dependencies.
- Keep registrar code mechanical: register factories/values, do not encode business policy.
- Keep lifecycle-owned resources in the lifespan/infrastructure setup path so startup and shutdown are explicit.
- Avoid hidden global singletons when a dependency belongs in `svcs`.

## Testing

- For test design, fixture placement, fakes, async tests, and DI overrides, use the `testing` skill.
- Test routes for validation, status codes, auth behavior, and DTO mapping.
- Test services with fake stores/queues/event logs where possible.
- For async code, cover cancellation, timeout, retry, and duplicate-processing behavior when relevant.
- For worker/run/event flows, assert both event sequence and derived/folded state when useful.

## Avoid

- Business logic embedded in route handlers.
- Returning persistence objects directly from routes.
- Raw dictionaries for stable interfaces.
- Blocking I/O inside `async def`.
- New framework-level dependency systems that bypass the existing FastAPI plus `svcs` composition model.
- Broad exception handlers that hide actionable failures.
