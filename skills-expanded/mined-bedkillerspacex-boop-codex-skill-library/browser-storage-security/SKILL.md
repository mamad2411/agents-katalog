---
name: browser-storage-security
description: >
  Secure browser storage choices for owned web apps: HttpOnly cookies vs localStorage/
  sessionStorage/IndexedDB, XSS token theft, cookie flags (Secure, SameSite, Path),
  partition/storage access, and sensitive data retention. Use when reviewing JWT in
  localStorage, SPA auth storage, cookie security attributes, or client-side secret
  caching — not for attacking third-party sites.
---

# Browser Storage Security

## Scope And Authorization

- **In scope:** Web applications and SPAs you own or are authorized to assess.
- **Out of scope:** Stealing tokens from third-party sites; bypassing browser security for fraud.
- Prefer staging experiments for cookie flag changes (can break SSO/embeds).
- Redact real session tokens from tickets and HAR exports.
- Pair XSS defenses with `xss-cross-site-scripting`; CSRF with session/CSRF skills; extensions with `browser-extension-security`.

## When To Use

- Choosing where to put access/refresh tokens, CSRF secrets, or PII caches.
- Findings: JWT in `localStorage`, missing `HttpOnly`/`Secure`/`SameSite`.
- Third-party iframe / Storage Access API / CHIPS partitioned cookies issues.
- Reducing XSS blast radius for session compromise.
- Mobile WebView storage quirks for owned hybrid apps.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| XSS prevention sinks/CSP | `xss-cross-site-scripting` |
| OAuth/OIDC flow design | oauth / `api-auth-and-jwt-abuse` (authz testing) |
| Extension storage | `browser-extension-security` |
| Server session stores | backend session skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Storage | JS readable? | Survives tab? | Typical use | Risk notes |
| --- | --- | --- | --- | --- |
| Cookie `HttpOnly` | No | Configurable | Session ID | Prefer for session; set flags |
| Cookie non-HttpOnly | Yes | Configurable | CSRF double-submit rare patterns | XSS can read |
| `localStorage` | Yes | Until cleared | Non-secrets UI prefs | **Never** long-lived auth secrets |
| `sessionStorage` | Yes | Tab session | Wizard state | Still XSS-readable |
| IndexedDB | Yes | Until cleared | Offline app data | Classify data; encrypt if needed |
| Memory only | Yes | Navigation-dependent | Short-lived SPA state | Lost on refresh; still XSS |

## Workflow

### 1. Confirm scope and success criteria

1. Record apps, auth model (cookie session vs bearer JWT), embed/iframe needs, mobile WebViews.
2. Success: no long-lived raw refresh/access tokens in JS storage without documented exception; cookies flagged; threat model for XSS written.
3. Note SSO IdP cookie constraints you do not control.

### 2. Inventory client storage usage

```bash
# Source search
rg -n "localStorage|sessionStorage|indexedDB|document\\.cookie|js-cookie|Cookies\\.set" -g '*.{js,ts,tsx,vue}'
rg -n "access_token|refresh_token|id_token|Authorization" -g '*.{js,ts,tsx}'
```

**Runtime (DevTools on owned staging):**

1. Application → Cookies / Local Storage / Session Storage / IndexedDB.
2. Network → check `Set-Cookie` attributes on login responses.
3. Note third-party cookies blocked vs first-party.

### 3. Baseline threat model

```text
XSS in origin → reads localStorage/sessionStorage/non-HttpOnly cookies
             → exfiltrates bearer tokens → API as user
CSRF         → browser sends cookies on cross-site requests unless SameSite/CSRF tokens
Shared device → localStorage persists after logout if not cleared
```

1. Rate blast radius: token lifetime, refresh rotation, binding to client.
2. Document whether BFF (backend-for-frontend) cookie session is feasible for SPAs.

### 4. Apply storage decisions

**Preferred pattern for first-party browser apps:**

