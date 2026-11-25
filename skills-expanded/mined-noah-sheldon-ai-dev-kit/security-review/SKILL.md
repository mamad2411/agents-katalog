---
name: security-review
description: Security review methodology covering OWASP Top 10, input validation audit, auth/authorization review, secret management check, dependency CVE scan, threat modeling, and secure code review checklist.
origin: AI Dev Kit
disable-model-invocation: false
---

# Security Review

Systematic security review methodology for code, architecture, and infrastructure. Covers OWASP Top 10 vulnerabilities, input validation auditing, authentication and authorization review, secret management verification, dependency CVE scanning, threat modeling, and a comprehensive secure code review checklist. Use this skill when reviewing security-sensitive changes or establishing security standards.

## When to Use

- Reviewing PRs that touch authentication, authorization, or session management
- Auditing input validation boundaries on new or modified endpoints
- Reviewing secret management and credential handling code
- Evaluating new external integrations or third-party dependencies
- Conducting threat modeling for new services or architectures
- Pre-release security assessment before production deployment
- Reviewing changes to payment processing, PII handling, or data export

## Core Concepts

### OWASP Top 10 (2021) — Practical Review Guide

#### A01: Broken Access Control

**What to check:** Every endpoint that acts on a resource must verify the requester has permission.

```python
# BAD: Missing authorization check
@router.get("/users/{user_id}/profile")
async def get_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if user is None:
        raise HTTPException(404)
    return {"name": user.name, "email": user.email, "ssn": user.ssn}
    # Any authenticated user can read any profile!

# GOOD: Verify ownership or admin role
@router.get("/users/{user_id}/profile")
async def get_profile(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403, detail="Not authorized")
    user = db.query(User).get(user_id)
    if user is None:
        raise HTTPException(404)
    return {"name": user.name, "email": user.email}
    # SSN excluded — never expose sensitive fields
```

**Checklist:**
- [ ] Every route verifies current user identity
- [ ] Resource access checks ownership or role-based permission
- [ ] IDOR (Insecure Direct Object Reference) prevented — user can't access other users' resources by changing IDs
- [ ] Admin-only endpoints reject non-admin requests
- [ ] API keys and tokens validated on every request

#### A02: Cryptographic Failures

**What to check:** Sensitive data is encrypted, hashed, or tokenized appropriately.

```python
# BAD: Storing passwords in plaintext
class User(Base):
    password = Column(String)  # Plaintext password!

# GOOD: Using bcrypt hashing
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    password_hash = Column(String)

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)
```

**Checklist:**
- [ ] Passwords hashed with bcrypt, argon2, or scrypt (not MD5, SHA1, SHA256)
- [ ] TLS enforced for all endpoints (no HTTP-only paths)
- [ ] Sensitive data encrypted at rest (PII, payment info, health data)
- [ ] JWT tokens use strong signing algorithms (RS256, ES256 — not HS256 with weak secret)
- [ ] No custom cryptographic implementations — use established libraries

#### A03: Injection

**What to check:** All user input is parameterized, sanitized, or validated.

```python
# BAD: SQL injection via f-string
def search_users(name: str):
    query = f"SELECT * FROM users WHERE name LIKE '%{name}%'"
    return db.execute(query)

# GOOD: Parameterized query
def search_users(name: str):
    query = text("SELECT id, name, email FROM users WHERE name LIKE :pattern")
    return db.execute(query, {"pattern": f"%{name}%"})

# BAD: Command injection
def process_file(filename: str):
    os.system(f"convert {filename} output.png")  # User controls shell command!

# GOOD: Use subprocess with argument list
def process_file(filename: str):
    import subprocess
    # Validate filename is safe
    if '..' in filename or filename.startswith('/'):
        raise ValueError("Invalid filename")
    subprocess.run(["convert", filename, "output.png"], check=True)
```

**Checklist:**
- [ ] SQL queries use parameterized statements (no string interpolation)
- [ ] Shell commands use `subprocess.run([...])` with argument lists (no `shell=True`)
- [ ] No `eval()`, `exec()`, or `Function()` on user input
- [ ] HTML output is escaped/encoded (Jinja auto-escape enabled)
- [ ] File paths validated — no path traversal (`../`)

