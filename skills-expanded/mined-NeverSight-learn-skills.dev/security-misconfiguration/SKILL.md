---
name: security-misconfiguration
description: >
  Detect, audit, and remediate Security Misconfiguration vulnerabilities (OWASP A02:2025) in
  Python web applications — especially FastAPI and Flask. Use this skill whenever a user asks
  about: hardening a Python/FastAPI/Flask app, checking for debug mode leaks, missing security
  headers, exposed API docs, hardcoded secrets, insecure cookie flags, XXE vulnerabilities, or
  any OWASP A02 misconfiguration issue. Also trigger for tasks like "security audit", "pen test
  prep", "production checklist", "find misconfigs", or "harden my app". This skill covers
  static analysis patterns, runtime checks, tooling (Bandit, OWASP ZAP), and remediation code
  snippets for each sub-category of misconfiguration.
---

# Security Misconfiguration (OWASP A02:2025)

Security Misconfiguration leapt from #5 to **#2** in the OWASP Top 10:2025, found in **3.00%
of applications** with over **719,000 occurrences**. It occurs when systems are incorrectly
configured from a security perspective — and in Python web apps, the attack surface is wide.

---

## Workflow

1. **Identify the framework** — Flask, FastAPI, or both
2. **Run static checks** — Bandit SAST scan (see Tooling section)
3. **Walk the checklist** — go through each category below, flag issues
4. **Generate a report** — list findings with CWE IDs, severity, and remediation snippets
5. **Verify fixes** — re-run Bandit + dynamic header scan after remediation

For deep dives into any single category, read:
- `references/flask-hardening.md` — Flask-specific settings and extensions
- `references/fastapi-hardening.md` — FastAPI-specific settings and middleware
- `references/security-headers.md` — Full header reference with CSP examples

---

## Checklist by Category

### 1. Debug Mode Exposed (Critical)

**Flask**
```python
# BAD — never in production
app.run(debug=True)
app = Flask(__name__, debug=True)

# BAD — environment variable
# FLASK_DEBUG=1

# GOOD
app.run(debug=False)
# or: rely on FLASK_ENV=production (Flask 2.x) / FLASK_DEBUG=0
```
- Werkzeug's interactive debugger allows **arbitrary code execution** via PIN bypass
- Bandit rule: `B201` (flask_debug_true)

**FastAPI** — has no debug mode equivalent but `/docs` and `/redoc` exposure is analogous (see §3)

---

### 2. Hardcoded Secrets (Critical)

Detect patterns:
```python
# BAD
SECRET_KEY = "supersecretkey123"
DATABASE_URL = "postgresql://user:password@host/db"
JWT_SECRET = "my-jwt-secret"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

Correct approach:
```python
import os
SECRET_KEY = os.environ["SECRET_KEY"]          # raises if missing — intentional
DATABASE_URL = os.environ.get("DATABASE_URL")  # or use python-dotenv / pydantic-settings
```

- Bandit rule: `B105`, `B106`, `B107` (hardcoded_password_*)
- Also flag: secrets committed to `.env` files checked into version control
- **Key CWEs:** CWE-526 (Sensitive Info in Env Vars), CWE-321 (Hard-coded Crypto Key)

---

### 3. Exposed API Documentation (High)

**FastAPI** — `/docs` (Swagger UI) and `/redoc` must be disabled in production:
```python
# BAD — default behaviour exposes full API schema
app = FastAPI()

# GOOD — disable in production
import os
docs_url = None if os.getenv("ENV") == "production" else "/docs"
redoc_url = None if os.getenv("ENV") == "production" else "/redoc"
app = FastAPI(docs_url=docs_url, redoc_url=redoc_url)
```

- If docs must be kept, protect behind auth middleware or IP allowlist
- Also flag: Flask `flask-swagger-ui` or `flasgger` blueprints without auth

---

### 4. Missing or Weak Security Headers (High)

Scan HTTP responses for these headers. All must be present in production.

| Header | Required Value / Pattern |
|--------|--------------------------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` |
| `Content-Security-Policy` | Domain-specific; at minimum block `unsafe-inline` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Restrict camera, mic, geolocation as appropriate |

**Flask** — use `flask-talisman`:
```python
from flask_talisman import Talisman
Talisman(app, force_https=True, content_security_policy={
    "default-src": "'self'",
    "script-src": ["'self'", "cdn.example.com"],
})
```

**FastAPI** — middleware approach:
```python
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware import Middleware
from secure import SecureHeaders  # 'secure' package

secure_headers = SecureHeaders()

@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.starlette(response)
    return response
```

**Key CWEs:** CWE-16 (Configuration), CWE-1021 (Improper Frame Restrictions)

---

### 5. Insecure Cookie Flags (High)

**Flask session cookie:**
```python
# BAD defaults — cookies sent over HTTP, accessible by JS
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = False

# GOOD
app.config.update(
    SESSION_COOKIE_SECURE=True,       # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,     # No JS access
    SESSION_COOKIE_SAMESITE="Lax",   # CSRF protection
    SESSION_COOKIE_NAME="__Host-session",  # __Host- prefix enforces additional constraints
    PERMANENT_SESSION_LIFETIME=3600,  # 1-hour expiry
)
```

