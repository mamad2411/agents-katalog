---
name: verify-nextjs-fullstack
description: "Verification checklist for a full-stack Next.js backend — Drizzle, Auth.js, route handlers, server actions, Redis/BullMQ."
disable-model-invocation: true
---

# Skill: Verify Next.js Full-Stack

## Purpose
Systematic verification checklist for the backend layer of a full-stack Next.js project — Drizzle, Auth.js, Route Handlers, Server Actions, Redis, and BullMQ. Use alongside `verify-nextjs.md` (which covers frontend concerns).

## Verification Process

Run through each section. Flag issues as PASS, WARN, or FAIL.

### 1. Tests
- [ ] Tests exist for new/changed services, route handlers, and server actions
- [ ] `vitest` passes with no failures
- [ ] Service unit tests mock db/redis, not service functions themselves
- [ ] Route handler integration tests cover success and error paths
- [ ] Factory functions produce realistic test data (not "test123" placeholders)

### 2. Database (Drizzle)
- [ ] Migrations are generated and match schema changes (`drizzle-kit generate`)
- [ ] No migration conflicts with main branch
- [ ] New columns have sensible defaults or are nullable where appropriate
- [ ] Indexes exist on fields used in filters/lookups
- [ ] Queries use Drizzle query builder — no raw SQL without justification
- [ ] Relational queries use `with` (not manual joins) where appropriate
- [ ] All queries are scoped (filtered by user/tenant) — no unscoped data access

### 3. Route Handlers (API)
- [ ] Auth checked via `auth()` on protected endpoints
- [ ] Request bodies validated with Zod before processing
- [ ] Response shapes are consistent: `{ page, count, num_pages, results }` for collections, object for singles, `{ error }` for failures
- [ ] Appropriate HTTP status codes (201 for creation, 404 for not found, etc.)
- [ ] No business logic in handlers — delegated to services
- [ ] Pagination configured for list endpoints

### 4. Server Actions
- [ ] `"use server"` directive at top of file
- [ ] Auth checked via `auth()` before mutations
- [ ] Input validated with Zod before processing
- [ ] Return `ActionResult<T>` pattern — not void or raw throws
- [ ] `revalidatePath` / `revalidateTag` called after mutations
- [ ] No `redirect()` inside try/catch blocks
- [ ] No business logic in actions — delegated to services

### 5. Service Layer
- [ ] Business logic lives in `server/services/`, not in handlers or actions
- [ ] Services are plain functions receiving data as arguments
- [ ] Services do not import from `next/headers` or Next.js request APIs
- [ ] Service functions are independently testable

### 6. Auth (Auth.js)
- [ ] Auth.js configuration in `lib/auth.ts`
- [ ] Protected routes check `auth()` — no manual cookie/token parsing
- [ ] Middleware matcher correctly identifies public vs protected routes
- [ ] Session type extensions in `types/next-auth.d.ts` if custom fields added
- [ ] No sensitive user data stored in session (fetch from DB when needed)

### 7. Redis & Queues (if applicable)
- [ ] Redis keys follow naming convention: `{app}:{domain}:{id}`
- [ ] All cache keys have TTL set — no indefinite caching
- [ ] BullMQ job payloads are small and serializable (IDs, not full objects)
- [ ] Workers call services — no business logic in job processors
- [ ] Failed jobs have retry configuration with exponential backoff

### 8. Security
- [ ] No secrets or API keys in client code or committed to git
- [ ] `AUTH_SECRET` is set and not a default value in production
- [ ] Database credentials use environment variables, not hardcoded strings
- [ ] User input is validated (Zod) before database operations
- [ ] SQL injection prevented (using Drizzle query builder, not raw SQL)
- [ ] Rate limiting on sensitive endpoints (login, registration)

### 9. Development Environment
- [ ] `docker-compose.yml` includes all required services (app, db, redis, worker if full)
- [ ] `Makefile` includes database commands (`db-generate`, `db-migrate`, `dbshell`, `dbreset`)
- [ ] No `npm` / `npx` commands used directly on host
- [ ] `.env.local` has all required variables documented
- [ ] Migrations can run cleanly from scratch (`dbreset` + `db-migrate`)

### 10. Code Quality
- [ ] No commented-out code
- [ ] No `console.log` left in (except workers where it's intentional logging)
- [ ] ESLint passes
- [ ] TypeScript compiles cleanly (`tsc --noEmit`)
- [ ] Consistent naming conventions (services, actions, routes)

## Output
Produce a `verification-report.md`:
```markdown
# Verification Report: [Feature/Phase]
Date: [date]
Reviewer: Claude (automated)

## Summary: [PASS/WARN/FAIL]

## Details
### Tests: [PASS/WARN/FAIL]
- [notes]

### Database: [PASS/WARN/FAIL]
- [notes]

### Route Handlers: [PASS/WARN/FAIL]
- [notes]

### Server Actions: [PASS/WARN/FAIL]
- [notes]

### Service Layer: [PASS/WARN/FAIL]
- [notes]

### Auth: [PASS/WARN/FAIL]
- [notes]

### Redis & Queues: [PASS/WARN/FAIL]
- [notes]

### Security: [PASS/WARN/FAIL]
- [notes]

### Dev Environment: [PASS/WARN/FAIL]
- [notes]

### Code Quality: [PASS/WARN/FAIL]
- [notes]

## Issues Found
1. [FAIL] Description + suggested fix
2. [WARN] Description + recommendation

## Recommended Actions
- [ ] Fix: ...
- [ ] Consider: ...
```
