---
name: backend-admin-database
description: Use whenever designing a database schema, creating tables/migrations, building backend architecture (repositories, services, DI), building an admin panel/CMS, or designing API contracts. Enforces schema-first design so database, API, admin CMS, frontend, and mobile never drift out of sync. Trigger on "create a table," "design the schema," "build the admin panel," "add an API endpoint," or any request touching the data layer.
---

# Backend, admin CMS & database - zero mismatch

Prime rule: the database schema is the contract. If you change a column,
every layer (types, validation, API, admin CMS, frontend, mobile) updates
from it - nothing is hand-maintained in parallel where it can drift.

## 1. Database design

**Base table pattern - every table gets these, no exceptions:**
`id` (UUID, default gen), `created_at`, `updated_at`, `created_by`,
`updated_by` (FK to users, `ON DELETE SET NULL`), `deleted_at` (soft
delete), `is_active`, `metadata` (JSONB, flexible extensibility),
`sort_order`, `version` (optimistic locking).

**Naming conventions (non-negotiable):** tables plural snake_case
(`order_items`) · columns snake_case (`first_name`) · foreign keys
`table_id` (`user_id`) · pivot tables alphabetical singular
(`user_role`) · indexes `idx_table_column` · enums singular PascalCase
(`OrderStatus`).

**Relationships:** one-to-many via FK on the "many" side · many-to-many
via a pivot table · one-to-one via a unique FK · self-referential via
`parent_id`.

**Anti-patterns to reject:** arrays stored as delimited strings in a
column (use a junction table) · JSONB for relational data that needs
querying · nullable FKs with no `ON DELETE` rule · missing unique
constraints on business keys (email, slug, SKU).

**Migrations:** never edited after being applied to staging/prod. Every
migration is reversible (up + down), idempotent (safe to run twice), and
transactional (all-or-nothing). Local dev generates the migration; CI/CD
runs `deploy` against staging/prod - never hand-run against production.

## 2. Backend architecture

Layered, not a pile of controllers talking straight to the ORM:

- **Domain** - business logic, entities, validators (no ORM dependency).
- **Application** - use cases: commands (writes), queries (reads), DTOs.
- **Infrastructure** - repository implementations, cache, storage, email.
- **Interface** - HTTP controllers/middleware, GraphQL resolvers,
  admin-specific endpoints.

Repository pattern: controllers depend on an interface
(`IUserRepository`), never the concrete ORM client directly - this is
what lets you swap Prisma/TypeORM/Drizzle, mock in tests, and enforce
soft-delete/scoping rules in exactly one place instead of scattered
`where: { deleted_at: null }` clauses everywhere. Dependency injection
container wires concrete implementations at startup, not inline `new`
calls buried in business logic.

## 3. Admin CMS architecture

Derive ~80% of the CMS UI from the schema itself: a `Product` model with
typed fields generates a sortable list view, a form with correctly
mapped inputs (text/number/select/datepicker/image upload), a filter
sidebar, and bulk actions - without hand-building each screen.

**Feature matrix to cover:** dashboard (stats, recent activity) · list
view (pagination, sorting, filtering, column visibility, CSV export) ·
form builder mapped from DB types with override hooks · media library
(drag-drop, optimization, CDN URLs) · role-based access (CRUD per
resource, field-level where needed) · audit log (who/what/when,
before/after diff) · soft-delete trash bin with restore · bulk
operations with progress indicator · relationship pickers (searchable
dropdowns, inline creation) · version history with rollback.

**Admin endpoints follow the same REST shape as the public API:**
`GET/POST /api/admin/:resource`, `GET/PATCH/DELETE /:id`, `POST
/:resource/bulk`, `GET /:resource/export`, `GET /:resource/stats`. The
CMS is not a separate app with duplicate logic - it consumes the exact
same generated types and, wherever the data isn't admin-only, the exact
same endpoints as the public frontend.

## 4. API design

**URL structure:** versioned path (`/api/v1/...`), resource-nested where
it's genuinely nested (`/users/:id/orders`), auth/webhooks as their own
top-level namespaces.

