---
name: team-security-review
description: Security review methodology. Authentication, authorization, input validation, secret management, dependency scanning and finding reporting. The playbook of the security role.
---

# Security Review

## Core principle

**Read the code, do not guess.** A security finding is only a finding if you have read the actual code path. A "this might happen" hypothesis is not a finding — mark it as "suspicious".

## 1. Authentication

- Password: strong hash (argon2id/bcrypt), never SHA/MD5, never plaintext
- Session: cookie with `httpOnly` + `secure` + `sameSite`, idle and absolute timeout
- Token: short lifetime, `refresh` rotation, revocable in case of leakage
- Account lockout: attempt count + time-based throttling
- Password reset: single-use and time-limited token
- MFA: for administrator/critical operations

## 2. Authorization

Do two checks for every endpoint:
1. **Functional**: does this person have permission to perform this action?
2. **Resource-based**: do they own this resource? (IDOR)

Patterns to check:
- An endpoint without authentication (not on the allowlist)
- The `id` parameter used directly (not compared against the user's own record)
- An "edit" endpoint exists but the "delete" endpoint has no permission check
- Administrator endpoints are only hidden in the interface, not checked on the server
- Bulk operation endpoints (could mix the user's data with someone else's)

## 3. Input validation

| Attack | Protection |
|---|---|
| SQL/NoSQL injection | Parameterized queries, ORM, schema validation |
| XSS | Output escaping, dangerouslySetInnerHTML forbidden, CSP |
| SSRF | Allowlist of permitted hosts, private IP range blocking |
| Path traversal | Path normalization, blocking escapes from the root directory |
| Mass assignment | Allowlist of permitted fields |
| Deserialization | Untrusted data is never deserialized |
| ReDoS | No dangerous regex, input length limited |

Checklist:
- Does every user input pass through a class (type + format + length + range)?
- Is input validation applied in the application layer, or only on the client? (client validation is not security)
- Do error messages leak internal details (stack trace, SQL)?

## 4. Secret management

- Are secrets embedded in the code? (Has `.env` entered the repo, is it in `git log`?)
- Are there secrets in the logs? (token, password, full card number)
- Is the secret in production or in development?
- Is the error shown to the user separate from the error that is logged?
- Is `.gitignore` correct? Is `.env` tracked?

In the finding report, **do not write the value of the secret** — the file path and the type are enough.

## 5. Dependencies

Run these and put the output in the report:
```bash
npm audit        # Node
pip-audit        # Python
cargo audit      # Rust
govulncheck      # Go
```

List the critical/high vulnerabilities and state which ones are actually on a code path that is used.

## 6. Transport and browser

- HTTPS mandatory, HSTS
- Cookie flags: `httpOnly`, `secure`, `sameSite`
- CORS: `Access-Control-Allow-Origin: *` + authenticated requests = critical
- Security headers: CSP, `X-Content-Type-Options`, `Referrer-Policy`
- CSRF protection on form POSTs (cookie-based sessions)

## 7. Finding report

For each finding:

```
[Severity] Title
Location: file:line
Impact: <what an attacker can do>
Reproduction: <step by step>
Fix: <concrete suggestion>
Status: fixed / open / accepted
```

Severity levels:

| Level | Criteria |
|---|---|
| Critical | Data leak, authentication bypass, remote code execution |
| High | Privilege escalation, IDOR, secret leak |
| Medium | XSS (reflected), CSRF, missing rate limit |
| Low | Information leak, missing header, version disclosure |

Do not make up a CVSS score. Write the impact and derive the severity from the impact.

## Common mistakes

| Mistake | The right way |
|---|---|
| Making up a finding without reading the code | Read it, verify it, then write it |
| Guessing a CVSS score | Write the impact text |
| Writing the secret into the report | Location and type only |
| Looking only at the application layer | Infrastructure and deployment settings are in scope too |
| Closing a finding before it is fixed | Fix first, then verify |

## Output format

Markdown: Summary / Finding table (severity, location, impact, status) / Finding details / Dependency scan output / Remaining risks.

In the user's language (Turkish or English).
