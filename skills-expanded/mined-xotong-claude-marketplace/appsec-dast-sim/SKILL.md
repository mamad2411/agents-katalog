---
name: appsec-dast-sim
description: >
  LLM-based DAST simulation following OWASP WSTG v4.2. No containers, no running app
  required — works at design time by reading the codebase. Enumerates all API endpoints
  and routes, walks every WSTG v4.2 test category, inspects relevant code (auth
  middleware, input handling, session logic, business rules), generates specific test
  probes (curl commands, payload examples), and reports findings grouped by severity.
  Use when the user says: "DAST scan", "OWASP security review", "WSTG check",
  "web security audit", "security code review", "OWASP top 10 check",
  "audit my API", "is my API secure", "review my endpoints".
  Also activate for a SINGLE WSTG area and cover only that one (Phase 0 routes):
  Auth — "check auth security", "is my login secure", "authentication review";
  Access control — "authorization check", "can users access other users' data",
  "IDOR", "privilege escalation";
  Sessions — "check session handling", "cookie security", "session fixation";
  Injection — "find XSS or SQLi", "injection vulnerabilities", "SSRF", "XXE",
  "command injection", "is my input validated";
  Crypto — "crypto review", "am I hashing passwords properly", "TLS check";
  Business logic — "business logic vulnerabilities", "can this flow be abused";
  API — "API security audit", "GraphQL security", "REST security review";
  Config — "security misconfiguration", "check my headers", "CORS review".
  Do NOT activate for general code review, unit testing, linting, or container scanning.
---

# AppSec DAST Sim — OWASP WSTG v4.2

LLM-based Dynamic Application Security Testing simulation. Works entirely from the
source tree — no running app, no scanner containers required. Walks the full OWASP
Web Security Testing Guide v4.2 checklist and produces actionable findings with curl
probes and remediation guidance.

WSTG quick reference: `reference/wstg-v42-checklist.md` (vendored locally).

---

## Phase 0 — Decide which areas to review

Set `WSTG_SCOPE` from the user's words before reading any code. Phase 1 always
runs — you cannot review what you have not enumerated.

| The user asked about | `WSTG_SCOPE` | Phases |
|---|---|---|
| login, auth, passwords, MFA, tokens | `AUTHN` | 3 |
| permissions, IDOR, "other users' data", privilege escalation | `AUTHZ` | 4 |
| sessions, cookies, logout, fixation | `SESS` | 5 |
| XSS, SQLi, SSRF, XXE, command injection, input validation | `INPV` | 6 |
| crypto, hashing, TLS, encryption at rest | `CRYP` | 8 |
| business logic, workflow abuse, race conditions | `BUSL` | 9 |
| REST, GraphQL, API security | `APIT` | 10 |
| headers, CORS, TLS config, exposed admin panels | `CONF` | 2 |
| errors, stack traces, information leakage | `ERRH` | 7 |
| everything, full review, OWASP audit, bare invocation | `ALL` | 2–10 |
| anything you are not sure about | **ask — below** |

**When unsure, ask — never guess.** Use `AskUserQuestion` with `multiSelect: true`.
Label by what a developer would recognise, not by WSTG code:

- `Everything (recommended)` — the full OWASP WSTG v4.2 checklist
- `Login and access control` — who can sign in, and what they can reach (AUTHN + AUTHZ)
- `Untrusted input` — XSS, SQL injection, SSRF, command injection (INPV)
- `Sessions and cookies` — how sessions are issued, stored, and revoked (SESS)
- `API surface` — REST and GraphQL specifics (APIT)
- `Configuration and secrets handling` — headers, CORS, crypto, error leakage (CONF + CRYP + ERRH)

Run Phase 1, then only the phases the scope selects. In the Phase 11 coverage table,
mark every phase you skipped as `SKIP (out of requested scope)` — never as `PASS`.
A scoped review is not an OWASP pass; say so when you report.

---

## Phase 1 — Enumerate endpoints and entry points

Read the codebase to build a complete inventory of attack surface. Look in:

- **Express/Node:** `app.js`, `server.js`, `src/routes/`, `src/controllers/`, any file
  with `router.get`, `router.post`, `app.get`, `app.post`, `router.use`
