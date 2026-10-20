---
name: framework-laravel
description: Laravel security review — validate .env exposure, APP_DEBUG leaks, Eloquent mass-assignment, Telescope/ignition exposure, session and CSRF configuration, queue/storage hardening with docs-first read-only checks and no deserialization exploitation or credential testing.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Laravel security — configuration and surface review

Use this skill to review Laravel application security posture on authorized in-scope targets. Validate `.env` file exposure, `APP_DEBUG` status, Eloquent mass-assignment protections, Laravel Telescope and Ignition exposure, session-cookie configuration, CSRF middleware bypass, queue-connection hardening, and public-storage accessibility. All tests are read-only and low-rate. Never exploit PHP deserialization for code execution, brute-force `APP_KEY`, forge session cookies, or test credential endpoints — those behaviors are prohibited unless separately approved for destructive validation.

## Required inputs

- Written scope covering the Laravel application hosts, API routes, admin paths, storage paths, and allowed review methods. Explicit confirmation that deserialization exploitation, APP_KEY brute-forcing, session forgery, and credential testing are prohibited unless separately approved.
- Laravel version from: `composer.lock`, response headers (`X-Powered-By` when not suppressed), error-page signatures, or local source code (if provided).
- Official Laravel documentation for the detected version — prefer laravel.com/docs.
- Valid authorization cache for the target application.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for read-only execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — version detection and fingerprinting

1. Detect Laravel from response indicators: `laravel_session` cookie name, `X-Powered-By` header (may show PHP version), default 404/503 error page format, and CSRF `_token` field presence in forms.
2. Check for `composer.lock` exposure at `/composer.lock` — if accessible, the exact Laravel and dependency versions are disclosed. Record as a finding and extract the Laravel framework version from the lockfile.
3. Identify the application environment: production Laravel apps should suppress debug output, disable Telescope/Ignition in production, and avoid exposing `.env` or configuration routes. Development/staging indicators suggest the application was not hardened for production.
4. Document version evidence and note any uncertainty. If the version appears end-of-life (Laravel versions receive bug fixes for 18 months and security fixes for 2 years), flag immediately.

### Phase 2 — .env exposure and APP_DEBUG

1. Probe common `.env` exposure paths: `/.env`, `/.env.backup`, `/.env.example`, `/.env.production`, `/.env.local`, and `/.env.old`. Laravel's default `.htaccess` in the `public/` directory should block these — if any return 200, the web server is misconfigured.
2. If `.env` is exposed, it typically contains `APP_KEY`, database credentials (`DB_USERNAME`, `DB_PASSWORD`), mail driver credentials, Redis credentials, cloud storage keys, and third-party service tokens. Do not store the raw `.env` content in evidence — record that it was exposed, the key categories of secrets leaked, and recommend immediate rotation.
3. Check `APP_DEBUG` status: trigger a 404 on a non-existent route. If the response includes a Whoops-styled stack trace with file paths, environment variables, and request context, `APP_DEBUG=true`. Record as a critical finding — this exposes internal paths, query logs, and possibly `APP_KEY`.
4. Check for `APP_DEBUG` via the Ignition error page: Laravel 6+ ships with Ignition by default. Submit a request that triggers an unhandled error and inspect whether the Ignition debug page renders with stack trace, request data, and environment details.

### Phase 3 — Telescope and Ignition exposure

1. Probe for Laravel Telescope at `/telescope`. Telescope is a debugging dashboard that shows requests, exceptions, database queries, queued jobs, mail, notifications, cache operations, and scheduled tasks. It has no authentication by default — exposure is a critical finding.
2. If `/telescope` is reachable, probe `/telescope/requests`, `/telescope/exceptions`, and `/telescope/queries` — these API endpoints return structured JSON with full request payloads, headers, and query bindings.
3. Probe for Ignition at `/_ignition/health-check`. Ignition is the default Laravel error page and its health-check endpoint should only be enabled in local development. If reachable in production, it confirms Ignition is active and may expose application internals.
4. Check `/_ignition/execute-solution`: in older Laravel versions (before the CVE-2021-3129 fix), this endpoint allowed remote code execution via variable manipulation. Do not attempt exploitation. Record the endpoint reachability as a critical finding and note the CVE if version data suggests it applies.

