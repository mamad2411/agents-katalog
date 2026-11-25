---
name: supabase-self-hosting
description: "Knowledge base from the Supabase Self-Hosting guides (Docker). Use when configuring or operating self-hosted Supabase: docker-compose, API keys/JWT auth, Kong/Envoy gateway, OAuth/SAML/MFA, S3 storage, Postgres 17 upgrade, HTTPS reverse proxy, edge functions, MCP, platform migration."
---

<!-- argument-hint: [topic, env var, service, or chapter number] -->

# Supabase Self-Hosting (Docker)
**Source**: Supabase official self-hosting guides (15 docs) | **Chapters**: 15 | **Generated**: 2026-06-19

## How to Use This Skill

- **Without arguments** — load the core operating model below.
- **With a topic** — ask about `oauth`, `envoy`, `pg17 upgrade`, `s3 storage`, `restore`; I find and read the relevant chapter.
- **With chapter** — ask for `ch03`; I load that chapter file.
- **Browse** — ask "what chapters do you have?" for the full index.

When you ask about a topic not covered below, I read the relevant chapter file before answering.

---

## Core Operating Model

**The whole stack runs from `docker-compose.yml` + `.env`, fronted by an API gateway on `:8000`.** Master these and most tasks follow:

- **`.env` holds values; `docker-compose.yml` references `${VARS}`.** A `.env` value does nothing inside a container without a matching passthrough in that service's `environment:` block. This two-layer rule is the #1 source of "it's not working" — verify with `docker compose exec <svc> env | grep <PREFIX>`.
- **`recreate`, not `restart`, after config changes.** `sh run.sh recreate <svc>` (= `up -d --force-recreate --no-deps`) picks up config; plain `restart` silently keeps old config. (New function *files* are the exception — `restart functions --no-deps` suffices.)
- **Replace every secret before first start.** `generate-keys.sh` + `add-new-auth-keys.sh` do this; never run `.env.example` defaults in production. Move secrets to a manager (Doppler/Infisical/Vault) for prod.
- **Manage the stack with the wrappers:** `run.sh` (start/stop/recreate/secrets/config/logs/printenv), `reset.sh` (full destructive teardown). Enable optional features with override files: `sh run.sh config add logs`, or `-f docker-compose.<name>.yml`.

**Gateway & auth (Kong default, Envoy optional via override):**
- Both gateways route to services, enforce the `apikey` header, and **translate opaque `sb_` keys into pre-signed internal ES256 JWTs** before upstream. A real user-session JWT in `Authorization` (anything not `Bearer sb_`) passes through unchanged.
- **Two key systems coexist:** legacy HS256 (`ANON_KEY`/`SERVICE_ROLE_KEY`) and new opaque (`SUPABASE_PUBLISHABLE_KEY`/`SECRET_KEY`). Auth **signs** with `JWT_KEYS`; PostgREST/Realtime/Storage **verify** with `JWT_JWKS` (holds both EC public + legacy symmetric → both token types verify). Keep `JWT_SECRET` in the JWKS for backward compat.
- **Rotate** keys (`rotate-new-api-keys.sh`) → sessions survive. **Regenerate** the EC keypair (`add-new-auth-keys.sh`) → ES256 sessions die (maintenance window).
- `/pg/` is service_role-only; `/storage/v1/` and `/functions/v1/` self-authenticate (gateway bypasses key check); `/mcp` and Realtime mgmt routes are denied by default.

**Auth configuration patterns:**
- **OAuth** = env vars only (`GOTRUE_EXTERNAL_<PROVIDER>_*`), callback always `${API_EXTERNAL_URL}/auth/v1/callback`, HTTPS required, recreate `auth`.
- **SAML** = env vars enable the engine (restart) + **admin API registers IdPs at runtime** (no restart). SP entity-ID/ACS are open gateway routes.
- **Phone/MFA** = `GOTRUE_SMS_*` provider config; TOTP on by default, phone MFA opt-in.
- **Email templates** = Auth fetches from URLs (never mounted files); serve via a private `templates-server`.

**Data & networking:**
- **Postgres via Supavisor**: 5432 session / 6543 transaction; user is `postgres.<tenant>`. PG17 is default; upgrades use two-phase `pg_upgrade` — **protect the `db-config` volume (pgsodium key); never `down -v`; keep `data.bak.pg15` until verified.**
- **HTTPS** = reverse proxy (Caddy/Nginx) terminating TLS at 443; backend stays HTTP:8000; update `SUPABASE_PUBLIC_URL`/`API_EXTERNAL_URL`/`SITE_URL`.
- **Storage** = S3 protocol endpoint and S3 backend are independent features; uploads need RLS even on Public buckets.
- **Migration** = DB via `supabase db dump` (not raw `pg_dump`) + single-transaction restore; storage via rclone S3-to-S3 (not file copy); secrets/providers/SMTP reconfigured manually.

