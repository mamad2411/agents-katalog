---
name: owasp-checklist
description: "When to activate: OWASP, security checklist, injection, XSS, IDOR, SSRF, security misconfiguration, vulnerability"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: security
  language: security
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# OWASP Top 10 2021 Checklist

## A01 — Broken Access Control

```python
# BAD: user can access any order by guessing ID
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return db.query(Order).get(order_id)  # no ownership check!

# GOOD: enforce ownership
@app.get("/orders/{order_id}")
def get_order(order_id: int, current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id  # IDOR prevention
    ).first()
    if not order:
        raise HTTPException(status_code=404)
    return order
```

## A02 — Cryptographic Failures

```python
# BAD: MD5/SHA1 for passwords, unencrypted PII
import hashlib
hashed = hashlib.md5(password.encode()).hexdigest()  # NEVER

# GOOD: bcrypt/argon2
from passlib.hash import argon2
hashed = argon2.hash(password)
verified = argon2.verify(password, hashed)

# Encrypt sensitive fields at rest
from cryptography.fernet import Fernet
key = Fernet.generate_key()  # store in secrets manager, not code
cipher = Fernet(key)
encrypted_ssn = cipher.encrypt(ssn.encode())
```

## A03 — Injection

```python
# BAD: SQL injection via f-string
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# GOOD: parameterized query (all ORMs do this by default)
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

# BAD: shell injection
import subprocess
subprocess.run(f"convert {filename} output.pdf", shell=True)

# GOOD: no shell, argument list
subprocess.run(["convert", filename, "output.pdf"], shell=False)

# NoSQL injection prevention
# BAD: MongoDB with user-supplied operator
db.users.find({"password": request.json["password"]})
# If password = {"$ne": ""} → bypasses auth!
# GOOD: validate and cast types
from pydantic import BaseModel
class LoginForm(BaseModel):
    email: str
    password: str  # ensures string, not object
```

## A04 — Insecure Design

- Threat model during design, not after
- Rate-limit sensitive endpoints (login, register, password reset)
- Multi-factor authentication for privileged actions
- Separate admin API from public API

## A05 — Security Misconfiguration

```python
# Checklist:
# - Debug mode OFF in production
# - Default credentials changed
# - Unnecessary features disabled
# - Security headers set
# - CORS restricted to known origins

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware,
    allow_origins=["https://myapp.com"],  # NOT "*"
    allow_methods=["GET", "POST"],
    allow_credentials=True)

# Security headers middleware
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

## A06 — Vulnerable Components

```bash
# Python
pip-audit                          # audit installed packages
safety check -r requirements.txt

# Node.js
npm audit
npx snyk test

# Docker
trivy image myapp:latest
```

## A07 — Auth Failures

```python
# Rate limiting on login (use slowapi or similar)
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
@app.post("/login")
@limiter.limit("5/minute")  # 5 attempts per minute per IP
async def login(form: LoginForm, request: Request): ...

# Account lockout after N failures
# Secure session: httpOnly + secure + sameSite cookies
response.set_cookie("session", token, httponly=True, secure=True, samesite="Strict")
```

## A09 — Logging Failures

```python
# Log security events (never log passwords/tokens)
import logging
logger = logging.getLogger("security")

logger.warning("Failed login attempt", extra={
    "email": email,  # OK — not sensitive
    "ip": request.client.host,
    "user_agent": request.headers.get("user-agent")
})
# NEVER: logger.info(f"Login attempt password={password}")
```

## A10 — SSRF

```python
# BAD: fetch user-supplied URL without validation
import httpx
response = httpx.get(user_supplied_url)

# GOOD: allowlist domains
from urllib.parse import urlparse
ALLOWED_HOSTS = {"api.trusted.com", "cdn.trusted.com"}
parsed = urlparse(user_supplied_url)
if parsed.hostname not in ALLOWED_HOSTS:
    raise ValueError("URL not allowed")
# Also: bind to non-internal IPs, block 169.254.x.x (AWS metadata)
```
