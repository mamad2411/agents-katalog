---
name: supabase-docs
description: "Knowledge base from the full Supabase documentation. Use when building on Supabase — Postgres/RLS, Auth (JWT/OAuth/SSO/MFA), auto-generated REST & GraphQL APIs, Storage, Realtime, Edge Functions, pgvector/AI, Queues, Cron, CLI/local dev, deployment/branching, self-hosting, the managed platform, security/compliance, and telemetry — or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Supabase Documentation
**Source**: Supabase official docs (19 sections, 547 pages) | **Chapters**: 18 | **Generated**: 2026-06-19

## How to Use This Skill

- **Without arguments** — load the core frameworks below for reference.
- **With a topic** — ask about `RLS`, `pgvector`, `connection pooling`, `branching`, etc.; I find and read the relevant chapter.
- **With a chapter** — ask for `ch03`; I load that file.
- **Browse** — ask "what chapters do you have?" for the index.

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file first. For decision rules see [cheatsheet.md](cheatsheet.md); for techniques [patterns.md](patterns.md); for terms [glossary.md](glossary.md).

> Note: deep self-hosting how-tos live in the separate **supabase-self-hosting** skill; Ch13 here is an overview.

---

## Core Frameworks & Mental Models

**Postgres is the product.** Every Supabase feature is a thin layer over an unabstracted, full-privilege Postgres: PostgREST reflects your schema as REST, pg_graphql as GraphQL, GoTrue issues JWTs read by RLS, Realtime streams the WAL, Storage keeps object metadata in Postgres, pgvector adds similarity search, pgmq/pg_cron add queues/scheduling. Learn Postgres and you've learned Supabase.

**Row Level Security (RLS) is the security model.** A policy is an implicit `WHERE` appended to every query, evaluated against JWT claims via `auth.uid()` / `auth.jwt()`. Rules:
- Any table exposed via the Data API **must** have RLS enabled — no policy means *deny all*, but a *granted table without RLS is fully readable by anon*.
- Write `using` (visible rows) + `with check` (allowed new rows); wrap helpers as `(select auth.uid())` and add `to authenticated` for ~95% scan speedup; index the policy column.
- `as restrictive` ANDs (hard gates, e.g. MFA `aal2`); permissive policies OR. Store authz in `app_metadata` (not user-editable `user_metadata`). RLS gates rows; use column GRANT/REVOKE (CLS) for fields.

**The two-key model.** `sb_publishable_…` is low-privilege and safe in public/client code (RLS protects data); `sb_secret_…` / `service_role` runs on a trusted backend and **bypasses RLS**. Every Data API call also carries the non-JWT `apikey` header.

**Auth = JWT bridge.** Short-lived access token + one-time refresh token (reuse detection revokes the session). The `role` claim selects the Postgres role; `aal`/`amr` encode MFA; OAuth/SSO(SAML)/phone/email-OTP/anonymous all mint the same JWT that RLS then enforces. Verify externally via JWKS/asymmetric keys, never the HS256 secret.

**Auto-generated APIs.** PostgREST compiles one request to one SQL statement; `supabase-js` is a fluent builder over it (filters, FK embedding, `.rpc()` for functions — RLS doesn't apply to RPC, EXECUTE grant does). On error, log the whole object: `error.hint` is often the exact GRANT, branch on stable `error.code`. Two-layer security = grants (object) + RLS (row).

**Connections.** Supavisor pools Postgres: **transaction mode `:6543`** for serverless/edge (no session features/prepared statements), **session `:5432`** for long-lived backends and migrations.

**Realtime = three extensions.** Broadcast (ephemeral msgs), Presence (shared state, CRDT), Postgres Changes (DB row events). Use Broadcast for high-frequency data (Presence floods); re-stream via Broadcast when Postgres Changes is slow (single ordering thread). Private channels gate on RLS over `realtime.messages`; drive UI from SQL with `realtime.broadcast_changes()`.

**Edge Functions** are regional Deno/TS isolates. Combine actions into **fat functions** (each cold-starts independently); pin `x-region` for DB-heavy work; outlast the response with `EdgeRuntime.waitUntil`; `withSupabase({auth:'user'|'none'|…})` handles auth/CORS and injects `ctx`.

**Vectors / AI (pgvector).** `vector(N)` must match the model's dimensions; only compare same-model embeddings. Always wrap similarity in a SQL function + `rpc()` (PostgREST can't call `<->`/`<#>`/`<=>`) and `order by` the raw distance expression, not the alias. Default to **HNSW**; `<#>` for normalized, `<=>` otherwise; fuse keyword+semantic with RRF.

**Schema as code.** Imperative migrations (forward-only) or declarative `schemas/*.sql` → `db diff -f` (migra). Promote local→staging→prod via `link` + `db push` in CI, gated by branch-protection; one push at a time. Preview branches are ephemeral and data-less.

