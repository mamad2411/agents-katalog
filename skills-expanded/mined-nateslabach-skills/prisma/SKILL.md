---
name: prisma
description: TypeScript and Prisma ORM best practices for schema design, type-safe queries, migrations, and error handling. Use when writing Prisma schemas, building database access layers, or debugging query performance in TypeScript projects.
---

# prisma

Ensures Prisma code is type-safe, performant, and architecturally clean — covering the non-obvious patterns that trip up even experienced developers.

## Core Principles

- **One PrismaClient per process.** Multiple instances create multiple connection pools and exhaust your database connection limit.
- **Enums vs client imports.** Import from the generated `enums.ts` in client/shared code; import from `client.ts` only in server-side code. Never import `client.ts` in client components.
- **Repository pattern.** Keep data access logic separate from business logic. Create repository modules for complex query sets.
- **Transactions for multi-step writes.** Any operation that modifies more than one record should use `$transaction`.
- **Never modify existing migrations.** Treat migrations as append-only history.

## When to Use

- Writing or reviewing Prisma schema models
- Building or refactoring a database access layer
- Debugging N+1 queries or performance regressions
- Setting up Prisma in a new project (especially Next.js)

## Implementation Guide

### Client Setup (Singleton)

The hot-reload guard is required in Next.js — without it, dev mode creates a new PrismaClient on every file change and exhausts connections:

```ts
// lib/prisma.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== "production")
  globalForPrisma.prisma = prisma;
```

### Enums vs Client Imports

```ts
// ✅ Client component or shared validation code
import { Role, Status } from "@prisma/client/enums";

// ✅ Server-side only (API routes, server components, background jobs)
import { prisma } from "@/lib/prisma";
import type { User } from "@prisma/client";

// ❌ Never in client components
import { PrismaClient } from "@prisma/client";
```

### Schema Design

- Use domain-driven model names. Keep schemas normalized and DRY.
- Declare all relations explicitly with `@relation`.
- Implement soft delete via `deletedAt DateTime?` — never hard-delete records that may be referenced.
- Use Prisma's native type decorators for database-level precision.

### Queries & Performance

- **N+1**: Use nested `include` or `select` instead of looping with separate queries.
- **Pagination**: Use `take` and `skip`; add a `cursor`-based approach for large datasets.
- **Field selection**: Use `select` to fetch only needed fields; avoid over-fetching with blanket `include`.
- **Join strategy**: `relationLoadStrategy` (`"join"` or `"query"`) is available but requires enabling the `relationJoins` preview feature flag. `"join"` uses a single `LATERAL JOIN`; `"query"` sends one query per table and joins at the application level.

### Error Handling

Catch Prisma-specific errors at the repository boundary:

- `PrismaClientKnownRequestError` — structured DB errors. Check `error.code`:
  - `P2002` — unique constraint violation
  - `P2025` — record not found (replaces the removed `NotFoundError` from Prisma 5)
- `PrismaClientUnknownRequestError` — unstructured DB errors
- `PrismaClientValidationError` — invalid query shape (usually a type error)

Provide user-friendly messages upstream; log the full error with context for debugging.

### Migrations

- Use descriptive names: `prisma migrate dev --name add_user_email_index`.
- Review generated SQL before applying to production.
- Never edit existing migration files — create a new migration instead.
- Keep migrations idempotent where possible.

## Review Checklist

- Is there a single PrismaClient instance with the hot-reload guard in place?
- Are enums imported from `enums.ts` in any client or shared code?
- Do multi-record writes use `$transaction`?
- Are N+1 patterns avoided (no DB calls inside loops)?
- Are `PrismaClientKnownRequestError` codes handled at the repository boundary?
- Do migrations have descriptive names and remain unmodified after creation?
