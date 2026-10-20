---
name: supabase-core
description: "Shared reference for the Supabase cluster: the authorization model (Row-Level Security as the one boundary every product enforces), the keys/roles that reach the database, the auth-claims rule (app_metadata not user_metadata), the security-checklist traps, and the schema-change → advisor → migration workflow. USE WHEN designing tables, writing RLS policies, choosing keys, reviewing security, or shipping a Supabase schema change — the interlocking rules every Supabase spoke shares."
cluster: supabase
version: 1.0.0
---

# Supabase Core

Shared model for the `supabase` cluster. The feature-build, current-API, and performance
spokes all depend on these interlocking concepts — keep them consistent here so no spoke
contradicts another.

## 1. The authorization model (Supabase's defining decision)

**Authorization lives in the database, as Postgres Row-Level Security.** Supabase exposes your
tables directly (the auto-generated Data API / PostgREST), so a request can reach a table
without passing through any app server. RLS *is* the boundary every product enforces:

```
Request ──carries──> Role + JWT claims ──checked by──> RLS Policy(ies) ──on──> Table/Storage object
```

- **RLS is default-deny once enabled, but OFF by default on a new table.** Enable RLS on **every** table in an exposed schema (especially `public`), then write policies that match the *actual* access model — don't reflexively stamp the same `auth.uid()` policy on every table. → `supabase`, `supabase-developer`
- **A policy is per-command.** An `UPDATE` first has to `SELECT` the row — **without a `SELECT` policy, updates silently affect 0 rows** (no error). Storage **upsert needs INSERT + SELECT + UPDATE**; INSERT alone makes file replacement fail silently.
- **Views and privileged code bypass RLS.** Create views `WITH (security_invoker = true)` (Postgres 15+); keep `security definer` functions in a private/unexposed schema; on older Postgres, revoke view access from `anon`/`authenticated`.

**Rule:** the narrowest policy that satisfies the real access model — and treat *enabling the
Data API on a schema*, *adding a permissive policy*, or *exposing a view* as a security change
worth stating.

## 2. Keys & roles (who reaches the database, and as what)

| Key / role | Where it belongs | Notes |
|---|---|---|
| **publishable** (frontend) | public clients, browser | preferred for client code; subject to RLS as `anon`/`authenticated` |
| legacy **anon** | compatibility only | same RLS roles; prefer publishable |
| **service_role** / secret | server-only, never shipped | **bypasses RLS** — never in a public client; in Next.js, never behind `NEXT_PUBLIC_` |

The role + JWT decide which policies apply. `service_role` ignores RLS entirely, which is
exactly why it must never reach the browser.

## 3. Auth claims & sessions (the silent traps)

- **Never use `user_metadata` / `raw_user_meta_data` in authorization.** It is **user-editable**
  and can appear in `auth.jwt()`. Put authorization data in `app_metadata` / `raw_app_meta_data`. → `supabase`
- **JWT claims aren't fresh** until the user's token refreshes — `app_metadata`/`auth.jwt()` can lag.
- **Deleting a user does not invalidate existing access tokens** — sign out / revoke sessions,
  keep JWT expiry short, validate `session_id` against `auth.sessions` for sensitive ops.
- On the client, distinguish `getSession` (fast, trusts local) from `getUser`/`getClaims`
  (revalidated); use `@supabase/ssr` for cookie-based SSR. → `supabase`

## 4. Products map onto the same boundary

| Product | What it is | Access controlled by |
|---|---|---|
| **Database / Data API** | Postgres + auto REST (PostgREST), optional `pg_graphql` | RLS policies |
| **Auth** | email/OAuth/magic-link/phone, issues the JWT | claims feed RLS |
| **Storage** | S3-compatible objects | RLS on storage objects |
| **Realtime** | WebSocket DB-change / broadcast / presence | RLS on the underlying tables |
| **Edge Functions** | Deno serverless (TS) | the key the function uses |
| **Extensions** | `pgvector`, `pg_cron`, `pg_graphql`, queues | SQL / schema |

Feature wiring across these → `supabase-developer`. Current per-product API/config (which drifts
between versions) → `supabase`. Query/index/pooling performance underneath → `supabase-postgres-best-practices`.

## 5. The schema-change workflow (iterate freely, commit cleanly)

1. **Iterate** with `execute_sql` (MCP) or `supabase db query` (CLI) — runs SQL directly, **no**
   migration-history entry, so you can change your mind. Do **NOT** use `apply_migration` to
   iterate a local schema — it writes history on every call and breaks `db diff`/`db pull`.
2. **Run advisors** → `supabase db advisors` (CLI v2.81.3+) or MCP `get_advisors`; fix findings.
3. **Re-check the security traps** in §1–§3 if the change touches views, functions, triggers, storage, or auth.
4. **Generate the migration** → `supabase db pull <name> --local --yes`, then `supabase migration list --local` to verify. → `supabase`

CLI gotchas: `supabase db query` needs **v2.79.0+**; `supabase db advisors` needs **v2.81.3+** —
fall back to MCP `execute_sql` / `get_advisors`. Always discover commands via `--help`; the CLI
structure changes between versions.

## 6. Version / conventions

- **Supabase changes frequently — do not trust training data.** Function signatures,
  `config.toml`, and API conventions drift between versions. Look up the topic first:
  MCP `search_docs` → fetch any docs page as markdown (append `.md` to the URL) → web search. → `supabase`
- **Verify your work**: after any fix, run a test query confirming it. A fix without verification is incomplete.
- **Recover, don't loop**: if an approach fails 2–3 times, change method / check docs / read logs — don't re-run the same command.

## 7. Shared guardrails

- **RLS-by-default**: enable it on every table in an exposed schema; policies match the *real* access model.
- Remember per-command policies: `UPDATE` needs `SELECT`; storage upsert needs INSERT + SELECT + UPDATE.
- **`app_metadata`, never `user_metadata`**, for authorization claims.
- **Never expose `service_role`/secret keys** in public clients; publishable keys for the browser.
- Views `security_invoker`; `security definer` functions out of exposed schemas.
- State every data-access-surface change (RLS enable/policy, exposed schema, view, storage policy, key).
- Verify against **live docs** before implementing; verify the result with a **test query** after.
- Supabase vs a hand-rolled backend: pick Supabase for Postgres + the RLS boundary + batteries-included
  Auth/Storage/Realtime; if you need heavy custom server logic beyond Edge Functions, weigh a
  dedicated backend cluster alongside it.
