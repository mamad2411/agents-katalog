---
name: framework-flask
description: Flask security review — validate debug console exposure, Jinja2 template safety, session-cookie configuration, secret-key hygiene, and Werkzeug server settings with docs-first, read-only checks and no SSTI exploitation or session forgery.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Flask security — configuration and surface review

Use this skill to review Flask application security posture on authorized in-scope targets. Validate Werkzeug debug console exposure, Jinja2 template auto-escaping, session-cookie configuration, secret-key hygiene, and server/proxy trust settings. All tests are read-only and low-rate. Never exploit Jinja2 SSTI for code execution, brute-force the Werkzeug debug PIN, forge session cookies, or test credential endpoints — those behaviors are prohibited unless separately approved for destructive validation.

## Required inputs

- Written scope covering the Flask application hosts, API routes, static paths, and allowed review methods. Explicit confirmation that template injection exploitation, debug-PIN brute-forcing, session forgery, and credential testing are prohibited unless separately approved.
- Flask/Werkzeug version from: response `Server` header, error-page signatures, debug-console format, or local source code (if provided).
- Official Flask and Werkzeug documentation for the detected version — prefer flask.palletsprojects.com and werkzeug.palletsprojects.com.
- Valid authorization cache for the target application.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for read-only execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — version detection and server fingerprinting

1. Detect Flask and Werkzeug from response headers: `Server: Werkzeug/X.Y.Z Python/A.B.C` is the default development-server header. In production behind a reverse proxy, this header may be suppressed or overridden — its presence suggests the development server is exposed directly.
2. Check for Flask-specific response signatures: default 404 page format, default 500 debugger page (Werkzeug interactive debugger), and redirect response format.
3. If the application triggers an unhandled error, inspect the error page: the Werkzeug debugger shows a full stack trace, local variable values, and an interactive Python console when enabled. The format differs by Werkzeug version and can identify whether `DEBUG = True`.
4. Check for production server indicators: a missing `Server` header or a generic value (nginx, gunicorn, uwsgi) suggests a reverse-proxy setup. The Flask application server may be Werkzeug (development), Gunicorn, uWSGI, or Waitress — each has different security characteristics.
5. Document version evidence and note any uncertainty. If the version appears end-of-life or unpatched, flag immediately.

### Phase 2 — debug console and error disclosure

1. Check whether the Werkzeug interactive debugger is exposed. Probe `/console` — if the debugger is enabled (`DEBUG = True`), this path presents an interactive Python console protected by a numeric PIN. The console allows arbitrary Python code execution.
2. If `/console` is reachable, the debugger is exposed. Do not attempt to guess or brute-force the PIN. Record the exposure as a critical finding and stop active testing on that host — the application is in a development state and further testing could cause unintended damage.
3. Trigger a safe error (404 on an allowed path) and inspect the response. If a Werkzeug debug traceback is returned with source code, local variables, and the PIN input field, `DEBUG = True` and `PROPAGATE_EXCEPTIONS` may both be enabled — a critical finding.
4. Check for custom error handlers: does the application return a consistent JSON error response for API routes and an HTML error page for browser routes? Custom error handlers in Flask (registered with `@app.errorhandler`) indicate the application has been production-hardened for error output.
5. Check for information leakage in error responses: do 400/403/404/405/500 responses include stack traces, file paths, database connection strings, or internal IP addresses? Any of these is a finding.

### Phase 3 — Jinja2 template safety and auto-escaping

