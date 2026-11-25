---
name: postgres-triggers-and-functions
description: >-
  Use when adding Postgres triggers, database functions (RPC), generated columns,
  or moving invariant logic into the database. Not for edge functions (use
  edge-functions-and-webhooks) or client-only validation.
---

# Postgres triggers and functions

## When to use DB logic

- **Invariants** that must hold regardless of client (e.g. `updated_at`, audit fields).
- **Derived fields** on insert/update.
- **Profile creation** on `auth.users` insert.

Keep business workflows that call external APIs in **edge functions**, not triggers.

## `updated_at` trigger

```sql
create or replace function public.set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger posts_set_updated_at
  before update on public.posts
  for each row execute function public.set_updated_at();
```

## Auth signup hook (profile row)

Triggers on `auth.users` require sufficient privileges. Run via the Supabase SQL editor (which runs as `postgres`) or a migration applied with the management CLI — not from a user-scoped session.

```sql
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, email, display_name)
  values (new.id, new.email, coalesce(new.raw_user_meta_data->>'full_name', ''))
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
```

`on conflict do nothing` keeps the trigger safe if the profile is also created elsewhere (e.g. first sign-in upsert as a fallback).

## RPC (`supabase.rpc`)

Expose safe, parameterized functions:

```sql
create or replace function public.transfer_credits(
  p_to_user uuid,
  p_amount int
) returns void language plpgsql security definer as $$
-- validate caller, deduct/add with checks
$$;
```

- Mark `security definer` only when needed; set `search_path = public`.
- Grant `execute` to `authenticated` selectively.
- Validate `auth.uid()` inside function for user-scoped actions.

## Avoid

- Triggers calling HTTP (use edge + queue).
- `security definer` without access checks.
- Duplicating RLS rules in triggers instead of policies.

## Checklist

- [ ] Trigger tested on insert/update/delete paths
- [ ] RPC documented; typed in generated types if exposed
- [ ] Migrations reversible or follow `migration-playbook`
