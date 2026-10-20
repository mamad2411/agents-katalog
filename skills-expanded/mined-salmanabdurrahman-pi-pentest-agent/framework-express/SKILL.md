---
name: framework-express
description: Express.js/Node.js security review — validate prototype pollution, CORS and middleware configuration, JWT handling, path traversal via static serving, and package hygiene with docs-first, read-only checks and no exploitation or server modification.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Express.js security — middleware and surface review

Use this skill to review Express.js application security posture on authorized in-scope targets. Validate prototype pollution vectors, CORS and security-header middleware configuration, JWT handling, static-file path traversal, and dependency hygiene. All tests are read-only, low-rate. Never exploit prototype pollution for RCE, inject JWT claims, run arbitrary payloads against the server, or modify application state.

## Required inputs

- Written scope covering the Express application hosts, API endpoints, static paths, and allowed review methods. Explicit confirmation that prototype-pollution exploitation, JWT forging, server-side code execution, and state mutation are prohibited unless separately approved.
- Express/Node.js version from: `X-Powered-By: Express` header, error-page signatures, `package.json` exposure, or local source code if provided.
- Official Express.js and Node.js documentation for the detected version — prefer expressjs.com.
- Valid authorization cache for the target application.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for read-only execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — version detection and header fingerprinting

1. Detect Express from response headers: `X-Powered-By: Express` is the default and confirms Express. Its presence also signals that the header has not been suppressed — a minor hardening gap.
2. Check for additional framework signals: `etag` header format (Express uses weak ETags by default), default 404/500 response format, and JSON error-response structure.
3. Check the Node.js version if visible: `X-Powered-By` may include the Node version, error stack traces may reveal the runtime version, and the `Server` header (when not overridden) may identify the HTTP server.
4. If the application exposes `package.json` via a static route or source map, extract the Express version, middleware list, and dependency versions. Flag any end-of-life or vulnerable dependencies.
5. Document version evidence. Flag: Express versions before 4.x (unmaintained), Node.js versions that are end-of-life, and any dependency with known critical CVEs.

### Phase 2 — prototype pollution detection

1. Identify endpoints that parse JSON or URL-encoded request bodies: Express applications commonly use `express.json()`, `express.urlencoded()`, or `body-parser`. These middleware parse user input into JavaScript objects, which can be polluted.
2. Test for prototype pollution via JSON body: send a request with `{"__proto__": {"polluted": true}}` or `{"constructor": {"prototype": {"polluted": true}}}` in the JSON body. Check for behavioral changes: does a subsequent request return unexpected properties? Does error output change? Does response timing change?
3. Test for prototype pollution via query string: send `?__proto__[polluted]=true` or `?constructor[prototype][polluted]=true` in the URL. Express's `qs` parser (used by `express.urlencoded({extended: true})`) may parse these into prototype assignments.
4. Test for prototype pollution via nested object merge: identify endpoints that accept complex nested objects (user profiles, configurations, filters). Submit deeply-nested JSON with `__proto__` or `constructor.prototype` keys and observe behavior.
5. Do not exploit confirmed prototype pollution for: RCE (child_process spawn), authentication bypass, or server-side request forgery. Record the pollution vector and affected endpoint, then stop.

### Phase 3 — CORS and security header review

1. Inspect CORS response headers: send cross-origin requests with a custom `Origin` header. Check `Access-Control-Allow-Origin`: if it reflects the request origin exactly, the application has a permissive CORS policy. If it returns `*` with `Access-Control-Allow-Credentials: true`, credentials can be exfiltrated cross-origin.
2. Check allowed methods: `Access-Control-Allow-Methods` listing `PUT`, `DELETE`, or `PATCH` beyond what the API actually exposes expands the attack surface unnecessarily.
3. Check allowed headers: `Access-Control-Allow-Headers` listing `Authorization`, `Cookie`, or `X-API-Key` means these headers can be sent cross-origin if the origin is trusted — combined with a reflective origin, this enables credential theft.
4. Inspect security headers: check for `Content-Security-Policy` (missing or weak policy allows XSS data exfiltration), `X-Content-Type-Options: nosniff`, `X-Frame-Options` or `Content-Security-Policy: frame-ancestors` (missing allows clickjacking), `Strict-Transport-Security` (missing on HTTPS allows SSL stripping), and `X-XSS-Protection` (legacy — `0` is recommended, `1; mode=block` is deprecated).
5. Flag missing security headers at their appropriate severity: missing CSP is medium (needs application-specific policy), missing HSTS on HTTPS is high, missing `X-Content-Type-Options` is low/medium, and missing frame protection is medium.

### Phase 4 — static-file serving and path traversal

1. Identify static file serving: Express applications commonly serve static files with `express.static()`. Check for common static paths: `/static/`, `/public/`, `/assets/`, `/js/`, `/css/`, `/images/`, `/uploads/`.
2. Test for directory listing: request a static directory path without a trailing file. If Express returns a directory listing (file list), the `express.static()` configuration likely does not have `index: false` or a default index file — flag as information disclosure.
3. Test for path traversal in static serving: request paths like `/static/..%2f..%2fetc/passwd`, `/public/..%2f..%2fpackage.json`, or `/assets/%2e%2e/%2e%2e/app.js`. Express's `express.static()` uses `send` which should prevent traversal — if traversal succeeds, flag as critical.
4. Test for path traversal in file-download endpoints: identify routes that accept a filename or path parameter (e.g., `/download?file=report.pdf`). Test traversal sequences (`../`, `..%2f`, `..%5c`, `%2e%2e%2f`) and absolute paths (`/etc/passwd`, `C:\windows\win.ini`).
5. Check whether `res.sendFile()` is used with user-controlled paths — this is a known dangerous pattern that bypasses `express.static()` traversal protections. If found, flag as high.