1. Identify endpoints that render user-controlled input in responses: search results, user profile pages, error messages that echo input, URL parameters reflected in the page, and form submissions that are redisplayed on error.
2. For each endpoint, test whether Jinja2 auto-escaping is active: submit HTML metacharacters (`<b>test</b>`) and observe whether they are rendered as HTML (bold text — auto-escaping off) or displayed literally (escaped — auto-escaping on). Flask enables auto-escaping by default for `.html` templates.
3. Test whether `| safe` filter or `Markup()` is used unsafely: submit content that would be rendered as HTML or interpreted as template syntax. If `{{ user_input }}` renders as HTML, the `| safe` filter is applied — flag as a potential SSTI vector.
4. Identify whether template syntax is evaluated from user input: submit `{{ 7 * 7 }}` or `{{ config }}` in a parameter. If the response contains `49` or the Flask config dictionary, the application is evaluating user input as a Jinja2 template — a critical SSTI vulnerability.
5. Do not escalate SSTI detection to exploitation. If template evaluation is confirmed, record the finding (critical) and stop. Do not attempt `__class__.__mro__`, `__subclasses__()`, `popen`, file read, or any RCE payloads unless separately approved through destructive-executor gates.

### Phase 4 — session cookie and secret-key security

1. Inspect the session cookie from response `Set-Cookie` headers: the default Flask session cookie name is `session`. Check for `HttpOnly` flag, `Secure` flag, `SameSite` attribute, and reasonable expiration. Flask sessions are client-side by default (signed, not encrypted) — the session data is base64-encoded and visible to the client.
2. Decode the session cookie payload (base64 decode the part before the first `.`, decompress if zlib-compressed). Inspect the session data structure: are there fields that should not be client-visible (internal IDs, roles, permissions, or sensitive user data)? Flask sessions are integrity-protected (signed) but not confidential.
3. Check for `SESSION_COOKIE_SECURE` enforcement: if the application uses HTTPS, send a plain-HTTP request and verify the session cookie is not transmitted.
4. Check for `SECRET_KEY` exposure in: public JavaScript bundles, source maps, git-exposed `.env` or `config.py` files, error-page output (already checked in Phase 2), and public code repositories if the application is open-source.
5. Do not attempt to brute-force `SECRET_KEY` or forge session cookies. Do not use `flask-unsign` or similar tools against live sessions. If the secret key is exposed, record the finding and recommend immediate rotation.

### Phase 5 — server configuration and proxy trust

1. Check whether the application trusts proxy headers: send `X-Forwarded-For`, `X-Forwarded-Host`, `X-Forwarded-Proto`, and `X-Real-IP` headers. If the application reflects these values in responses, redirects, or access-control decisions, proxy-trust is misconfigured — an attacker can spoof client IP, host, or protocol.
2. Check for open redirects: submit a `?next=` or `?redirect=` parameter with an external URL. If Flask's `redirect()` function accepts user-controlled URLs without validation, the application is vulnerable to open-redirect phishing.
3. Check for CORS configuration: if the application uses Flask-CORS, send cross-origin requests and inspect `Access-Control-Allow-Origin`, `Access-Control-Allow-Credentials`, and `Access-Control-Allow-Methods` response headers. `Access-Control-Allow-Origin: *` with `Access-Control-Allow-Credentials: true` is a misconfiguration — credentials cannot be sent with wildcard origins.
4. Check for secure file serving: are static files served via Flask's `send_file()` or `send_from_directory()`? Test for path traversal by submitting `../` sequences in file-path parameters. Flask's `safe_join()` should prevent traversal — if it does not, flag as a path-traversal finding.
5. Check for rate-limiting: does the application enforce rate limits on login, password reset, and API endpoints? Flask-Limiter is the common extension. If no rate-limiting headers or behavior is observed, flag as a hardening gap.

## Decision points

- **Escalate on Werkzeug debug console exposed**: `/console` reachable with interactive Python console → critical, stop all active testing on affected host.
- **Escalate on Jinja2 SSTI confirmed**: `{{ 7 * 7 }}` returning `49` or `{{ config }}` returning the Flask config → critical, stop template-injection testing.
- **Escalate on SECRET_KEY exposure**: key found in client-side code, error output, or public repository → critical, all sessions must be invalidated.
- **Escalate on client-visible sensitive session data**: PII, roles, or internal identifiers visible in decoded session cookies → high.
- **Escalate on proxy-trust misconfiguration**: `X-Forwarded-For` or `X-Forwarded-Host` accepted without validation → high, enables IP spoofing and host-header attacks.
- **Downgrade on default session cookie name**: informative — renaming `session` cookie is defense-in-depth.

