---
name: supabase-migration-writer
description: Write production-grade Postgres migrations for Supabase — RLS enabled by default, auth.uid() = user_id policies, indexes on every foreign key, comments, timestamped files. Use when the user says "add a table", "write a migration", "schema for", "alter the table", or is shaping Supabase/Postgres data. Don't use for testing the API the table serves — use api-endpoint-tester.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Builder Dev, Supabase, Postgres, Migrations, RLS]
    related_skills: [env-secrets-hygiene, api-endpoint-tester, vercel-deploy-check, git-ship-flow]
---

# Supabase Migration Writer

Writes migrations the way a senior DBA would: every table gets row-level security ON before it ever holds data, every foreign key gets an index, every object gets a comment, and every file gets a timestamp so migrations run in order forever. A table without RLS on Supabase is a public table — this skill makes that mistake impossible.

## When to Use

- Creating or altering tables, columns, indexes, or policies on a Supabase project.
- Turning "the app needs to store X" into runnable SQL.
- Auditing an existing table for missing RLS or indexes.
- **Not for:** smoke-testing endpoints that read the table — use `api-endpoint-tester`. Not for committing/PR-ing the file — hand off to `git-ship-flow`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Timestamped filename | `echo "supabase/migrations/$(date -u +%Y%m%d%H%M%S)_add_projects.sql"` |
| New migration (CLI) | `supabase migration new add_projects` |
| Sanity-check SQL syntax | `python3 -c "import sys; s=open(sys.argv[1]).read(); assert s.count('(')==s.count(')'), 'unbalanced parens'; print('ok')" <file>` |
| Apply locally | `supabase db reset` (rebuilds local DB from all migrations) |
| Apply to remote | `supabase db push` (gate behind confirm) |
| Find tables missing RLS | `select tablename from pg_tables where schemaname='public' and rowsecurity=false;` |

## Procedure

1. **Precheck** — `command -v supabase` (optional but preferred; without it, deliver the SQL file and apply via the Supabase dashboard SQL editor). Confirm the target: local dev or remote project, and which schema (default `public`).
2. **Model** — pin down: table name (snake_case, plural), columns + types, which column ties a row to its owner (`user_id uuid` referencing `auth.users` in the standard case), and whether rows are per-user private, team-shared, or public-read.
3. **Write the file** — timestamped name (table above), then SQL in this exact order: table → comment → indexes → `enable row level security` → policies → `comment on policy`. Skeleton:

```sql
-- 20260724093000_add_projects.sql
create table public.projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  name text not null check (char_length(name) between 1 and 120),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
comment on table public.projects is 'One row per user-created project.';

create index projects_user_id_idx on public.projects (user_id);

alter table public.projects enable row level security;

create policy "owners select own rows" on public.projects
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "owners insert own rows" on public.projects
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "owners update own rows" on public.projects
  for update to authenticated using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);
create policy "owners delete own rows" on public.projects
  for delete to authenticated using ((select auth.uid()) = user_id);
```

Rules baked in: `(select auth.uid())` (initplan form — evaluated once per query, not per row); one policy per verb, never `for all`; `to authenticated` unless anonymous access is a stated requirement; index every FK and every column policies filter on; destructive DDL (`drop`, `alter ... drop column`) goes in its own migration with a header comment naming what data it loses.
4. **Lint pass** — reread against the checklist: RLS enabled? all four verbs covered (or the omission is intentional and commented)? `with check` present on insert/update? timestamps `timestamptz`? FK has `on delete` behavior chosen deliberately?
5. **Apply locally** — `supabase db reset`; success is a clean run with no errors and the table visible via `psql`/Studio. Prove the policy works: as user A insert a row, as user B select — expect zero rows.
6. **Confirm before remote push** — `supabase db push` changes a live database. Show the user the file list and what each does; on destructive changes, restate what's dropped and require an explicit yes plus a fresh backup/branch. Never push destructive DDL to prod as the first application.

## Output Template

```
## Migration Ready
File: supabase/migrations/20260724093000_add_projects.sql
Creates: public.projects (RLS ✅, policies: select/insert/update/delete for owners)
Indexes: projects_user_id_idx
Destructive: none | ⚠️ drops <thing> — data lost: <what>
Applied: local ✅ (db reset clean) | remote: awaiting your confirm
Policy proof: user B cannot read user A's rows ✅
```

## Pitfalls

- **Table created, RLS forgotten** — on Supabase that table is readable/writable by anyone with the anon key. Recovery: run the rowsecurity query from Quick Reference now; for any hit, ship an immediate migration enabling RLS + policies, then check logs for unexpected access.
- **Policy uses bare `auth.uid()` in a hot path** — works, but re-evaluates per row and tanks big queries. Recovery: rewrite as `(select auth.uid()) = user_id`; same semantics, one evaluation.
- **`for all` policy hides a missing `with check`** — users can hand rows to other users on update. Recovery: split into per-verb policies; every insert/update policy gets an explicit `with check`.
- **Editing an already-applied migration file** — local and remote histories now disagree and `db push` misbehaves. Recovery: never edit applied files; write a new migration that alters forward.
- **Unindexed FK** — deletes on the parent table and policy filters go slow at scale. Recovery: `create index concurrently` on the FK column (run outside a transaction).

## Verification

- [ ] Filename starts with a UTC timestamp and describes the change
- [ ] `alter table ... enable row level security` present for every new table
- [ ] Every policy verb intentional; insert/update have `with check`
- [ ] Every FK and policy-filter column indexed
- [ ] `supabase db reset` runs clean locally; cross-user read test returns zero rows
- [ ] No remote push happened without explicit user confirmation