- **Spring Boot:** `@RestController`, `@GetMapping`, `@PostMapping`, `@RequestMapping`
  annotated classes
- **Django/Flask:** `urls.py`, `views.py`, `@app.route`, `@blueprint.route`
- **FastAPI:** `@app.get`, `@app.post`, `@router.get` decorated functions
- **Rails:** `config/routes.rb`, controllers in `app/controllers/`
- **GraphQL:** schema files (`*.graphql`, `*.gql`), resolver files
- **OpenAPI/Swagger:** `openapi.yaml`, `swagger.json` — parse all paths and methods

For each endpoint, record:
- HTTP method(s)
- Path (including path parameters, e.g. `/users/:id`)
- Auth middleware applied (or absent)
- Input parameters (path, query, body, headers)
- Response shape (infer from handler code)

Output a numbered endpoint inventory before proceeding.

---

## Phase 2 — WSTG-CONF (Configuration and Deployment)

### WSTG-CONF-01 — Network and infrastructure configuration

Look for debug/admin endpoints that should not be reachable in production:

Search for routes or middleware mounting:
- `/actuator`, `/actuator/**` (Spring Boot Actuator)
- `/debug`, `/__debug__`, `/debug-toolbar`
- `/swagger-ui`, `/swagger-ui.html`, `/api-docs`, `/v2/api-docs`, `/v3/api-docs`
- `/graphiql`, `/graphql-playground`, `/altair`
- `/metrics`, `/health`, `/info` (when exposed without auth)
- `/_admin`, `/admin`, `/internal`

Check: are these routes protected by auth middleware in production config? Is there
a `NODE_ENV === 'production'` guard or equivalent?

Finding format if unprotected:
```
[WSTG-CONF-01] Debug/admin endpoint exposed without production guard
Severity: HIGH
File: <file>:<line>
Endpoint: GET /actuator/env
Issue: Actuator endpoint mounted unconditionally — exposes environment variables and config in production.
Probe: curl -X GET http://localhost:8080/actuator/env
Remediation: Guard with auth middleware or disable in production profile.
```

### WSTG-CONF-02 — Application platform configuration

Check framework config files (`application.properties`, `application.yml`,
`settings.py`, `config/environments/production.rb`, `.env.example`) for:
- `DEBUG=True` / `debug: true` / `FLASK_DEBUG=1` set as default or in production config
- Stack traces enabled in error responses (`server.error.include-stacktrace=always`)
- Verbose logging of request bodies or PII (`logging.level.root=DEBUG` in prod config)

### WSTG-CONF-05 — HTTP methods

For each endpoint, check whether HTTP methods are explicitly restricted. Look for:
- Routes that only need GET but use a wildcard method handler
- Missing `@RequestMapping(method = RequestMethod.GET)` narrowing
- `router.all()` or `app.use()` without method guards on sensitive paths
- TRACE and OPTIONS responses — are they disabled globally?

### WSTG-CONF-07 — HTTP Strict Transport Security

Search middleware stack and response headers for HSTS configuration:
- Look for `helmet()`, `helmet.hsts()`, `Strict-Transport-Security` header setting
- Check: `max-age` >= 31536000 (1 year)
- Check: `includeSubDomains` present
- Check: `preload` (optional but recommended)

If not found or misconfigured, flag as MEDIUM.

### WSTG-CONF-08 — CORS configuration

Search for CORS setup (`cors()`, `@CrossOrigin`, `Access-Control-Allow-Origin` headers):
- Flag wildcard origin (`*`) combined with `credentials: true` — this is CRITICAL,
  browsers will reject it but misconfigurations in custom CORS logic can bypass this
- Check `allowedOrigins` list — are there overly broad patterns? (`*.company.com` ok;
  reflecting arbitrary `Origin` header is CRITICAL)
- Check `allowedMethods` — is DELETE or PUT allowed on read-only endpoints?

### WSTG-CONF-10 — File upload restrictions

Find file upload endpoints (`multipart/form-data`, `multer`, `@RequestParam MultipartFile`,
`request.files`). Check for:
- MIME type validation (is only the `Content-Type` header checked, or is magic byte
  inspection used?)
