---
name: hono-best-practices
description: >
  Production patterns for Hono v4+ backends with Bun, Drizzle ORM, Better Auth,
  Stoker, hono-openapi + Zod + Scalar, and TDD with Bun test runner.
  Use when building features, writing tests, reviewing code, or setting up
  auth/RBAC in modular monolith Hono projects. Apply whenever you see Hono route
  definitions, createRouter(), describeRoute(), Better Auth config, Stoker imports,
  or Bun test files in this stack. Also use when adding new modules, writing
  OpenAPI specs, or debugging auth middleware issues.
---

# Hono Best Practices (Bun + Drizzle + Better Auth + Stoker + Scalar)

Production patterns for **Hono v4+ / Bun / Drizzle / Better Auth / Stoker / hono-openapi + Scalar**.

## When to Apply

Reference these guidelines when:

- Creating new feature modules (routes, handlers, services, schemas)
- Writing or reviewing Hono route definitions with `describeRoute` + `validator`
- Setting up or modifying Better Auth config (social auth, RBAC, hooks)
- Writing tests with Bun test runner (`bun:test`)
- Using Stoker HTTP status codes and error handlers
- Generating OpenAPI specs or configuring Scalar docs UI
- Deriving Zod schemas from Drizzle tables via `drizzle-zod`

## Architecture: Modular Monolith

```
src/
├── index.ts                # Bun.serve entry + OpenAPI spec endpoints
├── app.ts                  # CORS, error handler, route mounting
├── factory.ts              # createRouter() + AppEnv — SINGLE SOURCE OF TRUTH
├── env.ts                  # t3-env validation
├── auth.ts                 # Better Auth config (social, hooks, RBAC)
├── db/                     # Drizzle client + domain-split schemas
├── lib/                    # Shared kernel (errors, pagination, openapi, upload)
├── middlewares/             # Auth, error handler
├── services/               # Cross-module orchestration
└── modules/                # Feature verticals
    └── [module]/
        ├── [name].schema.ts
        ├── [name].service.ts
        ├── [name].handlers.ts
        ├── [name].routes.ts
        ├── [name].index.ts
        └── __tests__/
```

## Golden Rules

| Rule | Enforcement |
|------|-------------|
| **Factory Rule** | `createRouter()` from `@/factory`, NEVER `new Hono()` |
| **Service Purity** | Services take primitives, NEVER `Context` |
| **Schema Derivation** | `drizzle-zod` -> `.omit()` -> `.extend()`, NEVER hand-write DB types |
| **ISO Dates** | `z.iso.datetime()`, NEVER `z.date()` |
| **OpenAPI Always** | Every route: `describeRoute` + `resolver` + `validator` |
| **Import Direction** | `modules/` -> `lib/`, `db/`, `middlewares/`. NEVER `modules/A -> modules/B` |
| **Named Status Codes** | `stoker/http-status-codes`, NEVER magic numbers |
| **Domain Errors** | Services throw domain errors, handlers map to `AppError` subclasses |

## Anti-Patterns

| Don't | Do |
|-------|-----|
| `new Hono()` | `createRouter()` |
| `Context` in services | Primitives only |
| `z.date()` | `z.iso.datetime()` |
| Magic status numbers | `stoker/http-status-codes` |
| Missing `describeRoute` | Every route documented |
| `modules/A -> modules/B` | Via `.index.ts` or `services/` |
| Manual error JSON | Throw `AppError` subclass |
| `z.object()` for DB types | `createInsertSchema` / `createSelectSchema` |

## Middleware Chain Order

```
describeRoute() -> requireAuth() -> requireRole() -> validator() -> handler
```

## New Feature Checklist

1. **Schema**: Drizzle table -> `db:generate` -> `db:migrate` -> Zod schemas via `drizzle-zod`
2. **Service**: Pure functions + domain errors (TDD: tests first!)
3. **Handlers**: Thin glue, map domain -> HTTP errors
4. **Routes**: `describeRoute` + `validator` + auth middleware
5. **Index**: Export router(s), mount in `app.ts`
6. **Verify**: `bun test` -> `bun fl` -> `bun check` -> `bun openapi:generate`

## Reference Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Architecture & Modules | CRITICAL | `architecture-` |
| 2 | Factory & Types | CRITICAL | `factory-` |
| 3 | Schema (drizzle-zod) | CRITICAL | `schema-` |
| 4 | Service Layer | HIGH | `service-` |
| 5 | Handler Layer | HIGH | `handler-` |
| 6 | Routes & OpenAPI | HIGH | `routes-` |
| 7 | Error Handling (Stoker) | HIGH | `error-` |
| 8 | OpenAPI & Scalar | MEDIUM | `openapi-` |
| 9 | Better Auth | MEDIUM | `auth-` |
| 10 | Pagination | MEDIUM | `pagination-` |
| 11 | Testing (Bun) | MEDIUM | `testing-` |

## How to Use

Read individual reference files for detailed code examples:

```
references/architecture-modular-monolith.md  # Modular monolith + module patterns
references/factory-types.md                  # createRouter() + AppEnv types
references/schema-drizzle-zod.md             # drizzle-zod derivation
references/service-pure-logic.md             # Pure business logic
references/handler-http-glue.md              # Thin HTTP glue
references/routes-hono-openapi.md            # hono-openapi + validation
references/error-stoker-apperror.md          # Stoker + AppError hierarchy
references/openapi-scalar-spec.md            # Spec generation + Scalar UI
references/auth-better-auth.md              # Auth setup, social, RBAC, hooks
references/pagination-helpers.md             # Pagination schemas + helpers
references/testing-bun-tdd.md               # TDD with Bun test runner
references/_sections.md                      # Full index of all references
```

## Import Quick Reference

```typescript
// Factory
import { createRouter, factory, type AppContext, type AppEnv } from "@/factory";
// Database
import { db } from "@/db";
import { achievements } from "@/db/schema/content-schema";
import { eq, and, desc, sql, ilike } from "drizzle-orm";
// Schemas
import "zod-openapi/extend"; // Side-effect: adds .openapi() to Zod (import once at entry)
import { z } from "zod";
import { createInsertSchema, createSelectSchema } from "drizzle-zod";
// OpenAPI
import { describeRoute, resolver, validator } from "hono-openapi";
// Stoker
import * as HttpStatusCodes from "stoker/http-status-codes";
import * as HttpStatusPhrases from "stoker/http-status-phrases";
import notFound from "stoker/middlewares/not-found";
import onError from "stoker/middlewares/on-error";
// Errors
import { NotFoundError, ValidationError, ForbiddenError } from "@/lib/errors";
// Pagination
import { paginationQuerySchema, createPaginatedResponse } from "@/lib/pagination";
// Auth
import { requireAuth, requireRole } from "@/middlewares/auth.middleware";
// Scalar
import { Scalar } from "@scalar/hono-api-reference";
```