### Phase 4 — Eloquent mass-assignment protection

1. Identify registration and profile-update endpoints. Laravel protects against mass-assignment through `$fillable` and `$guarded` properties on Eloquent models. Test by submitting unexpected fields in request bodies.
2. On the registration endpoint, add fields like `is_admin`, `role`, `verified`, `approved`, `plan`, or `subscription_tier` to the request body. If the application accepts and persists these values, mass-assignment protection is missing — a high finding.
3. On profile-update endpoints, submit fields such as `role`, `is_admin`, `email_verified_at`, `balance`, or `credit`. These should never be client-writable.
4. Test nested and array mass-assignment: submit `user[is_admin]`, `profile[role]`, or `account[verified]` with unexpected values. Some applications protect top-level attributes but miss nested arrays.
5. Do not set values that would lock out or damage real accounts. Use values that are safe to test (boolean flags, non-destructive role changes that can be reverted).

### Phase 5 — session, CSRF, and cookie security

1. Inspect the session cookie from response headers: the default Laravel session cookie name is `laravel_session`. Check for `HttpOnly`, `Secure`, `SameSite`, and the `Domain`/`Path` attributes.
2. Test CSRF protection: Laravel applies CSRF middleware to all `POST`, `PUT`, `PATCH`, and `DELETE` routes by default, requiring a `_token` field or `X-CSRF-TOKEN` header. Test whether API routes bypass this middleware — Laravel typically excludes routes in `routes/api.php` from CSRF protection, which is expected when using token-based auth.
3. Test `SameSite` cookie enforcement: if the session cookie uses `SameSite=Lax` or `Strict`, cross-site form submissions should not include the session cookie. Verify by checking response cookies and testing a cross-origin POST.
4. Check for CSRF token exposure in client-side JavaScript, public source maps, or error responses.
5. Do not attempt to forge CSRF tokens or session cookies. Do not brute-force `APP_KEY` values.

### Phase 6 — storage, queue, and file exposure

1. Check public storage accessibility: Laravel's `public/storage` is a symlink to `storage/app/public` created by `php artisan storage:link`. Probe `/storage/` for directory listings or accessible files. Publicly accessible storage directories may expose user uploads, exported reports, or backups.
2. Check log file exposure: probe `/storage/logs/laravel.log`. Laravel's default log file can contain stack traces, SQL queries, request payloads, and sometimes credential information from misconfigured services.
3. Check for debug toolbar or clockwork exposure: Laravel Debugbar (`/_debugbar`) and Clockwork (`/__clockwork`) are development toolbars that expose extensive application internals. Both should be disabled in production.
4. Check queue dashboard exposure: Laravel Horizon (`/horizon`) provides a dashboard for Redis queue monitoring. It has no authentication by default — exposure reveals job payloads, failed job data, and queue statistics.
5. Do not download exposed files that may contain secrets. Record the exposure, note the file category, and count (not content) of what is exposed.

## Decision points

- **Escalate on .env exposed**: `.env` file returns 200 → critical. All secrets in that file must be rotated immediately. Any credential in the exposed file is compromised.
- **Escalate on APP_DEBUG=true**: Whoops/Ignition stack trace visible → critical. The `APP_KEY` may be visible in the environment section of the error page.
- **Escalate on Telescope accessible**: `/telescope` dashboard reachable without authentication → critical. Stop active testing — Telescope may expose your own testing requests.
- **Escalate on Ignition execute-solution reachable**: `/_ignition/execute-solution` accepts POST → critical on older Laravel versions. Do not exploit; record and recommend immediate upgrade.
- **Escalate on mass-assignment accepted**: privilege-escalation fields persisted → high. Account integrity is at risk.
- **Escalate on Horizon accessible without auth**: job data and queue contents exposed → high.
- **Downgrade on missing SameSite attribute**: informative in isolation — defense-in-depth gap.

