---
name: django-security
description: Django security review — CSRF, ORM-level SQL injection (raw/extra/annotate), template injection via |safe, admin hardening, middleware ordering, settings deploy checklist, and recent Django CVE patterns.
---

# Django Security

## When to use

This skill is the Django-specific layer on top of `secure-coding`. Use it when Django gets in its own way: defaults that invite misunderstanding, ORM paths that look safe but still allow SQLi, or settings that may go wrong per environment.

Triggers on:

- A question like "review this Django app", "is our deploy safe", "what are our SECURE_ settings", "are we using CSRF correctly", "Django admin hardening".
- Presence of `manage.py`, `settings.py`, `urls.py`, `models.py`, `views.py`, Django middleware class paths in `MIDDLEWARE`, DRF `viewsets.py` or `serializers.py`.
- A PR that introduces `@csrf_exempt`, `|safe`, `mark_safe`, `.raw()`, `.extra()`, `RawSQL`, or `HttpResponse(user_input)`.
- Django version bumps that are a security release (release notes will explicitly mention fixes).
- A handoff from `security-review` where Django is in the stack.

### When NOT (handoff)

- General Python secure-coding (not Django-specific) → `secure-coding`.
- DRF as an API layer overlaps heavily with `api-security`: OAuth/JWT flow, OWASP API Top 10 belong there. Django-specific DRF foot-guns (e.g. `HyperlinkedModelSerializer` authorization bypass) stay here.
- SAST tool config (Bandit, Semgrep `p/django`) → `sast-orchestrator`.
- Dep vulns in Django or third-party packages → `cve-triage`.
- Deploy infrastructure (nginx, gunicorn, containers) → `container-hardening` / `iac-security`.
- Secrets handling (SECRET_KEY, DB creds) → `secrets-scanner`.

## Approach

Six phases. Django defaults are reasonably safe; most issues arise where you deliberately override them.

### 1. Settings and deploy checklist

`python manage.py check --deploy` is a Django-built-in checker. Always run it, fix every warning before production. Not sufficient, but necessary.

Critical settings:

- **`DEBUG = False`** in production. `DEBUG = True` leaks stack traces, env vars, SQL queries: full app-internal exposure. No exceptions.
- **`ALLOWED_HOSTS`** explicit. Wildcard `['*']` in prod is a Host-header-injection vector.
- **`SECRET_KEY`** from environment or vault, never in source. Rotation schedule on suspicion of leak. See `secrets-scanner`.
- **`SECURE_SSL_REDIRECT = True`**, **`SECURE_HSTS_SECONDS >= 31536000`** with `SECURE_HSTS_INCLUDE_SUBDOMAINS` and `SECURE_HSTS_PRELOAD`, **`SESSION_COOKIE_SECURE = True`**, **`CSRF_COOKIE_SECURE = True`**. Only where TLS is guaranteed.
- **`SESSION_COOKIE_HTTPONLY = True`** (default), **`SESSION_COOKIE_SAMESITE = 'Lax'`** or `'Strict'`.
- **`SECURE_CONTENT_TYPE_NOSNIFF = True`**, **`SECURE_REFERRER_POLICY`** explicitly set.
- **`CSRF_TRUSTED_ORIGINS`** with full scheme+host where relevant (Django 4+).
- **`PASSWORD_HASHERS`** with Argon2 first, then PBKDF2 as fallback. Requires `django-argon2` package.
- **Database**: `ATOMIC_REQUESTS` where appropriate, separate DB user with least privilege (no DROP/CREATE rights for the web user).

### 2. ORM and SQL injection

Django's ORM parameterizes by default. SQLi arises in places where you step out of it:

- **`.raw()`**: string formatting in the raw queryset gives SQLi. Use placeholder params: `Model.objects.raw('SELECT * FROM app_model WHERE name = %s', [name])`. Not `f'SELECT ... WHERE name = {name}'`.
- **`.extra()`**: deprecated, still widely used. `where=`, `params=`, `select=` can be abused. Prefer to replace with `Func()`, `RawSQL()` with params, or `annotate()` with `ExpressionWrapper`.
- **`RawSQL`**: parameter list MUST be used. The example in the Django docs shows `RawSQL("select col from sometable where othercol = %s", (someparam,))`. Follow that.
- **`QuerySet.annotate()` / `aggregate()` with dict keys from user input**. Historically vulnerable (see CVE-2022-28346, SQL injection via column aliases in dict keys). Reviewer rule: dict keys in annotate/aggregate never come from user input, hardcode them.
- **Order-by with user input**. `.order_by(request.GET.get('sort'))` lets users pick columns. Allowlist permitted column names.
- **`__in=` with large lists** from user input: not SQLi but still DoS. Cap list size.

Django CVE references (within a 3-year window, verify against release notes):

- CVE-2022-28346: QuerySet.annotate/aggregate SQLi via dict keys. Fixed in Django 2.2.28, 3.2.13, 4.0.4. Canonical example of "the ORM is safe, except when ..."
- CVE-2023-43665: Truncator DoS via crafted HTML. Fixed in 3.2.22, 4.1.12, 4.2.6.
- More recent CVEs in the Django 4.2/5.x series: `[verify against https://docs.djangoproject.com/en/dev/releases/security/]` for the current window.

### 3. Template injection and XSS

Django templates have **autoescape on by default**. XSS arises when you turn it off.

