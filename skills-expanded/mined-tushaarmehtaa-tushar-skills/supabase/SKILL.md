---
name: supabase
description: Set up, extend or audit Supabase schema, grants, RLS, migrations, API keys, SSR sessions, typed clients and external auth. Use when integrating Supabase or repairing data access and tenant isolation.
license: MIT
---

# Supabase

Build a migration-backed, typed Supabase integration with explicit authorization boundaries. This skill owns Supabase grants, RLS, API keys and SSR session checks. The `auth-implementation` skill defers to it for all of them.

## Dated facts

Platform facts in this skill carry a check date and source. Before acting on one, re-check the source if the date is more than 90 days old or the installed package version differs from the one noted. For raw API shapes, use Supabase's official agent skill (`supabase/agent-skills`) if it is installed, otherwise the Supabase docs for the installed version. This skill keeps the judgment: what to grant, who owns a row, what to test.

Rules that change the work (checked 2026-11-04, sources in the references):

- **Default grants vary by project.** New projects have defaulted to no automatic grants on new `public` tables since a gradual rollout from 30 May 2026. Enforcement on existing projects was scheduled for 30 Oct 2026, but the Securing your API docs (updated 22 Oct 2026) still describe auto-grants on existing projects, and no first-party post confirms the switch happened. Without a grant, a table is not reachable through the Data API or GraphQL and PostgREST returns `42501 permission denied`. Always write explicit grants in the same migration as `create table`. That is correct in both states. Check a project's defaults with the `pg_default_acl` query in [grants and RLS](references/grants-and-rls.md). Supabase's docs note that its own agent skill handles grants.
- **Keys changed.** Clients use `sb_publishable_...`. Servers use `sb_secret_...`. Legacy `anon` and `service_role` JWT keys are deprecated, with deletion scheduled for "Late 2026, TBC".
- **Server checks use `getClaims()`.** It verifies the JWT signature, locally against a cached JWKS on projects with asymmetric signing keys. Never trust `getSession()` in server code.
- **Session refresh lives in `proxy.ts` on Next.js 16+ and `middleware.ts` on 15 and earlier.** A `proxy.ts` on Next.js 15 is never called, so sessions never refresh.

## Workflow

1. Inspect `supabase/`, `config.toml`, migrations, generated types, Supabase package and CLI versions, framework and its major version, which of `proxy.ts`/`middleware.ts` exists, environment-variable names without printing values (publishable/secret or legacy anon/service_role), auth/session flow, schemas exposed through the Data API, and existing grants/RLS. When a database is reachable, run the read-only default-privileges query in [grants and RLS](references/grants-and-rls.md) to learn what new tables receive.
2. Infer table ownership and tenant relationships from the domain model. Ask only when ownership, collaboration, deletion, retention, or external-auth behavior is ambiguous. Do not add `user_id` or four CRUD policies to every table mechanically.
3. Design keys, foreign keys, constraints, indexes, timestamps, lifecycle/deletion behavior, and server-generated ownership defaults appropriate to each table. Use external provider subject IDs as text unless a local identity mapping is intentionally modeled.
4. Write each exposed table as one unit in one migration: `create table`, explicit grants per role, `enable row level security`, then policies. Grant each role the minimum it needs. Give `anon` nothing unless signed-out access is intended. Grant `service_role` only where server code with the secret key touches the table. Write the grants even if the project still has permissive default privileges, so access is reviewable and works whether or not the project has switched. Tables the API must not reach get no grants, or live in an unexposed schema. Read [grants and RLS](references/grants-and-rls.md) for the template, functions, views and the 42501 debugging path.
5. Scope policies to roles, use indexed predicates, wrap `auth.uid()`/`auth.jwt()` in `(select ...)`, add `with check` for inserts and updates, review views and functions separately, and set a safe `search_path` on `security definer` functions.
6. Create named migrations with `supabase migration new` or a reviewed `db diff`. Treat diff output as a draft: check it for grants, publications, storage buckets and view options before committing. Verify with `supabase db reset` locally. Apply remotely (`db push`, or `migration up --linked`/`--db-url`) only when remote deployment is explicitly in scope, after showing `db push --dry-run` output and naming the target project. `migration up` has no dry-run flag.
7. Choose keys and clients with [keys and sessions](references/keys-and-sessions.md). Publishable key in anything shipped. Secret key only in a dedicated server-only client with its own authorization checks, never behind a `NEXT_PUBLIC_` prefix. If the project still runs on legacy keys, plan the swap to publishable/secret keys now. Disabling legacy keys and rotating signing keys are dashboard steps for the user. Do not perform them.
8. Match the auth strategy:
   - Supabase Auth: policies use `auth.uid()`/`auth.jwt()`. Server code protects pages and data with `getClaims()`.
   - Clerk or another supported third-party provider: configure the native third-party integration, make sure provider tokens carry `role: authenticated`, pass the provider token through the client's `accessToken` callback, and read the actual JWT `sub`/claims. An RLS expression alone does not configure token verification.
   - Server administration: a separate secret-key client with explicit authorization. It bypasses RLS but still needs grants.
9. For `@supabase/ssr`, create a client per request, use the `getAll`/`setAll` cookie adapter, await async framework cookie APIs, and refresh the session in `proxy.ts` or `middleware.ts` to match the installed Next.js major. Do not use legacy single-cookie adapters.
10. Generate TypeScript types after applying migrations to the target used for generation, then run type checks and update typed queries. Avoid `any` and handle `{ data, error }` explicitly.

Stop and confirm before remote migrations, revoking grants on existing tables, disabling legacy keys, rotating signing keys, or any change that widens `anon` access.

## Verification

Run local migration reset/apply, schema/type drift checks, and repository lint/type/test/build. Through the Data API, query every new table as anon, as a signed-in user and with the secret key. Expect success where granted and `42501` where not. A `42501` means a missing grant. An empty result means a policy matched no rows. Fix the grant before debugging the policy. For each policy, test allowed owner/member/admin/service access and denied anonymous/other-user/other-tenant reads and mutations, including attempts to change ownership. Test session refresh and expiry in the target runtime, confirm a tampered session cookie fails the server `getClaims()` check, and test external-provider tokens.

## Output

Report tables/functions/storage changed, migration files, grants per table and role, RLS policies with auth strategy, keys in use (publishable/secret or legacy, with migration status), client/session changes, type-generation command/result, negative authorization tests, dated facts re-checked, and remaining linked-project/dashboard/production steps.
