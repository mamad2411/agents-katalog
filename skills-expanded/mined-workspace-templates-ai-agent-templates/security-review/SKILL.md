---
name: security-review
description: Reviews a code change for injection, broken authorization, secrets, SSRF and unsafe input handling, and reports only exploitable findings with a fix.
---

# Security review

Review the change as an attacker. Report only what you can exploit.

## Steps

1. Get the change: `git diff main...HEAD` or the files named. List every entry point it touches: routes, handlers, CLI args, file uploads, webhooks, queue messages.
2. Trace each untrusted value from entry to sink. Flag sinks reached without validation or encoding:
   - SQL, shell, template, LDAP or NoSQL queries built from strings (injection)
   - HTML output without escaping, `innerHTML`, `dangerouslySetInnerHTML` (XSS)
   - Outbound requests to a user-supplied URL, including redirects and DNS names that resolve to internal addresses (SSRF)
   - File paths with `..` or absolute paths (traversal), unsafe deserialization, archive extraction
3. Check authorization on every handler: is the caller logged in, and are they allowed to touch this specific record? Look for IDs taken from the request without an ownership check (IDOR).
4. Check secrets and crypto: keys in code or logs, weak hashes for passwords, home-made tokens, missing expiry, cookies without HttpOnly, Secure and SameSite.
5. Check new dependencies and CORS, CSRF and rate limits on state-changing routes.
6. For each candidate, write the exact request or input that exploits it. If you cannot, drop it.

## Rules

- Never run exploits against real services, and never print secrets you find; quote the file and line only.

## Report

Findings ranked Critical to Low: file:line, the exploit input, impact, the fix as a code snippet. End with the areas you checked and found clean.
