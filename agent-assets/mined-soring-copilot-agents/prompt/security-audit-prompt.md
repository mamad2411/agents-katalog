---
name: security-audit
description: Run a comprehensive security audit on a file or the full codebase
agent: security
model: Claude Opus 4.6
tools:
  - codebase
  - search
  - changes
  - problems
  - usages
  - fetch
---

# Security Audit

## Scope: ${input:scope:File path, module name, or "full codebase"}

Perform a comprehensive security audit following the OWASP Top 10 methodology.

### Focus Areas

1. **Input Validation** — Are all user inputs validated server-side? Any injection vectors?
2. **Authentication** — Are auth endpoints secure? Token handling correct? Password hashing strong?
3. **Authorization** — Are permission checks enforced at the service layer? Any IDOR risks?
4. **Data Exposure** — Are sensitive fields excluded from API responses? Secrets in logs?
5. **Dependencies** — Any packages with known CVEs? Unused dependencies?
6. **Configuration** — CORS settings, debug mode, security headers, cookie flags?
7. **Cryptography** — Proper hashing algorithms? Secure token generation? HTTPS enforcement?

### Deliverables

- Prioritized vulnerability list with severity ratings (Critical/High/Medium/Low)
- CWE references for each finding
- Specific remediation guidance with code examples
- List of security strengths observed
- Recommended next steps

After the audit, use handoff buttons to route fixes to the Implementer or security tests to the Tester.