## Prohibited behavior

- Exploiting Jinja2 SSTI for code execution: no `__class__.__mro__`, `__subclasses__()`, `popen`, file read, or RCE payloads.
- Brute-forcing the Werkzeug debug console PIN — record exposure, do not attempt PIN calculation.
- Forging session cookies using a discovered or guessed `SECRET_KEY` — record exposure, recommend rotation.
- Attempting to brute-force `SECRET_KEY` values with `flask-unsign` or similar tools.
- Testing credential endpoints, login forms, or password-reset flows with any credentials.
- Running directory brute-force or wordlist scans against the application.

## Stop conditions

- Werkzeug debug console exposed → stop, critical finding, do not attempt PIN input.
- Jinja2 SSTI confirmed (template syntax evaluated) → stop, do not exploit further.
- SECRET_KEY found exposed → stop, record finding, do not use for session manipulation.
- Sensitive session data observed (PII, internal IDs, permissions) → stop, record finding.
- Target not in scope or error triggers would impact production → stop.

## Evidence — Flask security matrix

For each target, record:

```text
Target: <URL> | Flask/Werkzeug version: <detected | estimated>
Version evidence: <Server header | error page | debug console format | behavioral>

Debug and error disclosure:
  Werkzeug debug console: <exposed at /console | not found>
  DEBUG mode: <True — traceback with source | False — generic error>
  Custom error handlers: <yes — JSON/HTML consistent | no — raw tracebacks>
  Error info leakage: <stack traces | file paths | DB strings | none>

Template safety:
  Auto-escaping active: <yes — HTML escaped | no — rendered | not tested>
  Templates in endpoints: <count of user-input-reflection endpoints>
  SSTI confirmed: <yes — {{ }} evaluated | no>
  | safe filter misuse: <detected — endpoint | not found>

Session security:
  Session cookie HttpOnly: <yes | no>
  Session cookie Secure: <yes | no — HTTP transmits>
  Session cookie SameSite: <Lax | Strict | None>
  Sensitive data in session: <yes — field types | no>
  SECRET_KEY exposure: <exposed in error/js/repo | not found>

Server configuration:
  Proxy-trust misconfigured: <X-Forwarded-* accepted | properly validated>
  Open redirect: <yes — endpoint | no>
  CORS misconfigured: <wildcard + credentials | properly restricted | no CORS>
  Path traversal in file serving: <yes — endpoint | no>
  Rate limiting: <observed — endpoints | not observed>

Overall risk: <critical | high | medium | low>
```

Never store: SECRET_KEY values, Werkzeug debug PIN fragments, session cookie values, SSTI payload responses containing server internals, or decoded session contents with PII.

## Report handoff

1. `pentest_agent_record_finding` for: exposed Werkzeug debug console, confirmed Jinja2 SSTI, SECRET_KEY exposure, client-visible sensitive session data, proxy-trust misconfiguration, open redirects, CORS misconfiguration, and path traversal.
2. Reference the Flask security matrix.
3. Recommend: disable `DEBUG` and `PROPAGATE_EXCEPTIONS` in production, run Flask behind a hardened reverse proxy (nginx/gunicorn), set `SESSION_COOKIE_SECURE = True`, `SESSION_COOKIE_HTTPONLY = True`, and `SESSION_COOKIE_SAMESITE = 'Lax'`, enable Jinja2 auto-escaping (default — verify no `| safe` misuse), rotate `SECRET_KEY` immediately if ever exposed, validate proxy headers with a trusted proxy middleware, set `app.config['PREFERRED_URL_SCHEME'] = 'https'`, and upgrade Flask and Werkzeug to supported versions.
