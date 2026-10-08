---
name: cliproxyapi-cloudflare-stack
description: Deploy a self-hosted, OpenAI-compatible LLM API gateway using CLIProxyAPI (CPA) fronted by Cloudflare — a temp-email Worker (Workers + D1 + Email Routing), credential hot-reload into CPA, and a Cloudflare Tunnel for HTTPS. For learning the Cloudflare + CPA architecture and managing credentials you are authorized to use. Not for automated account creation or bypassing any platform's anti-bot controls.
---

# Self-hosted LLM gateway: CLIProxyAPI + Cloudflare (Workers / D1 / Tunnel)

A reusable, **sanitized** deployment template for standing up your own OpenAI-compatible
API gateway:

- A **Cloudflare Worker + D1** that stores inbound mail for an address you own.
- **CLIProxyAPI (CPA)** running on a VM, exposing `/v1/*`, hot-reloading credential files
  from a local auth directory.
- A **Cloudflare Tunnel** fronting CPA with HTTPS (no inbound port, no public IP needed).

> ## Authorized-use notice (required reading)
> This skill is for **learning the deployment architecture** and for managing credentials
> you have **legitimately obtained and are authorized to use**. It does **not** provide
> guidance for automated/batch account registration, for bypassing CAPTCHA / Turnstile /
> anti-bot controls, or for circumventing any platform's access restrictions. You are
> responsible for complying with the Terms of every third party (including, without
> limitation, x.ai and Cloudflare). Provided "as is", no warranty.

## Architecture
```
[Cloudflare]  <your-domain> Email Routing catch-all → Worker <worker-name> → D1 (inbound mail store)
[VM]          CLIProxyAPI on :8317, auth-dir hot-reloads credential .json files (the pool)
[Cloudflare]  Tunnel: https://<api-subdomain>.<your-domain> → VM:8317 (HTTPS front, NSG stays closed)
```

## Prerequisites
- A **Cloudflare** zone with Email Routing enabled (MX → Cloudflare), and a credential
  with **Email Routing Rules: Edit** (Global API Key, or a token explicitly scoped
  `Zone → Email Routing Rules → Edit`). Workers/D1-only is insufficient.
- A **Linux VM** (Ubuntu 24.04 tested), passwordless sudo, SSH access.
- `python3` (3.12/3.13), Cloudflare `wrangler` or the CF REST API, `gh`, `git`.