### Phase 5 — session, JWT, and authentication middleware review

1. Identify the session mechanism: inspect `Set-Cookie` headers. Common Express session middleware: `express-session` (server-side session store), `cookie-session` (client-side signed cookies), and JWT-based sessions (client-side tokens).
2. If JWT is used: decode the JWT payload (base64 decode the middle section). Inspect the algorithm (`alg` field in header): `none` algorithm should be rejected, `HS256` with a weak secret is insecure, and `RS256` to `HS256` key-confusion is a known attack — but do not attempt it without destructive approval.
3. Check JWT expiration: does the token have an `exp` claim? Is the expiration reasonable (minutes to hours, not days or absent)? JWTs without expiration are permanent unless the server maintains a blocklist.
4. Check session cookie flags: `HttpOnly` (must be set), `Secure` (must be set on HTTPS), `SameSite` (should be `Lax` or `Strict`), and `Path` (should be restricted, not `/` if avoidable).
5. Check for authentication middleware bypass: identify routes that appear to require authentication (based on response difference: 401 vs 200 for authenticated vs unauthenticated). Test sending requests with: no auth header, empty auth header, malformed JWT, expired JWT, and JWT signed with `alg: none`. Record whether the application correctly rejects each case — do not craft working tokens.

## Decision points

- **Escalate on confirmed prototype pollution**: `__proto__` or `constructor.prototype` injection accepted by the application → high to critical, depending on impact surface.
- **Escalate on path traversal success**: reading `package.json`, source files, or system files through traversal → critical.
- **Escalate on reflective CORS with credentials**: `Access-Control-Allow-Origin` reflecting arbitrary origins combined with `Access-Control-Allow-Credentials: true` → high, enables cross-origin credential theft.
- **Escalate on JWT `alg: none` accepted**: the application accepts unsigned JWTs → critical, authentication bypass.
- **Escalate on `res.sendFile()` with user-controlled path**: user input directly passed to `sendFile()` without path sanitization → high, potential arbitrary file read.
- **Downgrade on missing `X-Powered-By` suppression**: informational — not a vulnerability, but reveals framework identity.

## Prohibited behavior

- Exploiting prototype pollution for code execution, authentication bypass, or SSRF.
- Forging JWT tokens or attempting key-confusion attacks (HS256 vs RS256).
- Extracting source code, environment variables, or secrets through path traversal.
- Testing login endpoints, password-reset flows, or credential submission.
- Running `npm audit`, `npm install`, or any package-manager commands on the target.
- Modifying application state, creating resources, or deleting data.

## Stop conditions

- Prototype pollution confirmed with server-wide impact → stop, record critical finding, do not exploit.
- Path traversal yields source code or secrets → stop extraction, record finding.
- JWT `alg: none` accepted → stop, record critical finding, do not craft further tokens.
- `package.json` exposed and reveals vulnerable dependencies → stop, record findings per CVE.
- Target not in scope or testing would impact production → stop.

## Evidence — Express security matrix

For each target, record:

```text
Target: <URL> | Express version: <detected | estimated> | Node.js: <detected>
Version evidence: <X-Powered-By | error page | package.json | behavioral>

Prototype pollution:
  JSON body vector: <accepted — polluted | rejected | not tested>
  Query-string vector: <accepted — polluted | rejected | not tested>
  Nested-merge vector: <accepted — polluted | rejected | not tested>
  Impact surface: <error change | response change | timing change | unknown>

CORS configuration:
  Allow-Origin: <reflects origin | fixed domain | * | not set>
  Allow-Credentials: <true | false | not set>
  Allow-Methods: <list | over-permissive>
  Allow-Headers: <list — Authorization/Cookie present>

Security headers:
  CSP: <present — strong | present — weak | missing>
  X-Content-Type-Options: <nosniff | missing>
  Frame protection: <DENY | SAMEORIGIN | CSP frame-ancestors | missing>
  HSTS: <present — max-age=... | missing on HTTPS>
  X-Powered-By: <present — Express | suppressed>

Static files and traversal:
  Static paths: <list>
  Directory listing: <enabled — path | disabled>
  Path traversal (static): <successful — path | blocked>
  Path traversal (download endpoint): <successful — endpoint | blocked>
  sendFile() user input: <detected — endpoint | not found>

Authentication:
  Session mechanism: <express-session | cookie-session | JWT | custom>
  JWT alg: none accepted: <yes — critical | no>
  JWT expiration: <present — duration | absent — permanent>
  Session cookie HttpOnly: <yes | no>
  Session cookie Secure: <yes | no — HTTP transmits>
  Session cookie SameSite: <Lax | Strict | None>

Overall risk: <critical | high | medium | low>
```

Never store: JWT token values, session cookie values, prototype-pollution payload responses containing server internals, source code extracted via path traversal, `package.json` dependency lists with version details (summarize CVE counts only), or any discovered secrets, keys, or environment variables.

## Report handoff

1. `pentest_agent_record_finding` for: prototype pollution vectors, path traversal, reflective CORS with credentials, JWT `alg: none` acceptance, missing HSTS on HTTPS, `res.sendFile()` with user input, directory listing, and missing security headers.
2. Reference the Express security matrix.
3. Recommend: disable `X-Powered-By` with `app.disable('x-powered-by')`, use `helmet` middleware for security headers, configure CORS with explicit origins and no `*` with credentials, validate and sanitize all user input that reaches object assignment (use `Object.create(null)` or Map for user data), never pass user input to `res.sendFile()` directly, enforce JWT algorithm whitelist (reject `none`, specify `RS256` or `HS256` explicitly), set short JWT expirations with refresh tokens, serve static files with `express.static()` only (never manual path resolution), and update Express and all middleware to supported versions.
