---
name: prisma-schema-conventions
description: Data modeling conventions for Prisma + PostgreSQL in multi-tenant systems — workspace isolation, numeric criticality, idempotent recurrence, document versioning by lineage and decoupled audit via a queue in Postgres itself. Use whenever creating or changing schema.prisma, designing new entities, planning migrations or discussing data modeling in any project on this stack.
---

# Prisma schema conventions

Modeling decisions locked in by production experience. They apply to every new entity unless an explicit, recorded decision says otherwise.

## 1. Multi-tenancy: `workspaceId` on every entity

Every business entity carries a `workspaceId` (row-level isolation, single database). Isolation is enforced at the data layer — every query filters by workspace — and the id always comes from the authenticated context, never from client input.

```prisma
model Task {
  id          String   @id @default(uuid())
  workspaceId String
  workspace   Workspace @relation(fields: [workspaceId], references: [id])
  // ...
  @@index([workspaceId])
}
```

**Watch out**: confirm early with the architect whether the project is actually multi-tenant. A mismatch between the data model document (single-tenant) and the commercial document (multi-tenant) is a classic error — resolve it BEFORE the first production migration, not after.

## 2. Criticality / priority: numeric scale, never boolean

`criticality Int` (e.g. 1–5). A boolean ("critical yes/no") doesn't survive the first meeting where the client asks for "medium priority". If the model document shows boolean on one entity and integer on another, treat it as an inconsistency to resolve — model as `Int` and flag it.

## 3. Idempotent recurrence

Recurring tasks/events are generated from a template, with a **composite unique key (templateId + target date)**:

```prisma
model Task {
  // ...
  templateId String?
  targetDate DateTime?
  @@unique([templateId, targetDate])
}
```

The recurrence generator can run any number of times (duplicated cron, retry, reprocessing) without creating duplicates. Idempotency by design, not by application logic.

## 4. Documents versioned by lineage

Never overwrite a file. Each version is a new row, grouped by a lineage id:

```prisma
model Document {
  id        String  @id @default(uuid())
  lineageId String              // groups all versions of the "same" document
  version   Int
  active    Boolean @default(true) // only one active version per lineage
  // ...
  @@unique([lineageId, version])
}
```

## 5. Decoupled audit (queue in Postgres itself)

Auditing must not slow down the main operation nor take it down if it fails. The pattern: the business transaction writes an event to a queue table (`AuditQueue`); a separate worker consumes the queue and materializes the audit record. **No Redis, no external queue** — Postgres handles it until proven otherwise (the justified-complexity rule).

## 6. Dates in UTC, always

Database in UTC, timezone conversion only at the edge (presentation). Prisma's `DateTime` is UTC-friendly; the sin is application code creating dates in local time.

## 7. Soft delete by default

`deletedAt DateTime?` on business entities. Hard delete only with a recorded decision (e.g. data-protection requirements such as LGPD/GDPR for personal data).

## Before any production migration

Mandatory checklist:

- [ ] Schema checked against the data model document (source of truth)
- [ ] Divergences between documents resolved with the architect and recorded
- [ ] Multi-tenancy confirmed (item 1)
- [ ] Ambiguous field types confirmed (item 2)
- [ ] Migration reviewed (descriptive name, no accumulated `migrate dev` garbage)