---

## Chapter Index

| # | Title | Key Topics |
|---|-------|-----------|
| [ch01](chapters/ch01-docker-setup.md) | Self-Hosting with Docker | install paths, run.sh/reset.sh, secrets, URLs, Supavisor |
| [ch02](chapters/ch02-api-keys-asymmetric-auth.md) | New API Keys & Asymmetric Auth | opaque keys, JWT_KEYS/JWKS, rotation, Kong logic |
| [ch03](chapters/ch03-envoy-gateway.md) | Envoy API Gateway | filter chain, routes, RBAC, hardening, admin |
| [ch04](chapters/ch04-oauth-social-login.md) | Social Login (OAuth) | GOTRUE_EXTERNAL_*, callback, providers |
| [ch05](chapters/ch05-saml-sso.md) | SAML SSO | engine env vars, admin API, attribute mapping |
| [ch06](chapters/ch06-s3-storage.md) | Configure S3 Storage | protocol endpoint vs backend, RustFS/MinIO, session token |
| [ch07](chapters/ch07-postgres-17-upgrade.md) | Upgrade to Postgres 17 | pg_upgrade two-phase, backups, rollback |
| [ch08](chapters/ch08-reverse-proxy-https.md) | Reverse Proxy & HTTPS | Caddy, Nginx+Certbot, self-signed |
| [ch09](chapters/ch09-edge-functions.md) | Self-Hosted Functions | Deno functions, env vars, internal vs external URL |
| [ch10](chapters/ch10-phone-login-mfa.md) | Phone Login & MFA | SMS provider, OTP settings, TOTP/phone MFA |
| [ch11](chapters/ch11-enable-mcp.md) | Enabling MCP Server Access | IP allow-list, SSH tunnel, Kong/Envoy edits |
| [ch12](chapters/ch12-copy-storage-from-platform.md) | Copy Storage from Platform | rclone S3-to-S3, bucket pre-creation |
| [ch13](chapters/ch13-custom-email-templates.md) | Custom Email Templates | URL-fetched templates, templates-server |
| [ch14](chapters/ch14-remove-superuser-access.md) | Remove Superuser Access | reassign-owner.sh, postgres role |
| [ch15](chapters/ch15-restore-from-platform.md) | Restore Platform Project | supabase db dump, single-transaction restore |

## Topic Index

- **admin API (SSO)** → ch05
- **API keys / JWT** → ch02, ch09
- **attribute mapping** → ch05
- **backups** → ch07, ch15
- **Caddy / Nginx** → ch08, ch13
- **CORS** → ch03
- **db-config / pgsodium** → ch07
- **edge functions** → ch09, ch01
- **Envoy** → ch03, ch08, ch11
- **HTTPS / TLS** → ch08, ch04
- **Kong** → ch02, ch01, ch08, ch11
- **MCP** → ch11, ch03
- **MFA / OTP / SMS** → ch10
- **OAuth / OIDC** → ch04
- **override files** → ch01, ch03, ch06, ch07, ch08
- **Postgres / Supavisor** → ch01, ch07, ch15
- **rclone / storage migration** → ch12, ch06
- **RBAC** → ch03, ch11
- **rotation / regeneration (keys)** → ch02
- **S3 (protocol/backend)** → ch06, ch12
- **SAML SSO** → ch05
- **secrets / generate-keys** → ch01, ch02
- **SMTP / email templates** → ch13, ch01
- **superuser / roles** → ch14, ch15
- **system requirements** → ch01
- **URLs (SUPABASE_PUBLIC_URL etc.)** → ch01, ch08, ch04

## Supporting Files

- [glossary.md](glossary.md) — all key terms, env vars, and services with chapter refs
- [patterns.md](patterns.md) — reusable techniques (two-layer config, recreate vs restart, gateway translation, migrations)
- [cheatsheet.md](cheatsheet.md) — decision rules, error→cause table, ports, thresholds, danger smells

---

## Scope & Limits

Covers the self-hosted Supabase Docker guides only (server-side configuration). Client-side SDK integration, the managed platform dashboard, and Supabase Cloud features are out of scope — combine with the main Supabase docs for those. Always cross-check exact env vars against your version's `.env.example` and the [self-hosted CHANGELOG](https://github.com/supabase/supabase/blob/master/docker/CHANGELOG.md), since config surface changes between releases.