#### A04: Insecure Design

**What to check:** Architecture decisions don't introduce systemic vulnerabilities.

| Design Flaw | Risk | Mitigation |
|---|---|---|
| Business logic bypass | Revenue loss, fraud | Rate limits, transaction validation |
| Missing workflow enforcement | State manipulation | State machine, server-side validation |
| Unsafe default configuration | Data exposure | Secure defaults, require explicit opt-in |
| No audit trail | Untraceable incidents | Log all security-relevant events |

#### A05: Security Misconfiguration

**What to check:** Production configuration follows secure defaults.

```yaml
# BAD: Insecure production config
DEBUG: true                    # Exposes stack traces
CORS_ORIGINS: "*"              # Allows any origin
ALLOWED_HOSTS: ["*"]           # No host validation
SESSION_COOKIE_SECURE: false   # Cookies sent over HTTP
DATABASE_URL: "postgres://admin:password@localhost/db"  # Weak credentials

# GOOD: Secure production config
DEBUG: false
CORS_ORIGINS: "https://app.example.com"
ALLOWED_HOSTS: ["app.example.com"]
SESSION_COOKIE_SECURE: true
SESSION_COOKIE_HTTPONLY: true
SESSION_COOKIE_SAMESITE: "lax"
DATABASE_URL: "postgres://app_user:${DB_PASSWORD}@db.internal:5432/app"  # From env var
```

**Checklist:**
- [ ] DEBUG mode disabled in production
- [ ] CORS restricted to known origins (not `*`)
- [ ] Security headers set (HSTS, CSP, X-Frame-Options, X-Content-Type-Options)
- [ ] Default credentials changed or removed
- [ ] Unused features, routes, and services disabled

#### A06: Vulnerable and Outdated Components

**What to check:** Dependencies are current and free of known CVEs.

```bash
# Python dependency audit
pip install safety
safety check --full-report

# Node.js dependency audit
npm audit --audit-level=moderate

# Comprehensive SAST scan
semgrep --config auto .
```

**Checklist:**
- [ ] No dependencies with known critical CVEs
- [ ] Dependency updates applied within 30 days of security release
- [ ] No abandoned dependencies (no maintainer, >2 years since last release)
- [ ] Pin dependency versions in lockfile
- [ ] Automated alerts configured for new CVEs

#### A07: Identification and Authentication Failures

**What to check:** Auth mechanisms resist common attacks.

```python
# BAD: No rate limiting on login
@router.post("/login")
async def login(email: str, password: str):
    user = db.authenticate(email, password)
    return create_token(user)
    # Unlimited attempts — brute force viable

# GOOD: Rate-limited with account lockout
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, email: str, password: str):
    user = db.authenticate(email, password)
    if user is None:
        # Track failed attempts
        db.track_failed_login(email, request.client.host)
        raise HTTPException(401, detail="Invalid credentials")
    return create_token(user)
```

**Checklist:**
- [ ] Login endpoint rate-limited (≤ 5 attempts per minute)
- [ ] Account lockout after repeated failures
- [ ] Session tokens are cryptographically random (≥ 128 bits)
- [ ] Password reset tokens expire (≤ 1 hour)
- [ ] MFA supported for sensitive operations
- [ ] Token rotation on password change

#### A08: Software and Data Integrity Failures

**What to check:** Code and data integrity verified before use.

**Checklist:**
- [ ] CI/CD pipeline uses pinned dependencies (not `*` or `latest`)
- [ ] Container images signed and verified
- [ ] Serialized data (pickle, YAML) not loaded from untrusted sources
- [ ] JWT tokens verified server-side before use
- [ ] File uploads validated for type, size, and content (not just extension)

```python
# BAD: Trusting file extension
if filename.endswith('.pdf'):
    process_upload(file)

# GOOD: Validate actual file content
import magic

def validate_upload(file, max_size_mb: int = 10):
    # Check size
    file.seek(0, 2)
    if file.tell() > max_size_mb * 1024 * 1024:
        raise ValueError(f"File too large (max {max_size_mb}MB)")

    # Check actual MIME type
    file.seek(0)
    mime = magic.from_buffer(file.read(2048), mime=True)
    if mime not in ('application/pdf', 'image/png', 'image/jpeg'):
        raise ValueError(f"File type not allowed: {mime}")
```

