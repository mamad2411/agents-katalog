---
name: security-audit
description: Audits code for security issues and writes secure code, checking against the OWASP Top 10 risk categories with concrete, language-specific checks - broken access control and IDOR, injection, XSS, SSRF, authentication, sessions and JWTs, secrets, cryptography, unsafe deserialization, file uploads, CSRF, security headers, vulnerable dependencies and security logging. Use when asked for a security audit or security review of code, when writing code that handles user input, auth, files, URLs, secrets or money, when reviewing a PR for security, hardening an endpoint, or triaging scanner findings.
license: MIT
---

# Security Audit

Treat every input as hostile until it is validated, check authorization on every object for every request, and use the safe API instead of the clever one. Security bugs are mostly ordinary bugs in code that crosses a trust boundary.

## When to use

- Writing or changing code that handles requests, user input, authentication, authorization, files, URLs, HTML, SQL, shell commands, secrets, tokens or payments.
- Reviewing a PR for security, or before exposing an endpoint publicly.
- Triaging findings from a scanner (SAST, dependency or secret scanning).

Not for: designing org-wide security policy, penetration testing third-party systems, or anything without authorization from the system owner.

## Workflow

1. **Map the trust boundaries.** For the code in scope, list the entry points (HTTP handlers, message consumers, CLI args, file parsers, webhooks), what data comes in, and who can send it (anonymous, user, tenant admin, internal service).
2. **Follow untrusted data to its sinks:** SQL/NoSQL queries, shell commands, HTML output, URLs fetched server-side, file paths, deserializers, templates, redirects, logs. Every source-to-sink path needs validation or a safe API.
3. **Check each category below** that applies. Use the detailed checklist in [references/checklist.md](references/checklist.md) for reviews.
4. **Run the scanners** the repo has, or the defaults in the tools table. Triage the findings; do not paste them in unfiltered.
5. **Fix at the root:** use the safe API (parameterized query, auto-escaping template, allowlist). Do not add a blocklist filter on top of an unsafe API.
6. **Add a regression test** for each vulnerability fixed (for example "user A gets 404 for user B's invoice").
7. **Report** each finding with severity, location, an exploit scenario, and the fix. If you find a live secret or an actively exploitable issue in production, stop and tell the user right away. Never print the secret's value, and never test an exploit against a system you are not authorized to test.

## Broken access control (the most common serious bug)

- **Deny by default.** Every route requires authentication unless it is explicitly marked public.
- **Check ownership on every object access**, server-side, using the authenticated identity, never an ID from the request body: `SELECT ... FROM invoices WHERE id = :id AND tenant_id = :current_tenant`. Changing an ID in the URL must never expose someone else's data (IDOR).
- Enforce authorization in the service or data layer, not only in the UI or by hiding buttons.
- **Prevent mass assignment:** bind requests to explicit DTOs or allowlisted fields. Never bind straight into an ORM entity that has `role`, `isAdmin`, `ownerId`, `price` or `balance`.
- Check function-level permissions (admin endpoints) and field-level ones (who can see salary, PII).
- Return 404 rather than 403 when the existence of a resource is itself sensitive.
- Validate redirects against an allowlist (open-redirect bugs enable phishing and token theft).

## Injection

- **SQL:** parameterized queries only. Identifiers (column names in `ORDER BY`, table names) cannot be parameterized, so map them through an allowlist.
- **ORM raw-query traps.** These are safe only when used with parameters:

| Stack | Unsafe with string-built SQL | Safe form |
|---|---|---|
| Prisma | `$queryRawUnsafe`, `$executeRawUnsafe` | `$queryRaw` tagged template |
| EF Core | `FromSqlRaw` / `ExecuteSqlRaw` with interpolated strings | `FromSql` / `FromSqlInterpolated`, or parameters |
| SQLAlchemy | `text(f"... {x}")` | `text("... :x")` with bound params |
| Django | `raw()`, `extra()`, `RawSQL` with formatting | params argument |
| Sequelize / TypeORM / Knex | ``query(`... ${x}`)``, `knex.raw` with concatenation | replacements / bindings |
| Rails | `where("name = '#{x}'")` | `where(name: x)` or `where("name = ?", x)` |
| JPA / Hibernate | Concatenated JPQL/HQL | Named or positional parameters |

- **Shell:** never build a command string from input. Pass an argument array with no shell: Python `subprocess.run([...], shell=False)`, Node `execFile`/`spawn` (not `exec`), Go `exec.Command(name, args...)` (no `sh -c`), Java `ProcessBuilder(List)`. Put `--` before user-supplied positional arguments.
- **NoSQL:** reject operator objects from user input (for example `{"$gt": ""}` in MongoDB queries); validate types with a schema.
- **Others:** LDAP, XPath, template injection (never render user input *as* a template), header injection (CR/LF in header values), log injection.

