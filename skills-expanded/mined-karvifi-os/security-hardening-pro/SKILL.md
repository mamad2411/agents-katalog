---
name: security-hardening-pro
description: Application security hardening — OWASP Top 10, CSP, rate limiting, secrets management
triggers: [security, security hardening, OWASP, CSP, XSS, CSRF, secrets management, rate limiting]
---

# SKILL: Security Hardening Pro

## OWASP Top 10 Protection

### 1. SQL Injection Prevention
```python
# ❌ VULNERABLE
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ SAFE: Parameterized queries
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

### 2. XSS Prevention
```tsx
// ❌ VULNERABLE
<div dangerouslySetInnerHTML={{__html: userInput}} />

// ✅ SAFE: Automatic escaping
<div>{userInput}</div>

// Content Security Policy header
headers = {
  "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'"
}
```

### 3. CSRF Protection
```python
from fastapi import Depends
from fastapi_csrf_protect import CsrfProtect

@app.post("/transfer")
async def transfer(csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf()
    # Process request
```

### 4. Authentication & Authorization
```python
# ✅ Strong password hashing
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed = pwd_context.hash(password)
verified = pwd_context.verify(password, hashed)

# ✅ JWT with expiration
import jwt

token = jwt.encode({
    "sub": user_id,
    "exp": datetime.utcnow() + timedelta(hours=1)
}, SECRET_KEY)
```

### 5. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")  # Max 5 login attempts per minute
async def login(request: Request):
    pass
```

## Secrets Management

```python
# ❌ NEVER commit secrets
API_KEY = "sk_live_abc123"  # DON'T DO THIS

# ✅ Use environment variables
import os
API_KEY = os.getenv("API_KEY")

# ✅ Use secret managers (AWS Secrets Manager)
import boto3

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='myapp/api_key')
API_KEY = response['SecretString']
```

## HTTPS Enforcement

```python
# Force HTTPS redirect
@app.middleware("http")
async def redirect_https(request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url, status_code=301)
    return await call_next(request)
```

## Quality Checks
- [ ] HTTPS enforced (no HTTP)
- [ ] Parameterized queries (no SQL injection)
- [ ] CSP headers configured
- [ ] CSRF protection enabled
- [ ] Rate limiting on auth endpoints
- [ ] Secrets in environment/vault (not code)
- [ ] Input validation on all endpoints
- [ ] Security headers (HSTS, X-Frame-Options)