## Prohibited behavior

- Exploiting PHP deserialization for code execution: no `PHPGGC` payloads, no unserialize chains, no cookie manipulation beyond decoding.
- Brute-forcing `APP_KEY` values with tools like `laravel-keygen` or similar — record exposure, recommend rotation.
- Forging session cookies using a discovered `APP_KEY` — record exposure, do not sign forged cookies.
- Testing credentials on login, password-reset, or registration flows.
- Running directory brute-force or wordlist scans against the application.
- Downloading exposed `.env` files, log files, or Telescope data that contain real credentials or PII.
- Attempting Ignition RCE (CVE-2021-3129) exploitation — detection only, no variable manipulation or file write payloads.

## Stop conditions

- `.env` file exposed → stop, critical finding, all secrets must be rotated.
- `APP_DEBUG=true` with stack trace visible → stop, critical finding, `APP_KEY` may be exposed.
- Telescope dashboard accessible without authentication → stop, critical finding.
- Ignition health-check or execute-solution reachable in production → stop, critical finding.
- Mass-assignment allows privilege escalation → stop, record finding, do not exploit further.
- Evidence contains secrets or PII → redact immediately and store only minimal proof refs.

## Evidence — Laravel security matrix

For each target, record:

```text
Target: <URL> | Laravel version: <detected | estimated from composer.lock>
Version evidence: <composer.lock | response header | error page | behavioral>

Environment and debug:
  .env exposed: <yes — paths | no>
  APP_DEBUG: <true — Whoops/Ignition traceback | false>
  Composer lock exposed: <yes | no>

Dashboard and debug tooling:
  Telescope (/telescope): <accessible without auth | requires auth | not found>
  Ignition health-check: <reachable | not found>
  Ignition execute-solution: <reachable — CVE-2021-3129 | not found>
  Horizon (/horizon): <accessible without auth | requires auth | not found>
  Debugbar/Clockwork: <exposed | not found>

Mass assignment:
  Registration extra fields accepted: <yes — fields | no>
  Profile extra fields accepted: <yes — fields | no>
  Nested/array bypass: <detected | not found>

Session and CSRF:
  Session cookie HttpOnly: <yes | no>
  Session cookie Secure: <yes | no>
  Session cookie SameSite: <Lax | Strict | None | not set>
  CSRF bypass on API routes: <expected — token auth | unexpected>

Storage and logs:
  Public storage listing: <yes — path | no>
  Log file exposed: <yes — storage/logs/laravel.log | no>
  Backup/config files exposed: <yes — paths | no>

Overall risk: <critical | high | medium | low>
```

Never store: `.env` file contents, `APP_KEY` values, Telescope request data with credentials, session cookie values, exposed database credentials, or unredacted stack traces with internal paths.

## Report handoff

1. `pentest_agent_record_finding` for: exposed `.env`, `APP_DEBUG=true`, Telescope/Horizon accessible without auth, Ignition endpoints reachable, mass-assignment accepted, CSRF bypass on non-API routes, public storage/log exposure, and `composer.lock` disclosure.
2. Reference the Laravel security matrix.
3. Recommend: set `APP_DEBUG=false` and `APP_ENV=production`; regenerate `APP_KEY` if ever exposed; block `.env`, `composer.lock`, and storage/log access at the web-server level; disable Telescope, Horizon, Ignition, and Debugbar in production via environment checks; enforce `$fillable` on all Eloquent models or use `Model::preventAccessingMissingAttributes()` in Laravel 9+; set `SESSION_SECURE_COOKIE=true`, `SESSION_HTTPONLY=true`, and `SESSION_SAMESITE='lax'`; route API endpoints through token-based or OAuth authentication without CSRF middleware; and upgrade to a supported Laravel version.
