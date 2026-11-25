---
name: nestjs-11-fastify-hardening
description: Reviews and hardens NestJS 11 applications that use FastifyAdapter, including adapter consistency, bootstrap configuration, route behavior, middleware/plugin compatibility, and e2e test alignment. Use only when a project has chosen @nestjs/platform-fastify.
license: MIT
compatibility: "For NestJS 11.x projects using @nestjs/platform-fastify and Fastify v5-compatible behavior."
---

# NestJS 11 Fastify Hardening

This skill applies only when the project uses `@nestjs/platform-fastify`.

## When to Use This Skill

Use this skill when:

- `package.json` includes `@nestjs/platform-fastify`.
- `main.ts` uses `FastifyAdapter`.
- Code uses `NestFastifyApplication`, `FastifyRequest`, or `FastifyReply`.
- A route or middleware broke after moving to NestJS 11.
- The user asks to harden runtime configuration for a Fastify-backed Nest app.

## Do Not Use This Skill When

- The project uses the default Express adapter.
- The user has not chosen Fastify.
- The task is general performance tuning without Fastify-specific context.

## Workflow References

- `workflows/fastify-runtime-review-workflow.md`
- `workflows/fastify-route-consistency-workflow.md`

## Resource References

- `resources/fastify-hardening-checklist.md`
- `resources/fastify-adapter-consistency.md`

## Example References

- `examples/fastify-bootstrap-example.md`

## Guidance

1. Verify the project intentionally uses Fastify.
2. Keep adapter-specific APIs isolated.
3. Replace Express-only assumptions with Fastify-compatible equivalents.
4. Align e2e test bootstrap with production bootstrap.
5. Validate listen host and runtime options for the deployment environment.
6. Test adapter-sensitive routes.
