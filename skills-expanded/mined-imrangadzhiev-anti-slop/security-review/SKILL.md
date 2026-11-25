---
name: security-review
description: Review code for security issues before merge — authz gaps, injection, secrets, unsafe defaults, SSRF, path traversal. Use when reviewing a PR, auditing a diff, shipping auth/payments/uploads, or when the user asks for a security review or OWASP check.
---

# Security Review

Review the current change like a security-minded senior. Prefer concrete findings over generic advice.

## Scope

Focus on the diff and directly related call paths. Do not audit the whole repo unless asked.

## Checklist

### Auth & access

- [ ] Every sensitive action checks authentication **and** authorization
- [ ] IDs from the client are not trusted for ownership (`userId` in body ≠ proof)
- [ ] Admin/debug routes are gated; no "temporary" open endpoints

### Input & data

- [ ] User input is validated at the boundary (type, length, allowlist)
- [ ] SQL/NoSQL/search queries are parameterized — no string concat
- [ ] HTML/Markdown/user content is escaped or sanitized where rendered
- [ ] File uploads: size limits, type allowlist, stored outside web root, randomized names
- [ ] Path joins cannot escape intended directories (`../`)

### Secrets & config

- [ ] No secrets in source, logs, client bundles, or example env files with real values
- [ ] New env vars documented; defaults are safe for production
- [ ] Tokens/passwords not written to analytics or error trackers

### Network & server

- [ ] Outbound fetches do not accept raw user URLs without allowlisting (SSRF)
- [ ] CORS is least-privilege; credentials only when required
- [ ] Cookies: `HttpOnly`, `Secure`, `SameSite` where applicable

### Dangerous APIs

- [ ] No `eval`, `dangerouslySetInnerHTML`, shell `exec` with unsanitized input
- [ ] Deserialization of untrusted data is avoided or hardened
- [ ] Crypto/auth libraries are standard — no home-rolled JWT/crypto

## Output format

Group findings:

| Severity | Rule | Where | Why it matters | Fix |
|----------|------|-------|----------------|-----|
| Critical / High / Medium / Low / Note | short name | `file:line` or symbol | 1 sentence | concrete change |

End with:

- **Blockers** — must fix before merge
- **Safe to ship with follow-ups** — optional

If no issues: say so explicitly and list what you checked.
