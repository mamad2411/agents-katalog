---
name: supabase-database-design
description: >-
  Use when designing Supabase/Postgres schemas: new tables, relationships, indexes,
  enums, constraints, or normalizing data models. Not for RLS policies only (use
  supabase-rls-and-auth) or client hooks (use typed-api-hooks-forms).
---

# Supabase database design

## Table conventions

- `id uuid primary key default gen_random_uuid()` (or bigint for high-volume internal).
- `created_at timestamptz not null default now()`
- `updated_at timestamptz` — maintain via trigger or app on update.
- Snake_case table/column names; plural table names (`projects`, `comments`).

## Relationships

- Every FK explicit: `project_id uuid not null references public.projects(id) on delete cascade`.
- Choose `on delete`: `cascade` (owned children), `restrict` (prevent orphaning), `set null` (optional link).
- Junction tables for many-to-many: `project_members(project_id, user_id, role)`.

## Indexes

Add indexes for:

- FK columns used in joins/filters (`project_id`, `user_id`).
- Common filters: `where status = ?`, `order by created_at desc`.
- Unique business keys: `slug`, `stripe_customer_id`.

```sql
create index posts_project_id_created_at_idx
  on public.posts (project_id, created_at desc);
```

Avoid over-indexing low-cardinality booleans alone.

## Enums vs lookup tables

- Few fixed values, rare changes → `create type post_status as enum (...)`.
- User-defined or admin-editable labels → `statuses` lookup table.

## Constraints

- `not null` on required fields; `check` for ranges (`amount_cents >= 0`).
- `unique (organization_id, slug)` for scoped uniqueness.

## Money and time

- Money: `bigint` cents (`amount_cents`), not `numeric` or `float`. Currency in a separate column.
- Time: always `timestamptz`, never `timestamp` (timezone-naive). Store UTC; format in UI.

## Types and codegen

After schema changes: `supabase gen types typescript` → app uses `Database` types.

Keep types in source control so reviewers see schema drift in PRs.

## Avoid

- JSON blobs for relational data you query/filter often.
- Missing FKs with “logical” IDs only in app code.
- `user_id` as text instead of `uuid references auth.users`.

## Checklist

- [ ] PK + timestamps on every table
- [ ] FKs + indexes on filter/join columns
- [ ] Migration file named and ordered (`migration-playbook`)
