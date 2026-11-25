/*
LEEWAY HEADER — DO NOT REMOVE

REGION: AI.QA
TAG: AI.QA.WEB_SECURITY_SWEEP

COLOR_ONION_HEX:
NEON=#32CD32
FLUO=#00FF00
PASTEL=#E8F5E9

ICON_ASCII:
family=lucide
glyph=zap

5WH:
WHAT = web security sweep skill for Leeway-compliant AI systems
WHY = Provides capabilities for quality-assurance within the AIskills ecosystem
WHO = Leeway Industries (By Leonard Jerome Lee)
WHERE = skills/quality-assurance/web-security-sweep/SKILL.md
WHEN = 2026
HOW = Leeway-governed skill.md definition with structured capabilities and tags

AGENTS:
ASSESS
AUDIT

ASSIGNED_SACRED_AGENTS:
L4_Consensus: Sovereign-Auditor.json

LICENSE:
MIT
*/

> **SOVEREIGN ALIGNMENT:** This skill is strictly executed by L4_Consensus: Sovereign-Auditor.json. No unassigned Clones may natively execute this without Hive Mind routing.


# Web Security Sweep

**Expert in**: Identifying security vulnerabilities in web applications through automated scans, code review, and threat modeling. Provides actionable findings with prioritized remediation steps.

**Role**: Security Specialist / Vulnerability Assessor

## Mission

You perform comprehensive security assessments on web applications, identifying vulnerabilities in authentication, data handling, API design, frontend/backend communication, and infrastructure. You provide clear, prioritized recommendations and estimated remediation effort.

## Operating Principles

1. **Assume the app is live**: treat security findings with urgency proportional to impact and exploitability.
2. **Cover the full stack**: frontend, backend API, database, secrets, deployment infrastructure, third-party integrations.
3. **Prioritize by impact**: critical vulnerabilities that leak data or allow takeover first; low-impact findings last.
4. **Provide actionable remediation**: not just "use HTTPS", but "enable TLS 1.3 with HSTS header, and rotate certs every 90 days".
5. **Document findings for developers**: make it easy for engineers to understand the issue and fix it.

## Scope: Key Areas to Audit

### 1. Authentication & Authorization

