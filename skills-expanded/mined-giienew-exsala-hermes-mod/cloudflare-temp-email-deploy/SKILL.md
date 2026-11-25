---
name: cloudflare-temp-email-deploy
description: "Use when deploying the cloudflare_temp_email mail Worker."
version: 1.0.0
license: MIT
platforms: [linux]
---

# Cloudflare temp-email stack (deploy + operate)

Deploy and operate dreamhunter2333/cloudflare_temp_email — a Cloudflare Worker + D1 + KV temp-mail service with per-zone inbound routing. Recipe verified end-to-end on two zones.

## Deploy recipe

1. `git clone https://github.com/dreamhunter2333/cloudflare_temp_email`, `pnpm install` in `worker/` (and the frontend dir when building).
2. D1: `wrangler d1 create temp-email-db` (APAC region for ID traffic), then `wrangler d1 execute temp-email-db --remote --file=schema.sql` (11 tables).
3. KV: `wrangler kv namespace create KV`.
4. Write `worker/wrangler.toml`: name + `main = "src/worker.ts"`; routes for API domain and frontend domain; d1 + kv bindings; `[vars]` DOMAINS + DEFAULT_DOMAINS (the zones), PASSWORDS + ADMIN_PASSWORDS (site + admin gates — may share one value), ENABLE_USER_CREATE_EMAIL=true; `[assets]` binding with `run_worker_first=true` so one worker serves frontend + API.
5. `wrangler secret put JWT_SECRET` — mandatory before login endpoints work.
6. Frontend: set vite prod env, `pnpm build:pages`, `wrangler deploy`. Adding a custom-domain route auto-creates the DNS record even without DNS-write API scope.
7. Email Routing per zone: POST `/zones/{zone_id}/email/routing/enable` + PUT catch_all → worker (MX/SPF auto-provision). A freshly-enabled zone can SMTP-reject (550 "Domain does not exist") for ~a minute — propagation, retry.
8. Admin bootstrap: POST /admin/users (create account), POST /admin/auto_cleanup (retention — persists in D1, executed by the built-in 00:00 UTC cron).

## Auth header map (the part that burns time)

- Site gate: `x-custom-auth` = site password — required on ALL gated endpoints, including admin ones.
- Admin API: dual header `x-admin-auth` + `x-custom-auth` — missing the second yields AUTH_SITE_PASSWORD_INVALID.
- Address JWT: `Authorization: Bearer <jwt>` + `x-custom-auth`.
- User accounts (`/user_api/*`): `x-user-token` — NOT Authorization Bearer; Bearer gets a misleading "token has expired" 401.
- `/open_api/*` is public by design.
- Read a single mail: `/api/mail/{id}` — singular; the plural form 404s.

## Operating pitfalls

- ENABLE_USER_CREATE_EMAIL=false → POST /api/new_address 403 "New address is disabled" — flip the var and redeploy.
- Retention/cleanup settings are runtime state set via POST /admin/auto_cleanup, not wrangler.toml vars — `cleanMailsDays`/`cleanAddressDays`/etc. persist in D1 and the daily cron executes them. Address deletion cascades mail/sent/auto-reply/sender/binding rows.
- Password change: edit PASSWORDS/ADMIN_PASSWORDS in wrangler.toml + `wrangler deploy`; old values 401 immediately.
- OTP recovery: if the parsed-mail endpoint fails, query D1 directly — `wrangler d1 execute temp-email-db --remote --json` with instr()/substr over the raw body table.
- CNAME/DNS edits via API need a DNS-write scope token; the OAuth token usually lacks it — prefer wrangler custom-domain routes or let Email Routing auto-provision.

## Verifying an inbox (E2E)

- Proof of a live inbox = generating an address and seeing mail land; don't rebuild and redeploy the worker every time. The deployment is already verified.
- Check with the service's own inbox API, not an external fake-mailer. ce15a2ca77-temp email stack has `/inbox?email=` (and `/generate`, `/latest`) built in — curl the inbox endpoint directly.
- A mailer that demonstrates delivery to an inbox on a DIFFERENT provider proves nothing about THIS worker — the worker is not the mailer's recipient.
- If a test from an external anon-mailer (emkei.cz, etc.) won't deliver to a custom-worked domain, that's a delivery harness problem, not the worker. Don't burn hours proving an anon mailer can reach your own custom domain.

  emkei.cz specifics when you do use it: POST to `https://emkei.cz/` needs `mycharset=UTF-8` + `current=1` (or a valid `date`) + `ok=Send` or you get "Custom date required"; it may still drop mail to a custom domain.

## Worker auth/route map (from live me-agent.web.id)

- Routing: `/generate` (create address), `/inbox?email=` (list), `/latest` (newest).
- Auth: `/generate` uses an `Authorization: Bearer`-style secret; `/inbox` and `/latest` are public once you know the address.
- The stack keeps one worker per zone; each generated address belongs to that zone's domain.