**Response envelope - every response follows this shape:**
```
{ success: boolean, data?: T,
  error?: { code, message, field? },
  meta?: { page, limit, total, totalPages },
  requestId: string }
```
Error codes are a standardized enum across the whole API
(`VALIDATION_ERROR`, `NOT_FOUND`, `UNAUTHORIZED`, `RATE_LIMITED`,
`IDEMPOTENCY_KEY_REUSED`, `INSUFFICIENT_INVENTORY`, ...) - never ad hoc
per-endpoint error strings.

**Idempotency on mutations:** `Idempotency-Key` header required on
POST/PATCH/DELETE that cost money or create records. Same key within
24h → cached response, 200. Same key with a different payload → 409.

**Versioning:** URL path versioning, not headers. Maintain the previous
version for a defined window after a breaking release, with deprecation
warnings in response headers and a communicated sunset date.

## 5. The sync strategy - zero mismatch

Pipeline: **database schema → code generator → TypeScript types + Zod
validation schemas → OpenAPI spec → API client SDK (web + mobile)**.
When a developer changes the schema: run the migration, then regenerate
types, Zod schemas, OpenAPI docs, and SDKs in one pass - CI fails if
generated files aren't committed, so every team gets the update on next
pull, not on next manual sync.

**What this actually prevents:** a column existing in the DB but not the
API (TypeScript compilation fails on strict DTOs) · an API returning a
field the DB doesn't have (ORM type error) · the CMS showing a field the
API doesn't expose (shared types enforce it) · the frontend expecting a
field the API never sends (generated SDK has the real shape) · mobile
running against a stale schema (SDK regenerates from the OpenAPI spec).

## 6. Common features - reference architecture

- **Auth/RBAC:** `User` ↔ `Role` ↔ `Permission` tables (`resource` +
  `action` pairs), permission middleware checked before the controller
  body runs, never inside it.
- **File uploads:** client requests a signed URL, uploads directly to
  object storage (no server bandwidth spent), server validates the file
  reference exists before storing it. Image optimization on upload,
  virus scanning if risk warrants it, type validated by magic bytes not
  extension.
- **Notifications:** one unified `Notification` table (type, channel,
  status, data payload) with a worker queue (Redis/BullMQ) fanning out
  to email/push/SMS/in-app - never bespoke send logic scattered per
  feature.
- **Search & filtering:** one standardized list-query shape
  (`page`, `limit`, `sort`, `search`, `filters`) applied to every list
  endpoint, not a bespoke query interface per resource.
- **Audit logging:** automatic via ORM middleware/extension on
  create/update/delete - captures table, action, record ID, before/after
  diff, user, IP, user agent - never a manual `logAudit()` call someone
  forgets to add.

## 7. Production checklist

**Security:** inputs validated client + server · SQL injection
impossible (parameterized only) · XSS prevented (encoding + CSP) · CSRF
tokens on state changes · rate limiting per endpoint · CORS to exact
origins · security headers set · secrets in env vars only · DB encrypted
at rest · keys rotated on a schedule.

**Performance:** connection pooling · caching with a real TTL strategy ·
N+1 eliminated · pagination on every list endpoint · image CDN with
format conversion · compression · indexes on FKs and search fields.

**Reliability:** health/ready endpoints · graceful shutdown · structured
logging with correlation IDs · error tracking · point-in-time backup
recovery · circuit breakers · retry with backoff.

**Deploy:** containerized services · CI/CD gate (lint → test → build →
deploy) · staging mirrors production · migrations run before code
deploys, never after · feature flags for risky changes · automated API
contract tests · load testing before major releases.

## 8. The "no mismatch" commandments

1. Schema is law - never hand-write a DTO that could drift from it.
2. One API spec, generated from code, not written separately.
3. Admin is not special - same endpoints and types as the public
   frontend, no duplicate logic.
4. Soft deletes everywhere - never `DELETE FROM`, always
   `UPDATE deleted_at`; admin sees trashed items, public API hides them.
5. Validation at the edge - Zod schemas derived from DB types validate
   at the API boundary; business rules validate in the domain layer.
6. Events, not callbacks - side effects (notifications, analytics)
   listen to emitted events, they don't live inline in the controller.
7. Idempotency by default on anything that costs money or creates a
   record (see the defensive-coding skill).
8. Audit everything a human or admin changes: who, when, what.
