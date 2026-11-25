---
name: security-audit
description: "On-demand security audit checklist based on OWASP Top 10. Use before any git push. Reports written to .attacca/audits/latest.md with verdict that unlocks the push gate."
---

<!-- Delete when: native Claude Code OWASP-based security scanner with remediation suggestions is available -->

# Security Audit Skill

On-demand security audit before push. Can delegate to security-auditor subagent or run inline.

## When to Use
- Before any git push (pre-push gate)
- After implementing authentication or authorization
- When adding new API endpoints
- When handling user input or file uploads
- When adding dependencies
- When user requests a security review

## Quick Flow

1. **Run checks** (inline or delegate to security-auditor subagent with file paths only)
2. **Triage findings** into CRITICAL, HIGH, MEDIUM, LOW
3. **Write report** to `.attacca/audits/latest.md`
4. **Verdict**: `VERDICT: CLEAN` (if zero CRITICAL/HIGH) or `VERDICT: FINDINGS`
5. **Push gate**: blocked if verdict is FINDINGS; unlocked if CLEAN

---

## Audit Checklist (OWASP Top 10)

### A1. Broken Access Control
- [ ] Every route/endpoint has authorization checks
- [ ] RBAC enforced server-side, not UI-only
- [ ] Direct object references validated (user A can't access user B's data)
- [ ] Unauthorized returns 403/404, not 200 with empty data
- [ ] Admin functions not bypassable via parameters

### A2. Cryptographic Failures
- [ ] No secrets/keys/passwords in source code
- [ ] No secrets in committed `.env` files
- [ ] Passwords hashed (bcrypt/argon2, not MD5/SHA1)
- [ ] Sensitive data encrypted at rest and in transit
- [ ] No custom cryptography implementations

### A3. Injection
- [ ] SQL queries parameterized (no string concatenation)
- [ ] NoSQL queries parameterized
- [ ] HTML output escaped
- [ ] Shell arguments sanitized
- [ ] File paths validated (no traversal)
- [ ] GraphQL has rate/complexity limits

### A4. Insecure Design
- [ ] Rate limiting on auth endpoints
- [ ] Input validation client + server
- [ ] File upload: type/size checks
- [ ] No debug endpoints in production
- [ ] Least privilege throughout

### A5. Security Misconfiguration
- [ ] CORS configured restrictively (not `*`)
- [ ] Security headers present (CSP, HSTS, X-Frame-Options)
- [ ] Default credentials changed
- [ ] Directory listing disabled
- [ ] Stack traces not exposed
- [ ] Unnecessary services disabled

### A6. Vulnerable Components
- [ ] `npm audit` / `pip audit` / equivalent: no CRITICAL
- [ ] No deprecated dependencies
- [ ] Dependencies pinned to versions
- [ ] Known CVEs checked

### A7. Authentication Failures
- [ ] Strong password requirements
- [ ] Account lockout after N failures
- [ ] Session tokens: random, long, httpOnly
- [ ] JWT tokens: expiration + server-side validation
- [ ] Logout invalidates server-side
- [ ] Password reset: single-use, time-limited

### A8. Data Integrity
- [ ] CSRF protection on mutations
- [ ] API requests authenticated (not cookies alone)
- [ ] Update signatures verified
- [ ] Untrusted deserialization avoided

### A9. Logging & Monitoring
- [ ] Auth events logged (login, fail, logout)
- [ ] Authorization failures logged
- [ ] Sensitive data NOT in logs
- [ ] Logs tamper-resistant
- [ ] Alerting for suspicious patterns

### A10. SSRF
- [ ] User-supplied URLs validated against allowlist
- [ ] Internal addresses blocked
- [ ] Redirects don't access internal services

---

## Report Format

Write to `.attacca/audits/latest.md`:

```markdown
# Security Audit
**Date**: [ISO date] | **Scope**: [what was audited]

## Findings

### CRITICAL (Block Push)
| # | Category | File:Line | Issue | Remediation |
|---|----------|-----------|-------|------------|
| 1 | A3-Injection | app.js:42 | SQL concat | Use parameterized query |

### HIGH (Fix Before Next Push)
| # | Category | File:Line | Issue | Remediation |
|---|----------|-----------|-------|------------|

### MEDIUM (Fix This Sprint)
| # | Category | File:Line | Issue | Remediation |
|---|----------|-----------|-------|------------|

### LOW (Track)
| # | Category | File:Line | Issue | Remediation |
|---|----------|-----------|-------|------------|

## Passed Checks
- [x] [Check that passed]
- [x] [Check that passed]

## Notes
[Any context or recommendations]

VERDICT: CLEAN
```

Or:

```markdown
...
VERDICT: FINDINGS
```

---

## Delegation Option

Optionally invoke security-auditor subagent with **file paths only** (no implementation details):

```
Please audit these files for OWASP Top 10 vulnerabilities:
- src/auth/login.ts
- src/api/users.ts
- src/db/queries.ts
```

Subagent audits and returns findings. You triage and write the final report.

---

## Push Gate

- **VERDICT: CLEAN** → push is allowed
- **VERDICT: FINDINGS** → push is blocked until verdict changes to CLEAN

Hook greps for "VERDICT: CLEAN" in `.attacca/audits/latest.md` before push.