- File size limits set
- Upload directory — is it inside the web root / publicly accessible?
- Filename sanitization (path traversal via `../` in filename)

### WSTG-CONF-11 — Cloud storage security

Search for AWS SDK (`s3.putObject`, `s3.getObject`), GCS (`storage.bucket`),
Azure Blob usage. Check for:
- Hardcoded bucket names or storage keys in source code
- `ACL: 'public-read'` or equivalent on bucket creation/object upload
- Exposed credentials in `.env.example`, config files, or comments

---

## Phase 3 — WSTG-AUTHN (Authentication)

### WSTG-AUTHN-01 — Credentials over encrypted channel

Check server config and route definitions:
- HTTP (non-HTTPS) endpoints that accept `Authorization` header or login forms
- Redirect from HTTP to HTTPS not enforced for auth routes
- `secure: false` on auth cookies in production config

### WSTG-AUTHN-02 — Default credentials

Search codebase for hardcoded credentials:
- Patterns: `admin`, `password`, `secret`, `test123`, `changeit`, `default`
- Look in: seed files, test fixtures, `docker-compose.yml`, `application.properties`,
  comments in auth code
- API keys with obvious test values (`APIKEY=test`, `TOKEN=example`)

### WSTG-AUTHN-03 — Account lockout / brute force protection

Find login endpoints (POST to `/login`, `/auth`, `/signin`, `/token`). Check for:
- Rate limiting middleware (`express-rate-limit`, `@nestjs/throttler`, Django `ratelimit`)
- Lockout after N failed attempts (check user model for `failedLoginAttempts`,
  `lockedUntil` fields or equivalent)
- CAPTCHA on login form
- Absence of any of the above is HIGH severity

### WSTG-AUTHN-04 — Authentication bypass via direct browsing

For every route in the endpoint inventory, verify auth middleware is applied:
- Is there a global auth middleware applied to all routes, with explicit exclusions for
  public routes?
- Or is auth middleware applied per-route (prone to missing routes)?
- Check each non-public route explicitly — look for the middleware chain in the route
  definition

Flag any route that handles sensitive data (user profiles, admin functions, payments)
without auth middleware as CRITICAL.

### WSTG-AUTHN-06 — Weak password policy

Find password creation/change endpoints and validation logic. Check:
- Minimum length enforced server-side (not just client-side)
- Complexity requirements (if required by policy)
- Check password validator libraries used (`zxcvbn`, `joi`, custom regex)
- Absence of server-side validation when client-side only is MEDIUM

### WSTG-AUTHN-07 — Weak password reset

Find password reset flow. Check:
- Reset token generation: is `crypto.randomBytes(32)` or equivalent used? Flag
  `Math.random()`, UUIDs, or timestamp-based tokens as CRITICAL
- Token expiry: is there a TTL? Absent expiry is HIGH
- Token single-use: is the token invalidated after use? Reusable tokens are HIGH
- Reset link sent to unverified email address?

### WSTG-AUTHN-09 — Weak cryptography for passwords

Search for password hashing in user creation/update code:
- Flag: `md5`, `sha1`, `sha256` used directly for passwords — CRITICAL
- Flag: `sha512` without salt — HIGH
- Flag: bcrypt with rounds < 10 — MEDIUM
- Acceptable: `bcrypt` (rounds >= 10), `argon2`, `scrypt`, `pbkdf2` with ≥ 100k iterations

### WSTG-AUTHN-10 — Weaker authentication in alternative channels

Compare auth enforcement across:
- REST API endpoints vs. web routes — do API endpoints skip checks the web UI enforces?
- Mobile-specific API versions (`/api/v1/mobile/`) — same middleware stack?
- Webhook endpoints — is signature verification required?

---

## Phase 4 — WSTG-AUTHZ (Authorization)

### WSTG-AUTHZ-01 — Directory traversal / file include

Search for file operations using user-supplied input:
- `fs.readFile`, `fs.readFileSync`, `path.join` with user input
- `open()`, `read()` in Python with user input
- `File()`, `FileInputStream` in Java with user input
- Check for path normalization before use — is `path.resolve` + prefix check used?

