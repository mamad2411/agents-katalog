---
name: security-audit
description: Comprehensive security auditing for code, dependencies, and infrastructure.
---

# Security Audit

Systematic security review for applications and infrastructure.

## Code Security
1. **Input Validation**: Check all entry points — API params, URL paths, form data, headers
2. **Output Encoding**: Verify HTML, JS, CSS, URL context encoding
3. **Auth & Session**: Token expiry, session invalidation, privilege boundaries
4. **Crypto**: Algorithm choices, key management, random number generation
5. **Injection**: SQL, NoSQL, command, LDAP, XPath injection vectors
6. **SSRF/CSRF**: Server-side request forgery, cross-site request forgery

## Dependency Audit
1. Run `npm audit` / `pip-audit` / `cargo audit` / `govulncheck`
2. Check transitive dependencies for known CVEs
3. Verify license compatibility
4. Pin critical dependencies to specific versions

## Infrastructure Security
1. **Network**: Firewalls, security groups, VPC configuration
2. **Storage**: Encryption at rest, access policies, backup security
3. **Secrets**: Vault integration, no hardcoded secrets, rotation policy
4. **TLS**: Certificate validity, cipher suites, HSTS headers
5. **Cloud**: IAM policies, least-privilege, resource exposure

## OWASP Top 10 Coverage
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable Components
- A07: Auth Failures
- A08: Software & Data Integrity
- A09: Logging & Monitoring
- A10: SSRF

## Reporting Format
```
SEVERITY: [CRITICAL/HIGH/MEDIUM/LOW]
LOCATION: file:line
DESCRIPTION: What the vulnerability is
EVIDENCE: Code snippet or command output
REMEDIATION: Specific fix with code example
```
