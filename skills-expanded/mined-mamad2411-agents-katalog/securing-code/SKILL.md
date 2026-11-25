---
name: securing-code
description: Audits and hardens application code against the OWASP Top 10 and OWASP ASVS — injection, broken access control, authentication, secrets, crypto, SSRF, dependencies, and logging. Use for security reviews, before releasing features that handle user input, auth, payments, or PII, or when the user mentions vulnerabilities, CVEs, or OWASP.
metadata:
  role: senior-developer
  version: "1.0"
---

# Securing code

Assume every input is hostile and every dependency can be compromised. Report only issues you can tie to a concrete exploit path.

## Workflow

```
Security review progress:
- [ ] 1. Map entry points and trust boundaries
- [ ] 2. Trace untrusted data to dangerous sinks
- [ ] 3. Check authentication and authorization
- [ ] 4. Check secrets, crypto, and configuration
- [ ] 5. Scan dependencies and supply chain
- [ ] 6. Verify findings and report
```

**1. Entry points.** HTTP handlers, message consumers, CLI args, file uploads, webhooks, env/config, third-party callbacks. Mark where data crosses a trust boundary.

**2. Source → sink.** Follow each untrusted value to:

| Sink | Risk | Safe pattern |
|------|------|--------------|
| SQL / NoSQL query | Injection | Parameterized queries / query builders; never string concat |
| Shell / `exec` | Command injection | Avoid shell; pass argv arrays; allowlist |
| HTML / templates | XSS | Context-aware auto-escaping; CSP; no `innerHTML` with user data |
| File paths | Path traversal | Resolve and verify prefix; never join raw input |
| Outbound URL fetch | SSRF | Allowlist hosts; block private/link-local/metadata IPs after DNS resolve |
| Deserializer | RCE | Safe formats (JSON) with schema; no native object deserialization of untrusted data |
| Redirects | Open redirect | Allowlist relative paths |
| Regex | ReDoS | Bounded patterns, timeouts, linear-time engines |

**3. AuthN/AuthZ (OWASP A01, A07).**
- Every endpoint checks authorization server-side, *per object* (IDOR/BOLA): "can this user access *this* record?"
- Deny by default. Role checks centralized, not copy-pasted.
- Passwords: Argon2id/bcrypt/scrypt; MFA available; rate-limit and lock out brute force.
- Sessions/tokens: short-lived, rotated, `HttpOnly; Secure; SameSite` cookies; validate JWT `alg`, `iss`, `aud`, `exp`.
- CSRF protection on cookie-authenticated state-changing requests.

**4. Secrets, crypto, config (A02, A05).**
- No secrets in code, logs, URLs, or error messages; load from a secret manager.
- TLS everywhere; modern AEAD ciphers (AES-GCM, ChaCha20-Poly1305); never roll your own crypto; use CSPRNG for tokens.
- Security headers (HSTS, CSP, X-Content-Type-Options), debug off, verbose errors off in production, least-privilege IAM.

**5. Supply chain (A06, A08).** Run the ecosystem audit (`npm audit`, `pip-audit`, `govulncheck`, `cargo audit`, `osv-scanner`). Pin versions with lockfiles, verify integrity, generate an SBOM, pin CI actions by commit SHA.

**6. Logging (A09).** Security events (login, authz failure, privilege change) logged with user/request id; no PII/secrets in logs; alerts on anomalies.

## Report format

```markdown
### [Critical|High|Medium|Low] <title> — `path:line`
**Category:** OWASP A0x / CWE-nnn
**Exploit scenario:** <attacker input → impact>
**Fix:** <specific code change>
```

Rate severity by exploitability × impact. Put Critical/High first. If nothing is found, say what was checked.
