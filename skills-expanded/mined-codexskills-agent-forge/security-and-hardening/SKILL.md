---
name: security-and-hardening
description: >-
  Systematic application of security controls across the entire software
  development lifecycle. Covers OWASP Top 10 prevention, authentication
  patterns, secrets management, dependency auditing, input validation, and a
  three-tier security boundary system that enforces defense in depth.
---

# Security & Hardening

## Overview

Security is not a feature — it is a property of the entire system. You cannot
"add" security to an application after it is built; you must design it into
every layer. Most security vulnerabilities share a common root cause: trusted
input. Every piece of data that crosses a trust boundary (network, file system,
user input, environment variable, database) must be validated, sanitized, and
treated as hostile until proven otherwise.

This skill establishes a **three-tier boundary system**, applies the **OWASP
Top 10** preventive controls, and defines repeatable patterns for auth,
secrets, dependencies, and data validation. Compliance with these patterns is
a non-negotiable review gate.

## When to Use

- Designing or implementing authentication/authorization flows
- Handling any user-supplied input (forms, API params, file uploads, headers)
- Storing or transmitting secrets (API keys, passwords, tokens, certificates)
- Adding a new dependency or upgrading an existing one
- Writing database queries (especially raw SQL or dynamic queries)
- Rendering user content in HTML, PDF, email, or any output format
- Implementing file upload, download, or processing
- Configuring CORS, CSP, or other HTTP security headers
- Setting up CI/CD pipelines that require secret access
- Any code change that touches PII, financial data, or authentication tokens

## Process

### Step 1: Identify Trust Boundaries (Three-Tier System)

Every system has three tiers of trust. Every data flow between tiers must
be mediated.

| Tier | Definition | Examples |
|------|------------|----------|
| **T1 — Untrusted** | Any source the attacker controls | User input, HTTP headers, URL params, request bodies, file uploads, third-party API responses, cookies, WebSocket messages |
| **T2 — Internal** | Systems within the deployment boundary | Application servers, internal APIs, message queues, worker processes, environment variables |
| **T3 — Secure** | Vaults and persistent stores | Database, object storage, secrets manager, key store, certificate store |

**Rules:**
1. T1 → T2: Every value must be validated (type, length, format, range) and
   sanitized (escaped, encoded, parameterized) before crossing the boundary.
2. T2 → T3: Queries use parameterized statements or ORM-safe methods.
   No dynamic query construction with string interpolation.
3. T3 → T2: Data returned to T2 must still be validated before being sent
   to T1 (defense in depth — stored XSS is a real threat).
4. T2 → T1: Output encoding must match the context. HTML encoding for HTML,
   JS encoding for JavaScript, URL encoding for URLs, CSS encoding for CSS.

**Exit criteria:** Every data flow in the system is labeled with source tier,
destination tier, and the control enforced at the boundary. No unlabeled flows.

### Step 2: Apply Authentication & Authorization Patterns

**Authentication** verifies identity. **Authorization** verifies permission.
Never conflate the two.

**Auth patterns by context:**

| Pattern | Use Case | Implementation |
|---------|----------|----------------|
| **JWT (stateless)** | REST APIs, microservices | Short expiry (15 min access, 7 day refresh). Store refresh tokens in httpOnly cookies. Always validate `aud`, `iss`, `exp`, `nbf`. Rotate signing keys. |
| **OAuth 2.0 / OIDC** | Third-party login, delegated access | Use the authorization code flow with PKCE. Never use the implicit flow. Validate the ID token's signature, issuer, audience, and nonce. |
| **Session (stateful)** | Server-rendered web apps | Secure, httpOnly, SameSite cookies. Session IDs must be cryptographically random (≥128 bits). Store session data server-side. Rotate session ID on privilege escalation. |
| **API Keys** | Service-to-service, machine clients | Rate-limit per key. Ability to revoke instantly. Store as SHA-256 hashes. Never log the plaintext key. |
| **MFA / TOTP** | High-value operations | Require for admin actions, password changes, payment confirmation. Use a well-vetted library (not a custom implementation). |

