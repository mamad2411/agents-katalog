---
name: security-audit
description: Conduct a comprehensive security audit of an application or infrastructure. Outputs vulnerability assessment, threat modeling, and remediation roadmap.
argument-hint: [system architecture, technology stack, compliance requirements]
allowed-tools: Read, Write, Bash
---

# Security Audit

Conduct a systematic security audit to identify vulnerabilities, assess risks, and prioritize remediation. Not a checkbox exercise — actionable findings with exploit scenarios, business impact, and fix timelines.

## Process

1. **Define scope.** Which systems, applications, infrastructure components to audit?
2. **Gather information.** Architecture diagrams, tech stack, access patterns, data flows.
3. **Threat modeling.** STRIDE analysis — what can go wrong?
4. **Vulnerability scanning.** Automated tools + manual testing.
5. **Assess risks.** Severity (critical/high/medium/low) × likelihood.
6. **Document findings.** Vulnerability details, proof of concept, business impact.
7. **Prioritize remediation.** Quick wins vs long-term fixes.
8. **Create roadmap.** 30/60/90-day plan with owners.

## Output Format

### Security Audit Report: [System Name]

**Audit Date:** 2024-01-15  
**Scope:** Web Application + API + Database + AWS Infrastructure  
**Tools Used:** OWASP ZAP, Burp Suite, Nmap, AWS Security Hub, Bandit  
**Total Findings:** 37 (5 Critical, 12 High, 15 Medium, 5 Low)  
**Remediation Timeline:** 90 days  

---

## Executive Summary

**Critical Findings (Fix Immediately):**
1. SQL Injection in user search (CVSS 9.8) — Database compromise risk
2. Hardcoded AWS credentials in source code (CVSS 9.1) — Full AWS account takeover
3. Missing authentication on admin endpoints (CVSS 9.0) — Unauthorized admin access
4. Exposed S3 buckets with customer PII (CVSS 8.5) — Data breach risk
5. Outdated Django version with known RCE (CVSS 8.1) — Remote code execution

**High Priority (Fix Within 30 Days):**
- CSRF protection disabled (12 endpoints)
- Weak password policy (no complexity requirements)
- Session tokens never expire
- No rate limiting on login endpoints (brute force risk)

**Recommended Actions:**
1. **Week 1:** Fix all Critical vulnerabilities (estimated 40 engineering hours)
2. **Week 2-4:** Address High priority issues (60 hours)
3. **Month 2-3:** Implement security tooling (SAST/DAST, dependency scanning)

---

## Threat Model (STRIDE Analysis)

### Spoofing Identity
**Threat:** Attacker impersonates legitimate user  
**Attack Vectors:**
- Session hijacking (weak session management)
- Credential stuffing (no account lockout)
- JWT token forgery (weak signing key)

**Controls:**
- ✅ HTTPOnly cookies for session tokens
- ❌ No multi-factor authentication (MFA)
- ❌ JWT secret key is hardcoded `"secret123"`

**Risk:** HIGH

---

### Tampering with Data
**Threat:** Attacker modifies data in transit or at rest  
**Attack Vectors:**
- SQL injection (user input not sanitized)
- API parameter tampering
- Direct database access (overprivileged DB user)

**Controls:**
- ✅ HTTPS for data in transit
- ❌ No parameterized queries in legacy code
- ❌ Application DB user has DELETE, DROP privileges

**Risk:** CRITICAL

---

### Repudiation
**Threat:** User denies actions (no audit trail)  
**Attack Vectors:**
- No logging of sensitive actions
- Logs can be modified by application

**Controls:**
- ✅ Access logs for HTTP requests
- ❌ No audit log for order modifications
- ❌ Logs stored locally (not immutable)

**Risk:** MEDIUM

---

### Information Disclosure
**Threat:** Sensitive data exposed to unauthorized parties  
**Attack Vectors:**
- Error messages reveal stack traces
- S3 buckets publicly readable
- Debug mode enabled in production

**Controls:**
- ✅ Database encryption at rest
- ❌ Error responses expose full stack trace
- ❌ DEBUG=True in production settings

**Risk:** HIGH

---

### Denial of Service
**Threat:** Attacker overwhelms system  
**Attack Vectors:**
- No rate limiting
- Expensive queries without pagination
- File uploads without size limits

**Controls:**
- ✅ CloudFlare DDoS protection
- ❌ No application-level rate limiting
- ❌ /search endpoint allows full table scan

**Risk:** MEDIUM

---