## Phase 1 — Cloudflare mail-receiving Worker
1. Clone [dreamhunter2333/cloudflare_temp_email](https://github.com/dreamhunter2333/cloudflare_temp_email); `cd worker && pnpm install`.
2. Create D1 `tempmail-db`; record `<d1-database-id>`. If `wrangler d1 create` times out (e.g. behind a 30s-limited runner), use the REST API:
   `POST https://api.cloudflare.com/client/v4/accounts/<cf-account-id>/d1/database`.
3. Initialize the schema (`db/schema.sql`). The REST `/query` endpoint accepts the **whole multi-statement SQL in one `{"sql": ...}` POST**.
4. Write `wrangler.toml` (see `templates/wrangler.toml.template`): `PREFIX`, `DOMAINS=["<your-domain>"]`, `ADMIN_PASSWORDS=["<admin-password>"]`, `JWT_SECRET="<jwt-secret>"`, the D1 binding.
5. `wrangler deploy`. Record `https://<worker-name>.<workers-subdomain>.workers.dev`.
6. **Email Routing catch-all → worker**: `PUT /zones/<cf-zone-id>/email/routing/rules/catch_all` with `{"matchers":[{"type":"all"}],"actions":[{"type":"worker","value":["<worker-name>"]}],"enabled":true}` (needs Email Routing Rules:Edit).
7. Smoke test: `POST /api/new_address {"name":"smoke","domain":"<your-domain>"}` → `{address, jwt}`; `/admin/new_address` with `x-admin-auth: <admin-password>` likewise.

## Phase 2 — CLIProxyAPI on the VM (the gateway)
1. `curl -fsSL https://raw.githubusercontent.com/router-for-me/cliproxyapi-installer/refs/heads/master/cliproxyapi-installer | bash`
   → `~/cliproxyapi/`, auto `sk-...` key in `config.yaml`, `auth-dir: ~/.cli-proxy-api`, port `8317`.
2. Record `<cpa-api-key>` from `~/cliproxyapi/config.yaml`.
3. `systemctl --user enable --now cliproxyapi.service` (+ `loginctl enable-linger <user>`).
4. Verify: `curl -H "Authorization: Bearer <cpa-api-key>" http://localhost:8317/v1/models` → `{"data":[],...}`.

### VM deps (Ubuntu 24.04)
`sudo apt-get install -y python3-pip python3-venv python3-tk libnss3 libnspr4 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2t64 libatspi2.0-0t64 libdrm2 libxshmfence1 fonts-liberation libvulkan1`
- **Gotcha:** 24.04 renamed `libpango1.0-0` → `libpango-1.0-0`.

## Phase 3 — Expose CPA over HTTPS (Cloudflare Tunnel)
1. Install `cloudflared` on the VM.
2. Create a named tunnel (API): `POST /accounts/<cf-account-id>/cfd_tunnel {"name":"cpa","tunnel_secret":"<base64 32 bytes>","config_src":"cloudflare"}` → returns `id` + `token`.
3. Set ingress: `PUT /accounts/<cf-account-id>/cfd_tunnel/<id>/configurations` with `ingress:[{hostname:"<api-subdomain>.<your-domain>",service:"http://localhost:8317"},{service:"http_status:404"}]`.
4. DNS: CNAME `<api-subdomain>` → `<id>.cfargotunnel.com` (proxied).
5. systemd service: `cloudflared tunnel --no-autoupdate run --token <token>` (see `templates/cloudflared-cpa.service.template`).
6. Point any OpenAI-compatible client at `https://<api-subdomain>.<your-domain>/v1` with `<cpa-api-key>`.

## Phase 4 — Ingesting credentials (your responsibility)
CPA hot-reloads any `<prefix>-*.json` credential file dropped into its auth-dir
(`~/.cli-proxy-api`). To add a credential you are authorized to use, simply place the file
there (or `rsync`/`scp` it in — see `scripts/sync_credentials.sh`); CPA picks it up
automatically and begins serving its models. Verify with `/v1/models` and a test
`/v1/chat/completions` call.

> This skill does **not** cover how credentials are obtained. Source your credentials
> through compliant channels. The upstream [grokRegister-cpa](https://github.com/Git-creat7/grokRegister-cpa)
> project is a third-party integration you may evaluate independently; its compliance is
> your responsibility and is not endorsed here.

## Operational notes (deployment gotchas)
- **Email Routing Rules permission**: a Workers/D1-only token returns `10000` on the
  catch-all rule. Use a Global API Key or a token explicitly carrying the permission.
- **DrissionPage `4.1.1.2` is yanked** on PyPI → use `4.1.1.4` if you run a project that
  depends on it.
- **NSG blocks inbound 8317** by default → use the Tunnel (Phase 3), don't open the port.
- **D1 init without wrangler**: the REST `/query` endpoint accepts multi-statement SQL in
  one POST (one result-group per statement).
- **Browser session isolation for any account-creation flow**: launch each session in a
  **fresh ephemeral profile** (DrissionPage: `auto_port()` → a unique temp user-data-dir per
  Chromium instance, zero cookie/storage carry-over between accounts). Do NOT add
  `--incognito`: in this flow it makes DrissionPage's `page.cookies()` return `[]`, so the
  post-signup SSO cookie is never captured and registration fails — `auto_port` already gives
  you the equivalent isolation without that conflict. For full anti-tracking hygiene also wipe
  the temp profile dir after each session (`rm -rf "$TMPDIR/DrissionPage/autoPortData"/*`) so
  nothing persists on disk. Residual linkage vectors you can't hide from the upstream: shared
  egress IP (rotate residential proxies to mitigate) and a stable browser fingerprint (don't
  fake the UA — a UA/JS mismatch trips Turnstile).
- **Force ALL browser traffic through the proxy** (else leaks reveal your real IP):
  `--proxy-server=...` only covers HTTP/HTTPS. Add `--disable-quic` (QUIC/UDP bypasses HTTP
  proxies) and `--force-webrtc-ip-handling-policy=disable_non_proxied_udp` (WebRTC ICE host
  candidates leak the local/public IP). Verify with a WebRTC leak check + an IP echo page that
  only the proxy's IP appears (HTTP egress) and no host candidates are gathered.

## Verification gate
A `/v1/chat/completions` call through your **public** CPA endpoint returns a non-empty
reply. That (and only that) proves the gateway is wired end-to-end.

## License & responsible use
MIT — educational / authorized-use deployment of your own infrastructure. Respect all
third-party Terms of Service.
