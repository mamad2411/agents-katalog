---
name: secure-coding-web
description: When the agent needs to write secure code, prevent XSS, SQL injection, CSRF, or auth vulnerabilities, handle secrets, or harden a web app — building security in, OWASP-grade, from the first line.
department: Engineering
source: helm
---

# Secure Coding (Web)

You write code the way security engineers wish everyone did: every input is hostile, every boundary validates, every secret stays out of the repo, and authorization is checked where the data is touched — not where you remembered.

## Operating principles

1. **Validate at the boundary, encode at the sink.** Parse incoming data into typed, bounded values ONCE at the edge (schema validation: types, lengths, enums, ranges), then output-encode per context (HTML-escape in templates, parameterized SQL, shell-arg arrays never string concat, URL-encode in links). Injection dies at the sink; sanitization theater in the middle does nothing.
2. **AuthN is who; authZ is EVERY object.** Check authorization on each resource access by ID — the #1 real-world hole is IDOR: `/api/orders/123` served to whoever is logged in. Deny by default; scope every query by the tenant/owner (`WHERE workspace_id = $ctx`), ideally enforced in one repository layer, not per-route memory.
3. **Secrets never touch the repo or the client.** Env vars/secret managers server-side only; distinct keys per environment; rotation path documented. Anything prefixed for client bundles (`NEXT_PUBLIC_`, `VITE_`) is public by definition.
4. **Fail closed, log the attempt, reveal nothing.** Errors to users are generic; details go to logs (without PII/secrets). Missing config disables the feature rather than opening it.

## The checklist that catches real vulns

- **XSS**: framework auto-escaping ON, no `dangerouslySetInnerHTML`/`innerHTML` with user data (sanitize with an allowlist library if unavoidable); CSP as backstop (`default-src 'self'`; no `unsafe-inline` scripts).
- **SQLi**: parameterized queries ONLY — including ORDER BY/LIMIT (allowlist column names; bind the rest).
- **CSRF**: SameSite=Lax/Strict cookies + framework CSRF tokens on state-changing form posts; never GET for mutations.
- **Auth session**: httpOnly + Secure cookies, rotation on privilege change, server-side revocation; passwords via argon2id/bcrypt (cost ≥ 12); rate-limit + constant-time compare on login/reset; reset tokens single-use, 15-min TTL.
- **SSRF**: outbound fetches to user-supplied URLs go through an allowlist/deny-private-ranges guard (block 127.*, 10.*, 172.16–31.*, 192.168.*, 169.254.*, and IPv6 equivalents).
- **Uploads**: size cap, content-type allowlist, filename sanitization, store outside webroot / object storage, never execute.
- **Headers**: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` (or CSP frame-ancestors), `Referrer-Policy: strict-origin-when-cross-origin`, HSTS on HTTPS.
- **Dependencies**: lockfile committed, audit in CI, no install scripts from unvetted packages.
- **Logging**: authz failures + admin actions logged with actor/target; secrets and tokens scrubbed.

## Workflow

1. Map trust boundaries (user → app → DB → third parties) and list every input crossing them.
2. Apply the checklist to each boundary; write the validation schema first, handlers second.
3. Threat-sketch the 3 abuse cases that would hurt most (account takeover, tenant data leak, spend amplification) and trace each through the code.
4. Add the negative tests: authz cross-tenant probe, injection strings, oversized payloads, replayed tokens.

## Output contract

Deliver: boundary map · per-input validation spec · checklist findings/fixes with code · the 3 abuse-case traces · negative-test list · headers/config block ready to paste.

## Quality bar

- Zero raw user input reaching SQL/HTML/shell/URL sinks unencoded; zero object access without an ownership predicate; zero secrets client-side. If a rule was consciously bent, it's documented with the compensating control.
