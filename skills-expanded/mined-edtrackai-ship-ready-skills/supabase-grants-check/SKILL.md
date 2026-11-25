---
name: supabase-grants-check
description: Check Supabase migrations for the security side of the 30 Oct 2026 Data API grants change (Supabase's changelog schedules it) - GRANT ALL or write grants to anon, grants on tables with RLS off, policies whose role has no grant (42501), grants with no policy, SECURITY DEFINER functions anon can execute, default privileges that still auto-grant, and the local auto_expose_new_tables setting. Use when the user asks about Supabase grants, a 42501 permission-denied error, the 30 October change, or whether a GRANT fix is safe.
allowed-tools: Read Grep Glob
---

# supabase-grants-check

Review only. Don't edit files unless the user asks for the fixes afterwards.

## Scope
Read every `.sql` file under `supabase/migrations/` in filename order (later files can fix earlier ones), plus `supabase/config.toml` if it exists. Track per table in `public` (and any other schema the user says the Data API exposes) what holds at the end of the history: RLS on or off, the policies (command and roles) and the grants per role (`anon`, `authenticated`). Treat `grant all` as select, insert, update, delete, truncate, references and trigger. Treat `revoke` as removing privileges. Dashboard changes aren't in these files, so say that in the report instead of guessing. If the user can run SQL, point them to the free SQL checker on the live database. It checks the same things, and its C1–C7 ids match G1–G7 here.

## Checks
For each finding, give file:line, the id, severity and the fix.

| Id | Severity | Look for | Fix |
|---|---|---|---|
| G1 | critical | A table where `anon` or `authenticated` has any grant and RLS is never enabled | In one migration: `enable row level security`, add policies, then keep only the minimum grant. |
| G2 | high | `anon` holds insert, update, delete or truncate on a table (including through `grant all ... to anon`) | Revoke the writes from `anon`, for example `revoke insert, update, delete, truncate on public.t from anon;`. Signed-out visitors usually need `select` at most. |
| G3 | medium | `authenticated` holds `truncate` (TRUNCATE ignores RLS) or write grants on a table with RLS off | Revoke `truncate`. Grant only the commands that policies cover. |
| G4 | medium | A policy `for <cmd> to <role>` where that role has no matching grant. After the change the Data API returns 42501 for it. | Add the matching minimum grant, for example `grant select on public.t to authenticated;`. Never grant to `anon` just to silence 42501. Server code using the service-role key through supabase-js or REST also needs `grant ... to service_role` on new tables. |
| G5 | low | A grant to a role on a table with RLS on but no policy for that role and command (every row is denied) | Add the policy if the access is wanted. Otherwise revoke the grant. |
| G6 | high | A `security definer` function in an exposed schema with no `revoke execute ... from public` (and none from `anon`) after it. Functions are executable by PUBLIC by default. | `revoke execute on function public.f(...) from public, anon;`, grant to `authenticated` only if needed, and `set search_path = ''`. Or use `security invoker`. |
| G7 | info | `alter default privileges ... grant ... on tables to anon/authenticated`, or `grant ... on all tables in schema public to anon` | Prefer per-table grants written next to RLS and policies. A blanket grant also exposes tables where RLS is off. |
| G8 | info | `supabase/config.toml` has no `[api] auto_expose_new_tables = false` | With it unset, the generated config (Supabase CLI 2.121.0) says a local stack falls back to exposing new tables automatically, so local tests won't show the 42501 a project returns once the change applies to it (date may move; see supabase/cli PR #6337). Set it to `false` to test that behaviour. |

The safe fix order for any table is: RLS on, then policies, then the minimum grant, all in the same migration. Never suggest `grant all ... to anon`. Per Supabase's changelog, tables that already exist keep their current grants. New tables made after the change need explicit grants.

## Report
1. One line: how many migration files you read, and findings by severity.
2. A table: severity, id, file:line, what you saw, fix.
3. For each table with a finding, the end state you worked out: RLS, policies and grants per role.
4. End with: "Findings are prompts to review, not proof of a vulnerability. A clean result is not proof the app is secure."
