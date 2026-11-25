---
name: fastapi-expert
description: "Build production FastAPI services: dependency injection, Pydantic v2 models, async database sessions, background tasks and OpenAPI that tells the truth."
type: procedural
category: development
domain: development
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - fastapi dependency injection
  - pydantic v2 validator
  - fastapi async sqlalchemy session
  - fastapi background task
  - fastapi openapi schema
aliases:
  - fastapi
keywords:
  - fastapi
  - pydantic
  - async
  - dependency-injection
  - openapi
  - uvicorn
mcp_servers:
  - filesystem
  - postgres
  - context7
source: custom
enabled: true
---

# FastAPI Services

## Purpose

Build production FastAPI services: dependency injection, Pydantic v2 models, async database sessions, background tasks and OpenAPI that tells the truth.

## When to Use

- A Python HTTP service needs typed request/response models and real validation.
- Async endpoints are blocking the event loop under load.
- The generated OpenAPI document disagrees with actual behaviour.

## When NOT to Use

- The service is sync Flask/Django and staying that way.
- A background worker is really needed rather than a request-scoped task.
- The task is a data pipeline with no HTTP surface.

## Capabilities

- Model requests and responses with Pydantic v2 and explicit validators.
- Inject sessions, settings and auth through `Depends` with clean lifetimes.
- Keep the event loop unblocked; offload CPU work to a thread or worker.
- Return accurate status codes and error shapes via exception handlers.
- Document every endpoint so the OpenAPI schema is trustworthy.

## Inputs

- The API contract: routes, payloads, status codes and error format.
- Async or sync stack, and the database driver in use.
- Deployment model: single process, workers, serverless.

## Workflow

1. Define Pydantic models first, including constrained fields and examples.
2. Wire dependencies for settings, DB session and auth; keep them overridable in tests.
3. Make I/O async end to end; audit for blocking calls inside `async def`.
4. Add exception handlers that map domain errors to consistent HTTP responses.
5. Generate the OpenAPI document and diff it in CI to catch accidental breaking changes.
6. Load-test the critical path with realistic concurrency, not one request at a time.

## Tools

- fastapi
- pydantic
- uvicorn
- httpx
- pytest

## Examples

- `A blocking `requests.get` inside `async def` stalls every concurrent request; `httpx.AsyncClient` fixes it.`
- ``response_model` strips fields you did not intend to expose, including secrets.`

## Safety

- Never log request bodies wholesale; they carry credentials and PII.
- Validate file uploads by content, not by extension.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |
| `context7` | stdio | standard | low | `CONTEXT7_API_KEY` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/development/fastapi-expert`). First-party skill, maintained in this repository.

## Notes

- TestClient exercises the app synchronously; use `httpx.AsyncClient` for real async paths.
- Keep settings in one typed object; scattered `os.getenv` calls drift.
- Pairs with: `database-query-optimization`, `api-security-testing`.
