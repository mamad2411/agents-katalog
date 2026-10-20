---
name: csrf-double-submit-cookie
description: >
  Implement and review the double-submit cookie CSRF pattern on owned apps:
  CSRF cookie value mirrored in header/body, cookie flags, strict equality checks,
  and limitations vs synchronizer tokens. Use when SPA/API designs prefer cookie
  + header CSRF without server-side token stores — not as the only defense for
  highly sensitive actions.
---

# CSRF Double-Submit Cookie

## Scope And Authorization

- **In scope:** Apps you own implementing or reviewing double-submit CSRF cookies.
- **Out of scope:** Bypassing CSRF on third-party sites without authorization.
- Prefer staging for cookie domain/path experiments.
- Pair with `csrf-cross-site-request-forgery` for overall threat model and `code-quality-standards`.

## When To Use

- SPA on same site as API using cookie sessions.
- Stateless app tiers that avoid server session token stores.
- Frameworks that emit `X-CSRF-Token` style headers from a readable cookie.
- Reviewing whether double-submit is sufficient given subdomain XSS risk.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full CSRF methodology | `csrf-cross-site-request-forgery` |
| Subdomain takeover / XSS | XSS / recon skills |
| CORS credentialed | `cors-credentialed-requests` |
| Session fixation | `session-fixation-management` |
| Implementation quality baseline | `code-quality-standards` |

## Pattern definition

1. Server sets a CSRF secret in a cookie (may be non-HttpOnly so JS can read — tradeoff).
2. Client copies value into `X-CSRF-Token` header (or form field) on mutating requests.
3. Server verifies **cookie value == header/body value** with constant-time compare.
4. Attacker site cannot read the cookie (same-origin policy) so cannot set matching header — **unless** XSS or broad cookie Domain scope helps them.

Variants: signed double-submit (HMAC cookie) reduces pure forgery if attacker can set cookies.

## Workflow

### 1. Confirm suitability

| Condition | Double-submit OK? |
| --- | --- |
| Clean single site, no untrusted subdomains | Often acceptable |
| `*.example.com` cookie + many apps | Risky — XSS on sibling subdomain |
| Highly sensitive banking actions | Prefer synchronizer + re-auth |
| Pure bearer API no cookies | CSRF N/A for classic pattern |

### 2. Cookie design

```http
Set-Cookie: csrf=RANDOM; Path=/; Secure; SameSite=Lax; # often not HttpOnly if JS must read
Set-Cookie: session=...; Path=/; Secure; HttpOnly; SameSite=Lax
```

1. CSRF cookie distinct from session cookie.
2. High entropy random (16+ bytes).
3. Prefer `__Host-csrf` when possible (`Secure`, `Path=/`, no Domain).
4. Rotate on login/logout.

### 3. Client wiring

```js
function readCookie(name) {
  return document.cookie.split('; ').find(r => r.startsWith(name + '='))?.split('=')[1];
}

export async function api(url, options = {}) {
  const headers = new Headers(options.headers);
  if (options.method && !/^(GET|HEAD)$/i.test(options.method)) {
    headers.set('X-CSRF-Token', decodeURIComponent(readCookie('csrf') || ''));
  }
  return fetch(url, { ...options, headers, credentials: 'same-origin' });
}
```

### 4. Server verification

```python
import hmac

def validate_csrf(cookie: str | None, header: str | None) -> bool:
    if not cookie or not header:
        return False
    return hmac.compare_digest(cookie, header)
```

1. Reject if either missing.
2. Do not accept token from query string (leaks via Referer/logs).
3. Apply to all unsafe methods; never trust method override blindly.

### 5. Signed double-submit (stronger)

```text
cookie = base64(nonce + "." + HMAC(server_secret, nonce + session_id))
header must match cookie; server re-validates HMAC
```

Binds token to session and prevents arbitrary cookie injection by attackers who can only set unsigned cookies (depends on browser cookie jar attacks — still study modern limits).

### 6. Verify

```bash
# Legitimate: session + matching header
# Missing header → 403
# Header != cookie → 403
# Cross-site form without custom header → fail (form posts cannot set arbitrary headers easily)
```

Automated tests for mismatch and absence.

### 7. Limitations to document

1. XSS bypasses double-submit (can read cookie / call API).
2. Overbroad `Domain=` cookies increase risk.
3. MITM without Secure cookies can rewrite — always `Secure`.
4. Not a replacement for authorization checks (IDOR still exists).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Compare | Constant-time equality | `==` early exit on secrets (minor) / loose parse |
| Transport | Header on POST JSON | Token only in query |
| Cookie scope | `__Host-` / tight host | `Domain=.example.com` casual |
| Entropy | CSPRNG 128-bit | Timestamp token |
| Sensitivity | + step-up MFA for wire transfers | Double-submit alone for all |

## Output Checklist

- [ ] Threat model accepts double-submit limitations
- [ ] Cookie flags and name designed
- [ ] Client sends header on mutations
- [ ] Server constant-time compare
- [ ] Login rotation of CSRF cookie
- [ ] Tests for missing/mismatch
- [ ] Subdomain cookie risk reviewed
- [ ] Sensitive actions extra controls
- [ ] Documented vs synchronizer alternative
- [ ] Residual XSS dependency noted

## Rules

- Double-submit is only as strong as XSS and cookie scope hygiene.
- Authorized apps only.
- Focus on **double-submit cookie CSRF** implementation and review.