**Operate.** Managed platform: org owns plan/billing/SSO, project owns compute/replicas/backups/domains; harden with custom domain → SSL verify-full → IPv4+IPv6 network restrictions; PITR (RPO ~2 min) replaces daily backups. Self-host via Docker `setup.sh`; `sh run.sh recreate` after any `.env` change; front Kong with an HTTPS proxy. Telemetry: logs are per-component BigQuery-SQL tables (unnest `metadata`), Prometheus metrics endpoint, log drains.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-getting-started.md) | Getting Started | quickstart bootstrap, createClient, two-key model |
| [ch02](chapters/ch02-database.md) | Database (Postgres) | RLS, SECURITY DEFINER, tsvector+GIN, Supavisor, webhooks |
| [ch03](chapters/ch03-auth.md) | Auth & Authorization | RLS, JWT claims, sessions, OAuth, MFA/AAL, SSO/SAML |
| [ch04](chapters/ch04-storage.md) | Storage | bucket access, RLS-on-objects, upload methods, signed URLs, CDN |
| [ch05](chapters/ch05-edge-functions.md) | Edge Functions | withSupabase, verify_jwt, fat functions, waitUntil, regions |
| [ch06](chapters/ch06-realtime.md) | Realtime | Broadcast/Presence/Postgres Changes, channel RLS, broadcast-from-DB |
| [ch07](chapters/ch07-api.md) | REST & GraphQL APIs | PostgREST, pg_graphql, grants+RLS, RPC, type generation |
| [ch08](chapters/ch08-ai-vectors.md) | AI & Vector Embeddings | pgvector, semantic/hybrid search, HNSW/IVFFlat, RAG, MCP |
| [ch09](chapters/ch09-queues.md) | Queues (pgmq) | pgmq, visibility timeout, pgmq_public, cron consumer |
| [ch10](chapters/ch10-cron.md) | Cron (pg_cron) | cron.schedule, pg_net HTTP, alter_job |
| [ch11](chapters/ch11-local-development.md) | Local Dev & CLI | migrations, declarative schemas, db diff/reset, pgTAP, seeding |
| [ch12](chapters/ch12-deployment.md) | Deployment & Environments | branching, CI/CD, db push, maturity model, production checklist |
| [ch13](chapters/ch13-self-hosting.md) | Self-Hosting (Docker) | docker-compose, Kong/Envoy, asymmetric keys, run.sh recreate |
| [ch14](chapters/ch14-platform.md) | Platform (Managed Cloud) | compute/replicas, PITR, network restrictions, SSL, spend cap, RBAC |
| [ch15](chapters/ch15-security.md) | Security & Compliance | shared responsibility, RLS/CLS, SOC2/HIPAA+BAA, supply-chain |
| [ch16](chapters/ch16-telemetry.md) | Telemetry | logs explorer (BigQuery SQL), Prometheus metrics, log drains, tracing |
| [ch17](chapters/ch17-integrations.md) | Integrations | Management API, OAuth2+PKCE, Supabase-for-Platforms, branches |
| [ch18](chapters/ch18-resources.md) | Resources & Migration | glossary, Postgres dump/restore, Firebase→Supabase mapping |

## Topic Index

- **AAL / MFA / OTP** → ch03
- **API keys / publishable / secret / service_role** → ch01, ch03, ch07, ch15
- **Auth / JWT / sessions** → ch03, ch18
- **Backups / PITR** → ch14
- **Branching / preview branches** → ch12, ch17
- **CLI / supabase commands** → ch11, ch12
- **Compliance / SOC2 / HIPAA / BAA** → ch15
- **Connection pooling / Supavisor** → ch02, ch13
- **Cron / pg_cron / scheduling** → ch10, ch05, ch09
- **Custom domains / network restrictions / SSL** → ch14
- **Declarative schemas / migrations** → ch11, ch12
- **Edge Functions / Deno** → ch05
- **Full-text search / tsvector** → ch02
- **GraphQL / pg_graphql** → ch07
- **Logs / metrics / tracing** → ch16
- **Management API / OAuth apps / PKCE** → ch17
- **Migrating from Firebase/Heroku/RDS** → ch18
- **pgvector / embeddings / semantic / hybrid search / RAG** → ch08
- **PostgREST / REST API / filters / RPC** → ch07
- **Postgres / extensions / triggers / functions** → ch02
- **Queues / pgmq** → ch09
- **Quickstarts / createClient / frameworks** → ch01
- **Realtime / Broadcast / Presence / Postgres Changes** → ch06
- **RLS / policies / CLS** → ch02, ch03, ch07, ch15
- **Self-hosting / Docker / Kong / Envoy** → ch13
- **Storage / buckets / signed URLs / uploads** → ch04
- **Vault / secrets** → ch15
- **Webhooks / pg_net** → ch02, ch10

## Supporting Files

- [glossary.md](glossary.md) — key terms with definitions
- [patterns.md](patterns.md) — concrete techniques (when/how/trade-offs)
- [cheatsheet.md](cheatsheet.md) — decision rules and quick-reference tables

---

## Scope & Limits

Covers the Supabase docs as of generation. For deep self-hosting operations use the **supabase-self-hosting** skill. For hands-on work, combine with your project's actual schema, keys, and CLI. For API/library specifics that may have changed, verify against the live docs.