1. **Server session** or **BFF**: opaque session cookie `HttpOnly; Secure; SameSite=Lax|Strict; Path=/;`.
2. Prefer `__Host-` prefix when host-only and path=/ and Secure: `__Host-session=...`.
3. CSRF: SameSite + anti-CSRF token for state-changing requests when needed.
4. Access tokens for APIs: stay on server; or short-lived memory-only if pure SPA must call APIs directly — with refresh in `HttpOnly` cookie (BFF) when possible.

**Cookie flag checklist:**

| Flag | Guidance |
| --- | --- |
| `Secure` | Always in production HTTPS |
| `HttpOnly` | Session/refresh cookies |
| `SameSite=Lax` | Default-ish for app cookies; `Strict` if UX allows |
| `SameSite=None; Secure` | Only for known cross-site needs |
| `Path` / `Domain` | Least scope; avoid parent domain over-sharing |
| `Max-Age` / `Expires` | Align to session policy; sliding refresh server-side |
| `Partitioned` | Consider for embedded third-party contexts (CHIPS) |

**If bearer tokens in SPA are mandatory (exception):**

1. Short access token TTL (minutes); refresh rotation + reuse detection.
2. Avoid `localStorage`; prefer memory + silent refresh via HttpOnly refresh cookie on same site.
3. Bind tokens (DPoP/mTLS) where threat model requires.
4. Aggressive CSP + Trusted Types to reduce XSS probability.
5. Clear all storage on logout; revoke server-side.

```js
// Bad
localStorage.setItem("access_token", token);

// Better direction: memory only (still XSS-visible while page open)
let accessToken = null;
export function setToken(t) { accessToken = t; }
export function getToken() { return accessToken; }
```

### 5. Verify

```bash
# Staging login; inspect Set-Cookie (names redacted in notes)
curl -sI -X POST https://staging.example/login ... | rg -i set-cookie
```

1. Confirm JS cannot read session cookie: `document.cookie` lacks it.
2. XSS lab probe (authorized): script should not obtain HttpOnly session; document residual risk for any JS-visible tokens.
3. CSRF tests for cookie sessions; cross-site image/form where applicable.
4. Logout clears client storage and server session.
5. Multi-tab logout broadcast (`storage` event or BroadcastChannel) if required.

### 6. Special contexts

| Context | Notes |
| --- | --- |
| WebViews | Cookie stores may differ; avoid file:// mixed origins |
| iFrames / embeds | Third-party cookie restrictions; Storage Access API |
| PWAs | Persistent caches — do not cache authenticated JSON in Cache API without care |
| Service workers | Can see non-HttpOnly; do not store secrets in SW caches |
| Shared workstations | Shorter idle timeout; avoid localStorage secrets |

### 7. Hand off

1. Architecture decision record: storage choice + residual XSS risk.
2. Dashboard: auth failure spikes after cookie flag changes.
3. Apply `code-quality-standards` and CSP/XSS skills for complementary controls.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Session | HttpOnly Secure cookie | JWT in localStorage for months |
| Logout | Server revoke + clear storage | Only `localStorage.clear()` client-side |
| Flags | `__Host-` + SameSite | `Domain=.example.com` on all cookies loosely |
| XSS assumption | Design as if XSS happens | “We have no XSS so storage is fine” |
| Refresh | Rotating refresh + reuse detect | Infinite refresh in localStorage |
| PII cache | Encrypted/minimized IDB | National ID in plain localStorage |

## Output Checklist

- [ ] Auth model and apps inventoried
- [ ] Storage usage search + runtime inventory done
- [ ] Threat model XSS/CSRF/shared device written
- [ ] Cookie flags verified on staging/prod
- [ ] No unjustified secrets in localStorage/sessionStorage
- [ ] Logout and revocation tested
- [ ] Embed/WebView cases considered
- [ ] Residual risks and exceptions ticketed
- [ ] Related XSS/CSP work linked
- [ ] `code-quality-standards` on code changes

## Rules

- Treat all JS-readable storage as XSS-exfiltratable.
- Prefer HttpOnly session cookies / BFF over durable bearer tokens in web storage.
- Change cookie flags carefully — test SSO and payment iframes.
- Authorized testing only; redact live tokens.
- This skill is client storage; route pure XSS sink hunting to `xss-cross-site-scripting`.
