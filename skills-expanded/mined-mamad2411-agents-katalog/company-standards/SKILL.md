---
name: company-standards
description: >
  Enforce the Going2 company development standards when writing, reviewing, or generating code.
  Use this skill whenever the user asks to create a new module, entity, service, controller, component,
  hook, page, form, test, or any piece of code in a NestJS backend or Next.js frontend project.
  Also trigger when the user asks to scaffold a feature, refactor existing code to match standards,
  or when they reference the project boilerplate. Even if the user doesn't explicitly say "follow
  standards", apply this skill whenever you're writing code in this codebase — consistency matters
  across the whole team.
---

# Going2 Company Development Standards

You are working inside the Going2 company codebase. All code you produce **must follow these
standards**. When in doubt, prefer the patterns described here over general best practices.

## Quick Reference

| Area | Standard |
|---|---|
| Backend | NestJS 11+ / TypeScript 5+ / TypeORM / PostgreSQL |
| Frontend | Next.js 16+ App Router / TypeScript 5+ / shadcn/ui / Tailwind 4+ |
| Forms | React Hook Form + Zod |
| State | TanStack Query (React Query) |
| Auth | JWT + Passport (backend) / NextAuth.js (frontend) |
| Tests (FE) | Vitest + React Testing Library + Cypress E2E |

Read the full standards in `references/standards.md` before producing any code.

## How to apply this skill

1. **Identify the layer** — backend (NestJS) or frontend (Next.js)?
2. **Load the relevant section** from `references/standards.md` for the artifact type requested
   (entity, DTO, controller, service, component, hook, page, form, test…).
3. **Generate code** that follows naming conventions, folder structure, and patterns exactly.
4. **Do not add** comments explaining what the code does — only add a comment when the WHY is
   non-obvious (a hidden constraint, a workaround, a subtle invariant).
5. When creating a new backend module, scaffold all four files: entity, service, controller, module.
6. When creating a new frontend feature component, scaffold both `index.tsx` and `useComponentName.tsx`.

## Critical rules (never skip these)

- Backend entities **must** extend `EntityBase` from `@/common/entity/entity-base`
- DB column names are `snake_case`; TypeScript property names are `camelCase`
- Never use soft-delete by dropping records — use `deleted_at` from `EntityBase`
- Never use `any` — type everything
- Frontend components **must** separate visual (index.tsx) from logic (useComponentName.tsx)
- Forms always use `React Hook Form` + `Zod` schema validation
- API errors on the backend use NestJS exceptions (`NotFoundException`, `ForbiddenException`, etc.)
- Frontend errors surface via `sonner` toast notifications
- Use `cn()` from `@/lib/utils` for Tailwind class merging
- UI components: always reach for shadcn/ui first

## File naming

| Pattern | Convention |
|---|---|
| Files & folders | `kebab-case` |
| React components (export) | `PascalCase` |
| Custom hooks | `use[NomePascalCase].tsx` |
| Classes & interfaces | `PascalCase` |
| Variables & functions | `camelCase` |
| Constants | `SCREAMING_SNAKE_CASE` |
| Enum names & values | `PascalCase` |
| DB table names | `snake_case` |