**Authorization checklist:**
- Every endpoint has an explicit authorization check (not just authentication)
- Authorization is checked at the API boundary, not in the UI
- Role-based or attribute-based checks use least-privilege principles
- Default-deny: unlisted roles do not have access
- Horizontal access control: User A cannot access User B's data (verify
  ownership or scope)
- Vertical access control: Regular users cannot perform admin actions
- Rate limiting is applied per-user/per-key, not globally

### Step 3: Secrets Management

Secrets are API keys, database passwords, encryption keys, certificates,
OAuth tokens, and any other credential. They must never appear in code,
logs, error messages, or build artifacts.

**Rules:**
1. Secrets live in a dedicated secrets manager (AWS Secrets Manager, GCP
   Secret Manager, HashiCorp Vault, 1Password CLI, Doppler, etc.)
2. Access to secrets is audited and role-restricted
3. Local development uses a `.env.local` file (gitignored) or a local
   secrets store
4. CI/CD pipelines inject secrets via the CI platform's built-in secrets
   mechanism (GitHub Actions secrets, GitLab CI variables, etc.) — never
   plaintext in YAML files
5. Secrets are rotated on a schedule (90 days for service keys, immediately
   on compromise)
6. Hardcoded secrets are detected by pre-commit hooks (`truffleHog`,
   `git-secrets`, `detect-secrets`)
7. Encryption keys use a key management service (KMS) — keys are never in
   application memory longer than needed
8. Logging pipelines redact known secret patterns before storage

### Step 4: Input Validation & Injection Prevention

Every input from T1 must be validated before use.

**Validation hierarchy:**
- **Type check:** Is it a string? Number? Boolean? Reject unexpected types.
- **Format check:** Regex, schema validation (JSON Schema, Zod, Pydantic),
  or type-specific validators (email, URL, UUID, date).
- **Length check:** Minimum and maximum length. Prevent buffer overflows and
  storage exhaustion.
- **Range check:** Numeric ranges, string length bounds, collection size limits.
- **Allowlist check:** Known-good values are always safer than blocklists.
  If possible, validate against an allowlist of permitted characters, values,
  or patterns.
- **Semantic check:** Does the value make sense in context? (e.g., delivery
  date is not in the past, quantity is positive, email domain exists.)

**SQL injection prevention (non-negotiable):**
- Use parameterized queries or prepared statements for all SQL/NoSQL queries.
- Never concatenate user input into query strings.
  ```python
  # BAD
  cursor.execute(f"SELECT * FROM users WHERE id = {user_input}")
  # GOOD
  cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))
  ```
- ORMs are typically safe — but `.raw()` or `.execute()` methods bypass
  protections. Review these explicitly.
- Stored procedures are not immunity. Parameterize within procedures too.

**XSS prevention:**
- Context-sensitive output encoding: `&lt;` in HTML, `\x3C` in JS,
  `%3C` in URLs.
- Use a strict Content Security Policy (CSP): no `'unsafe-inline'` in
  production, report violations to a monitoring endpoint.
- Set `X-Content-Type-Options: nosniff` to prevent MIME sniffing.
- Use React/Vue/Svelte's built-in escaping. Review `dangerouslySetInnerHTML`
  and equivalents with extreme scrutiny.
- Sanitize rich HTML input with DOMPurify or equivalent.

**CSRF prevention:**
- Use anti-CSRF tokens for all state-changing requests (POST, PUT, DELETE,
  PATCH) in session-based auth.
- Set `SameSite=Strict` or `SameSite=Lax` on session cookies.
- For APIs: require a custom header (e.g., `X-Requested-By`) that JavaScript
  cannot set cross-origin.
- Check the `Origin` or `Referer` header for sensitive operations.

### Step 5: Dependency Auditing

Every dependency is a potential attack vector. Audit on every change.