Generate probe if found:
```
Probe: curl -X GET "http://localhost:3000/files?path=../../etc/passwd"
```

### WSTG-AUTHZ-02 — Bypassing authorization schema (IDOR)

For every endpoint with an object ID in path or query (e.g. `/users/:id`, `/orders/:id`):
- Does the handler verify `resource.ownerId === currentUser.id`?
- Is there a generic `findById` without ownership check?
- Can user A access user B's data by changing the ID?

Flag missing ownership checks as CRITICAL with a specific probe showing the ID substitution.

### WSTG-AUTHZ-03 — Privilege escalation

Check for role-based access control implementation:
- Is `role` or `isAdmin` a field in the JWT payload or session? Is it verified server-side
  against the database, or trusted from the token directly without re-verification?
- Does any endpoint accept a `role` field in the request body and use it without
  server-side role verification?
- Can a regular user elevate to admin by modifying the JWT payload (check JWT verification)?

### WSTG-AUTHZ-04 — IDOR (Insecure Direct Object Reference)

Specifically look for sequential or guessable IDs (integers, short UUIDs) used to
reference resources without per-request ownership verification. Look at:
- Database query patterns: `WHERE id = $userInput` without `AND user_id = $currentUser`
- ORM queries: `Model.findById(req.params.id)` without scope restriction

---

## Phase 5 — WSTG-SESS (Session Management)

### WSTG-SESS-01 — Session management schema

Check JWT implementation:
- Search for JWT signing: `jwt.sign()`, `Jwts.builder()`, `PyJWT.encode()`
- Is the secret a hardcoded string? Flag as CRITICAL if found in source
- Secret length < 32 bytes? Flag as HIGH
- Is `alg` validated on decode? Accepting `none` algorithm is CRITICAL
- Is the `kid` header sanitized before use in key lookup?

Check session tokens:
- Cookie-based: is `session.secret` loaded from environment (good) or hardcoded (CRITICAL)?
- Token entropy: `Math.random()` or `uuid()` without crypto — HIGH

### WSTG-SESS-02 — Cookie attributes

Search for cookie creation (`res.cookie()`, `response.addCookie()`, `set_cookie()`):
- Missing `HttpOnly`: flag as HIGH (enables XSS cookie theft)
- Missing `Secure`: flag as HIGH (transmits over HTTP)
- `SameSite` not set or set to `None` without `Secure`: flag as MEDIUM

### WSTG-SESS-03 — Session fixation

Check login flow: after successful authentication, is a new session ID generated?
- Express: `req.session.regenerate()` called after login?
- Spring: `SessionManagement.sessionFixation().newSession()` configured?
- Missing session regeneration on login is HIGH

### WSTG-SESS-04 — Exposed session variables

Search for session data or tokens in:
- URL query parameters (`?token=`, `?session=`, `?auth=`)
- Log statements (`console.log(req.session)`, `logger.debug(token)`)
- Error responses that include session state

### WSTG-SESS-05 — CSRF

For every state-changing endpoint (POST, PUT, PATCH, DELETE):
- Is a CSRF token verified? Look for `csurf` middleware, `@EnableWebSecurity` with CSRF,
  Django's `{% csrf_token %}`
- Is `SameSite=Strict` or `SameSite=Lax` set on session cookie (partial mitigation)?
- REST APIs with `Content-Type: application/json` only are partially mitigated — check if
  `Origin` or `Referer` header is validated

Missing CSRF protection on state-changing forms is HIGH.

### WSTG-SESS-06 — Session timeout

Check token/session expiry configuration:
- JWT: `expiresIn` set? Missing is MEDIUM; value > 24h is LOW (note it)
- Session: `cookie.maxAge` or `rolling` expiry configured?
- No absolute expiry on long-lived tokens is MEDIUM

### WSTG-SESS-08 — Session puzzling

Check if the same session variable name is reused across different authentication flows:
- e.g. `session.userId` set during normal login AND during password reset flow — could
  allow reset flow to authenticate as a different user

---

## Phase 6 — WSTG-INPV (Input Validation)

