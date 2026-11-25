---
name: security-audit
description: Audits a file or directory for security vulnerabilities (OWASP Top 10 focus)
argument-hint: [file-or-directory]
user-invocable: true
allowed-tools: Read Grep Glob
effort: medium
---

## Security Audit

Target: **$1** (or entire `src/` if not specified)

Check for each OWASP Top 10 category:

### A01 - Broken Access Control
- Routes missing auth middleware
- Direct object references without ownership check
- Admin endpoints without role check

### A02 - Cryptographic Failures
- Hardcoded secrets or keys
- Weak hashing (MD5, SHA1 for passwords)
- HTTP instead of HTTPS for sensitive data
- Sensitive data stored in localStorage

### A03 - Injection
- SQL string concatenation (not parameterized queries)
- Unsanitized input passed to `eval()`, `exec()`, `child_process`
- Template injection risks

### A04 - Insecure Design
- Missing rate limiting on auth endpoints
- No account lockout after failed attempts

### A05 - Security Misconfiguration
- Debug mode enabled in production
- Overly permissive CORS (`*`)
- Default credentials

### A07 - Auth & Session Failures
- Weak JWT validation
- Missing token expiry
- Session not invalidated on logout

---

Report findings as:
- **CRITICAL** - immediate action required
- **HIGH** - fix before next release
- **MEDIUM** - fix in next sprint
- **INFO** - best practice recommendation
