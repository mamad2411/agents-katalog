---
description: Audit the selected code or recent changes against the xChe AI-App Security policy (OWASP / API / LLM / MCP). Reports prioritized findings with fixes.
disable-model-invocation: true
---

# Security audit

Audit the code I've selected (or the most recent changes) for security issues.
Use the checklist below. For full rationale, see `reference/SECURITY.md` in this
plugin directory.

## Check for

1. **Secrets** — hardcoded keys/tokens/DB URLs; secrets in client code, logs, URLs, or errors; missing `.env` gitignore.
2. **Injection** — string-built SQL (concatenation/f-strings/`.format()`/`%`); `dangerouslySetInnerHTML`/`innerHTML`/`v-html`/`document.write` with user input; shell/`eval`/unsafe deserialization; missing server-side validation.
3. **Access control** — endpoints that read/write objects without verifying ownership/permission server-side (IDOR/BOLA); missing tenant scoping; unprotected admin/debug routes; mass assignment of role/owner/price/tenant.
4. **Auth & sessions** — weak password hashing (MD5/SHA-1/unsalted); no rate limiting on auth; cookies missing `HttpOnly`/`Secure`/`SameSite`; secrets/PII in JWT or signed-cookie payloads.
5. **API & network** — missing security headers (CSP/HSTS/X-Frame-Options/nosniff); wildcard CORS on authed endpoints; SSRF (user-controlled request targets, no private-range block); open redirect; unsafe file uploads; path traversal.
6. **Dependencies** — hallucinated/slopsquatted package names; unpinned versions; known-vulnerable deps.
7. **LLM/MCP** — model/tool output used without validation or encoding; un-sandboxed MCP servers; commands not allow-listed by absolute path; secrets/unminimized PII sent to models; high-impact actions without human confirmation.
8. **Errors/logging** — stack traces, SQL, or internal paths leaked to clients; secrets/PII in logs.

## Output format

For each finding:
- **Severity**: Critical / High / Medium / Low
- **Location**: `file:line`
- **Issue**: one sentence
- **Fix**: the concrete change (show the corrected pattern)

Order findings by severity. Be concise and actionable. If nothing is found in a
category, skip it rather than padding the report.

> This is a baseline review, not a guarantee. Business-logic flaws and novel
> issues still need human judgment. For money/auth/PII code, recommend a full audit.
