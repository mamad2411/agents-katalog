---
name: schema0-web-crud
description: Web frontend CRUD features — query collections, table columns, dialogs, forms, views, sidebar, and orchestration
---

# Web Feature Development

> **Web only.** Requires `apps/web/` to exist. Skip this entirely if `apps/web/` does not exist.

## Web Stack

- React Router v7 + TanStack DB + TanStack React Table
- oRPC for API (NOT tRPC)
- Drizzle ORM + drizzle-zod for schema
- shadcn/ui components (Dialog, AlertDialog, DataTable, Form)
- react-hook-form + zodResolver for forms
- `import { z } from "zod/v4"` everywhere -- NEVER `import z from "zod"`

## Implementation Order

For every new entity, create files in this exact sequence:

1. Database Schema (`packages/db/src/schema/{entities}.ts`)
2. API Router (`packages/api/src/routers/{entities}.ts`)
3. Query Collection (`apps/web/src/query-collections/custom/{entities}.ts`)
4. Dialog (`apps/web/src/components/ui/data-table/custom/{entities}/{Entities}Dialog.tsx`)
5. Form (`apps/web/src/components/ui/data-table/custom/{entities}/{Entities}Form.tsx`)
6. Table Columns (`apps/web/src/components/ui/data-table/custom/{entities}/{Entities}Column.tsx`)
7. Component Index (`apps/web/src/components/ui/data-table/custom/{entities}/index.ts`)
8. List Route (`apps/web/src/routes/_auth.{entities}.tsx`)
9. Detail Route (`apps/web/src/routes/_auth.{entities}_.$id.tsx`)
10. Sidebar entry (`apps/web/src/components/app-sidebar.tsx`)

## Key Rules

- `queryFn` MUST use `client.{entity}.selectAll({})` directly -- never `fetchCustomResources`.
- `loader` MUST be exported as a named export (React Router v7).
- Delete uses AlertDialog (2-step confirm). NEVER use `window.confirm()`.
- Form `handleSubmit` MUST include the `onInvalid` callback for debugging.
- Edit form schema MUST NOT include `id` -- Dialog adds it after submission.
- Actions column uses `aria-label="Edit"` / `aria-label="Delete"` (used by tests).
- Never perform database operations in loaders -- loaders only call ORPC client methods.

## References

- `references/collections.md` -- Collection pattern, Dialog pattern, Form pattern, index export
- `references/table-columns.md` -- Base columns template, customization examples (date, badge, boolean, price, etc.)
- `references/views.md` -- List Route pattern, Detail Route pattern, sidebar entry, loader requirement
- `references/orchestration.md` -- Execution order diagram, post-creation steps, completion verification