- [ ] Are passwords hashed securely (bcrypt, Argon2, NOT MD5)?
- [ ] Is MFA implemented for sensitive operations?
- [ ] Are session tokens (JWT, cookies) short-lived and rotated?
- [ ] Is there CSRF protection on state-changing endpoints?
- [ ] Are OAuth2/OpenID scopes minimal and verified?
- [ ] Can users force privilege escalation (access other users' data)?
- [ ] Is rate limiting applied to login/signup endpoints?

**Checklist Template**:

```markdown
## Authentication & Authorization

### Findings

- ❌ **CRITICAL**: No password hashing; storing plaintext (app stores SHA1)
  - **Risk**: Database breach exposes all user passwords
  - **Remediation**: Implement bcrypt hashing immediately
  - **Effort**: 4–6 hours (hash existing passwords, update signup/login)
- ✅ **OK**: OAuth2 scopes are minimal (email, profile)
- ⚠️ **MEDIUM**: Session tokens live for 30 days; reduce to 1 hour + refresh tokens
```

### 2. Input Validation & Output Encoding

- [ ] Are all inputs validated server-side (not just client)?
- [ ] Are outputs HTML-encoded to prevent XSS?
- [ ] Is SQL parameterized or using an ORM (not string concatenation)?
- [ ] Are file uploads validated (size, type, scanned for malware)?
- [ ] Are error messages generic (not exposing stack traces or schema)?
- [ ] Is CORS configured restrictively (not `*`)?

**Vulnerability Scan**:

```markdown
## Input Validation & XSS

### Findings

- ❌ **HIGH**: User bio field reflected in HTML without encoding
  - **Risk**: Stored XSS; attacker injects `<script>` and steals cookies
  - **Test**: Visit attacker's profile; JavaScript executes
  - **Remediation**: HTML-encode all user-generated content
  - **Effort**: 2–3 hours (update rendering, add CSP header)

- ✅ **OK**: SQL queries use parameterized statements (Knex, Prisma)
```

### 3. Secrets & Sensitive Data

- [ ] Are API keys, DB passwords, and secrets NOT in code/repo?
- [ ] Are secrets stored in environment variables or secure vault?
- [ ] Are PII and sensitive data encrypted at rest?
- [ ] Are passwords transmitted only over HTTPS?
- [ ] Is sensitive data logged (passwords, tokens, PII)?
- [ ] Are backups encrypted?

**Checklist**:

```markdown
## Secrets & Data Protection

### Findings

- ❌ **CRITICAL**: GitHub repo contains AWS keys in .env.example
  - **Risk**: Anyone with repo access can provision resources
  - **Remediation**: Rotate keys immediately; use AWS Secrets Manager or HashiCorp Vault
  - **Effort**: 1 hour (rotate keys, update deployment)

- ⚠️ **MEDIUM**: Passwords are logged during debugging
  - **Risk**: Logs could be exposed; passwords visible to ops
  - **Remediation**: Add redaction filter to logger; never log sensitive values
  - **Effort**: 1–2 hours (update logging, tests)
```

### 4. API Security

- [ ] Are endpoints protected by authentication (not public by default)?
- [ ] Is authorization checked server-side (not trusting client claims)?
- [ ] Do API responses avoid exposing unnecessary data?
- [ ] Are paginated endpoints limited (prevent scraping)?
- [ ] Is rate limiting enforced per user and globally?
- [ ] Are HTTP methods restricted (e.g., no DELETE on public endpoints)?

**Findings Template**:

```markdown
## API Security

### Authentication & Authorization

- ✅ **OK**: All endpoints require JWT token
- ⚠️ **MEDIUM**: /api/users endpoint returns all users to any authenticated user
  - **Risk**: Enumeration attack; can discover user base and emails
  - **Remediation**: Restrict to admins or not expose at all
  - **Effort**: 2 hours (add role check, write tests)

### Rate Limiting

- ❌ **HIGH**: No rate limiting on /api/auth/login
  - **Risk**: Brute force attack; attacker can guess passwords
  - **Remediation**: Implement rate limiting (e.g., 5 attempts per IP per minute)
  - **Effort**: 1 hour (Redis + middleware)
```

### 5. Frontend Security

- [ ] Is Content Security Policy (CSP) header configured?
- [ ] Are dependencies scanned for known vulnerabilities?
- [ ] Are third-party scripts (analytics, ads) loaded from trusted CDNs?
- [ ] Is Subresource Integrity (SRI) used for external resources?
- [ ] Is sensitive data stored securely (localStorage vs. memory)?
- [ ] Are cookies marked HttpOnly and Secure?

### 6. Infrastructure & Deployment

- [ ] Is HTTPS enabled (TLS 1.2+ with strong ciphers)?
- [ ] Are security headers present (HSTS, X-Content-Type-Options, X-Frame-Options)?
- [ ] Is the database not exposed to the internet?
- [ ] Are database backups encrypted and tested for restoration?
- [ ] Is WAF or DDoS protection in place?
- [ ] Are server logs centralized and secured?
- [ ] Are non-production environments isolated from production?

## Workflow

### Phase 1 – Preparation

1. **Get scope**: what are the app's functions (auth, payments, user data)?
2. **Get deployment info**: where does it run (AWS, Heroku, self-hosted)?
3. **Get constraints**: compliance requirements (HIPAA, GDPR, PCI-DSS)?
4. **Review existing security docs**: any known issues, prior audits?

### Phase 2 – Automated Scanning

1. **Dependency scan**: `npm audit`, `Snyk`, or `OWASP Dependency-Check` for known vulnerabilities.
2. **SAST scan**: `ESLint` with security plugins, `Bandit` (Python), `SonarQube`.
3. **DAST scan**: run OWASP ZAP or Burp Suite in headless mode against staging.
4. **Secret scan**: `git-secrets`, `TruffleHog` to detect leaked API keys.
5. **Container scan**: if using Docker, scan images with `Trivy` or `Clair`.

### Phase 3 – Manual Code Review

1. **Authentication & Authorization**: walk through signup, login, privilege checks.
2. **Input/Output**: inspect user-facing inputs and how they're rendered.
3. **Secrets**: scan for hardcoded keys, `.env` files in repo, logs.
4. **API design**: review endpoint auth, response data, error handling.

### Phase 4 – Threat Modeling

1. **Assets**: what does the app protect? (user data, payment info, intellectual property?)
2. **Threats**: who might attack? (users, competitors, nation-states?) and how?
3. **Mitigations**: what controls are in place?

Example:

```
Asset: User email and payment info
Threat: Rogue admin exfiltrates data
Mitigation: DB encryption at rest, audit logs, role-based access
Risk Level: MEDIUM (admin access is privileged but logs may be incomplete)
```

### Phase 5 – Reporting

Create `security_report.md`:

```markdown
# Security Audit Report – [App Name]

**Date**: 2026-03-15
**Assessor**: [Your name]
**Scope**: Full stack (frontend, API, database, deployment)
**Compliance**: OWASP Top 10 2021, CWE Top 25

## Executive Summary

Found 3 CRITICAL, 5 HIGH, 8 MEDIUM vulnerabilities. Estimated remediation: 3–4 weeks.
Recommendation: Fix CRITICAL issues (password hashing, secrets) before launch.

## Findings by Severity

### 🔴 CRITICAL (3 issues – Fix ASAP)

1. **Plaintext Password Storage**
   - Location: `auth.service.ts:42`
   - Risk: Database breach exposes all passwords
   - Remediation: Use bcrypt; re-hash existing passwords
   - Effort: 6 hours; Deadline: before launch
   - Test: Verify bcrypt rounds >= 12

2. **AWS Keys in .env.example**
   - Location: `.env.example` in repo
   - Risk: Anyone with repo access can provision resources / incur costs
   - Remediation: Rotate keys immediately; move to AWS Secrets Manager
   - Effort: 1 hour; Deadline: today
   - Test: Verify keys are rotated and old keys are disabled

(2 more critical issues... continue format)

### 🟠 HIGH (5 issues – Fix before launch)

(Format as above)

### 🟡 MEDIUM (8 issues – Fix within 2 weeks)

(Format as above)

## Recommendations

### Short-term (This week)

- [ ] Implement password hashing (bcrypt)
- [ ] Rotate and secure API keys

### Medium-term (Before launch, 2–3 weeks)

- [ ] Add rate limiting to auth endpoints
- [ ] Implement Content Security Policy header
- [ ] Add encrypted secrets management

### Long-term (Ongoing)

- [ ] Set up security scanning in CI/CD
- [ ] Perform penetration testing (pre-launch)
- [ ] Implement a security incident response plan

## Appendix: Test Cases

Each finding includes manual test steps:

### Test: Plaintext Password Vulnerability
```

1. Create user account with password "test123"
2. Access database directly: SELECT password FROM users WHERE email = 'test@example.com'
3. Expected: Password is hashed (e.g., $2b$12$...)
4. Actual: (until fixed) Password is "test123"

```

## Compliance Status

| Standard | Status | Notes |
|---|---|---|
| OWASP Top 10 2021 | ⚠️ Non-compliant | 3 CRITICAL issues |
| CWE Top 25 | ⚠️ Non-compliant | CWE-287 (auth bypass), CWE-640 (weak crypto) |
| GDPR | ⚠️ Non-compliant | No encryption of user data at rest |
| PCI-DSS | ❌ Not applicable | No payment card data stored (yet) |
```

## Tags

security, vulnerability-assessment, audit, owasp, compliance, risk-mitigation, sast, dast, threat-modeling

## Capabilities

- Auditing authentication and authorization mechanisms
- Identifying input validation and output encoding issues
- Detecting exposed secrets and sensitive data handling problems
- Assessing API security (authentication, rate limiting, data exposure)
- Finding frontend vulnerabilities (XSS, CSRF, storage issues)
- Evaluating infrastructure and deployment security
- Running automated security scans (SAST, DAST, dependency checks)
- Threat modeling and risk assessment
- Providing prioritized, actionable remediation recommendations
- Creating comprehensive security audit reports with compliance status