- **`{{ user_input|safe }}`**: renders raw HTML. Apply only to content you have controlled yourself (e.g. sanitized HTML from a trusted bleach call), never on unwashed user input.
- **`{% autoescape off %}`**: disables escaping for the entire block. Rarely needed, review every use.
- **`mark_safe(s)`** in Python code: same effect as `|safe`. If `s` contains user input or is composed of user input, you have XSS.
- **`format_html('<a href="{}">', user_url)`**: URL attributes are a separate problem. `javascript:` URLs via `href` bypass HTML escaping. Validate `user_url.startswith(('http:', 'https:'))`.
- **Server-side template injection**: if you render templates yourself with user-controlled template strings (`Template(user_input).render(...)`), you get SSTI with potential RCE. Never do this.
- **`HttpResponse(user_input)`**: bypasses template autoescape because there is no template. Use `render()` or encode explicitly.

### 4. CSRF model

Django's `CsrfViewMiddleware` is on by default for POST/PUT/PATCH/DELETE.

- **`@csrf_exempt`**: turns CSRF off for a specific view. Use only on endpoints where CSRF structurally cannot work (e.g. webhook receivers with signature verification). Every `@csrf_exempt` in a PR is a security-review moment.
- **DRF and CSRF**: DRF `SessionAuthentication` enforces CSRF, `TokenAuthentication`/`JWT` does not (stateless). Mixed auth modes: be explicit about which endpoints use which model.
- **`CSRF_COOKIE_HTTPONLY`**: default `False`, which is needed for JS to read the token. Do not change unless you have a custom CSRF setup.
- **`CSRF_TRUSTED_ORIGINS`**: stricter interpretation since Django 4 (full origin with scheme). Without correct config: legitimate POSTs are 403-rejected.

### 5. Auth, session, and admin

- **`django.contrib.auth.password_validation`**: never remove. Length check, common-password check, attribute-similarity check must be active.
- **`AUTHENTICATION_BACKENDS`**: custom backends are a classic foot-gun. Every custom backend must be timing-safe (identical response time for "user does not exist" vs. "wrong password").
- **Admin interface**:
  - **`ADMIN_URL`** not `/admin/` (security through obscurity + bot-traffic reduction).
  - **IP allowlist** via middleware or reverse proxy for `/admin/*`.
  - **2FA** required via `django-otp` or `django-allauth` with TOTP.
  - **`is_staff` and `is_superuser`** assigned carefully. Superuser status only for a small team.
- **Session management**: `SESSION_COOKIE_AGE` reasonably short, `SESSION_EXPIRE_AT_BROWSER_CLOSE` where appropriate, session rotation on privilege change (automatic on login since Django 2+).
- **django-allauth/django-axes** for rate-limiting on login (brute-force prevention). Native Django has no rate limiter on auth endpoints.

### 6. Misc and verification-loop

- **File uploads**: `FileField` does not validate content type. `UploadedFile.content_type` is set by the client. Validate magic bytes, whitelist extensions, store outside web root.
- **Open redirects**: `redirect(request.GET.get('next'))` without validation is an open redirect. Django has `url_has_allowed_host_and_scheme(url, allowed_hosts=...)` for this purpose.
- **Middleware order**: `SecurityMiddleware` belongs high, `CsrfViewMiddleware` before `AuthenticationMiddleware`, custom middleware with side effects close to the view. Wrong order can produce subtle bypasses.
- **django-admin `check` with `--deploy`** required in CI.
- **Bandit + Semgrep `p/django`** as the SAST layer, see `sast-orchestrator`.

Verification-loop: Layer 1 scope (settings file + urls + middleware stack all walked through?), assumptions (autoescape on everywhere, no `|safe` on user input?), gaps (DRF views included in the same review?). Layer 2 specifically on CVE IDs (verify against Django release notes, not memory), security-setting names (Django sometimes changes default values per major version), admin-hardening claims backed by concrete middleware/package.

## Output

Follow the `security-review` report format, with a Django-specific scan summary at the top:

```
Django security review — <app/project>
Django version: <x.y.z> (latest security release: <...>)

Deploy checklist (python manage.py check --deploy):
  Warnings: N → resolved/open
  DEBUG in prod:        <False | FINDING>
  ALLOWED_HOSTS:        <explicit | wildcard — FINDING>
  SECURE_* settings:    <complete | gaps>
  PASSWORD_HASHERS:     <Argon2 first | PBKDF2 default>

Code patterns:
  @csrf_exempt:         <N, location, reason>
  |safe / mark_safe:    <N, on user input? FINDING>
  .raw() / .extra():    <N, parameterized?>
  order_by(user input): <list>

Admin:
  URL not /admin/:      <yes/no>
  IP restriction:       <yes/no>
  2FA on staff:         <yes/no>

Version check:
  On latest security release: <yes | N months behind>
  CVE relevance:              <handoff to cve-triage>

Findings (severity-sorted, follow security-review format)
Verification-loop: ...
```

## References

- Django Security — [https://docs.djangoproject.com/en/stable/topics/security/](https://docs.djangoproject.com/en/stable/topics/security/). Official security topic page.
- Django Deployment Checklist — [https://docs.djangoproject.com/en/stable/howto/deployment/checklist/](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/). Exactly what `manage.py check --deploy` checks.
- Django Security Releases — [https://docs.djangoproject.com/en/dev/releases/security/](https://docs.djangoproject.com/en/dev/releases/security/). Canonical CVE log per version.
- Django Admin Security — [https://docs.djangoproject.com/en/stable/ref/contrib/admin/#adminsite-objects](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#adminsite-objects). Admin configuration reference.
- OWASP Django Security Cheat Sheet — [https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html).
- Django Rest Framework — Authentication — [https://www.django-rest-framework.org/api-guide/authentication/](https://www.django-rest-framework.org/api-guide/authentication/). DRF auth-mode matrix.
- django-axes — [https://django-axes.readthedocs.io/](https://django-axes.readthedocs.io/). Login-attempt rate-limiting.
- django-otp — [https://django-otp-official.readthedocs.io/](https://django-otp-official.readthedocs.io/). 2FA on admin.

## Categories

- appsec