## Cross-site scripting (XSS)

- Use auto-escaping templates and frameworks, and **find every escape hatch**: React `dangerouslySetInnerHTML`, Vue `v-html`, Svelte `{@html}`, Angular `bypassSecurityTrust*`, Jinja2/Django `|safe` and `mark_safe`, Handlebars `{{{ }}}`, EJS `<%- %>`, Thymeleaf `th:utext`, Razor `Html.Raw`.
- DOM sinks: `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval`, `new Function`, string `setTimeout`, jQuery `.html()`. Use `textContent` instead.
- User-controlled URLs in `href`/`src`: allow only `https:` (and `mailto:` if needed). Block `javascript:` and `data:`.
- When rich HTML is required, sanitize with a maintained sanitizer (DOMPurify in browsers; nh3 for Python, since bleach is deprecated; OWASP Java HTML Sanitizer; HtmlSanitizer for .NET).
- Add a Content Security Policy as defense in depth. A strict policy uses nonces: `script-src 'nonce-{random}' 'strict-dynamic'; object-src 'none'; base-uri 'none'`. Roll it out with `Content-Security-Policy-Report-Only` first.

## Server-side request forgery (SSRF)

Applies whenever the server fetches a URL that a user influences (webhooks, URL previews, imports, image fetchers, PDF renderers).

- Prefer an **allowlist** of hosts. If arbitrary URLs are a feature, allow only `https` (and `http` if needed) and reject anything else.
- Resolve the hostname, **reject private, loopback, link-local and metadata addresses** (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `100.64.0.0/10` (carrier-grade NAT), `169.254.0.0/16` including `169.254.169.254`, `0.0.0.0/8`, `::1`, `fc00::/7`, `fe80::/10`, IPv4-mapped IPv6), then **connect to the IP you validated**. Re-resolving lets DNS rebinding bypass the check.
- Disable automatic redirects, or validate every hop.
- Run fetchers with no cloud credentials and network egress rules. On AWS, require IMDSv2.
- Never return raw responses or error details from internal fetches to the user.

## Authentication and sessions

- Use the framework's or a well-maintained identity provider's authentication. Do not write your own.
- **Password hashing:** Argon2id (preferred), scrypt, or bcrypt (watch its 72-byte input limit); PBKDF2 only where FIPS is required. Use the parameters from the current OWASP Password Storage Cheat Sheet. Never use MD5/SHA-1/SHA-256 alone, and never encrypt passwords reversibly.
- Rate-limit and lock out progressively on login, reset and MFA endpoints. Return the same error for "unknown user" and "wrong password".
- Support MFA. Rotate the session ID on login and on privilege change. Invalidate sessions on logout and on password change.
- **Cookies:** `HttpOnly; Secure; SameSite=Lax` (or `Strict`), narrow `Path`, the `__Host-` prefix where possible.
- **JWTs:** pin the expected algorithm and reject `none`; verify signature, `exp`, `nbf`, `iss` and `aud` on every request; keep lifetimes short and use refresh tokens with rotation; never put secrets in the payload (it is only base64url-encoded); rotate keys via `kid` + JWKS. For browser sessions, prefer HttpOnly cookies over tokens in `localStorage`.
- Password-reset and magic-link tokens: random from a CSPRNG, single use, short expiry, stored hashed.

## Secrets

- No secrets in code, config committed to the repo, container images, logs, error messages or client bundles. Load them at runtime from a secret manager or the environment.
- Scan with gitleaks (`gitleaks git` on recent versions, `gitleaks detect` on older ones) and enable push protection on the hosting platform if available.
- **A leaked secret must be rotated.** Deleting it from git history is not enough, because clones and caches keep it. Tell the user; do not rotate production credentials yourself.

## Cryptography

