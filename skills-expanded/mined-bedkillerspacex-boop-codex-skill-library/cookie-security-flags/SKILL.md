---
name: cookie-security-flags
description: >
  Set and audit browser cookie security attributes for owned web apps: Secure,
  HttpOnly, SameSite (Strict/Lax/None), Path, Domain, Max-Age/Expires, Priority,
  and interaction with CSRF and XSS. Use as the primary cookie-hardening skill;
  use cookie-prefix-host-secure for __Host-/__Secure-, cookie-partitioned-chips for
  CHIPS, and cookie-consent-mode-ops for marketing consent — not for stealing cookies
  from third parties.
---

# Cookie Security Flags

## Scope And Authorization

- **In scope:** applications and IdPs you own; authorized security reviews.
- **Out of scope:** session hijacking on systems without authorization.
- Cookie flag changes can break SSO, embeds, and native apps — test thoroughly.
- Pair with CSRF defenses, XSS prevention, and `clear-site-data-api` for logout.

## When To Use

- Reviewing `Set-Cookie` on login/session/CSRF cookies.
- Fixing missing Secure/HttpOnly or wrong SameSite.
- Tokens: Set-Cookie, Secure, HttpOnly, SameSite, Domain, Path, session cookie.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| `__Host-` / `__Secure-` details | `cookie-prefix-host-secure` |
| Partitioned / CHIPS | `cookie-partitioned-chips` |
| CMP / Consent Mode | `cookie-consent-mode-ops` |
| Clear-Site-Data | `clear-site-data-api` |
| XSS / CSRF methodology | respective skills |

## Flag Matrix

| Attribute | Recommendation (session) | Notes |
| --- | --- | --- |
| `Secure` | Always on HTTPS apps | Required for SameSite=None |
| `HttpOnly` | Yes for session tokens | Blocks JS access (XSS still bad) |
| `SameSite=Strict` | High security apps | May break return from external pay |
| `SameSite=Lax` | Default good balance | Top-level GET navigations send cookie |
| `SameSite=None` | Cross-site needs only | Must Secure; CSRF careful |
| `Path` | As narrow as practical | `/` common for apps |
| `Domain` | Prefer host-only (omit Domain) | Wide Domain increases CSRF/XSS blast |
| `Max-Age` / `Expires` | Align with session policy | Idle timeout server-side still required |
| `Partitioned` | Embed cases | See CHIPS skill |

## Workflow

### 1. Confirm scope and success

1. Cookie inventory: session, refresh, CSRF, prefs, marketing.
2. Success: session cookies not readable by JS; not sent on unwanted cross-site POSTs; HTTPS only.
3. Map cross-site flows (OAuth return, payments, embeds).

### 2. Capture baseline

```bash
curl -sI -c /tmp/cj -b /tmp/cj -X POST https://app.example.com/login \
  -d 'user=test&pass=test' | rg -i set-cookie
```

DevTools → Application → Cookies: check checkboxes for Secure/HttpOnly/SameSite.

### 3. Apply session cookie hardening

```http
Set-Cookie: __Host-session=...; Secure; HttpOnly; Path=/; SameSite=Lax; Max-Age=3600
```

```javascript
res.cookie("session", token, {
  secure: true,
  httpOnly: true,
  sameSite: "lax",
  path: "/",
  maxAge: 3600_000,
});
```

1. Prefer **server-side session store** + opaque cookie over giant JWT in cookie when possible.
2. Refresh tokens: stricter (Strict, shorter, separate path) if used.
3. CSRF: SameSite helps but not complete for all cases — synchronizer tokens for state-changing requests.

### 4. SameSite decision tree

| Flow | SameSite |
| --- | --- |
| App only, no cross-site POST needed | `Lax` or `Strict` |
| OAuth/payment return top-level GET | `Lax` usually OK |
| Cookie needed in cross-site XHR/fetch | `None; Secure` (+ CSRF defenses) |
| Third-party iframe | `None; Secure` + consider `Partitioned` |

### 5. Domain / Path pitfalls

1. `Domain=example.com` shares with subdomains — XSS on blog.example.com can impact app.
2. Prefer host-only cookies for `app.example.com`.
3. Path-segment cookies can surprise; document multi-app hosting.

### 6. Verify

| Test | Expect |
| --- | --- |
| `document.cookie` in console | Session value **absent** if HttpOnly |
| HTTP site | Secure cookie not set/sent |
| Cross-site POST from evil lab | Cookie not sent if Lax/Strict |
| Login → logout | Cookie cleared + server revoke |
| Prefs cookie | May omit HttpOnly intentionally |

### 7. Hand off

1. Cookie table in security docs.
2. CI/header scan for session cookies missing flags (where feasible).
3. Link prefix/CHIPS/consent skills for specialized cases.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Session | Secure + HttpOnly + Lax/Strict | No flags on session ID |
| Domain | Host-only | `Domain=.company.com` for all apps |
| Cross-site | None only when required | None by default “for convenience” |
| Lifetime | Server idle timeout + Max-Age | Eternal cookie = eternal session |
| XSS | Still fix XSS | Rely on HttpOnly alone |

## Output Checklist

- [ ] All cookies classified (session vs other)
- [ ] Session: Secure + HttpOnly + appropriate SameSite
- [ ] Domain/Path minimized
- [ ] Cross-site flows tested
- [ ] Logout clears client + server
- [ ] CSRF strategy documented with SameSite
- [ ] Prefixes/CHIPS applied where relevant
- [ ] Residual risks (subdomain XSS) noted

## Rules

- Owned apps only; stage SameSite changes.
- Server-side session invalidation remains mandatory.
- Evidence from Set-Cookie captures and browser tests.
- Primary cookie hardening skill; specialized siblings for prefix/CHIPS/consent.