### Elevation of Privilege
**Threat:** Attacker gains higher permissions  
**Attack Vectors:**
- Missing authorization checks
- Broken access control (IDOR vulnerabilities)
- Admin endpoints accessible without auth

**Controls:**
- ✅ Role-based access control (RBAC) defined
- ❌ Authorization not enforced on 8 endpoints
- ❌ User can modify other users' data via API

**Risk:** CRITICAL

---

## Critical Vulnerabilities

### [CRITICAL-01] SQL Injection in User Search

**Severity:** CVSS 9.8 (Critical)  
**CWE:** CWE-89 (SQL Injection)  
**OWASP:** A03:2021 - Injection

**Location:** `api/search.py:45`

**Vulnerable Code:**
```python
def search_users(query):
    sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"  # VULNERABLE
    results = db.execute(sql)
    return results
```

**Proof of Concept:**
```
GET /api/search?q=' OR '1'='1
→ Returns all users

GET /api/search?q='; DROP TABLE users; --
→ Deletes users table
```

**Business Impact:**
- Attacker can extract entire database (customer PII, passwords, payment info)
- Attacker can modify or delete data
- Potential GDPR violation → €20M fine

**Remediation:**
```python
def search_users(query):
    sql = "SELECT * FROM users WHERE name LIKE %s"
    results = db.execute(sql, (f"%{query}%",))  # SAFE: Parameterized query
    return results
```

**Effort:** 1 day (includes testing)  
**Owner:** Backend Team  
**Target Date:** 2024-01-20 (5 days)

---

### [CRITICAL-02] Hardcoded AWS Credentials

**Severity:** CVSS 9.1 (Critical)  
**CWE:** CWE-798 (Use of Hard-coded Credentials)

**Location:** `config/aws.py:12`

**Vulnerable Code:**
```python
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

**Business Impact:**
- Credentials committed to public GitHub repo
- Attacker can access all AWS resources
- Estimated cost: $50k+ if attacker mines crypto

**Remediation:**
1. Rotate compromised credentials immediately
2. Enable AWS Secrets Manager:
```python
import boto3

client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='prod/aws/credentials')
credentials = json.loads(secret['SecretString'])
```
3. Add pre-commit hook to prevent future commits

**Effort:** 0.5 days  
**Owner:** DevOps Team  
**Target Date:** 2024-01-16 (IMMEDIATE)

---

### [CRITICAL-03] Missing Authentication on Admin Endpoints

**Severity:** CVSS 9.0 (Critical)  
**CWE:** CWE-306 (Missing Authentication)  
**OWASP:** A07:2021 - Identification and Authentication Failures

**Location:** `api/admin.py:78-120`

**Vulnerable Endpoints:**
- `POST /admin/delete-user`
- `POST /admin/change-user-role`
- `GET /admin/download-database`

**Proof of Concept:**
```bash
curl -X POST https://api.example.com/admin/delete-user \
  -d '{"user_id": "any_user_id"}'
# Success: User deleted (no auth required)
```

**Business Impact:**
- Anyone can delete users, change roles, download database
- Insider threat: Disgruntled employee can sabotage

**Remediation:**
```python
from functools import wraps
from flask import request, abort

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        user = verify_token(token)
        if not user or user.role != 'admin':
            abort(403, "Admin access required")
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/delete-user', methods=['POST'])
@require_admin  # ADD THIS
def delete_user():
    ...
```

**Effort:** 1 day  
**Owner:** Backend Team  
**Target Date:** 2024-01-20

---

## High Priority Vulnerabilities

### [HIGH-01] CSRF Protection Disabled

**Severity:** CVSS 6.5 (High)  
**Affected Endpoints:** 12 state-changing operations

**Location:** Django settings

**Issue:**
```python
# settings.py
MIDDLEWARE = [
    # 'django.middleware.csrf.CsrfViewMiddleware',  # COMMENTED OUT
]
```

**Attack Scenario:**
```html
<!-- Attacker's website -->
<form action="https://target.com/api/transfer-money" method="POST">
  <input name="to_account" value="attacker_account">
  <input name="amount" value="1000">
</form>
<script>document.forms[0].submit();</script>
```

**Remediation:**
1. Enable CSRF middleware
2. Include CSRF token in all forms
3. Validate token on backend

**Effort:** 2 days  
**Target:** Week 2

---

## Medium Priority Vulnerabilities

### [MEDIUM-01] Weak Password Policy

**Current Policy:**
- Minimum length: 6 characters
- No complexity requirements
- Common passwords allowed ("password123")

**Recommended Policy:**
- Minimum length: 12 characters
- Require uppercase, lowercase, number, special char
- Check against Have I Been Pwned database
- Enforce password rotation every 90 days

**Implementation:**
```python
from django.contrib.auth.password_validation import validate_password

