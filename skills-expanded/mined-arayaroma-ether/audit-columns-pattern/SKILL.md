---
name: audit-columns-pattern
description: Use when creating a new table/model in any schema (Prisma, SQL, ORM) or reviewing an existing one for missing audit metadata. Checks/applies the standard createdAt/updatedAt/createdBy/updatedBy/deletedAt pattern, and tells apart mutable domain rows (need it) from immutable event/log rows (don't). Triggers on "audit columns", "falta updatedAt", "quién modificó esto", "soft delete", "revisa el schema por columnas de auditoría".
allowed-tools: Read, Edit, Grep, Glob
---

# Audit Columns Pattern

Row-level audit metadata answers three questions any mutable table should
be able to answer without a separate audit-log table: when was this
created, when was it last touched, and by whom (both). This is distinct
from a request-level audit trail (e.g. this project's own
`AuditLogEntry` — who/what/when/how per HTTP request); the two are
complementary, not substitutes for each other. A row-level `updatedBy`
tells you who owns the current state of a record; a request-log tells you
the history of every request that touched it. Small apps often build the
request-log and skip the row-level columns, then can't answer "who set
this field" without replaying the whole log.

## The standard column set

For any **mutable domain row** (a record users create and later edit or
delete through the app):

| Column | Type | Nullable | Notes |
|---|---|---|---|
| `createdAt` | `DateTime` | no | Set once, `@default(now())` in Prisma. Never mutated. |
| `updatedAt` | `DateTime` | no | `@updatedAt` in Prisma — auto-touched on every write. |
| `createdBy` | actor FK (e.g. `userId`) | **yes** | Null allowed for system/seed/import-created rows. |
| `updatedBy` | actor FK | **yes** | Last human/service that mutated the row. Null = never edited since creation, or system-touched. |
| `deletedAt` | `DateTime?` | yes | Only add where soft-delete is an actual product requirement — see below. |

Don't add all five reflexively. Decide per table:

## What NOT to add it to

**Immutable event/log rows** — a row that is written once and never
updated or deleted by design (an audit-log entry, a webhook-received
event, a sent-email record, a parsed-receipt snapshot before user
confirmation). These get `createdAt` only. Adding `updatedAt`/`updatedBy`
to a table that's never updated is a lie the schema tells about itself —
it invites a future write path that shouldn't exist. This project's own
`AuditLogEntry` is the canonical example: `createdAt` only, explicitly
commented as "must survive a User being deleted — historical record, not
live application state."

**`deletedAt` (soft delete)** — only add where the product actually needs
"recoverable delete" or "hide but keep for reporting/reconciliation"
(e.g. a financial transaction that was voided but must stay in historical
reports). If deletion is just "gone", a hard delete + relying on
`createdBy`/`updatedBy` history elsewhere is simpler and avoids every
query in the codebase needing a `WHERE deletedAt IS NULL` filter forever.
Don't cargo-cult soft-delete onto every table "just in case."

## Auditing an existing schema

1. List every model/table. For each, classify: mutable domain row, or
   immutable event/log row.
2. For mutable rows, check for `updatedAt` first (cheapest, highest-value
   gap — usually missing more often than `createdAt`). Then check for
   `createdBy`/`updatedBy` — most schemas have an owner FK (`userId`) but
   conflate "who owns this row" with "who last touched it," which breaks
   the moment more than one actor can edit the same row (an admin editing
   another user's data, a shared/family record).
3. Report gaps as a table: model name, has createdAt, has updatedAt, has
   createdBy/updatedBy, immutable-by-design (skip) y/n.
4. Don't propose the migration unprompted — present the gap list and let
   the user decide scope (all at once vs. only tables about to change
   anyway) and whether `createdBy`/`updatedBy` should be nullable actor
   FKs or something lighter (e.g. just `updatedBy` as a plain string if
   there's no real actor table).

## Prisma-specific notes

- `updatedAt DateTime @updatedAt` is free — Prisma sets it on every write,
  no application code needed.
- `createdBy`/`updatedBy` need explicit `userId`/`actorId` passed by the
  service on every write — Prisma has no equivalent auto-fill. If the
  project already threads a request-scoped actor (e.g. via a Nest
  interceptor/CLS), wire audit columns through that instead of passing
  the actor down every service method by hand.
- A **shared base doesn't exist in Prisma** (no mixins/traits in the
  schema DSL) — the column block gets repeated per model. Keep the exact
  same field order/names across models so a schema-wide grep/diff stays
  meaningful.
