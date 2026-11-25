---
name: security-testing
description: >
  Plan security testing — OWASP test cases, authentication testing, authorization
  testing, input validation, session management, and vulnerability scanning.
  TRIGGER when: user says /security-testing, needs to plan application security
  testing, or asks about security QA practices.
argument-hint: "[application or feature to security test]"
user-invocable: true
---
# Security Testing Plan
## Process
### Step 1: Define Scope
| Element | Details |
|---------|---------|
| Application | Name, type (web/mobile/API), technology stack |
| Test type | SAST, DAST, penetration, code review |
| Priority areas | Auth, payments, data handling, file upload |
| Compliance | OWASP Top 10, PCI-DSS, HIPAA requirements |
### Step 2: OWASP Top 10 Test Matrix
| # | Category | Test Cases | Status |
|---|----------|-----------|--------|
| A01 | Broken Access Control | IDOR, privilege escalation, path traversal | ☐ |
| A02 | Cryptographic Failures | Weak ciphers, plaintext storage, cert validation | ☐ |
| A03 | Injection | SQL, XSS, command, LDAP injection | ☐ |
| A04 | Insecure Design | Business logic flaws, missing rate limits | ☐ |
| A05 | Security Misconfiguration | Default configs, unnecessary features, headers | ☐ |
| A06 | Vulnerable Components | Known CVEs in dependencies | ☐ |
| A07 | Auth Failures | Brute force, credential stuffing, session fixation | ☐ |
| A08 | Data Integrity Failures | Deserialization, CI/CD integrity | ☐ |
| A09 | Logging Failures | Missing audit logs, log injection | ☐ |
| A10 | SSRF | Server-side request forgery | ☐ |
### Step 3: Authentication Testing
| Test | Method |
|------|--------|
| Password policy enforcement | Try weak passwords |
| Brute force protection | Automated login attempts |
| Session management | Token expiry, rotation, invalidation |
| MFA bypass | Test MFA implementation |
| Password reset | Token predictability, account enumeration |
### Step 4: Authorization Testing
| Test | Method |
|------|--------|
| Horizontal privilege | Access other users' data |
| Vertical privilege | Access higher-privilege functions |
| Direct object reference | Modify IDs in requests |
| API authorization | Test endpoints without valid tokens |
### Step 5: Report Findings
| Finding | Severity | CVSS | Reproduction Steps | Recommendation |
|---------|----------|------|-------------------|---------------|
| [issue] | Critical/High/Med/Low | X.X | [steps] | [fix] |
## Output Format
```markdown
## Security Test Report: [Application]
### Scope: [What was tested]
### Findings Summary: [Critical: X, High: X, Medium: X, Low: X]
### Detailed Findings: [Per finding with reproduction steps]
### Recommendations: [Prioritized fixes]
```
## Quality Checklist
- [ ] OWASP Top 10 covered
- [ ] Authentication and authorization tested
- [ ] Findings have reproduction steps
- [ ] Severity ratings use CVSS
- [ ] Remediation recommendations provided
## Edge Cases
- For APIs, focus on authentication, rate limiting, and input validation
- For mobile apps, include local storage and certificate pinning checks
- If in regulated industry, map findings to compliance requirements