#### A09: Security Logging and Monitoring Failures

**What to check:** Security events are logged and monitored.

**Checklist:**
- [ ] Failed authentication attempts logged
- [ ] Authorization failures (403 responses) logged with context
- [ ] Admin actions logged with user identity
- [ ] No PII, passwords, or tokens in logs
- [ ] Logs structured (JSON) for automated analysis
- [ ] Alert configured for anomalous patterns (brute force, data exfiltration)

#### A10: Server-Side Request Forgery (SSRF)

**What to check:** Server-side HTTP requests validate target URLs.

```python
# BAD: User controls fetch target
@router.post("/fetch-preview")
async def fetch_preview(url: str):
    response = httpx.get(url)  # User can request http://localhost:5432
    return response.text

# GOOD: Validate and restrict URLs
from urllib.parse import urlparse

ALLOWED_SCHEMES = {'http', 'https'}
BLOCKED_HOSTS = {'localhost', '127.0.0.1', '169.254.169.254', '0.0.0.0'}

@router.post("/fetch-preview")
async def fetch_preview(url: str):
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise HTTPException(400, "Only HTTP/HTTPS allowed")
    if parsed.hostname in BLOCKED_HOSTS:
        raise HTTPException(400, "Host not allowed")
    if not parsed.hostname.endswith('.example.com'):
        raise HTTPException(400, "Only example.com domains allowed")

    response = httpx.get(url, timeout=10, follow_redirects=True)
    return response.text[:5000]  # Limit response size
```

## Threat Modeling

Use STRIDE methodology for new features:

| Threat | Question | Mitigation |
|---|---|---|
| **S**poofing | Can an attacker impersonate another user? | Strong auth, MFA, token validation |
| **T**ampering | Can data be modified in transit or storage? | Checksums, signatures, access controls |
| **R**epudiation | Can an action be denied after it occurs? | Audit logs, non-repudiation |
| **I**nformation Disclosure | Can sensitive data be exposed? | Encryption, least privilege, field-level access |
| **D**enial of Service | Can the system be made unavailable? | Rate limiting, resource quotas, timeouts |
| **E**levation of Privilege | Can a user gain unauthorized access? | Role validation, principle of least privilege |

### Threat Model Template

```markdown
## Threat Model: [Feature Name]

### Assets
- User PII (name, email, SSN)
- Payment records
- Session tokens

### Entry Points
- POST /api/login (authentication)
- GET /api/users/{id} (data access)
- POST /api/upload (file processing)

### Trust Boundaries
- Client → API (untrusted → trusted)
- API → Database (trusted, but validate)
- API → External service (trusted, but handle failures)

### Threats & Mitigations
1. **Spoofing**: Attacker forges session token
   - Mitigation: JWT signature verification, token expiry

2. **Tampering**: Attacker modifies request body
   - Mitigation: Pydantic validation, schema enforcement

3. **Data Exposure**: Attacker reads other user's data
   - Mitigation: Ownership check on every resource access
```

## Secret Management Review

```python
# BAD: Hardcoded secrets
API_KEY = "sk-proj-abc123def456"
DATABASE_URL = "postgres://admin:supersecret@db.example.com/app"
JWT_SECRET = "my-secret-key"

# GOOD: Environment variables
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    database_url: str
    jwt_secret: str
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# .env.example (committed to repo)
# API_KEY=your-api-key-here
# DATABASE_URL=postgresql://user:pass@localhost:5432/db
# JWT_SECRET=change-me-in-production
```

**Secret Management Checklist:**
- [ ] No secrets in source code, config files, or commit history
- [ ] `.env` in `.gitignore`
- [ ] `.env.example` present with placeholder values
- [ ] Secrets loaded from environment variables or secret manager
- [ ] Secrets not logged, printed, or included in error messages
- [ ] Secret rotation process documented
- [ ] Git history scanned for accidentally committed secrets

```bash
# Scan git history for secrets
gitleaks detect --source . -v

# Remove secrets from git history (if accidentally committed)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all
```

## Secure Code Review Checklist