### WSTG-INPV-01 — Reflected XSS

Find endpoints that render user input directly in HTML responses:
- Template engines: `res.render()`, `.ejs`, `.hbs`, `.pug` — look for unescaped output
  (`{{{var}}}` in Handlebars, `!= var` in Pug, `{{ var | safe }}` in Jinja2/Django)
- String concatenation into HTML responses
- `innerHTML = userInput` in client-side JS

```
Probe: curl -X GET "http://localhost:3000/search?q=<script>alert(1)</script>"
```

### WSTG-INPV-02 — Stored XSS

Find endpoints that store user input and later render it:
- User profile fields, comments, post content rendered in admin views
- Check sanitization at storage time AND at render time
- Look for missing `DOMPurify`, `bleach`, `sanitize-html` calls

### WSTG-INPV-05 — SQL Injection

Search for database query construction using string concatenation:
- `"SELECT * FROM users WHERE name = '" + name + "'"` — CRITICAL
- `query("SELECT ... WHERE id = " + req.params.id)` — CRITICAL
- ORM raw queries: `.query()`, `.raw()`, `session.execute(text(...))` with f-strings
- Check: parameterized queries / prepared statements used everywhere?

```
Probe: curl -X GET "http://localhost:3000/users?name=' OR '1'='1"
```

### WSTG-INPV-07 — XML Injection / XXE

Find XML parsing code (`DOMParser`, `javax.xml.parsers.DocumentBuilderFactory`,
`lxml.etree`, `xml.etree.ElementTree`, `libxml2`):
- Is external entity processing disabled?
  - Java: `factory.setFeature("http://xml.org/sax/features/external-general-entities", false)`
  - Python: `etree.XMLParser(resolve_entities=False)`
  - .NET: `XmlReaderSettings.DtdProcessing = DtdProcessing.Prohibit`
- Missing XXE protection on user-supplied XML input is CRITICAL

### WSTG-INPV-08 — SSI Injection

Look for server-side include processing or template rendering of user input directly.
Check: does any endpoint pass user-controlled strings through `ejs.render()`,
`Handlebars.compile()`, `eval()`, `new Function()` at runtime?

### WSTG-INPV-09 — XPath Injection

Find XPath query construction with user input:
- `xpath.select("//user[@name='" + username + "']", doc)` — CRITICAL
- Check for parameterized XPath or input sanitization

### WSTG-INPV-10 — IMAP/SMTP Injection

Find email sending code (`nodemailer`, `smtplib`, `JavaMail`):
- Is the `To`, `CC`, `BCC`, or `Subject` field constructed from user input without sanitization?
- CRLF injection in email headers allows adding arbitrary recipients

### WSTG-INPV-11 — Code Injection

Search for dynamic code execution:
- JavaScript: `eval(userInput)`, `new Function(userInput)`, `vm.runInNewContext(userInput)`
- Python: `eval(userInput)`, `exec(userInput)`
- Ruby: `eval(userInput)`, `instance_eval`
- Any of these with user-controlled input is CRITICAL

### WSTG-INPV-12 — Command Injection

Search for shell command execution with user input:
- Node.js: `child_process.exec(userInput)`, `child_process.execSync(userInput)`,
  `shell: true` with user input in `spawn`
- Python: `subprocess.run(userInput, shell=True)`, `os.system(userInput)`,
  `os.popen(userInput)`
- Java: `Runtime.exec(userInput)`, `ProcessBuilder` with unsanitized user segments

```
Probe: curl -X POST http://localhost:3000/convert -d '{"filename": "test.pdf; cat /etc/passwd"}'
```

### WSTG-INPV-13 — Format String

Search for logging or print statements using user input as the format string:
- C/C++: `printf(userInput)` (not applicable in most web stacks but check FFI bindings)
- Python: `logging.info(userInput)` (safe) vs. `logging.info(userInput % args)` with
  controlled format
- Check: `logger.log(userInput)` where logger processes format strings

### WSTG-INPV-17 — HTTP Splitting (CRLF Injection)

Find redirect responses or header construction using user input:
- `res.redirect(userInput)` without sanitizing `\r\n` — allows injecting response headers
- `response.setHeader('Location', userInput)` without validation

