---
name: cloudflare-account-ops
description: Use for Cloudflare deploys, Email Routing, temp-email ops.
version: 1.0.0
author: Me
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [cloudflare, wrangler, email-routing, temp-email, d1, workers]
    related_skills: [captcha-solver-service]
---

# Cloudflare Account & Mail Infra Ops

Operate the user's Cloudflare account (wrangler CLI + REST API) and the self-hosted temp-email stack built on it.

## When to Use
- Deploying Workers/D1/KV/Pages to the user's Cloudflare account, or adding domains to a CF-hosted service.
- Configuring Email Routing (enable, catch-all → worker) or debugging inbound mail on a CF zone.
- Creating/reading mailboxes or harvesting OTP codes via the self-hosted cloudflare_temp_email service.
- Any Cloudflare API auth error (token refresh, scope limits, OAuth re-auth).
- Answering "where is the email infra / what domain": Worker `cte` + zone `kalcer.dev` (MX → CF Email Routing, catch-all). Worker source is NOT on the VPS — redeploy via skill `cloudflare-temp-email-deploy`; `cte.kalcer.dev` has no DNS record (frontend HTTP dead) while inbound mail routing works.


## Auth & token lifecycle
- Token source: `cf_tokens.json` in the profile dir (OAuth access + refresh); `CLOUDFLARE_API_TOKEN` mirrored in profile `.env`. Export it for API curls: `Authorization: Bearer $CLOUDFLARE_API_TOKEN`.
- Access token lives 1h. On API error `9109 Invalid access token`, refresh — never start a new browser OAuth flow first:
  `bash /usr/local/bin/cf-refresh-token.sh`
  (POSTs `grant_type=refresh_token` + wrangler client_id to `dash.cloudflare.com/oauth2/token`, rewrites cf_tokens.json + .env; cron runs it every 45 min.)
