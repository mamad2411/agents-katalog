---
name: full-stack-security-engineer
description: "Audit and harden an application across the full stack: web, API,
  backend, database, and deployment. Use for security reviews and remediation."
metadata:
  tags: full, stack, security, engineer
---

# Full-Stack Security Engineering

## Use this skill when
- Performing security review of a web application end to end
- Hardening authentication, authorization, and data handling
- Prioritizing and remediating vulnerabilities
- Writing security-focused rules for a new feature

## Do not use this skill when
- When the user asked for a performance or feature review
- Code changes are explicitly forbidden and analysis is read-only (write a report)

## Instructions
1. Map the attack surface: entry points, auth flows, data stores, third-party surfaces.
2. Review in layers: frontend, API/backend, database, infrastructure.
3. Check identity: authn flows, session/token handling, MFA, password storage.
4. Check authorization: server-side enforcement at every action, not UI only.
5. Check input handling: injection (SQL, NoSQL, command, template), uploads, SSRF.
6. Check output: XSS, CSP, unsafe HTML, open redirects.
7. Check data: secrets in code/config, PII exposure in logs and responses, encryption at rest/in transit.
8. Check dependencies for known vulnerable versions.
9. Classify each finding by severity (CVSS-informed) with reproduction steps and a concrete fix.
10. Produce a prioritized remediation plan; verify fixes with tests.

## Rules
- READ ONLY by default for audit mode; never modify code unless explicitly asked

## Checklist
- OWASP Top 10 covered
- Auth enforced server-side
- No secrets in repo/logs
- Severity + fix per finding

## Output Format
- Finding | severity | location | impact | reproduction | fix

## Common Mistakes
- Trusting client-side security
- Security by obscurity (no real controls)
- Skipping authorization checks in review
- Reporting without reproduction or fix

## References
- `references/owasp-top10.md` – OWASP Top 10 (2021) quick reference and verification checklist
- `references/auth-checklist.md` – authentication, authorization, session, and secrets checklist
- `references/api-web-security.md` – injection/XSS, API pitfalls, headers, and data exposure notes
