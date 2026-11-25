---
name: auth-implementation
description: Implement authentication, authorization, tenant isolation, sessions, and protected routes. Use when adding sign-in, identity sync, provider integration, account linking, roles, or access control.
license: MIT
---

# Authentication implementation

Implement identity and authorization end to end. Prefer the existing provider. Do not introduce or replace an identity system without an explicit user decision.

## Dated facts

Provider facts in the references carry a check date and source. Before acting on one, re-check the source if the date is more than 90 days old or the installed package version differs. For raw API shapes, use the provider's official agent skill if it is installed (`clerk/skills`, `better-auth/skills`, `supabase/agent-skills`), otherwise the provider's docs for the installed version. This skill keeps the judgment: access matrix, enforcement points, safe linking, idempotent sync and negative tests.

## Workflow

1. Detect framework/router version, auth package and installed version, database/ORM, session transport, user/account tables, tenant model, middleware or proxy, protected resources, and existing migrations.
2. Distinguish authentication from authorization. Write an access matrix for public, signed-in, owner, team member, admin, and service/background paths that actually exist.
3. Decide whether a local user mirror is necessary. If it is, model provider identities separately from application users when multiple login methods or providers are possible. Never link accounts from an unverified client-supplied email.
4. Ask only when a material choice remains: provider selection, account-linking policy, deletion behavior, organization/tenant model, or whether existing users must be backfilled.
5. Use the matching provider reference only after detecting the exact stack and installed version. When the project already has an auth library, that library is the default. Do not route it to another one.
   - [Clerk](references/clerk.md) for resource-level protection, verified user synchronization and Clerk tokens for Supabase.
   - [Auth.js / NextAuth](references/nextauth.md) for existing Auth.js projects only. Detect v4 or v5 beta first.
   - [Better Auth](references/better-auth.md) for projects already on Better Auth, or a new project where the user chose a self-hosted library.
   - [Supabase Auth](references/supabase-auth.md) for the identity model and profile synchronization. The `supabase` skill owns Supabase grants, RLS, API keys and server session checks.
   - For Firebase, Auth0, custom JWT, or a provider/database combination not covered, preserve existing code and use that provider's documentation for the installed version instead of adapting an incompatible example.
   - New project with no auth: provider choice is the user's call (step 4). Offer a hosted provider (Clerk, Supabase Auth) or a self-hosted library. For a self-hosted library, recommend Better Auth over Auth.js. Auth.js v5 never left beta, npm `latest` still installs v4, and Auth.js has been in security-patch mode under the Better Auth team since 22 Sep 2025 (checked 2026-11-04: https://better-auth.com/blog/authjs-joins-better-auth, https://registry.npmjs.org/-/package/next-auth/dist-tags).
6. Enforce access next to every protected read/mutation. Middleware/proxy may provide broad routing, but it is not the sole authorization boundary.
7. When data goes through the Supabase Data API, every exposed table needs explicit grants and RLS in the same migration as `create table`. Default grants vary by project: new projects stopped auto-granting from 30 May 2026, and enforcement on existing projects was scheduled for 30 Oct 2026. Where grants are missing, the Data API returns `42501` (checked 2026-11-04: https://supabase.com/changelog/45329-breaking-change-tables-not-exposed-to-data-and-graphql-api-automatically, https://supabase.com/docs/guides/api/securing-your-api). Follow the `supabase` skill for grants, policies, keys and SSR sessions. If it is not installed, use https://supabase.com/docs/guides/api/securing-your-api.
8. Make sync idempotent and verifiable. Prefer signed provider webhooks for lifecycle sync, or fetch authoritative provider data on the server for just-in-time sync. Handle create, update, merge, deletion, replay, out-of-order delivery, and backfill.

## Verification

Test new sign-up, returning login, logout, expiry/refresh, account switching, verified linking, provider update/merge/deletion, and replayed sync. For every protected resource, run negative tests as unauthenticated, another user, another tenant, and a non-admin; test permitted owner/admin/service cases separately. Run migrations and the repository's lint/type/test/build commands in the target runtime.

## Output

Report provider/version and identity model, files/migrations changed, access matrix and enforcement points, sync strategy, Supabase grants/RLS if used (per the `supabase` skill), environment-variable names, dated facts re-checked, automated verification evidence, and manual dashboard/backfill/production checks.