- If refresh fails (refresh token revoked), redo the custom PKCE flow: authorize URL with wrangler client `54d11594-84e4-41aa-b438-e81b8fa78ee7`, redirect `http://localhost:8976/oauth/callback`, S256. Persist the verifier to a file BEFORE handing the user the link — a verifier held only by a wrangler process dies with that process, making the returned code unexchangeable.
- Remote-user OAuth re-auth (user on Telegram, no browser on the VPS): `wrangler login` refuses while `CLOUDFLARE_API_TOKEN` is set ("You are logged in with an API Token") — always run it as `env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID wrangler login`. Two fallback methods, in order of preference:
  1. **Copy-paste callback (RELIABLE — verified 2026-09-30)**: hand-roll PKCE with redirect_uri `http://localhost:8976/oauth2/callback` (wrangler's registered redirect, accepted by the token endpoint), persist verifier+state to a file, hand the user the auth URL. After Allow, the browser lands on an error page `localhost:8976/oauth2/callback?code=...&state=...` — user copies the FULL address-bar URL and pastes it back in chat; parse `code=` + verify `state=`, exchange at `dash.cloudflare.com/oauth2/token` with client_id + code_verifier + the SAME redirect_uri. Auth code lives ~15 min — tell the user to paste quickly.
  2. **Pinggy tunnel (NOT reliable from azza — dropped twice, exit 255)**: `ssh -p 443 -R0:localhost:8976 a.pinggy.io`, URL lives ~60 min, but the SSH connection has proven unstable on this VPS; only try if copy-paste is impossible. Note: a `wrangler login` callback listener binds IPv6 `[::1]:8976` ONLY, so an IPv4-dialed tunnel times out — run a custom IPv4 listener (0.0.0.0:8976) instead of relying on wrangler's.

## OAuth token scope limits (wrangler-login token)
- Zone access is READ-ONLY: POST/PUT on `zones/:id/dns_records` returns code 10000 Authentication error. Never hand-write DNS records via API with this token.
- Email Routing WRITE works: `POST zones/:id/email/routing/enable {"enabled":true}` and `PUT zones/:id/email/routing/rules/catch_all` with body `{"enabled":true,"matchers":[{"type":"all"}],"actions":[{"type":"worker","value":["<worker_name>"]}]}` — the actions array is required (else 2007 Invalid Input).
- Workers/KV/D1/Pages writes work via wrangler (`npx wrangler deploy`, `d1`, `kv namespace`).
- Enabling Email Routing auto-provisions the MX/SPF/DKIM records server-side even though the token cannot write DNS. Verify propagation with `dig MX <domain> @1.1.1.1` — do not trust the routing object's `synced` field (it stays false after records are live). Always dig against a public resolver (`@1.1.1.1` or DoH `cloudflare-dns.com/dns-query`) when auditing external DNS — the VPS local resolver can return stale or internally-overridden answers that contradict the authoritative record.).

## Deploy gotchas
- A workers.dev subdomain must exist before deploying anything with cron triggers, else the API rejects schedules (code 10063) and triggers only partially apply. Create once: `PUT /accounts/:id/workers/subdomain` body `{"subdomain":"<name>"}` — the key is `subdomain`; `default_subdomain` returns "Subdomain '' is invalid".
- Feed secrets via stdin: `echo "$V" | npx wrangler secret put NAME`. Missing secrets do NOT fail at deploy time — they surface at request time.
- Serve a frontend from the same worker instead of a separate Pages project: build the SPA (`pnpm build:pages` in frontend/, which loads `.env.pages` — set empty `VITE_API_BASE` for same-origin and `VITE_DEFAULT_LANG=en` there), then add `[assets]` block (see templates/wrangler.toml) and redeploy. Assets are baked into the worker version: any rebuild must be followed by `npx wrangler deploy` (with `CLOUDFLARE_API_TOKEN` exported), else the live frontend never changes.
- A route `{ pattern = "<sub>.<domain>", custom_domain = true }` auto-creates the DNS record on deploy.
- Zone status `pending` = registrar NS ≠ CF-assigned NS (compare `name_servers` vs `original_name_servers` on the zone object). Fix at the registrar panel; CF cannot force it. Email Routing only delivers on `active` zones — adding a domain to the service is blocked until the user updates NS at the registrar.

## Temp email service (dreamhunter2333/cloudflare_temp_email)
Deploy-from-scratch + operating procedure: see `references/temp-email-service.md`. Known-good worker config: `templates/wrangler.toml`.
Non-negotiables (all surface only at request time, not deploy time):
- `JWT_SECRET` must be a wrangler secret.
- `ENABLE_USER_CREATE_EMAIL = true` in [vars] or address creation 403s.
- Every API call needs `x-custom-auth: <site password>` — even alongside `Authorization: Bearer <jwt>`.
- Admin API (`/admin/*`) needs BOTH `x-admin-auth` and `x-custom-auth` — the site-password middleware checks first, so `x-admin-auth` alone returns AUTH_SITE_PASSWORD_INVALID.
- User API (`/user_api/*`) authenticates with header `x-user-token: <jwt>`, NOT `Authorization: Bearer` (Bearer returns "Your token has expired").
- OTP text lives in D1 table `raw_mails` (column `raw`), not `mails`; read endpoints are `/api/mails` (list) and singular `/api/mail/:id`.
- This user wants minimal D1 read burn: default all mail/address retention to 1 day via `POST /admin/auto_cleanup` (see reference) — the daily cron applies it; user accounts survive cleanup.
- Live deployment inventory (API/frontend URLs, mail domains, D1 id, password location) and the rediscovery procedure for any deployed CF service: "Live instance" section of `references/temp-email-service.md`.
- Adding a mail domain to temp-email: follow "Add a mail domain to the live instance" in `references/temp-email-service.md` — the worker `DOMAINS` redeploy comes BEFORE any farmer uses the domain, or address creation 403s.
- To wire the service into another project, run `scripts/mailbox_otp.py` (stdlib-only client: create mailbox, list mails, poll-for-OTP) instead of hand-rolling HTTP each time.
- `GET /api/mails` returns the mail array under key `results` (plus `count`) — a client reading `.get("mails")` sees an eternally empty inbox even when mail is flowing; always read `results` (the script accepts either key).
- A default OTP regex must reject raw-mail metadata, not just years: Date headers add timestamps (`10:32`) and timezone offsets (`+0000`) that are plain 4-digit runs — require a non-digit/`.`/`:`/`+` boundary before and a non-digit/`.`/`:` after the match, and skip bare 19xx/20xx.
- Frontend must open in English by default (standing user preference): rebuild/redeploy procedure + localStorage override pitfall — see "Frontend default language" in `references/temp-email-service.md`.
- The user-facing login is the frontend URL (`/admin` for the admin UI); the API custom domain has no UI — when asked "where to log in", answer with the frontend URL.
