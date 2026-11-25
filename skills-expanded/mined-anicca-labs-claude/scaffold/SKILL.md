---
name: scaffold
description: Scaffold a full CRUD feature (types, queries/hooks, pages, form) from a database table. Use when creating a new feature end-to-end from a database table.
argument-hint: "<table_name>"
---

Scaffold a complete CRUD feature for the table `$ARGUMENTS` using the project's database MCP server.

## Steps

1. **Understand existing structure** — read `CLAUDE.md` and one existing feature folder (`src/features/<any>/`) so the new feature mirrors the shapes already in the repo; do not invent new patterns

2. **Inspect schema** — call `get_tables` to confirm the table exists and review its columns; flag any ambiguous columns to the user before proceeding. Call `get_rls_policies` for the table — if it has no tenant-scoped policies, stop and tell the user before generating UI on top of an unprotected table

3. **Schema + types** — `src/features/<feature>/<feature>.schema.ts`: a zod schema for create/edit input (omit auto fields: `id`, `created_at`, `updated_at`, and the tenant column, which is set server-side from the caller's membership — never from the form) and the row type from `Database['api']['Tables']['<table>']['Row']`

4. **Query hooks** — `src/features/<feature>/use<Feature>.ts`: `useQuery` list hook + create/update/delete mutations following the `data-fetching` skill exactly (creates: `onSuccess` + `setQueryData`; updates/deletes: optimistic `onMutate` + `onSettled` invalidate); query key includes the tenant id

5. **Pages** — under the dashboard route group:
   - `app/(dashboard)/<feature>/page.tsx` — server component: fetch initial rows, render the list client component with `initialData`
   - `app/(dashboard)/<feature>/[id]/page.tsx` — detail/edit
   - `loading.tsx` alongside the list page; the list component renders empty and error states deliberately

6. **Form** — `<Feature>Form.tsx` per the `form` skill (react-hook-form + zodResolver + `FormField` + Tailwind tokens), used by both create and edit

7. **Type-check** — run `tsc --noEmit` and fix all errors before reporting done

8. **Preview** — run the `preview` skill on the new list route and confirm the page renders

## Rules

- Never duplicate a component that already exists — check `src/components/` first
- Tailwind token conventions from `coding-standards` (no inline styles, no ad-hoc hex, `cn()` for conditionals)
- Every generated query is tenant-scoped — the list select filters by the active `business_id` even though RLS also enforces it (defense in depth, and it keeps the cache per-tenant)
- Consolidate imports per module (no duplicate import lines for the same path)
- If `$ARGUMENTS` is empty, ask the user which table to scaffold before doing anything