### Input Validation
- [ ] All user inputs validated at API boundary
- [ ] Input validation uses schema (Pydantic, Zod) — not manual checks
- [ ] File uploads validated for type, size, content
- [ ] URL parameters validated and sanitized
- [ ] Batch/list inputs have maximum size limit

### Authentication & Authorization
- [ ] Every endpoint verifies identity
- [ ] Resource access checks ownership or role
- [ ] No IDOR vulnerabilities
- [ ] Password hashing uses bcrypt/argon2
- [ ] Token expiry configured
- [ ] Rate limiting on auth endpoints

### Data Protection
- [ ] PII encrypted at rest
- [ ] Sensitive fields excluded from API responses
- [ ] Database queries use parameterized statements
- [ ] No PII in logs, error messages, or analytics
- [ ] Data export limited to authorized data

### Dependencies & Infrastructure
- [ ] No dependencies with critical CVEs
- [ ] TLS enforced on all endpoints
- [ ] Security headers configured
- [ ] CORS restricted to known origins
- [ ] Container runs as non-root user

### Error Handling
- [ ] Errors don't expose stack traces in production
- [ ] Error messages don't reveal internal details (SQL, paths, credentials)
- [ ] 500 responses logged with full context
- [ ] User-facing errors are generic ("Something went wrong")

## Automated Security Review

Run these tools as part of the review process:

```bash
# Python SAST
bandit -r app/ -f json -o bandit-report.json

# Multi-language SAST
semgrep --config auto --json -o semgrep-report.json

# Dependency audit
safety check --full-report          # Python
npm audit --json > npm-audit.json   # Node

# Secret scanning
gitleaks detect --source . -v

# Container security (if applicable)
trivy image myapp:latest

# Combined report
echo "=== Security Review Report ==="
echo "Bandit issues: $(python -c "import json; print(len(json.load(open('bandit-report.json'))['results']))")"
echo "Semgrep issues: $(python -c "import json; print(len(json.load(open('semgrep-report.json'))['results']))")"
echo "CVEs found: $(npm audit --json | python -c 'import sys,json; print(json.load(sys.stdin).get("metadata",{}).get("vulnerabilities",0))')"
```

## Common Security Anti-Patterns

| Anti-Pattern | Risk | Fix |
|---|---|---|
| `eval(user_input)` | Remote code execution | Never eval untrusted input |
| `SELECT * FROM users WHERE id = ${id}` | SQL injection | Parameterized queries |
| Storing passwords in DB | Credential theft | Hash with bcrypt/argon2 |
| `CORS: *` in production | Cross-origin attacks | Restrict to known origins |
| Logging request bodies | Credential exposure | Log only safe fields |
| No rate limiting | Brute force | Rate limit auth endpoints |
| `pickle.loads(user_data)` | Code execution | Use JSON for serialization |

## Best Practices

1. **Review security-relevant PRs first** — auth, secrets, input handling, external APIs
2. **Use the OWASP Top 10 checklist** — systematic coverage beats ad-hoc review
3. **Threat model new features** — STRIDE before implementation, not after
4. **Automate what you can** — SAST, SCA, secret scanning in CI
5. **Never trust user input** — validate at every boundary, reject early
6. **Least privilege by default** — minimal permissions, explicit grants
7. **Defense in depth** — multiple layers, not a single checkpoint
8. **Fail secure** — deny on error, never allow on uncertainty
9. **Log security events** — but never log secrets or PII
10. **Rotate secrets regularly** — have a documented rotation process

## Escalation Procedure

If a **BLOCKER** security issue is found:

1. Label the comment **BLOCKER — SECURITY**
2. Do not merge until resolved
3. If the fix requires architectural change, escalate to `security-reviewer` agent
4. Document the decision in an ADR if it involves accepted risk or exception

## Success Metrics

- [ ] All PRs touching auth/secrets reviewed against full checklist
- [ ] Zero critical CVEs in dependencies
- [ ] No secrets in source code or git history
- [ ] All endpoints have input validation
- [ ] Threat model exists for all services handling PII or payments
- [ ] Security SAST scan passes in CI/CD
- [ ] Security incidents traced to reviewed code: 0

---

**Remember:** Security isn't a feature — it's a property of the entire system. Every line of code is a potential attack surface.
