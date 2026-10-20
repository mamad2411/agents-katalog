---
name: django-security-settings
description: >
  Django settings security checklist for org-owned projects: DEBUG, SECRET_KEY, ALLOWED_HOSTS,
  CSRF/CORS/cookies, SSL redirect, HSTS, XSS/clickjacking middleware, and safe production
  settings modules. Use when Django security settings, django settings hardening, SECRET_KEY,
  ALLOWED_HOSTS, CSRF_COOKIE, SECURE_* flags, or production Django deploy review.
---

# Django Security Settings

## Scope And Authorization

- **In scope:** Django projects and deploy configs you own.
- **Out of scope:** Weakening security settings on systems without authorization.
- Prefer split `settings/base.py` + `production.py`; never ship `DEBUG=True` to prod.
- Redact `SECRET_KEY` and DB passwords in tickets; rotate if leaked.
- Pair with `django-csrf-middleware-tuning`, `secrets-management-hygiene`, and `code-quality-standards`.

## When To Use

- Production deploy checklist for Django.
- Audit after incident or new environment (K8s, PaaS).
- Fixing host header issues, cookie theft risk, missing HSTS.
- Separating dev and prod settings modules.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| CSRF deep dive / SPA origins | `django-csrf-middleware-tuning` |
| ORM performance | `django-orm-nplusone` |
| Async pitfalls | `django-async-views-pitfalls` |
| Secrets platform | `secrets-management-hygiene` |
| Nginx TLS edge headers | `nginx-security-headers` |
| Code quality baseline | `code-quality-standards` |

## Production checklist (core)

| Setting | Production expectation |
| --- | --- |
| `DEBUG` | `False` |
| `SECRET_KEY` | Strong, from env/secret manager, unique per env |
| `ALLOWED_HOSTS` | Explicit hosts; no `*` in prod |
| `SECURE_SSL_REDIRECT` | `True` (behind proper proxy config) |
| `SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE` | `True` |
| `SESSION_COOKIE_HTTPONLY` | `True` |
| `SESSION_COOKIE_SAMESITE` | `Lax` or stricter as designed |
| `SECURE_HSTS_SECONDS` | Non-zero when HTTPS stable (e.g. 31536000) |
| `SECURE_HSTS_INCLUDE_SUBDOMAINS` / `PRELOAD` | As appropriate |
| `SECURE_CONTENT_TYPE_NOSNIFF` | `True` |
| `SECURE_BROWSER_XSS_FILTER` | Legacy; still often set |
| `X_FRAME_OPTIONS` | `DENY` or `SAMEORIGIN` intentionally |
| `CSRF_TRUSTED_ORIGINS` | Explicit https origins |
| `ADMINS` / error reporting | Configured without leaking secrets in emails |

## Middleware (typical secure stack)

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # ... WhiteNoise etc. carefully ordered
]
```

1. Do not remove `SecurityMiddleware`, CSRF, or clickjacking without a written exception.
2. CORS: use `django-cors-headers` with explicit origins—not `*` with credentials.

## Workflow

### 1. Confirm scope and success criteria

1. Environments, TLS termination (app vs load balancer), admin exposure.
2. Success: `manage.py check --deploy` clean (or accepted exceptions); DEBUG off; secrets not in git; cookies secure.
3. Rotate keys if previous DEBUG leak possible.

### 2. Inventory settings and secrets

```bash
rg -n "DEBUG|SECRET_KEY|ALLOWED_HOSTS|SECURE_|CSRF_|SESSION_COOKIE|CORS_" -g '*settings*'
git log -p --all -S SECRET_KEY -- '*.py' 2>/dev/null | head
```

1. Ensure `SECRET_KEY` not hardcoded; load from environment.
2. Check `default` insecure keys from tutorials.

### 3. Production settings module

```python
# settings/production.py
import os
from .base import *  # noqa

DEBUG = False
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(",")

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Database SSL, CONN_MAX_AGE, etc. per platform
```

1. Never use `base.py` alone for prod with dev defaults.
2. `ALLOWED_HOSTS` from env; validate at boot.

### 4. Cookies, sessions, auth

1. Prefer database/cache sessions over persistent cookie sessions for large data.
2. Password validators enabled (`AUTH_PASSWORD_VALIDATORS`).
3. `LOGIN_RATE` limiting via axes/django-ratelimit if exposed.
4. Admin: strong passwords, MFA optional via packages, IP allowlist at edge if possible.

### 5. Files, media, and XSS surface

1. Do not serve user uploads as same origin executable content carelessly.
2. Templates auto-escape on; avoid `mark_safe` on user input.
3. `STATIC`/`MEDIA` separation; signed storage URLs when private.

### 6. Run deploy checks

```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
python manage.py check --deploy
python manage.py check --fail-level WARNING
```

1. Fix issued warnings: silence only with documented risk acceptance.
2. Confirm reverse proxy sends `X-Forwarded-Proto` correctly before forcing SSL redirect (avoid loops).

### 7. Hand off

1. Document env vars required for prod.
2. Secret rotation procedure for `SECRET_KEY` (know session invalidation effects).
3. Periodic re-run of `check --deploy` in CI against prod settings module with dummy env.
4. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| DEBUG | False in prod | True “for a minute” |
| SECRET_KEY | Env/vault | In git |
| ALLOWED_HOSTS | Explicit | `*` |
| HSTS | After HTTPS proven | HSTS on broken HTTP-only |
| CSRF | Trusted origins set | Middleware removed |
| CORS | Allowlist | `*` + credentials |
| check --deploy | In CI | Ignored forever |

## Output Checklist

- [ ] `DEBUG=False` in production settings
- [ ] `SECRET_KEY` from secrets store; not in git
- [ ] `ALLOWED_HOSTS` explicit
- [ ] SSL redirect + proxy headers correct
- [ ] Secure cookie flags set
- [ ] HSTS configured appropriately
- [ ] CSRF/CORS/clickjacking middleware present
- [ ] `manage.py check --deploy` clean or exceptions documented
- [ ] Admin and upload surfaces reviewed
- [ ] CI validates deploy settings; rotation docs exist

## Rules

- Production defaults must be fail-safe, not tutorial-dev.
- Rotate `SECRET_KEY` if exposed; understand session impact.
- Do not disable security middleware to silence errors—fix root cause.
- Coordinate CSRF details with `django-csrf-middleware-tuning`.
- Owned projects only; evidence via `check --deploy` and config review.