```
Probe: curl -v "http://localhost:3000/redirect?url=http://evil.com%0d%0aSet-Cookie:%20session=hijacked"
```

### WSTG-INPV-18 — Open Redirect

Find redirect endpoints (common in OAuth flows, login redirects):
- `res.redirect(req.query.next)` without allowlist validation
- `return redirect_to(params[:return_to])` without validation

Check: is the redirect URL validated against an allowlist of allowed domains?

```
Probe: curl -v "http://localhost:3000/login?next=https://evil.com"
```

### WSTG-INPV-19 — JWT Attacks

For JWT implementations:
- `alg: none` acceptance: check if `jwt.verify()` is called with `algorithms` option
  restricted to expected algorithms
- Weak HMAC secret: search for hardcoded secrets or short strings (< 32 chars)
- `kid` header injection: if `kid` is used to look up the key, is it sanitized?
  SQL injection via `kid` is a known attack vector

---

## Phase 7 — WSTG-ERRH (Error Handling)

### WSTG-ERRH-01 — Improper error handling

Look at error handler middleware (Express: `app.use((err, req, res, next) => ...)`):
- Does the error response include `err.stack` or `err.message` in production?
- Are database errors passed directly to the response?
- Internal file paths, SQL queries, or ORM details exposed in error messages?

Check: is there a production vs. development error handler distinction?

### WSTG-ERRH-02 — Stack traces in production

Check framework configuration:
- Django: `DEBUG = True` in `settings.py` used in production
- Spring Boot: `server.error.include-stacktrace: always`
- Express: `app.set('env', 'development')` in production config

---

## Phase 8 — WSTG-CRYP (Cryptography)

### WSTG-CRYP-01 — Weak TLS configuration

Check server TLS configuration (nginx/Apache config files, Node.js `https.createServer`):
- `SSLv3`, `TLSv1`, `TLSv1.1` enabled — flag as HIGH
- Weak cipher suites (RC4, DES, 3DES, NULL ciphers) — flag as HIGH
- Check `ssl_protocols` in nginx config or `secureProtocol` in Node.js

### WSTG-CRYP-02 — Padding oracle

Search for AES-CBC usage:
- `AES/CBC/PKCS5Padding` in Java, `AES.new(key, AES.MODE_CBC)` in Python
- Is the padding error distinguishable from other errors in the response? If yes, MEDIUM

### WSTG-CRYP-03 — Sensitive data encryption

Search for PII storage and transmission:
- Are passwords, SSNs, credit card numbers, health data stored in plaintext?
- Are API tokens or secrets logged at INFO or DEBUG level?
- Check database column types for sensitive fields — are they encrypted at rest?

### WSTG-CRYP-04 — Weak random for security tokens

Search for non-cryptographic random in security contexts:
- `Math.random()` used to generate tokens, reset links, API keys — CRITICAL
- `random.random()` or `random.randint()` in Python for security tokens — CRITICAL
- `java.util.Random` for session tokens — CRITICAL
- Acceptable: `crypto.randomBytes()`, `secrets.token_bytes()`, `SecureRandom`

---

## Phase 9 — WSTG-BUSL (Business Logic)

### WSTG-BUSL-01 — Business logic data validation

Find numeric fields in business operations (quantity, price, discount):
- Negative quantities in order/cart — is there server-side validation that quantity > 0?
- Zero or negative prices in payment flows
- Integer overflow in large quantity/price calculations
- Discount percentage > 100%

### WSTG-BUSL-02 — Request forgery

Identify state-transition endpoints (order status changes, account state changes):
- Can an attacker forge a request to transition state out of sequence?
- Is the current state validated before allowing the transition?

### WSTG-BUSL-03 — Integrity checks

Look for hidden form fields or client-supplied values that affect business logic:
- Price, discount, tax sent from the client and trusted server-side
- Shopping cart totals calculated client-side and submitted
- Any `trusted=true` or `isAdmin=false` fields accepted from client

### WSTG-BUSL-04 — Process timing / race conditions