**FastAPI** — when setting cookies manually:
```python
response.set_cookie(
    key="session",
    value=token,
    httponly=True,
    secure=True,
    samesite="lax",
    max_age=3600,
)
```

**Key CWEs:** CWE-614 (Sensitive Cookie Without Secure), CWE-1004 (Sensitive Cookie Without HttpOnly)

---

### 6. XML External Entity (XXE) Processing (High)

Flag any XML parsing that doesn't explicitly disable external entities:

```python
# BAD — lxml with default parser
from lxml import etree
tree = etree.parse(xml_input)  # vulnerable

# BAD — stdlib xml.etree (not vulnerable to XXE by default, but flag for review)
import xml.etree.ElementTree as ET
ET.fromstring(user_input)  # safe in CPython, but document why

# GOOD — lxml with entity expansion disabled
parser = etree.XMLParser(
    resolve_entities=False,
    no_network=True,
    load_dtd=False,
)
tree = etree.parse(xml_input, parser)

# GOOD — use defusedxml for untrusted input
import defusedxml.ElementTree as ET
tree = ET.fromstring(user_input)
```

- Bandit rule: `B405`, `B408`, `B410` (xml_* rules)
- **Key CWE:** CWE-611 (XXE)

---

### 7. Unnecessary Features / Attack Surface (Medium)

Check for services, routes, or middleware that shouldn't exist in production:

- **Werkzeug profiler** — remove `ProfilerMiddleware` in production
- **Flask shell** — disable or restrict access to `/console` routes
- **Admin interfaces** — `flask-admin`, `sqladmin` must be behind auth + IP restriction
- **Debug endpoints** — flag any route returning `sys.environ`, stack traces, or internal state
- **Unused middleware** — audit `app.wsgi_app` chain in Flask; `app.middleware_stack` in FastAPI

---

### 8. Cloud / Infrastructure Misconfiguration (Medium)

While code-level scanning can't catch all infra misconfig, flag these patterns:

- **S3 bucket names in code** — check for public ACL patterns or missing bucket policies
- **Database connection strings** — flag if connection uses `sslmode=disable`
- **CORS too permissive:**

```python
# BAD — FastAPI
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True)
# allow_origins=["*"] + allow_credentials=True is rejected by browsers but signals intent error

# GOOD
app.add_middleware(CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# BAD — Flask
from flask_cors import CORS
CORS(app, origins="*")

# GOOD
CORS(app, origins=["https://app.example.com"], supports_credentials=True)
```

**Key CWE:** CWE-16 (Configuration)

---

## Tooling

### Bandit (SAST) — Primary Tool

```bash
pip install bandit
bandit -r ./app -f json -o bandit-report.json

# Focus on misconfiguration-relevant rules:
bandit -r ./app -t B105,B106,B107,B201,B405,B408,B410
```

Key Bandit rules for A02:
| Rule | Description |
|------|-------------|
| `B105` | Hardcoded password string |
| `B106` | Hardcoded password funcarg |
| `B107` | Hardcoded password default |
| `B201` | `flask_debug_true` |
| `B405` | `import xml.etree` — recommend defusedxml |
| `B408` | `import xml.minidom` — recommend defusedxml |
| `B410` | `import lxml` — flag for XXE review |

### OWASP ZAP (DAST) — Header & Config Validation

```bash
# Docker quick scan — checks headers, misconfigured endpoints, debug info leaks
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://your-app.example.com \
  -r zap-report.html
```

ZAP automatically tests for: missing security headers, exposed stack traces, directory listing, debug endpoints, insecure cookies.

### python-dotenv + pydantic-settings (Prevention)

```bash
pip install python-dotenv pydantic-settings
```

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str              # required — fails fast if missing
    database_url: str
    debug: bool = False          # safe default
    env: str = "production"

    class Config:
        env_file = ".env"        # loaded only in dev; never committed

settings = Settings()
```

---

## Key CWEs Summary

| CWE | Description | Severity |
|-----|-------------|----------|
| CWE-16 | Configuration (catch-all) | High |
| CWE-489 | Active Debug Code | Critical |
| CWE-526 | Sensitive Info in Environment Variables | High |
| CWE-321 | Hard-coded Cryptographic Key | Critical |
| CWE-611 | XML External Entity (XXE) | High |
| CWE-614 | Sensitive Cookie Without Secure Attribute | High |
| CWE-1004 | Sensitive Cookie Without HttpOnly Attribute | High |

---

## Quick Audit Command

Run this one-liner for a fast A02 surface scan on any Python project:

```bash
bandit -r . -t B105,B106,B107,B201,B405,B408,B410 --severity-level medium \
  && grep -rn "debug=True\|FLASK_DEBUG=1\|allow_origins=\[.\"\*\"\]\|verify=False" . \
  && echo "Manual checks needed: /docs exposure, cookie flags, security headers"
```