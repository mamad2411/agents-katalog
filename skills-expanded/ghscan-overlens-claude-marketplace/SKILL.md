---
name: idp-troubleshoot-auth-errors
description: >
  Symptom-driven troubleshooting guide for HTTP/transport errors when integrating the Overlens IDP —
  the "why am I getting this status code?" skill. Use this whenever a developer is BLOCKED by an
  error response from the IDP or from their own auth flow and needs to map symptom → cause → fix:
  `401 invalid_client` on `/auth/token`, `400 unauthorized_client` (grant type not allowed),
  `400 invalid_grant` (code expired/reused/PKCE mismatch), `400 invalid_redirect_uri` (redirect_uri
  doesn't exact-match), `404` on `POST /login/google` (PostHog feature flag off — older docs said 403), `429 Too Many Requests`
  (rate limit), `Max-Age=0` cookies (the ms-vs-seconds bug), missing `Set-Cookie` (forgot
  `credentials: 'include'`), and CORS failures in prod that worked in dev (`\.overlens\.com\.br$`
  origin regex). Triggers on phrases like "401 Overlens", "invalid_client Overlens", "CORS error
  Overlens", "Overlens login works locally but not in production", "429 Overlens rate limit",
  "Overlens cookie not being set", "Max-Age=0", "redirect_uri_mismatch IDP", "unauthorized_client
  Overlens", "my Overlens Google login returns 404 (or 403)", or any stuck-on-an-error-code report
  against the Overlens IDP. This skill diagnoses HTTP/transport/config failures. If instead the
  token IS received but its CONTENTS look wrong (bad `iss`/`aud`, `kid not found`, signature verify
  fails, decode the payload, algorithm-confusion, stale JWKS after rotation), prefer `idp-debug-jwt`.
  If nothing is failing yet and the dev just wants to integrate, prefer the integration skills
  (`idp-integrate-oauth-web`, `idp-auth-nextjs`, `idp-integrate-m2m`, `idp-validate-token`).
---

# Overlens IDP — Troubleshooting Auth Errors

This skill turns a **symptom** (a status code, a missing cookie, a CORS console error) into a **cause** and a **fix**. It exists because most IDP integration tickets are not "how do I integrate" — they're "I integrated and I'm stuck on this one error," and the same dozen errors recur. Each one has a precise, known cause.

> **Scope:** HTTP/transport/config failures — status codes, cookies, CORS, rate limits. If the request *succeeds* and returns a token but the **token itself** is wrong (wrong `iss`/`aud`, `kid` not found, signature fails, you need to decode the payload), that's a different problem → use `idp-debug-jwt`.

> **Canonical docs (track the code; this skill curates them):**
> `https://github.com/overlens/identity-provider/blob/main/docs/deploy/railway.md` §11 (the primary troubleshooting list), `../../references/docs/integration/frontend.md` §4 (error reference table), `../../references/docs/integration/login.md` §10 (token-endpoint errors), `../../references/docs/deploy/rate-limiting.md` (rate-limit profiles).

---

## How to use this skill: diagnose before you fix

Resist the urge to guess. The IDP's OAuth errors are deliberately precise — the `error` field in the body and the exact `Set-Cookie`/CORS headers tell you the cause. **Capture the full response first**, then read it off the table. Two minutes of `curl -i` saves an hour of speculation.

What you need before consulting the tables below:

1. **The exact status code** (401 ≠ 403 ≠ 429 — they have unrelated causes).
2. **The `error` field in the JSON body** — `invalid_client`, `unauthorized_client`, `invalid_grant`, `invalid_scope`, `invalid_redirect_uri` are *different* errors that can share a status code.
3. **Which endpoint** — `/auth/token`, `/auth/authorize`, `/login`, `/login/google`, `/token/refresh`. The same code means different things per endpoint.
4. **Response headers** (`-i` in curl, Network tab in the browser) — for cookie and CORS problems the body is empty; the headers ARE the diagnosis.
5. **Does it fail in dev, prod, or only prod?** "Works locally, breaks in production" is itself a strong signal (almost always CORS, cookie `Secure`/domain, or a missing env var).

The recipes in `references/diagnostic-recipes.md` give you copy-paste `curl`/browser commands to capture each of these. Reach for them when the cause isn't obvious from the description.

---

## Master table: symptom → cause → fix

Find your row. The detailed sections below expand the ones that bite hardest.

| Symptom | Endpoint | Most likely cause | Fix |
|---|---|---|---|
| `401` `invalid_client` | `/auth/token` | Bad `client_secret`, unknown `client_id`, malformed `Authorization: Basic`, or a **public** client trying to authenticate as confidential | Verify creds + env vars; check the Basic header is `base64("id:secret")`; public clients send no secret. Response carries `WWW-Authenticate: Basic realm="IDP"` |
| `400` `unauthorized_client` | `/auth/token` | The grant you requested isn't in the client's `allowedGrantTypes` (e.g. an M2M client asking for `refresh_token`, or a code client asking for `client_credentials`) | Use a grant the client is registered for, or fix the registration |
| `400` `unsupported_grant_type` | `/auth/token` | `grant_type` is not one of `authorization_code` \| `refresh_token` \| `client_credentials` — **there is no `revoke`** | Use a supported grant. For logout, don't hit `/auth/token` at all — navigate the browser to the `GET /auth/logout` end_session_endpoint (see the integration skills) |
| `400` `invalid_grant` | `/auth/token` | Authorization code expired (~5 min), already used (single-use), or the PKCE `code_verifier` doesn't hash to the sent `code_challenge` | Don't reuse codes; exchange immediately; verify you send the *original* verifier. Restart the login flow |
| `400` `invalid_scope` | `/auth/token` | Requested a scope not in the client's `allowedScopes` | Request only registered scopes, or widen `allowedScopes` on the client |
| `400` `invalid_redirect_uri` / authorize rejects | `/auth/authorize` (via Accounts) | `redirect_uri` doesn't **exact-match** a registered URI (trailing slash, http vs https, port, path all count), or `code_challenge_method != S256`, or unknown `client_id` | Register the exact `redirect_uri`; match it byte-for-byte; use S256 PKCE. This is a *client config* error, not a user error |
| `401` (generic, no `error` discrimination) | `/login`, `/auth/authorize` | Wrong email or password | Show the generic "Email or password incorrect" — never reveal which |
| `401` | `/token/refresh`, `/auth/token` (refresh) | Refresh token expired, already used (rotation invalidates the previous one), or the user is blocked (`blockedAt != null`) | Redirect to login. A rotated refresh token is single-use — store the newest one |
| `404` | `POST /login/google` | PostHog feature flag `idp_google-auth` is off — or `POSTHOG_API_KEY` is unset, so flags fail closed and the guard answers 404 Not Found | Enable the flag in PostHog; hide the Google button until it's on |
| `429` + `Retry-After` | any auth endpoint | Rate limit hit for that endpoint's profile | Back off using `Retry-After`. See the rate-limit profiles section — and if it's M2M, you forgot to cache the token |
| `Max-Age=0` on `Set-Cookie` (user logged out instantly) | `/login`, `/token/refresh` | `maxAge` passed in **seconds** instead of **milliseconds** — Express divides by 1000, so `900` → `Max-Age=0` | Use ms: `900_000` (access), `2_592_000_000` (refresh). This is an IDP-side bug; see detail below |
| No `Set-Cookie` reaches the browser at all | cross-subdomain SPA calls | Missing `credentials: 'include'` on `fetch`, or you're not under `*.overlens.com.br` | Add `credentials: 'include'`; cookie-mode only works under `*.overlens.com.br` — external apps must use OAuth |
| CORS error in prod, fine in dev | any browser → IDP call | The prod origin doesn't match `\.overlens\.com\.br$`, OR you're calling the IDP directly from a frontend that should go through OAuth | Frontends must not call the IDP directly — redirect to Accounts and exchange tokens server-side |
| `5xx` | any | IDP-side failure (often Neon connection) | Show "Service unavailable, try again"; check IDP health/logs. Not a client bug |

---

## The errors that bite hardest (detail)

### `401 invalid_client` on `/auth/token` — the #1 token-exchange failure

This is the back-channel credential check failing. It is **always** one of:
- `client_id` typo or not seeded in the IDP
- wrong `client_secret` (rotated? copied with a trailing newline? wrong environment's secret?)
- the `Authorization: Basic` header is malformed — it must be `base64("<client_id>:<client_secret>")`, the two values joined by a literal colon, then base64'd as one string
- a **public** client (mobile/SPA, `isPublic:true`) trying to authenticate *as confidential* by sending a secret — public clients authenticate with PKCE, not a secret

The response always includes `WWW-Authenticate: Basic realm="IDP"`. Confirm the secret round-trips: base64-decode your Basic header and eyeball the `id:secret`. The most common real cause is an env var that's empty in the deployed environment but set locally — print it (masked) on boot.

### `400 unauthorized_client` vs `400 unsupported_grant_type` — don't conflate them

Both are 400s on `/auth/token`, but:
- **`unsupported_grant_type`**: the `grant_type` value isn't one the IDP knows. The only valid values are `authorization_code`, `refresh_token`, `client_credentials`. The classic trap is `grant_type=revoke` — **it does not exist** (RFC 7009 per-token revocation is not implemented). If you're trying to log out, you're in the wrong place: logout is NOT a `/auth/token` call. Navigate the browser (top-level, not `fetch`) to the `GET /auth/logout` end_session_endpoint with `client_id` + a registered `post_logout_redirect_uri` + `state` → see the integration skills (`idp-integrate-oauth-web`, `idp-auth-nextjs`).
- **`unauthorized_client`**: the grant exists, but *this client* isn't allowed to use it. An M2M client asking for `refresh_token`, or a web client asking for `client_credentials`, gets this. Fix the request or the client's `allowedGrantTypes`.

### `400 invalid_redirect_uri` — exact match, every character counts

The IDP validates `redirect_uri` against the registered list by **exact string match**. These are all *different* URIs and three of them will be rejected if only one is registered:
- `https://app.overlens.com.br/api/auth/callback`
- `https://app.overlens.com.br/api/auth/callback/` ← trailing slash
- `http://app.overlens.com.br/api/auth/callback` ← http
- `https://app.overlens.com.br:443/api/auth/callback` ← explicit port

Register the URI your code actually sends, byte-for-byte. In dev that's usually `http://localhost:PORT/...`; in prod the https domain. Both must be registered. This is a configuration error surfaced to the *developer*, never shown to the end user.

### `404` on `POST /login/google` — it's a feature flag, not a missing route

A 404 here is almost never a wrong URL. The endpoint is gated by the PostHog feature flag `idp_google-auth`; when the flag is off — or PostHog isn't configured (`POSTHOG_API_KEY` unset), since flags fail closed — the guard answers **404 Not Found** for every call. Check the PostHog panel; in the meantime hide the Google button. (This gate applies to the cookie-mode `/login/google` only. The OAuth-path Google endpoints — `/auth/authorize/google`, `/auth/signup/google` — are NOT behind this flag; see `../../references/docs/integration/login.md` and `../../references/docs/integration/signup.md`.)

### `429 Too Many Requests` — which profile did you hit?

Rate limits are **per IP** (per **client** for M2M reads) and per-route. Every `429` carries a standard `Retry-After` header (seconds). Effective limits:

| Route | Limit | Window |
|---|---|---|
| `POST /login`, `POST /login/google`, `POST /auth/authorize`, `POST /auth/authorize/google` | 10 req | 60 s |
| `POST /token/refresh`, `POST /auth/token` (all grants) | 30 req | 60 s |
| `POST /signup`, `POST /auth/signup` | 10 req | 60 s |
| `PATCH /auth/me`, deactivate/delete, avatar | 20 req | 60 s |
| `GET /auth/me/email` | 10 req | 60 s |
| `POST /auth/me/password` | 5 req | 15 min |
| `GET /users/:sub` (M2M, per client) | 600 req | 60 s |
| Any other route (discovery, JWKS, revoke, admin…) | 60 req | 60 s |

Counting is **per route** — blowing the `/login` bucket does not affect `/auth/token`.

Common triggers and fixes:
- **CI / smoke tests** doing repeated logins from one IP blow the 10/min `/login` bucket (per-IP, so one CI runner = one bucket). Reuse the session (refresh instead of re-login), use a staging IDP with `IDP_RATE_LIMIT_DISABLED=true`, or allowlist the CI IP at Cloudflare.
- **M2M service hitting `429` on `/auth/token`** = you're fetching a token per request instead of caching it. A cached 5-min token hits the IDP ~once per 5 min, nowhere near 30/min. → `idp-integrate-m2m`.
- **Note:** the throttler is **active in every environment** (since 2026-07-14 — before that it was disabled everywhere). A `429` is reproducible locally. Kill-switch: `IDP_RATE_LIMIT_DISABLED=true` (ops/load-test only). Redis (`REDIS_URL`) is required for the count to be global across instances.

### `Max-Age=0` cookies — the milliseconds bug

If a user is logged out the instant they log in, inspect the `Set-Cookie` header: `Max-Age=0` means the browser was told to delete the cookie immediately. Cause: Express's `res.cookie({ maxAge })` expects **milliseconds** and divides by 1000 internally, so `maxAge: 900` becomes `Max-Age=0`. The IDP uses `900_000` (15 min) and `2_592_000_000` (30 d) on purpose. This is an **IDP-side** regression — if you see it in production after a change, that change broke the cookie helper. Verify:

```bash
curl -i -X POST https://idp.overlens.com.br/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"u@x.com","password":"x"}' | grep -i max-age
# Expected: Max-Age=900 and Max-Age=2592000  (NOT Max-Age=0)
```

### Cookies missing / CORS fails in prod but not dev

These two travel together because both are about cross-origin browser rules:

- **No `Set-Cookie` applied**: a `fetch` to the IDP without `credentials: 'include'` won't store or send cookies. But step back — **cookie-mode only works for SPAs hosted under `*.overlens.com.br`**. The cookies are scoped to `.overlens.com.br`; an app on any other domain will never receive them. If that's you, you shouldn't be calling the IDP directly at all → use OAuth (`idp-integrate-oauth-web` / `idp-auth-nextjs`).
- **CORS error only in production**: the IDP allows browser origins matching `\.overlens\.com\.br$`. A prod frontend on a different domain fails the preflight even though `localhost` worked in dev (dev CORS is permissive). The real fix is usually architectural: **frontends should never call the IDP directly** — they redirect to `accounts.overlens.com.br` and let their own server-side BFF do the token exchange. If you're hitting CORS on the IDP from browser JS, that call is in the wrong place.

---

## "Works locally but breaks in production" — the prod-only checklist

A large share of tickets are this. When dev is green and prod is red, walk these in order:

1. **Missing/empty env var in prod** — `IDP_CLIENT_SECRET`, `IDP_BASE_URL`, `GOOGLE_CLIENT_ID`, etc. set locally but not in Railway. Causes `401 invalid_client`, wrong discovery URLs, or `404` Google. Print them masked on boot.
2. **CORS origin** — prod origin not under `\.overlens\.com\.br$` (see above).
3. **Cookie `Secure`/`Domain`** — prod is HTTPS so `Secure` cookies work, but if `IDP_COOKIE_DOMAIN` is wrong the `Domain=.overlens.com.br` attribute is missing and cookies go host-only.
4. **`redirect_uri` not registered for the prod domain** — dev registered `http://localhost:...`, prod sends `https://app.overlens.com.br/...` which was never registered → `400 invalid_redirect_uri`.
5. **Rate limiting counts per instance without Redis** — the throttler is active in every environment, but without `REDIS_URL` each instance keeps its own count. Prod (multi-instance + Redis) can 429 earlier than your single local instance.
6. **PostHog flag** — Google login answers 404 in prod if the flag/env isn't set, even though dev may have bypassed it.

---

## When it's NOT this skill

Route correctly — these symptoms look adjacent but belong elsewhere:

- **Token received but rejected by your Resource Server** (`iss`/`aud` mismatch, `kid not found`, signature verify fails, "is this token even valid?", decode the payload) → `idp-debug-jwt`.
- **You haven't integrated yet, nothing is erroring** → the integration skills (`idp-integrate-oauth-web`, `idp-auth-nextjs`, `idp-auth-vite-bff`, `idp-auth-mobile`, `idp-integrate-m2m`, `idp-validate-token`).
- **Logout specifically** (the `revoke` trap, the `GET /auth/logout` end_session_endpoint, `post_logout_redirect_uri`) → the integration skills (`idp-integrate-oauth-web`, `idp-auth-nextjs`).
- **Registering an OAuth client / fixing its `allowedGrantTypes`/`redirectUris`/`allowedScopes`** → `idp-register-oauth-client`.

---

## Where the real docs live

This skill curates them; they track code changes:

- `https://github.com/overlens/identity-provider/blob/main/docs/deploy/railway.md` §11 — the primary, maintained troubleshooting list
- `../../references/docs/integration/frontend.md` §4 — front-end error reference table
- `../../references/docs/integration/login.md` §10 — token-endpoint error reference
- `../../references/docs/deploy/rate-limiting.md` — full per-route limits, per-IP/per-client keying, kill-switch

When a fix here disagrees with those, the docs win — re-sync this skill.

---

## File map of this skill

```
idp-troubleshoot-auth-errors/
├── SKILL.md                          (this file — triage + symptom→cause→fix tables)
└── references/
    └── diagnostic-recipes.md         (copy-paste curl/browser commands to capture the symptom)
```

Read `references/diagnostic-recipes.md` when the cause isn't obvious from the report and you need to reproduce/capture the exact response.