Identify operations that should be atomic but may not be:
- Balance checks followed by deductions (TOCTOU): `if balance >= amount; deduct(amount)`
  without database-level locking
- Coupon/voucher application without atomic check-and-use
- Look for `SELECT ... FOR UPDATE` or transactions wrapping check+modify patterns

### WSTG-BUSL-05 — Function limits

Check high-value functions for invocation limits:
- Referral code usage: is there a max redemption count enforced?
- Coupon/promo code: single-use enforced atomically?
- Password reset: can the same token be used multiple times?
- Email verification links: single-use?

### WSTG-BUSL-06 — Workflow circumvention

For multi-step flows (checkout, onboarding, password reset):
- Can step 3 be accessed directly without completing steps 1 and 2?
- Is the workflow state tracked server-side (not just client-side)?

### WSTG-BUSL-07 — Application misuse defenses

Check high-value actions for rate limiting:
- Account creation (signup abuse, bot accounts)
- Password reset request (email flooding)
- Search endpoints (data harvesting)
- Payment submission (card testing attacks)

### WSTG-BUSL-08 — Upload unexpected files

Extend WSTG-CONF-10 analysis:
- Are polyglot files handled safely (e.g. valid image that is also valid HTML)?
- Are zip files extracted? If so, is there protection against zip bombs and zip slip?
- Are SVG files sanitized for embedded scripts?

---

## Phase 10 — WSTG-APIT (API Testing)

### WSTG-APIT-01 — GraphQL security

If a GraphQL endpoint is present:
- Is introspection disabled in production? (`introspection: false` in Apollo Server config)
- Is query depth limited? (`depthLimit` middleware or equivalent)
- Is query complexity limited?
- Are N+1 query patterns present that can be abused for DoS?
- Can batch queries (`[{query1}, {query2}]`) be used to bypass rate limits?

```
Probe (introspection): curl -X POST http://localhost:4000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name } } }"}'
```

### WSTG-APIT-02 — REST API security

For all REST endpoints:
- Mass assignment: does the handler pass `req.body` directly to `Model.create()` or
  `Model.update()`? Check for allowlist of permitted fields (`pick`, `omit`, `@Expose`)
- Verb tampering: for a route defined as `GET /users/:id`, does the server reject
  `POST /users/:id` or does it fall through to a catch-all?
- Insecure direct object exposure: are internal database IDs (integer PKs) exposed in
  responses and used as route parameters? Prefer opaque UUIDs or add ownership checks

---

## Phase 11 — Produce findings report

Group all findings by severity. Use this format for each finding:

```
[WSTG-AUTHN-04] Missing auth middleware on protected route
Severity: CRITICAL
File: src/routes/admin.ts:42
Endpoint: GET /admin/users
Issue: Route handler is missing authentication middleware. Any unauthenticated user can access admin user list.
Probe: curl -X GET http://localhost:3000/admin/users
Remediation: Add auth middleware before handler: router.get('/admin/users', authenticate, authorize('admin'), handler)
```

Order: CRITICAL → HIGH → MEDIUM → LOW

After all findings, print a WSTG coverage table:

```
WSTG-ID         | Test Name                          | Result
----------------|------------------------------------|--------
WSTG-CONF-01    | Network configuration              | PASS / FAIL / SKIP (reason)
WSTG-CONF-02    | Application platform config        | PASS / FAIL / SKIP
...
```

Mark as SKIP when the codebase has no relevant surface (e.g. WSTG-APIT-01 skipped when
no GraphQL endpoint found), and `SKIP (out of requested scope)` for every phase a
Phase 0 scope excluded. Both are SKIP, never PASS — a test that did not run has not
passed. When `WSTG_SCOPE` was anything other than `ALL`, open the report by naming
what was reviewed and what was not, and state that this is not a full OWASP review.

---

## What NOT to do

- Do not make network requests to run actual attacks — this is a design-time analysis.
- Do not report findings without citing the specific file and line where the issue occurs.
- Do not flag framework-level protections as missing when the framework provides them by default.
- Do not report theoretical issues without evidence in the code — cite the exact code pattern.
- Do not skip WSTG tests without noting them in the coverage table.
- Do not produce a summary without grouping by severity.
