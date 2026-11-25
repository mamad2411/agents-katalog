---
name: nestjs-backend
description: >-
  Optional stack skill: NestJS API (modules, DTOs, validation, Prisma, REST).
  Use when working in the NestJS app path from project-context.
---

# NestJS Backend (optional)

Enable this skill when the project uses NestJS. Paths and package filters come from `.agents/skills/project-context/SKILL.md`.

Also read `.agents/skills/typescript/SKILL.md` and `.agents/skills/clean-code/SKILL.md`.

## Stack (typical)

- NestJS, TypeScript, Prisma, PostgreSQL
- Common location: `apps/api/`
- Package filter example: `@your-scope/api`

## Conventions

1. **Module layout** — One feature per Nest module under `src/modules/<name>/` with `*.module.ts`, `*.controller.ts`, `*.service.ts`, DTOs in `dto/`.
2. **DTOs** — Use `class-validator` + `class-transformer`; validate at controller boundary; never trust client shapes.
3. **Prisma** — Keep queries in services; use transactions for multi-step writes. Align schema with `docs/DATA_MODEL.md`.
4. **Errors** — Use Nest HTTP exceptions with clear messages; log server details, return safe client messages.
5. **Config** — Env via `@nestjs/config`; no secrets in code.
6. **Seed / content** — Prefer docs or DB seed for product content; do not hardcode large content blobs in services.

## API style

- REST JSON under a consistent prefix (e.g. `/api/v1`).
- Document new routes in code comments or OpenAPI when the project uses Swagger.

## Checklist before finishing

- [ ] DTO validation covers required fields and enums
- [ ] Prisma migrations named and reversible where possible
- [ ] No N+1 in list endpoints (use `include`/`select` deliberately)
- [ ] Lint passes for the API package
- [ ] Unit tests for new/changed logic; regression test for bug fixes
- [ ] All tests pass before handoff (see `.agents/skills/developer-quality/SKILL.md`)