def register_user(email, password):
    try:
        validate_password(password)
    except ValidationError as e:
        return {"error": e.messages}
    # ... proceed with registration
```

---

## Infrastructure Findings

### AWS Security Issues

**[INFRA-01] S3 Buckets Publicly Accessible**
```bash
aws s3 ls s3://company-customer-data --no-sign-request
# SUCCESS: Anyone can list and download files
```

**Fix:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Deny",
    "Principal": "*",
    "Action": "s3:*",
    "Resource": "arn:aws:s3:::company-customer-data/*",
    "Condition": {
      "Bool": {"aws:SecureTransport": "false"}
    }
  }]
}
```

**[INFRA-02] RDS Database Publicly Accessible**
```bash
nmap -p 5432 db.example.com
# Port 5432 (PostgreSQL) is open to internet
```

**Fix:**
- Move RDS to private subnet
- Security group: Allow only from application security group

**[INFRA-03] IAM Overprivileged Roles**
```json
{
  "Effect": "Allow",
  "Action": "*",  // FULL AWS ACCESS
  "Resource": "*"
}
```

**Fix:** Apply principle of least privilege
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::specific-bucket/*"
}
```

---

## Dependency Vulnerabilities

### Outdated Packages with Known CVEs

```
django==2.2.0  # EOL, 15 known CVEs
  └─ CVE-2023-XXXX (Critical): Remote Code Execution
  └─ CVE-2023-YYYY (High): SQL Injection

requests==2.18.0
  └─ CVE-2023-ZZZZ (Medium): Request smuggling

pillow==6.2.0
  └─ CVE-2023-AAAA (High): Arbitrary code execution via malicious image
```

**Automated Scanning:**
```bash
pip install safety
safety check --full-report

# Or use Snyk
snyk test
```

**Remediation:**
1. Upgrade Django to 4.2 LTS (8 days effort)
2. Update all dependencies to latest stable
3. Add dependency scanning to CI/CD

---

## Remediation Roadmap

### Week 1 (Critical Fixes)
- [x] Rotate AWS credentials
- [ ] Fix SQL injection
- [ ] Add authentication to admin endpoints
- [ ] Make S3 buckets private
- [ ] Disable DEBUG mode in production

**Owner:** Security + Backend Teams  
**Hours:** 40

---

### Weeks 2-4 (High Priority)
- [ ] Enable CSRF protection
- [ ] Implement rate limiting
- [ ] Add session expiration
- [ ] Move RDS to private subnet
- [ ] Upgrade Django to 4.2

**Owner:** Backend + DevOps Teams  
**Hours:** 60

---

### Months 2-3 (Security Tooling)
- [ ] Integrate SAST (Bandit, Semgrep)
- [ ] Add DAST to CI/CD (OWASP ZAP)
- [ ] Dependency scanning (Snyk)
- [ ] Set up AWS GuardDuty
- [ ] Implement WAF rules
- [ ] Security training for developers

**Owner:** Security Team  
**Hours:** 120

---

## Monitoring & Prevention

### SIEM Setup
```yaml
# AWS GuardDuty alerts to Slack
- Unusual API call patterns
- Privilege escalation attempts
- Compromised credentials
```

### Security Metrics Dashboard
```
- Vulnerabilities by severity (daily)
- Mean time to remediation (MTTR)
- Dependency freshness (% up-to-date)
- Failed login attempts
- Privilege escalation events
```

### Continuous Security
```bash
# Pre-commit hooks
pip install pre-commit
# .pre-commit-config.yaml
- repo: https://github.com/PyCQA/bandit
  hooks:
    - id: bandit
      args: ['-ll']  # Only high/critical

# CI/CD security gate
snyk test --severity-threshold=high
```

## Rules

- All Critical vulnerabilities must be fixed within 7 days — no exceptions.
- SQL injection and authentication bypass are always Critical severity.
- Hardcoded secrets in code warrant immediate credential rotation, not just removal.
- S3 buckets with customer data must never be public — default deny, explicit allow.
- Database servers must be in private subnets, accessible only from application servers.
- CSRF protection is mandatory for all state-changing operations.
- Session tokens must expire (24-hour max for web apps).
- Rate limiting is required on authentication endpoints (5 attempts per 15 minutes).
- Production must never run in DEBUG mode — stack traces expose too much.
- Dependency scanning must run in CI/CD — block merges with High+ vulnerabilities.
