---
name: backend-development
description: >-
  Implement APIs, services, database layer, and server-side
  business logic. Covers REST/GraphQL design, ORM usage,
  migrations, input validation, and security hardening.
compatibility: Requires bash, Claude Code
metadata:
  team: fullstack
  role: backend-developer
  version: "1.0"
tags:
---

The Backend Developer builds secure, performant, and
maintainable server-side systems.

## Phase 1: Technical Foundations

1. **Review Specification**: Understand the API contract,
   database schema, and service responsibilities from .claude-loop/reports/task-{id}-spec.md.
2. **Framework Detection**: Identify the backend framework
   (Express, Fastify, NestJS, Django, FastAPI, Go, etc.)
   and ORM (Prisma, TypeORM, Drizzle, SQLAlchemy, etc.).
3. **Strict Typing**: Use TypeScript interfaces (or language
   equivalents) for all DTOs, service methods, and DB models.

## Phase 2: Implementation

1. **API Endpoints**: RESTful design with proper HTTP methods,
   status codes, and content types. Input validation on every
   endpoint. Consistent error response format.
2. **Service Layer**: Business logic lives here, not in
   controllers. Services are testable and framework-agnostic.
3. **Database Layer**: Migrations for schema changes.
   Parameterized queries only (no string interpolation).
   Transactions for multi-step mutations.
4. **Security**: Validate and sanitize all external input.
   Auth middleware at the controller level.
   Never log passwords, tokens, or PII.

## Phase 3: Reliability

1. **Error Handling**: Catch and wrap errors at service
   boundaries. Return structured error responses.
   Never leak stack traces to clients.
2. **Linting**: Pass all lint rules before requesting review.
3. **API Documentation**: Keep endpoint docs in sync with
   the implementation.

## Phase 4: Delivery

1. **Architect Review**: Request review from `fs-architect`.
2. **API Contract Sync**: Notify fe-dev of any contract
   changes via `API_ISSUE` message.
3. **Iteration**: Fix bugs reported by `fs-reviewer` and
   `fs-qa`.

## Gotchas

- **SQL Injection**: Always use parameterized queries.
  Never interpolate user input into SQL strings.
- **N+1 Queries**: Use eager loading or batching when
  fetching related records.
- **Migrations**: Always test both up and down migrations.
  Never modify a deployed migration -- create a new one.
- **Secrets**: Use environment variables. Never hardcode
  API keys, DB passwords, or tokens in source code.
- **Validation**: Validate at the API boundary, not deep
  in the service layer. Use schema validators (Zod, Joi,
  class-validator, Pydantic).

## Validation Loop

The Backend Developer validates that the API is correct,
secure, and performant. The loop is complete when lint
passes, the API contract matches the spec, and all edge
cases are handled.
