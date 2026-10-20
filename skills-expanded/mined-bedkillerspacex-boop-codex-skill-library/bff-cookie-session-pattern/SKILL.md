---
name: bff-cookie-session-pattern
description: >
  Backend-for-Frontend (BFF) cookie session pattern for owned SPAs: HttpOnly Secure
  SameSite cookies, CSRF defenses, token relay to APIs without storing access tokens
  in localStorage, refresh handling, and logout. Use when securing browser apps with
  a BFF — not for stealing sessions or bypassing third-party auth.
---

# BFF Cookie Session Pattern

## Scope And Authorization

- **In scope:** Web apps and BFFs you own (SPA + backend on controlled domains).
- **Out of scope:** Session fixation/hijacking against systems without authorization.
- Misconfigured cookies cause account takeover risk — test carefully in staging.
- Pair with `code-quality-standards`; OAuth/OIDC deep dives with API auth skills as needed.

## When To Use

- SPA currently stores access tokens in `localStorage` / JS-readable cookies.
- Introducing a BFF that holds tokens server-side and issues browser session cookie.
- Hardening CSRF, cookie flags, and CORS for credentialed requests.
- Implementing silent refresh and logout/revocation.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic API JWT abuse testing | `api-auth-and-jwt-abuse` (authorized) |
| Account takeover methodology | `account-takeover-methodology` |
| Axum middleware layers | `axum-tower-layers` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| BFF | Browser-facing backend; session authority |
| Session cookie | Opaque ID; HttpOnly; Secure; SameSite |
| Token store | Server-side session → refresh/access tokens |
| CSRF | SameSite + anti-CSRF token for state-changing |
| APIs | Trust BFF identity or token exchange; not raw browser tokens |
| Tooling | Browser devtools, OWASP cheatsheets, auth libraries |

## Workflow

### 1. Confirm scope and success criteria

1. Domains (SPA, BFF, API), IdP, session TTL, authorization.
2. Success: no tokens in JS storage; authenticated API calls via cookie session work; CSRF blocked.
3. Logout clears server session and cookie.

### 2. Inventory current auth

```bash
rg -n "localStorage|sessionStorage|access_token|document.cookie" --glob '*.{ts,tsx,js,jsx}'
# Check Set-Cookie flags in responses
curl -sI https://bff.example/login/callback | rg -i set-cookie
```

1. Note OAuth authorization code flow vs implicit (avoid implicit).
2. CORS config: `Access-Control-Allow-Credentials`.
3. Existing CSRF protections.

### 3. Baseline threat model

| Threat | Control |
| --- | --- |
| XSS token theft | HttpOnly session; no tokens in JS |
| CSRF | SameSite=Lax/Strict + CSRF token on mutating requests |
| Session fixation | Rotate session ID at login |
| XSS still bad | CSP + encoding (defense depth) |
| Cookie replay | Short TTL, bind IP/UA carefully if used |

### 4. Implement BFF pattern

```text
Browser                    BFF                         IdP / API
   |-- OAuth login ------->|--- code exchange --------->|
   |<- Set-Cookie session -|<- tokens (server store) ---|
   |-- API proxy + cookie ->|--- attach access token ---> API
   |<- JSON ----------------|<-- response ---------------|
```

**Cookie flags (typical):**

```http
Set-Cookie: session=...; Path=/; HttpOnly; Secure; SameSite=Lax; Priority=High
```

1. Session store: server memory/Redis with encryption at rest; store refresh token hashed/encrypted.
2. SPA calls **same-site** BFF routes with `credentials: 'include'`.
3. CSRF: double-submit or synchronizer token for POST/PUT/DELETE; exempt safe GETs carefully.
4. Refresh: BFF refreshes access token server-side; browser never sees refresh token.
5. Logout: delete server session; `Set-Cookie` max-age=0; revoke refresh at IdP if supported.
6. CORS: explicit origins (not `*`) when credentials true.

```javascript
// Browser fetch pattern
await fetch("https://bff.example/api/me", {
  credentials: "include",
  headers: { "X-CSRF-Token": csrfToken },
});
```

### 5. Verify with evidence

1. Devtools Application: no access token in localStorage.
2. Cookie has HttpOnly/Secure/SameSite.
3. Cross-site form POST without CSRF fails.
4. XSS lab (authorized) cannot `document.cookie` read session (HttpOnly).
5. Expired session returns 401; refresh path works once.

### 6. Observe and harden

1. Metrics: session create/destroy, CSRF failures, refresh errors.
2. Alerts on mass session creation (credential stuffing).
3. Rotate signing keys for session IDs if using JWT sessions (prefer opaque IDs).

### 7. Hand off

1. Domain and cookie matrix (prod/staging).
2. CSRF client integration guide.
3. Incident: revoke sessions by user id.

## Cookie Attribute Cheatsheet

| Attribute | Recommendation |
| --- | --- |
| HttpOnly | Always for session |
| Secure | Always in prod |
| SameSite | Lax default; Strict if UX allows |
| Path/Domain | Narrow domain; avoid parent domain sprawl |
| __Host- prefix | When possible for extra binding |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tokens | Server-side only | Bearer in localStorage |
| CSRF | Token + SameSite | SameSite only on multi-domain legacy |
| CORS | Explicit origin allowlist | `*` with credentials |
| Session ID | Opaque random | Predictable incremental IDs |
| Logout | Server revoke | Only clear client memory |

## Output Checklist

- [ ] Token storage removed from JS
- [ ] BFF session cookie flags correct
- [ ] CSRF defense implemented
- [ ] OAuth code flow server-side exchange
- [ ] Logout/revocation works
- [ ] CORS credentials configured safely
- [ ] Tests for CSRF and unauthenticated access
- [ ] Monitoring for auth anomalies
- [ ] `code-quality-standards` applied

## Rules

- Authorized apps only.
- Never expose refresh tokens to the browser.
- HttpOnly+Secure session cookies required in prod.
- CSRF protect state-changing requests.
- XSS mitigations still mandatory.
