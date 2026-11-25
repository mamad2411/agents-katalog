---
name: insecure-defaults
description: Detects fail-open vulnerabilities where applications run insecurely with missing configuration. Finds hardcoded credentials, weak env var fallbacks, and insecure-by-default settings. Adapted from Trail of Bits methodology.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
group: security
triggers:
  - ".env"
  - "config"
  - "secrets"
  - "безопасно ли деплоить"
  - "есть ли hardcoded"
output: "security report: hardcoded credentials, insecure defaults, fail-open risks"
calls: []
---

# Insecure Defaults

Identifies fail-open vulnerabilities: configurations where missing env vars, secrets, or settings cause the application to run in an insecure state rather than failing safely.

## When to Use

- Pre-deployment security audit of production application
- Reviewing config files, `.env` handling, or secrets management
- Auditing environment variable usage across the codebase
- Checking cryptographic algorithm choices
- Reviewing Docker / IaC / Kubernetes configs for permissive defaults
- User asks "is this safe to deploy?" or "are there hardcoded secrets?"

## When NOT to Use

- Test code (`tests/`, `spec/`, `__tests__/`, `*.test.*`) — test defaults are intentional
- `.example`, `.template`, `.sample` files — placeholders by design
- Documentation examples
- Build-time config guaranteed to be replaced during deployment
- Dev-only tooling that never runs in production

## Rationalizations to Reject

- **"The default is only used locally"** — local development often mirrors production configs; defaults leak
- **"We always set the env var in production"** — "always" breaks eventually; code must fail-safe
- **"It's an internal service, not exposed"** — internal breach + fail-open = full compromise
- **"The weak algorithm is only for non-sensitive data"** — "non-sensitive" classifications drift over time
- **"The tests pass with the default"** — test pass ≠ production safe

---

## Core Distinction

The fundamental question for every finding:

**Fail-Open (DANGEROUS):** App runs insecurely when config is absent
```python
# DANGEROUS — runs with weak secret if env var missing
SECRET = os.environ.get('SECRET_KEY') or 'default-secret'
```

**Fail-Secure (SAFE):** App crashes/refuses to start when required config is absent
```python
# SAFE — raises KeyError if env var missing, app won't start
SECRET = os.environ['SECRET_KEY']

# Also safe — explicit error message
SECRET = os.environ.get('SECRET_KEY')
if not SECRET:
    raise RuntimeError("SECRET_KEY environment variable is required")
```

---

## Analysis Workflow (4 Phases)

### Phase 1 — Discovery

Map the attack surface:

```bash
# Find all env var reads
grep -rn "os.environ\|os.getenv\|process.env\|getenv" --include="*.py" --include="*.ts" --include="*.js" .

# Find all config/settings files
find . -name "config*.py" -o -name "settings*.py" -o -name "*.env*" | grep -v ".example"

# Find potential hardcoded secrets
grep -rn "password\|secret\|token\|api_key\|apikey\|credential" -i --include="*.py" .
grep -rn "password\|secret\|token\|api_key\|apikey\|credential" -i --include="*.ts" .
```

Inventory:
- All env var reads and their fallback values
- All cryptographic operations and algorithm choices
- All authentication/authorization configuration points
- All external service configuration (URLs, timeouts, TLS settings)

---

### Phase 2 — Verification

For each env var read, classify:

| Pattern | Classification | Risk |
|---------|---------------|------|
| `os.environ['KEY']` | Fail-secure | Safe |
| `os.environ.get('KEY')` with no default + validation | Fail-secure | Safe |
| `os.environ.get('KEY', '')` + `if not value: raise` | Fail-secure | Safe |
| `os.environ.get('KEY') or 'fallback'` | Fail-open | **HIGH** |
| `os.environ.get('KEY', 'fallback')` | Fail-open | **HIGH** |
| `os.environ.get('KEY', None)` used without None-check | Fail-open | MEDIUM |

Trace each fail-open pattern: where is the value used?
- Used in cryptographic operation → **CRITICAL**
- Used in auth check → **CRITICAL**
- Used in external API call → **HIGH**
- Used in logging / non-security context → LOW

---

### Phase 3 — Production Assessment

Verify whether production actually sets required variables:
- Check deployment configs: `docker-compose.yml`, `k8s/`, `.env.production`, CI/CD secrets
- Check if documented: is the env var listed in README / deployment guide?
- Check if validated at startup: is there an explicit startup check?

A fail-open pattern is more severe if:
- No startup validation exists
- Env var is not documented
- Deployment config shows it's sometimes unset

---

### Phase 4 — Findings Documentation

For each finding:

```
## [Severity] <Short title>

**File:** path/to/file.py:42
**Pattern:** fail-open / hardcoded / weak algorithm

**Vulnerable code:**
```python
SECRET = os.environ.get('SECRET_KEY') or 'dev-secret-change-me'
```

**What happens if env var is missing:**
Application starts with `SECRET_KEY = 'dev-secret-change-me'`. An attacker
who knows this default can forge session tokens / HMAC signatures.

**Fix:**
```python
SECRET = os.environ.get('SECRET_KEY')
if not SECRET:
    raise RuntimeError("SECRET_KEY is required. Set it in your environment.")
```
```

---

## Finding Categories

### 1. Weak Env Var Fallbacks
```python
# All of these are fail-open:
SECRET = os.getenv('SECRET') or 'default'
SECRET = os.environ.get('SECRET', 'changeme')
DB_PASSWORD = config.get('db_password', 'postgres')
API_KEY = os.environ.get('API_KEY', '')   # empty string = no auth
```

### 2. Hardcoded Credentials
```python
# Hardcoded in source — always a finding regardless of context
DB_URI = "postgresql://admin:password123@localhost/prod"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

### 3. Weak Cryptographic Algorithms
```python
# Weak — even if fallback looks "fine"
hashlib.md5(password)              # collision attacks, rainbow tables
hashlib.sha1(password)             # deprecated for password hashing
Cipher.new(key, AES.MODE_ECB)     # ECB reveals patterns
DES.new(key)                       # 56-bit key, brute-forceable
```

### 4. Permissive Default Access Controls
```python
CORS_ORIGINS = ["*"]               # any origin can send cookies
DEBUG = os.environ.get('DEBUG', True)   # debug on by default
ALLOW_REGISTRATION = True           # open registration in production
```

### 5. TLS / Certificate Validation
```python
requests.get(url, verify=False)    # MITM possible
ssl._create_unverified_context()   # disables cert validation globally
```

### 6. Insecure Defaults in Config Files
```yaml
# docker-compose.yml
services:
  db:
    environment:
      POSTGRES_PASSWORD: ""        # empty password

# nginx.conf
server_tokens on;                  # leaks nginx version
```

---

## Severity Classification

| Severity | When |
|----------|------|
| 🔴 Critical | Fail-open on auth/crypto/session secret; hardcoded production credential |
| 🟠 High | Fail-open on API key, DB password; weak algorithm for security-critical data |
| 🟡 Medium | Permissive CORS/access defaults; weak algorithm for non-critical data |
| 🟢 Low | Missing startup validation despite correct production config; undocumented required var |

---

## Output Format

```markdown
# Insecure Defaults Audit: <scope>

## Summary
- Fail-open patterns found: X
- Hardcoded credentials found: X
- Weak algorithms found: X
- Files audited: X / Y total

## 🔴 Critical

### [C1] Fail-open session secret
...

## 🟠 High
...

## ✅ What's secure
- `DATABASE_URL` correctly uses `os.environ['DATABASE_URL']` (fail-secure)
- Password hashing uses `bcrypt` correctly
```
