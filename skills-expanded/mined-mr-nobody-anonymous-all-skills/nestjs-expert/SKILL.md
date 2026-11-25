---
name: nestjs-expert
description: "Structure NestJS services: modules and providers, dependency injection scopes, guards and interceptors, validation pipes and testing with a real DI graph."
type: procedural
category: development
domain: development
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - nestjs module structure
  - nestjs guard interceptor
  - nestjs dependency injection scope
  - nestjs validation pipe
  - nestjs testing module
aliases:
  - nestjs
keywords:
  - nestjs
  - decorators
  - guards
  - interceptors
  - dto
  - typeorm
  - prisma
mcp_servers:
  - filesystem
  - postgres
  - context7
source: custom
enabled: true
---

# NestJS Services

## Purpose

Structure NestJS services: modules and providers, dependency injection scopes, guards and interceptors, validation pipes and testing with a real DI graph.

## When to Use

- A NestJS codebase has grown into circular modules and implicit dependencies.
- Cross-cutting concerns are copy-pasted instead of handled by guards or interceptors.
- Tests need the real DI graph rather than hand-built mocks.

## When NOT to Use

- The service is Express or Fastify without Nest.
- A tiny function service does not justify a framework's structure.
- The issue is purely database-level performance.

## Capabilities

- Draw module boundaries and export only what consumers need.
- Use request-scoped providers only where state demands it.
- Implement auth, validation and logging as guards, pipes and interceptors.
- Configure global exception filters with a stable error contract.
- Test modules with `Test.createTestingModule` and override providers deliberately.

## Inputs

- The domain boundaries and which module owns each entity.
- The auth model: JWT, session or third-party, and where roles are resolved.
- Whether the app runs in a single process or as microservices.

## Workflow

1. Map the domain into modules; each module owns its controller, service and repository.
2. Resolve circular dependencies by extracting a shared module rather than `forwardRef` everywhere.
3. Put validation in DTOs with `class-validator` and a global pipe.
4. Implement authorisation in guards, and keep business rules out of them.
5. Centralise error mapping in an exception filter so clients get one shape.
6. Test each module with its provider graph and override only external I/O.

## Tools

- nestjs
- typescript
- jest
- prisma
- typeorm

## Examples

- `A global `ValidationPipe({whitelist: true})` removes unknown fields instead of silently accepting them.`
- `Default singleton scope plus stateless services avoids the request-scope performance cliff.`

## Safety

- Never trust route parameters for authorisation; resolve ownership server-side.
- Do not expose stack traces or internal error messages to clients in production.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |
| `postgres` | stdio | standard | medium | `POSTGRES_URL` |
| `context7` | stdio | standard | low | `CONTEXT7_API_KEY` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/development/nestjs-expert`). First-party skill, maintained in this repository.

## Notes

- `forwardRef` everywhere is a design smell, not a fix.
- Interceptors must not swallow errors on their way out.
- Pairs with: `database-query-optimization`, `api-security-testing`.
