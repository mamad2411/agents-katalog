---
name: unifi-network
description: Build, debug and review integrations with Ubiquiti UniFi networks. Covers the official UniFi Network API (Integration API, /proxy/network/integration/v1, X-API-KEY), the Site Manager API and Cloud Connector at api.ui.com, and the unofficial classic controller API (/api/s/{site}/..., cookie login, CSRF, 2FA, WebSocket events). Use when code lists or controls UniFi devices, clients, sites, networks, WLANs, firewall policies, hotspot vouchers or guest access, power-cycles PoE ports, reads events or statistics, or talks to a UDM, UCG, UDR, Cloud Key or self-hosted UniFi controller. Not for UniFi Protect, Access or Talk APIs.
license: MIT
metadata:
  source: https://github.com/uchkunr/unifi-best-practices
---

# UniFi Network APIs

| API | Base | Auth |
| --- | --- | --- |
| Network API (official) | `https://{console}/proxy/network/integration/v1/...` | `X-API-KEY`, local key (Settings → Control Plane → Integrations) |
| Cloud Connector | `https://api.ui.com/v1/connector/consoles/{consoleId}/proxy/network/integration/v1/...` | `X-API-KEY`, Site Manager key (unifi.ui.com) |
| Site Manager | `https://api.ui.com/v1/...` | `X-API-KEY`, Site Manager key |
| Classic (unofficial) | UniFi OS: `https://{console}/proxy/network/api/s/{site}/...`; self-hosted: `https://{host}:8443/api/s/{site}/...` | Session cookie + CSRF |

## Choose the API

1. Prefer the official Network API. Use the Cloud Connector when the console is not reachable directly.
2. Use Site Manager for fleet-wide reads (hosts, sites, devices, ISP metrics).
3. Use the classic API only for what the official API lacks (block/kick/forget clients, port forwards, backups, DPI, events, legacy stats), behind one module.
4. Ask for or detect the Network version (`GET /v1/info` → `applicationVersion`). Read the spec for that version: `https://developer.ui.com/network/v{version}/openapi.json`. Do not assume an endpoint exists on older versions.

References:
- [references/official-api.md](references/official-api.md): Network API endpoints, filters, actions, vouchers, Site Manager and connector limits
- [references/classic-api.md](references/classic-api.md): classic endpoints, commands, payloads, WebSocket, Network 11 stats
- [references/client.md](references/client.md): working TypeScript clients for all three

## Rules that prevent the common bugs

**Official Network API**
- Sites are UUIDs. Resolve with `GET /v1/sites?filter=internalReference.eq('default')` and cache. Never put `default` in an official path.
- Pagination: `offset` + `limit` (default 25, max 200); response `offset`, `limit`, `count`, `totalCount`, `data`. Loop until `offset >= totalCount` or `count == 0`.
- Filters: `prop.fn(args)`, `and(...)`, `or(...)`, `not(...)`. Strings in single quotes, inner quote doubled. `like` uses `*`. Only the properties and functions listed for that endpoint are allowed. URL-encode.
- Actions are `POST {action: ...}`: device `RESTART`, port `POWER_CYCLE`, client `AUTHORIZE_GUEST_ACCESS` (`timeLimitMinutes`, `dataUsageLimitMBytes`, `rxRateLimitKbps`, `txRateLimitKbps`) and `UNAUTHORIZE_GUEST_ACCESS`.
- `/clients` lists connected clients only.
- Vouchers: `POST .../hotspot/vouchers` needs `name` and `timeLimitMinutes`; `count` 1–1000. `DELETE .../hotspot/vouchers?filter=...` deletes in bulk.
- Errors: `{statusCode, statusName, code, message, requestId}`. Branch on `statusCode`/`code`; log `requestId`.

**Cloud Connector and Site Manager**
- Connector limits: 100 requests/minute per console, 25 s per request, 10 MB per response, console firmware ≥ 5.0.3. Personal keys reach only the owner's consoles; organization keys reach all.
- Site Manager pages with `pageSize` + `nextToken`; envelope `{data, httpStatusCode, traceId, nextToken}`.
- On `429`, wait `Retry-After` seconds. Never hard-code a request rate as if it were guaranteed.
- `reportedState`, `meta`, `statistics` change shape between versions; read them defensively.

**Classic API**
- Detect UniFi OS with `GET /` without redirects: `200` = UniFi OS (login `/api/auth/login`, prefix `/proxy/network`, cookie `TOKEN`, CSRF required); redirect = self-hosted (login `/api/login`, port 8443, cookie `unifises`).
- CSRF on UniFi OS: `X-CSRF-Token` from the login response header or the `csrfToken` claim in the `TOKEN` JWT; replace it if a response carries `X-Updated-CSRF-Token`. Send on every non-GET.
- 2FA: self-hosted `api.err.Ubic2faTokenRequired` → resend with `ubic_2fa_token`; UniFi OS SSO MFA → HTTP 499 → resend with `token`. Recommend a dedicated local admin without MFA.
- Reuse one session. On `401`/`api.err.LoginRequired`, re-login once and retry once. Never loop logins (`429 AUTHENTICATION_FAILED_LIMIT_REACHED`).
- Check `meta.rc == "ok"`; errors can arrive with HTTP 200. `data` is always an array. `v2` endpoints have no envelope.
- Sites are short names (`default`). Controller-wide paths (`/api/self/sites`, `/api/stat/sites`, `/api/stat/admin`) have no `/s/{site}`.
- Commands: `POST cmd/stamgr` (`block-sta`, `unblock-sta`, `kick-sta`, `forget-sta` with `macs[]`, `authorize-guest`), `cmd/devmgr` (`restart` with `macs[]` + `reboot_type`, `power-cycle` with `mac` + `port_idx`, `set-locate`, `adopt`), `cmd/hotspot` (`create-voucher`), `cmd/sitemgr`, `cmd/evtmgr`, `cmd/backup`.
- Units: `stat/report` start/end in ms; `stat/session` in seconds; `within` in hours. `stat/event` caps at 3000 rows.
- On Network 11, `stat/report/*.site` returns empty data; use `/proxy/network/v2/api/stats/...` after checking `/v2/api/stats/source` is `MODERN`.
- For `PUT rest/...`, GET the object, change fields, send it back.
- WebSocket: `wss://{console}/proxy/network/wss/s/{site}/events` (self-hosted: `:8443/wss/s/{site}/events`) with the session cookie; reconnect and backfill on drop.

**Everywhere**
- MAC addresses are lowercase and colon-separated; normalise input.
- Consoles use self-signed certificates: trust the console certificate for console requests only. Never disable TLS verification globally.
- Do not auto-retry non-idempotent commands (restart, power-cycle) on timeout without checking state.
- Use least-privilege admins for keys and sessions; keep keys in a secret store.
