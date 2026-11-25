---
name: penetration-test-plan
description: Design penetration testing plans with scope, methodology, tools, and reporting. Outputs test scenarios, OWASP Top 10 coverage, and remediation priorities.
argument-hint: [application type, compliance requirements, risk tolerance]
allowed-tools: Read, Write, Bash
---

# Penetration Testing Plan

Design systematic penetration tests for applications. Not random poking — methodical testing with OWASP Top 10, defined scope, rules of engagement, and actionable findings.

## Process

1. **Define scope.** URLs, IP ranges, credentials, out-of-scope systems.
2. **Choose methodology.** Black box, grey box, white box.
3. **Set rules of engagement.** Time windows, DoS limits, data handling.
4. **Map attack surface.** Endpoints, parameters, authentication, file uploads.
5. **Execute tests.** OWASP Top 10, business logic, authorization flaws.
6. **Document findings.** Severity (critical/high/medium/low), reproduction steps, remediation.
7. **Retest fixes.** Verify vulnerabilities patched correctly.

## Output Format

### Penetration Test: [Application Name]

**Scope:** Web app + API (staging environment)  
**Methodology:** Grey box (credentials provided)  
**Duration:** 40 hours over 2 weeks  
**Findings:** 2 critical, 5 high, 12 medium, 8 low  
**CVSS Scores:** Average 6.2

---

## Scope Definition

```
In-Scope:
- Web application: https://app.example.com
- API: https://api.example.com
- Mobile app (iOS/Android)
- Test user credentials provided
- Staging environment only

Out-of-Scope:
- Production environment
- Third-party services (Stripe, Auth0)
- Physical security
- Social engineering
- Denial of Service attacks

Rules of Engagement:
- Testing window: Mon-Fri 9am-5pm EST
- Max 100 requests/second (avoid DoS)
- Don't delete/modify production data
- Report critical findings within 24 hours
- Encrypt all reports
```

---

## OWASP Top 10 Coverage

### 1. Broken Access Control
- Horizontal privilege escalation (IDOR)
- Vertical privilege escalation
- Forced browsing to admin pages

### 2. Cryptographic Failures
- Sensitive data in transit (HTTP)
- Weak encryption algorithms
- Exposed credentials in code/config

### 3. Injection
- SQL injection
- Command injection
- LDAP/NoSQL injection

### 4. Insecure Design
- Business logic flaws
- Race conditions
- Missing rate limiting

### 5. Security Misconfiguration
- Default credentials
- Directory listing
- Verbose error messages

### 6. Vulnerable Components
- Outdated libraries
- Known CVEs in dependencies

### 7. Authentication Failures
- Brute force attacks
- Session fixation
- Weak password policy

### 8. Software Integrity Failures
- Insecure deserialization
- Unsigned packages/updates

### 9. Logging Failures
- Missing audit logs
- No monitoring/alerting

### 10. SSRF
- Internal network access
- Cloud metadata endpoints

---

## Testing Tools

### Burp Suite
```
Configure proxy
Intercept/modify requests
Scanner for automated testing
```

### OWASP ZAP
```bash
zap-cli quick-scan https://example.com
# Automated vulnerability scanning
```

### SQLMap
```bash
sqlmap -u "https://site.com?id=1" --dump
# SQL injection testing
```

### Nmap
```bash
nmap -sV -sC example.com
# Port scanning, service detection
```

---

## Severity Scoring (CVSS)

```
Critical (9.0-10.0): RCE, Auth bypass, Full DB access
High (7.0-8.9): Stored XSS, Privilege escalation
Medium (4.0-6.9): Reflected XSS, CSRF
Low (0.1-3.9): Info disclosure, Missing headers
```

---

## Finding Report Template

```markdown
## Finding: [Vulnerability Name]

**Severity:** Critical  
**CVSS Score:** 9.8  
**Component:** /api/search

### Description
SQL injection allows database extraction.

### Reproduction
1. Navigate to /products
2. Search: ' OR '1'='1' --
3. Returns all records

### Impact
- Full database access
- Authentication bypass
- Data exfiltration

### Remediation
Use parameterized queries:
```python
cursor.execute("SELECT * FROM products WHERE name=%s", (search,))
```

### References
- OWASP A03:2021
- CWE-89
```

## Rules

- Define scope explicitly — avoid legal issues, stay in bounds.
- OWASP Top 10 minimum coverage — industry standard baseline.
- Document reproduction steps — developers need exact payloads.
- CVSS scoring for objectivity — standardized severity ratings.
- Test authorization, not just authentication — logged in ≠ authorized.
- Report critical immediately — don't wait for final report.
- Retest all fixes — verify patch works, not just deployed.
- Encrypt findings — contain sensitive vulnerability details.
- Provide fix guidance — how to remediate, not just "you're vulnerable."
- Track remediation status — ensure fixes actually happen.