- Do not design crypto. Use high-level libraries (libsodium/NaCl, Google Tink, or your platform's AEAD APIs).
- Symmetric encryption: AES-GCM or ChaCha20-Poly1305, with a unique nonce per key per message. Never ECB, never unauthenticated CBC.
- Randomness for tokens, IDs and keys comes from a CSPRNG only: Python `secrets`, Node `crypto.randomBytes`/`crypto.randomUUID`, Java `SecureRandom`, Go `crypto/rand`, .NET `RandomNumberGenerator`. Never `Math.random`, `random`, or `rand`.
- Compare MACs and tokens in constant time: Python `hmac.compare_digest`, Node `crypto.timingSafeEqual`, Go `subtle.ConstantTimeCompare`, Java `MessageDigest.isEqual`, .NET `CryptographicOperations.FixedTimeEquals`.
- TLS 1.2+ everywhere, with certificate verification left on. Never ship `verify=False` or `InsecureSkipVerify: true`.

## Deserialization, files and paths

- Never deserialize untrusted data with native object serializers: Python `pickle` and `yaml.load` (use `yaml.safe_load`), Java `ObjectInputStream`, .NET `BinaryFormatter` (obsolete; since .NET 9 it always throws), PHP `unserialize`, Ruby `Marshal`. Use JSON plus schema validation.
- **Uploads:** enforce a size limit; check type by content, not by the extension or the client's `Content-Type`; generate the stored filename yourself; store outside the web root or in object storage; serve with `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`; re-encode images; scan if the business requires it.
- **Paths:** resolve to a canonical absolute path and check that it stays under the base directory. Check every entry when extracting archives (Zip Slip).
- XML: disable external entities and DTDs (XXE) in the parser configuration.

## CSRF, headers and configuration

- Cookie-authenticated, state-changing requests need CSRF protection: the framework's anti-CSRF token plus `SameSite` cookies, and an `Origin` check where available. GET never changes state.
- Headers: `Strict-Transport-Security: max-age=63072000; includeSubDomains`, `X-Content-Type-Options: nosniff`, CSP with `frame-ancestors` (or `X-Frame-Options: DENY`), `Referrer-Policy: strict-origin-when-cross-origin`, and a restrictive `Permissions-Policy`.
- CORS: an explicit origin allowlist. Never reflect arbitrary origins together with `Access-Control-Allow-Credentials: true`.
- Production: debug mode off, default credentials changed, admin consoles not public, verbose errors off, unnecessary services and ports closed.
- **Fail closed:** when an authorization check or validation throws, deny the request. Never fall through to allow.

## Supply chain and dependencies

- Commit lockfiles and install from them (`npm ci`, `pip install -r` with pinned hashes where possible, `go.sum`).
- Run the ecosystem's vulnerability audit: `npm audit`, `pip-audit`, `govulncheck ./...`, `cargo audit`, `dotnet list package --vulnerable --include-transitive`, `bundle audit`, OWASP Dependency-Check for Maven/Gradle. Trivy covers file systems, images and IaC (`trivy fs .`, `trivy image <name>`, `trivy config .`).
- Check new dependencies for typosquatting, maintenance activity and install scripts before adding them. Pin CI actions and base images to digests or full SHAs.

## Security logging

- Log authentication successes and failures, access denials, privilege changes and admin actions, with who, what, when and from where.
- Never log passwords, tokens, session IDs, keys, full card numbers or unnecessary PII.
- Use structured logging so user input cannot forge log lines. Alert on spikes in auth failures and access denials.

## Tools

| Purpose | Tools |
|---|---|
| Static analysis | Semgrep (prefer explicit rulesets such as `semgrep scan --config p/default`), CodeQL, language linters (Bandit, gosec, eslint security plugins, SpotBugs + Find Security Bugs) |
| Secrets | gitleaks, trufflehog, platform push protection |
| Dependencies and images | Trivy, OSV-Scanner, the ecosystem audits above, Dependabot/Renovate |
| Dynamic testing (staging only, with authorization) | OWASP ZAP |

Ask before running any tool that uploads code or results to a third-party service.

## Anti-patterns

- **Blocklists and regex "sanitizers"** in front of unsafe APIs — use parameterization, encoding and allowlists.
- **Authorization in the frontend only** — every API call can be made directly.
- **Trusting IDs, roles or prices from the request body.**
- **`verify=False` / disabled TLS checks** "just for now".
- **Rolling your own auth, crypto, JWT parsing or HTML sanitizer.**
- **Secrets in `.env` files committed "temporarily"** — assume anything ever committed is leaked.
- **Catch-all exception handlers that return stack traces** or that skip a security check.
- **Fixing the scanner finding instead of the bug** — suppressing a rule without understanding it.

## Done when

- Every entry point in scope is authenticated (or explicitly public) and checks object-level authorization; tests prove cross-user/cross-tenant access fails.
- All source-to-sink paths use safe APIs; no string-built SQL, shell commands or raw HTML from user input.
- Secrets, crypto, cookies, tokens and headers follow the rules above.
- Scanners were run and every finding was fixed or documented with a justification.
- Regression tests exist for every vulnerability fixed, and the user was told about any secret that must be rotated.

## References

- [references/checklist.md](references/checklist.md) — the full checklist by OWASP Top 10 category, with review questions. Read it when doing a security review or a pre-release check.
