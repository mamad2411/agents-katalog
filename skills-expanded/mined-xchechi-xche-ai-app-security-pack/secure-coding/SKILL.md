---
description: Secure-by-default coding standards for AI-built apps. Apply these rules whenever writing or modifying application code that handles authentication, authorization, databases or SQL, HTTP APIs, user input, file uploads, secrets or config, sessions or cookies, or LLM/MCP integrations.
---

# Apply secure coding standards

When writing or editing code in the domains named above, apply these rules as you
go — don't wait to be asked, and don't weaken a rule to make something work. If a
requirement conflicts with a rule, flag it.

- **Secrets:** read keys/tokens/DB URLs from env vars; never hardcode. Ensure `.env`/`*.env*` is gitignored. No secrets/PII in client code, logs, URLs, or errors.
- **SQL:** parameterized queries / ORM only. Never concatenate user input into queries (no f-strings/`.format()`/`%`/template literals).
- **XSS:** never feed user input to `dangerouslySetInnerHTML`/`innerHTML`/`v-html`/`document.write`. Encode output for its context; rely on framework escaping.
- **Command injection / deserialization:** no user input into shells, `eval`, `new Function`, `pickle`, or unsafe `yaml.load`.
- **Validation:** validate every input server-side against a schema (allow-list). Treat client-side checks as UX only.
- **Access control:** every endpoint reading/writing an object verifies ownership/permission server-side. Scope every query to the caller's tenant (no IDOR/BOLA). Protect admin/debug routes.
- **Mass assignment:** bind to explicit allow-listed fields; never let users set role/owner/price/tenant.
- **Auth/sessions:** hash passwords with argon2id/bcrypt; rate-limit auth; cookies `HttpOnly`+`Secure`+`SameSite`; no secrets/PII in JWT or signed-cookie payloads.
- **Headers/CORS:** set CSP, HSTS, `X-Frame-Options`, `nosniff`, `Referrer-Policy`; no wildcard CORS on authed endpoints.
- **SSRF / uploads / traversal:** never let user input choose a server-side request target (allow-list, block private ranges); validate uploads by content + cap size + store outside web root; confine file paths.
- **Dependencies:** verify a package actually exists before adding it (no hallucinated/slopsquatted names); pin versions; keep deps minimal.
- **LLM/MCP:** treat model + tool output as untrusted (validate/encode before render or execute); sandbox MCP servers; allow-list commands by absolute path; never send secrets/unminimized PII to models; require human confirmation for high-impact actions.
- **Errors:** generic client messages; never leak stack traces/SQL/paths; log security events but never secrets/PII.

After writing security-sensitive code, briefly note which of these you applied so
the change is auditable. For a full review, the `/ai-app-security:audit` skill runs
the complete checklist.
