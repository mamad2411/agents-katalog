---
name: django-csrf-middleware-tuning
description: >
  Tune and review Django CsrfViewMiddleware and CSRF-related settings: CSRF_TRUSTED_ORIGINS,
  cookie flags, header names, exemptions, and middleware order for cookie-authenticated
  browser apps. Use when Django CSRF 403s after deploy, SPA/API Origin mismatches,
  CSRF_COOKIE_* / CSRF_TRUSTED_ORIGINS hardening, @csrf_exempt audit, or DRF session-auth
  CSRF wiring on owned apps.
---

# Django CSRF Middleware Tuning

## Scope And Authorization

- **In scope:** Django applications you own; authorized security configuration changes.
- **Out of scope:** Disabling CSRF on third-party apps; teaching CSRF bypass for unauthorized attacks.
- Prefer staging verification of login/POST flows after setting changes.
- Redact session cookies from bug reports.
- Pair with `django-security-settings`, `api-auth-and-jwt-abuse` (token APIs), and `code-quality-standards`.

## When To Use

- CSRF verification failed 403 after domain/TLS/proxy change.
- SPA on `app.example.com` posting to `api.example.com` with session cookies.
- Auditing `@csrf_exempt` and `csrf_exempt` middleware holes.
- Hardening cookie flags (`Secure`, `HttpOnly`, `SameSite`) with CSRF still working.
- DRF browsable API / session authentication CSRF behavior.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full Django secure settings | `django-security-settings` |
| Pure token Bearer API (no cookies) | API auth skills; CSRF less relevant |
| XSS that steals CSRF token | `xss-cross-site-scripting` |
| Clickjacking | clickjacking skills / `X_FRAME_OPTIONS` |
| Code quality baseline | `code-quality-standards` |

## How Django CSRF works (short)

1. Middleware issues CSRF cookie (and template token).
2. Unsafe methods (POST/PUT/PATCH/DELETE) must present matching token (form field or header).
3. With modern Django, **Origin/Referer** checks interact with `CSRF_TRUSTED_ORIGINS`.
4. Session-authenticated browser clients need CSRF; pure Bearer APIs typically do not use cookie session.

## Important settings

| Setting | Role |
| --- | --- |
| `CSRF_TRUSTED_ORIGINS` | Allowed scheme+host origins for cross-origin (include `https://`) |
| `CSRF_COOKIE_SECURE` | Cookie only over HTTPS |
| `CSRF_COOKIE_HTTPONLY` | Tradeoff: JS cannot read cookie (use double-submit patterns carefully) |
| `CSRF_COOKIE_SAMESITE` | `Lax`/`Strict`/`None` (+ Secure if None) |
| `CSRF_COOKIE_DOMAIN` / `PATH` | Cookie scope across subdomains |
| `CSRF_HEADER_NAME` | Default `HTTP_X_CSRFTOKEN` ← header `X-CSRFToken` |
| `CSRF_USE_SESSIONS` | Store token in session instead of cookie |
| `CSRF_FAILURE_VIEW` | Custom 403 page |

## Workflow

### 1. Confirm scope and success criteria

1. Browser apps vs token APIs; domains; reverse proxy TLS termination.
2. Success: legitimate same-site/SPA flows pass; cross-site hostile posts fail; exemptions inventoried and minimal.
3. Rollback plan for settings module.

### 2. Inventory CSRF surface

```bash
rg -n "csrf_exempt|CsrfViewMiddleware|CSRF_|ensure_csrf_cookie|csrf_protect" --type py
rg -n "CSRF_" --type py -g '*settings*'
```

1. List `@csrf_exempt` views—justify each or remove.
2. Note frontend: forms with `{% csrf_token %}` vs SPA header injection.

### 3. Fix trusted origins and proxy

```python
# settings/production.py
CSRF_TRUSTED_ORIGINS = [
    "https://app.example.com",
    "https://admin.example.com",
]
# Behind TLS-terminating proxy:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True  # only if proxy strips/forges safely
```

1. Origins need **scheme** (`https://`) on modern Django.
2. Mis-set `ALLOWED_HOSTS` / forwarded host can break Origin matching—fix both.
3. Local dev: `http://localhost:3000` in trusted origins if SPA separates ports—**do not** copy wildcard prod.

### 4. Cookie and SPA wiring

```javascript
// SPA: read csrftoken cookie if not HttpOnly, set header
// Headers: { "X-CSRFToken": getCookie("csrftoken") }
// fetch credentials: "include" for same-site cookies
```

```python
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"  # or None for true cross-site with Secure
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = True
```

1. Cross-site cookie needs `SameSite=None; Secure` **and** careful threat model.
2. Prefer same-site deployment (reverse proxy single site) to avoid cross-site cookies.
3. Ensure `CsrfViewMiddleware` is enabled in `MIDDLEWARE` (default order near top after session).

### 5. DRF and exemptions

1. SessionAuthentication in DRF enforces CSRF for session clients—keep it for browser session APIs.
2. Token/JWT auth: CSRF not applicable the same way; still protect against XSS token theft.
3. Replace `csrf_exempt` with narrower solutions: separate unsafe webhook views with signature verification (HMAC), not global exempt.

```python
# Webhook: verify signature instead of blanket CSRF trust from browsers
# @csrf_exempt  # only if non-browser client + strong authn of body
```

### 6. Verify

```bash
# Manual: login form POST works on staging
# curl sketch — session + csrf (owned staging)
# 1) GET form → capture csrftoken cookie and token
# 2) POST with Referer/Origin allowed and X-CSRFToken
pytest -k csrf -q
```

1. Negative: cross-origin POST without token → 403.
2. After domain change: full login, logout, admin POST, SPA mutate.
3. Check that exemptions remain justified.

### 7. Hand off

1. Document domains in `CSRF_TRUSTED_ORIGINS` and who may change them.
2. Alert/monitor spike in CSRF 403s (can indicate misconfig or attack).
3. Apply `code-quality-standards` to custom failure views.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Origins | Explicit https hosts | `*` or missing scheme |
| Exempt | Rare webhooks + sig | `@csrf_exempt` on login |
| SPA | Same site or correct SameSite+header | Disable middleware |
| Cookies | Secure in prod | Secure=False on public HTTPS site |
| Proxy | Correct forwarded proto | CSRF break → disable CSRF |
| DRF session | CSRF enforced | Exempt all API |

## Output Checklist

- [ ] App topology (domains, SPA, DRF) documented
- [ ] `CSRF_TRUSTED_ORIGINS` complete with schemes
- [ ] Cookie flags set for HTTPS/SameSite
- [ ] Middleware present and ordered
- [ ] `@csrf_exempt` audited
- [ ] SPA header/cookie flow verified
- [ ] Proxy SSL headers correct
- [ ] Positive + negative tests on staging
- [ ] Owners for domain changes assigned
- [ ] Residual risk noted

## Rules

- Do not disable CSRF to fix 403s—fix origins, cookies, and proxies.
- CSRF protects cookie-based browser sessions; design APIs accordingly.
- Exemptions need compensating authentication of the request.
- Owned apps only; no unauthorized bypass techniques as the goal.
- Coordinate with overall `django-security-settings`.
