---
name: security-hardening
description: |
  Security standards for web applications. Apply for any endpoint, authentication flow,
  file upload, or third-party integration. Covers OWASP Top 10, injection prevention,
  XSS/CSRF, secrets management, dependency auditing, and security checklist.
  Zero tolerance for SQL injection, hardcoded secrets, and insecure direct object references.
---

# Security Hardening

## OWASP Top 10 — Implementation Checklist

### A01: Broken Access Control
```python
# Always check ownership — never trust user-provided IDs
# ❌ WRONG
@app.get("/api/v1/orders/{order_id}")
async def get_order(order_id: str, current_user: User = Depends(get_current_user)):
    return await db.get(Order, order_id)  # User can access ANY order!

# ✅ CORRECT
@app.get("/api/v1/orders/{order_id}")
async def get_order(order_id: str, current_user: User = Depends(get_current_user)):
    order = await db.get(Order, order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(403, "Access denied")
    return order
```

### A02: Cryptographic Failures
```python
# Secrets in .env ONLY — never in code or git
import os
from dotenv import load_dotenv

SECRET_KEY = os.getenv("SECRET_KEY")  # ✅
SECRET_KEY = "hardcoded-secret-123"   # ❌ NEVER

# Encryption for PII at rest
from cryptography.fernet import Fernet
cipher = Fernet(os.getenv("ENCRYPTION_KEY"))
encrypted_phone = cipher.encrypt(user.phone.encode())
```

### A03: Injection Prevention
```python
# SQL — use ORM or parameterized queries ALWAYS
# ❌ NEVER
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# ✅ ALWAYS
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
# or ORM:
User.objects.filter(email=email)

# NoSQL injection
# Always validate ObjectId format before querying MongoDB
import re
if not re.match(r'^[a-f0-9]{24}$', user_id):
    raise ValueError("Invalid ID format")
```

### A05: Security Misconfiguration
```python
# Production Django settings checklist
SECURITY_SETTINGS = {
    "DEBUG": False,                          # NEVER True in production
    "SECRET_KEY": os.getenv("SECRET_KEY"),  # From environment
    "ALLOWED_HOSTS": ["yourdomain.com"],    # Never ['*'] in production
    "SECURE_SSL_REDIRECT": True,
    "SESSION_COOKIE_SECURE": True,
    "CSRF_COOKIE_SECURE": True,
    "SECURE_HSTS_SECONDS": 31536000,
    "SECURE_HSTS_INCLUDE_SUBDOMAINS": True,
    "SECURE_CONTENT_TYPE_NOSNIFF": True,
    "X_FRAME_OPTIONS": "DENY",
}
```

### A07: Authentication Failures
```python
# Account lockout after failed attempts
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 900  # 15 minutes

async def attempt_login(email: str, password: str, ip: str):
    key = f"login_attempts:{email}:{ip}"
    attempts = await redis.incr(key)
    if attempts == 1:
        await redis.expire(key, LOCKOUT_DURATION)
    if attempts > MAX_LOGIN_ATTEMPTS:
        raise TooManyAttempts("Account temporarily locked")
    
    user = await authenticate(email, password)
    if user:
        await redis.delete(key)  # Reset on success
    return user
```

### A08: Software and Data Integrity
```python
# Verify file uploads — never trust MIME type from client
import magic

ALLOWED_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'application/pdf'}

def validate_file_type(file_bytes: bytes) -> str:
    mime = magic.from_buffer(file_bytes, mime=True)
    if mime not in ALLOWED_TYPES:
        raise ValueError(f"File type not allowed: {mime}")
    return mime
```

## Secrets Management
```bash
# .env.example — commit this (no real values)
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379
PAYME_SECRET_KEY=your-payme-key

# .env — NEVER commit (add to .gitignore)
# .gitignore must contain:
.env
.env.local
.env.production
*.pem
*.key
```

## Dependency Security
```bash
# Run before every deploy
pip-audit                          # Python
npm audit --audit-level=moderate  # Node.js

# GitHub Dependabot: enable in repo settings
# Snyk: integrate into CI pipeline
```

## Security Review Checklist
```
Before every PR merge:
- [ ] No hardcoded secrets, tokens, or passwords
- [ ] All user inputs validated and sanitized
- [ ] Authorization checked for every protected endpoint
- [ ] Ownership verified for resource-specific endpoints
- [ ] Parameterized queries (no string interpolation in SQL)
- [ ] File uploads: type validated server-side, not just by extension
- [ ] Error messages don't expose internal details to client
- [ ] New dependencies audited for known vulnerabilities
- [ ] API keys and webhooks signed and verified
- [ ] Rate limiting applied to auth and sensitive endpoints
```
