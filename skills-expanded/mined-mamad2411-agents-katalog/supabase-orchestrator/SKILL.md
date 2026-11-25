---
name: supabase-orchestrator
description: "Route a Supabase task to the right skill among three specialists — full-stack feature build (Auth, Storage, Realtime, Edge Functions, RLS schema design), live-doc-verified product guidance with the security checklist and CLI/MCP workflow, and Postgres performance/query optimization. USE WHEN a user is building on, securing, or tuning Supabase but hasn't named whether the concern is feature-building, current-API correctness, or database performance."
cluster: supabase
version: 1.0.0
---

# Supabase Orchestrator

The single entry skill for Supabase work. It locates the task on the **concern × surface**
map and delegates to one of three specialist spokes. The cross-cutting model every Supabase
app shares — **authorization lives in Postgres Row-Level Security**, the keys/roles that
reach the database, and the schema-change → advisor → migration workflow — lives in
`supabase-core`; read it before designing tables, writing policies, or shipping a schema change.

## Routing map (intent → spoke)

**Build a feature end to end**
- New full-stack app, or wiring Auth / Storage / Realtime / Edge Functions into one → `supabase-developer`
- Designing the schema + RLS policies for a feature, client SDK integration (Next.js, React, Vue) → `supabase-developer`
- Phase-by-phase implementation plan (setup → schema → auth → storage → realtime → functions → deploy) → `supabase-developer`

**Get the current API / product behavior right (verify, don't guess)**
- "How does <Supabase feature> actually work *today*?" — signatures, `config.toml`, conventions that drift between versions → `supabase` *(it fetches live docs before implementing)*
- Auth/session correctness: `getSession` vs `getUser` vs `getClaims`, cookies, JWT, `@supabase/ssr` → `supabase`
- **Security review** of auth, RLS, views, storage, or privileged DB code → `supabase` *(runs the Supabase-specific security checklist; model in `supabase-core`)*
- CLI or MCP-server usage, troubleshooting, version gotchas → `supabase`
- Committing a schema change to a migration (advisors → review → `db pull`) → `supabase`

**Make the database fast / correct under load**
- Slow query, missing/partial index, query-plan review → `supabase-postgres-best-practices`
- Connection pooling / scaling, concurrency & locking, schema-design performance → `supabase-postgres-best-practices`
- Monitoring & diagnostics, advanced Postgres features → `supabase-postgres-best-practices`

## Standard Operating Flow

1. Classify the concern: **feature-build** (`supabase-developer`), **current-API correctness / security / CLI-MCP** (`supabase`), or **database performance** (`supabase-postgres-best-practices`).
2. If it touches **RLS, auth claims, exposed schemas, views, storage policies, or keys**, pull the model from `supabase-core` first — these are interlocking security rules, not independent toggles.
3. Delegate to the spoke(s). Multi-step asks fan out in lifecycle order (e.g. "build a feature and make it fast" → `supabase-developer` for the schema + policies, then `supabase-postgres-best-practices` for indexes/pooling, then `supabase` to run advisors and cut the migration).
4. Return: chosen spoke(s), any RLS/key/security-surface change implied, the target surface (Data API · Auth · Storage · Realtime · Edge Functions), and the next action.

## Guardrails

See `supabase-core`. In short: **RLS-by-default** — enable Row-Level Security on every table in
an exposed schema (especially `public`) and write policies that match the real access model;
never use user-editable `user_metadata` claims for authorization (use `app_metadata`); never
expose the `service_role`/secret key in a public client; keep views `security_invoker` and
`security definer` functions out of exposed schemas. Supabase changes frequently — **verify
against live docs before implementing**, and **verify your work with a test query** after.
Don't quietly widen the data-access surface.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
