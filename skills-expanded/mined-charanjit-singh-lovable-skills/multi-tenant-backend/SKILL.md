---
name: multi-tenant-backend
description: >-
  Use when building organization/workspace multi-tenancy: teams, memberships,
  roles, inviting members, or scoping all data by org_id. Not for single-user
  apps with only user_id ownership.
---

# Multi-tenant backend

## Core tables

```sql
create table public.organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text unique,
  created_at timestamptz default now()
);

create table public.memberships (
  organization_id uuid references public.organizations(id) on delete cascade,
  user_id uuid references auth.users(id) on delete cascade,
  role text not null check (role in ('owner','admin','member')),
  primary key (organization_id, user_id)
);
```

All tenant data includes `organization_id uuid not null references public.organizations(id)`.

## RLS pattern

**Avoid recursion**: if `memberships` itself has RLS that references `memberships`, policies can recurse. Use a `security definer` helper that bypasses RLS for the lookup:

```sql
create or replace function public.is_org_member(p_org uuid)
returns boolean
language sql security definer set search_path = public stable as $$
  select exists (
    select 1 from public.memberships
    where organization_id = p_org and user_id = auth.uid()
  );
$$;

create or replace function public.has_org_role(p_org uuid, p_roles text[])
returns boolean
language sql security definer set search_path = public stable as $$
  select exists (
    select 1 from public.memberships
    where organization_id = p_org
      and user_id = auth.uid()
      and role = any(p_roles)
  );
$$;

revoke all on function public.is_org_member(uuid) from public;
revoke all on function public.has_org_role(uuid, text[]) from public;
grant execute on function public.is_org_member(uuid) to authenticated;
grant execute on function public.has_org_role(uuid, text[]) to authenticated;
```

Then policies are simple and recursion-safe:

```sql
create policy "members_select_org_projects" on public.projects
  for select using (public.is_org_member(organization_id));

create policy "admins_update_projects" on public.projects
  for update using (public.has_org_role(organization_id, array['owner','admin']));
```

On `memberships` itself, scope policies to **the caller's own row** to avoid recursion:

```sql
create policy "members_select_own_membership" on public.memberships
  for select using (user_id = auth.uid());
```

## Invites

`invites(email, organization_id, role, token_hash, expires_at)` — accept via edge function:

1. Validate token, not expired.
2. Ensure signed-in user email matches (or allow any authenticated accept per product rule).
3. Insert `memberships`; delete invite.

Never expose invite tokens in logs.

## Active org context

Client stores `active_organization_id` (profile or localStorage); every query filters by it. Server still enforces RLS — client filter is UX only.

## Avoid

- Tenant id only in React state without RLS.
- Shared `organization_id` in URLs without membership check.
- `owner` role without transfer-ownership flow.

## Checklist

- [ ] Every tenant table has `organization_id` + index
- [ ] RLS on all tenant tables
- [ ] Invite accept is server-mediated
- [ ] Test user A cannot read org B (`supabase-rls-and-auth`)
