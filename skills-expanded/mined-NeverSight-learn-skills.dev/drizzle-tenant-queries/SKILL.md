---
name: drizzle-tenant-queries
description: Use this skill when you write or review any Drizzle DB read/write and must enforce strict `workspace_id` tenant isolation.
---

# Drizzle Tenant Query Skill

Use this skill whenever you write or review Drizzle ORM queries. Goal: absolute tenant isolation and correctness for money/time data.

## Golden rules

- **Every query must include workspace_id.** No exceptions.
- Derive `workspaceId` server-side via your tenant/workspace guard (Server Actions / Server Components); never trust client params.
- In Route Handlers, use a guard appropriate for handlers (non-React cached).
- Use UUIDs for public IDs; avoid exposing sequential IDs.
- Money stored as integer cents + currency code. Time stored UTC.

## Query patterns

- `db.query.table.findMany({ where: eq(table.workspaceId, workspaceId), ... })`
- For joins, include workspace filter on primary table and any joined tables that are tenant-scoped.
- For updates/deletes, always include workspace filter in `where` with the entity ID.

Example (list projects with client):

```ts
const rows = await db.query.projects.findMany({
  where: eq(projects.workspaceId, workspaceId),
  with: { client: true },
});
```

Example (update invoice guarded):

```ts
await db
  .update(invoices)
  .set({ status: "draft" })
  .where(
    and(eq(invoices.id, invoiceId), eq(invoices.workspaceId, workspaceId))
  );
```

## Snapshot & invoices

- When finalizing invoices, create snapshot row tied to invoice_id and workspace_id.
- PDFs for finalized invoices must read from snapshot.

## Caching & reuse

- Wrap read helpers in `cache()` when reused within a request.
- Prefer small helpers per entity: `getClientsByWorkspace`, `getProjectsByWorkspace`, `getInvoiceWithItems` (scoped).

Tenant-safe caching rules:

- Request-level `cache()` is safe when the function arguments include `workspaceId`.
- Cross-request caching (e.g., Next.js `next/cache`) must include workspace identity in keys/tags.
- Never use “global” cache keys/tags for tenant-private tables.

See also: nextjs-cost-performance skill

## Query performance patterns (still tenant-safe)

- Avoid N+1 in rendering: batch by IDs with `inArray(...)` or use Drizzle relations (`with`).
- Select only needed columns (reduces serialization and bandwidth).
- Prefer `Promise.all` for independent reads.
- Consider indexes for hot filters (`workspace_id`, foreign keys, timestamps) via migrations.

## Edge cases

- Prevent cross-tenant joins by scoping both sides.
- Avoid nullable money fields; prefer 0 default + currency code.
- Timezone: store UTC; convert at display.

## Testing

- Write isolation tests: querying entity from another workspace should return 0.
- Validate migrations with your migration toolchain (e.g., drizzle-kit).

## References

- Schema: your DB schema module(s)
- Tenant/workspace helper: your server-side tenant guard module
- Product spec: your PRD/spec doc (if present)