**Checklist:**
- [ ] `npm audit` (or `yarn audit`, `pnpm audit`) runs in CI — builds fail
       on critical or high vulnerabilities
- [ ] `pip-audit` for Python projects
- [ ] `cargo audit` for Rust projects
- [ ] `govulncheck` for Go projects
- [ ] `bundler-audit` for Ruby projects
- [ ] Dependencies with no maintainer activity in 12+ months are flagged for
       replacement
- [ ] Pin major versions (avoid floating `^` or `>=` ranges on core deps)
- [ ] Use lockfiles (`package-lock.json`, `Cargo.lock`, `poetry.lock`) —
       always committed
- [ ] Renovate or Dependabot configured with auto-merge only for patch
       versions with passing tests
- [ ] License compliance: no GPL/AGPL dependencies in proprietary projects
       (use `license-checker` or `fossa`)

---

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "We validate input on the frontend, so backend validation is redundant." | Frontend validation is a UX convenience, not a security control. An attacker sends requests directly to your API — they never see your frontend. Backend validation is the only validation that matters. |
| "We use an ORM, so we don't need to worry about SQL injection." | Most ORMs have raw query methods, `.raw()`, or fallback paths. Review every query that bypasses the ORM abstraction. Also: stored XSS in data returned from ORM queries is still a threat. |
| "The secret is only hardcoded for local development." | Hardcoded secrets find their way into commits, screenshots, pair programming sessions, and CI logs. Use a `.env.local` file. It takes 10 seconds to set up. |
| "Nobody would attack us — we're too small." | Automated scanners do not discriminate. Every public endpoint on the internet is scanned within hours of deployment. Small targets are exploited precisely because they assume obscurity. |
| "We'll add security headers in a follow-up sprint." | CSP headers are a one-line configuration change. There is no excuse to defer them. Deploy them in the first commit. |
| "We need to log the full request body for debugging." | Log the structure, not the values. Use structured logging with PII redaction. If you need request body debugging, use a local debug proxy (e.g., Charles Proxy). |
| "The dependency has a vulnerability but no patch exists yet." | This is a legitimate concern but must be tracked. Add a monitoring rule, create a ticket, set a review date, and consider a workaround (WAF rule, feature flag to disable the vulnerable path). Do not ignore it. |

## Red Flags

- Hardcoded keys or passwords in any committed file
- SQL queries built by string concatenation
- CSP header missing or allowing `'unsafe-inline'`
- No rate limiting on login/signup endpoints
- Error messages that expose stack traces or internal paths
- Session cookies without `httpOnly` and `Secure` flags
- User-uploaded files served directly (no content-type validation, no
  virus scanning)
- `Authorization: Bearer <token>` logged in plaintext
- Dependency audit not configured in CI
- Pre-commit hooks for secret detection not installed

## Verification

1. Run dependency audit (`npm audit`, `pip-audit`, etc.). Are there any
   critical/high vulnerabilities? If yes, fix or create a tracked ticket.
2. Run a linter with security rules (`eslint-plugin-security`, `bandit`,
   `gosec`, `cargo-audit`). Zero warnings?
3. Check all database queries: are they parameterized? Grep for string
   concatenation patterns near query execution.
4. Check all auth endpoints: is rate limiting applied? Is there an authz check
   distinct from an authn check?
5. Check CSP headers: present? Strict? Reporting endpoint configured?
6. Check secrets: search the codebase for any hardcoded secrets
   (`truffleHog`, `git-secrets`).
7. Test an XSS vector: try `<script>alert(1)</script>` in every user-input
   field. Is it rendered safely?
8. Test a CSRF vector: try submitting a state-changing request from a
   different origin. Is it blocked?
9. Review every `dangerouslySetInnerHTML`, `.innerHTML`, `.html()`,
   `v-html`, and equivalent.
10. Verify the three-tier boundary map: every data flow labeled and every
    boundary enforced.
