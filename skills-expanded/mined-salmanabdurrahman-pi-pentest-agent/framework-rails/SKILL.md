---
name: framework-rails
description: Ruby on Rails security review — validate secrets.yml exposure, mass-assignment via strong-params bypass, ActiveRecord SQL injection vectors, YAML deserialization surface, debug-route and Sidekiq exposure, session-cookie tampering risk with docs-first read-only checks and no deserialization exploitation or credential testing.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Ruby on Rails security — configuration and surface review

Use this skill to review Ruby on Rails application security posture on authorized in-scope targets. Validate `secrets.yml` and credentials exposure, mass-assignment via strong-parameters bypass, ActiveRecord SQL injection through raw queries and `order()` injection, YAML deserialization surface, debug-route and `/rails/info` exposure, Sidekiq/LetterOpener/PgHero dashboard accessibility, and session-cookie configuration. All tests are read-only and low-rate. Never exploit YAML deserialization for RCE, brute-force `secret_key_base`, forge session cookies, attempt ActiveRecord SQL injection exploitation beyond detection, or test credential endpoints — those behaviors are prohibited unless separately approved for destructive validation.

## Required inputs

- Written scope covering the Rails application hosts, API routes, admin paths, Sidekiq and other dashboard paths, and allowed review methods. Explicit confirmation that YAML deserialization exploitation, secret_key_base brute-forcing, session forgery, SQL injection exploitation, and credential testing are prohibited unless separately approved.
- Rails version from: `Gemfile.lock` exposure, response headers (`X-Powered-By`, `X-Request-Id`, `Server`), error-page signatures, `/rails/info` output (if exposed), or local source code (if provided).
- Official Ruby on Rails documentation for the detected version — prefer guides.rubyonrails.org and api.rubyonrails.org.
- Valid authorization cache for the target application.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for read-only execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — version detection and environment identification

1. Detect Rails from response indicators: `X-Powered-By: Phusion Passenger` (common Rails deployment), `X-Request-Id` header (Rails generates UUIDs per request), `_rails_session` or `_session_id` cookie names, and CSRF `authenticity_token` hidden fields in forms.
2. Identify the Rails environment: development mode exposes `/rails/info`, debug routes, and detailed error pages. Production mode suppresses these and typically uses `RAILS_ENV=production`. Check for `RAILS_ENV` leakage in error messages or exposed environment variables.
3. Check for `/rails/info/properties` — this route lists Rails version, Ruby version, environment, database adapter, and middleware stack. Accessible only in development by default, but misconfigured production apps may expose it.
4. Check for `/rails/info/routes` — lists all application routes, including admin and internal endpoints. Exposure is a high information-disclosure finding.
5. Document version evidence. Rails versions receive security patches for the current major series and the previous one; EOL versions (below Rails 7.0 for standard support) should be flagged.

### Phase 2 — secrets, credentials, and config exposure

1. Probe for `secrets.yml` and `credentials.yml.enc` exposure: Rails 4.x/5.0 used `config/secrets.yml`, while Rails 5.2+ uses encrypted `config/credentials.yml.enc` decrypted by `config/master.key`. Probe `/config/secrets.yml`, `/config/credentials.yml.enc`, and `/.env` for exposure.
2. If `secrets.yml` is exposed, it contains the `secret_key_base` — the master key used to sign cookies, sessions, and CSRF tokens. Exposure means all sessions can be forged. Record as critical and do not store the raw content.
3. If `credentials.yml.enc` is exposed without the `master.key`, it cannot be decrypted directly, but its presence combined with an exposed `master.key` (check `/config/master.key`) is a critical finding.
4. Check for `database.yml` exposure at `/config/database.yml` — this file contains database credentials. Accessible only through path-traversal or misconfigured static-file serving.
5. Do not download exposed config files that contain real credentials. Record exposure paths and recommend immediate rotation.

### Phase 3 — mass-assignment via strong-parameters bypass

1. Identify user-registration and profile-update endpoints. Rails uses strong parameters (`params.require(:user).permit(:name, :email)`) to prevent mass-assignment in controllers. Test by submitting unpermitted attributes.
2. Test registration endpoints: add `admin`, `role`, `is_admin`, `verified`, `confirmed_at`, `approved`, or `subscription_type` fields to the user params. If Rails permits these attributes because `permit!` or `tap` was used incorrectly, mass-assignment is exploitable.
3. Test nested-attributes bypass: Rails `accepts_nested_attributes_for` allows updating associated records. Submit nested attributes for sensitive associations (`account_attributes[credit]`, `subscription_attributes[plan]`, `profile_attributes[verified]`).
4. Test for `permit!` misuse: some controllers use `params.require(:user).permit!` which permits all attributes — a dangerous pattern. The presence of unexpected writable attributes confirms `permit!` or missing `permit` call.
5. Do not set values that would lock out or damage real accounts. Use safe boolean flags.

### Phase 4 — ActiveRecord SQL injection detection

1. Identify search, sort, filter, and order-by parameters that may be passed to ActiveRecord queries. Rails protects against SQL injection in `where` conditions using parameterized queries by default, but raw SQL fragments (`where("name = '#{params[:name]}'")`) and `order()` with string interpolation are common injection vectors.
2. Test `order()` injection: if the application accepts `?sort=` or `?order=` parameters, submit SQL fragments like `id ASC`, `id DESC`, or column names. If the application reflects the sort order, the parameter may be passed directly to `order()` without whitelisting. Submit a timing-based probe like `id,(SELECT CASE WHEN (1=1) THEN pg_sleep(1) ELSE pg_sleep(0) END)` for PostgreSQL or `id,(SELECT SLEEP(1))` for MySQL.
3. Test raw `where()` fragments: submit `' OR '1'='1` in search parameters. If the query returns all records, a raw SQL fragment is being interpolated without sanitization.
4. Do not attempt UNION-based extraction, data exfiltration, or schema enumeration. Stop at detection and record the vector.

### Phase 5 — YAML deserialization and cookie security

1. Rails 4.x used YAML-serialized (later JSON) session cookies. The session cookie is base64-encoded and may be decodable. Decode the `_session_id` cookie (base64 → raw bytes) and inspect the structure. Rails 4.x with YAML serialization is vulnerable to YAML deserialization RCE if `secret_key_base` is known.
2. Check the session cookie format: Rails 5.1+ uses JSON serialization with HMAC signing as the default. The cookie format is `payload--signature`. Older YAML-based cookies are identifiable by the `---` YAML prefix after base64 decoding.
3. Check `secret_key_base` exposure in: error pages, environment variable output, `/rails/info/properties`, exposed `secrets.yml`, or client-side JavaScript. If `secret_key_base` is exposed, all sessions and signed cookies are forgeable.
4. Inspect cookie security attributes: `HttpOnly`, `Secure`, `SameSite`, and expiration. Rails sets `SameSite=Lax` by default from Rails 6.1. Check whether `session_store.rb` configures `secure: true`, `httponly: true`, and `same_site: :lax`.
5. Do not attempt YAML deserialization exploitation. Do not forge session cookies even if `secret_key_base` is discovered.

### Phase 6 — debug routes, dashboards, and admin tools

1. Probe for `/rails/info/routes` and `/rails/info/properties` — development-only routes that list application internals. If accessible in production, flag as high.
2. Probe for Sidekiq web UI at `/sidekiq` — the default Sidekiq dashboard shows queue statistics, job payloads, retry data, and scheduled jobs. It has no built-in authentication. If accessible, flag as high — job payloads may contain PII, credentials, or API tokens.
3. Probe for LetterOpener at `/letter_opener` — a development email preview tool that shows all emails sent by the application, including password-reset links, confirmation tokens, and invitation URLs. Critical finding if exposed.
4. Probe for PgHero at `/pghero` — a PostgreSQL performance dashboard that shows query statistics, slow queries, and database health. If accessible without authentication, it may expose table names, query patterns, and database configuration.
5. Probe for `/rails/mailers` — Rails mailer previews show email templates with sample data. In production this should be disabled.
6. Do not interact with dashboard UIs beyond confirming they are accessible. Record the URL and whether authentication is required.

## Decision points

- **Escalate on secrets.yml exposed**: `secret_key_base` disclosed → critical. All sessions, signed cookies, and CSRF tokens can be forged. Rotate immediately.
- **Escalate on master.key exposed alongside credentials.yml.enc**: complete credential decryption possible → critical.
- **Escalate on Sidekiq accessible without auth**: job payloads and retry data exposed → high; critical if payloads contain credentials or PII.
- **Escalate on LetterOpener exposed**: email preview includes password-reset tokens → critical.
- **Escalate on Rails info routes exposed in production**: full route map disclosed → high.
- **Escalate on YAML session serialization detected**: pre-5.1 default with known secret_key_base enables RCE → high.
- **Escalate on ActiveRecord SQL injection confirmed**: timing differential or record-dump observed → high; stop exploitation.
- **Escalate on mass-assignment accepted**: privilege-escalation fields persisted → high.
- **Downgrade on x-powered-by header present**: informative — defense-in-depth hardening.

## Prohibited behavior

- Exploiting YAML deserialization for RCE: no YAML payload generation, no `universal_rop_gadget`, no cookie manipulation beyond decoding.
- Brute-forcing `secret_key_base` values — record exposure, recommend rotation.
- Forging session cookies using a discovered `secret_key_base` — record exposure, do not sign forged cookies.
- Exploiting ActiveRecord SQL injection beyond detection: no UNION-based data extraction, no schema enumeration, no data modification.
- Testing credentials on login, password-reset, or registration flows.
- Accessing LetterOpener emails that contain real user tokens or password-reset links.
- Running directory brute-force or wordlist scans against the application.

## Stop conditions

- `secrets.yml` or `master.key` exposed → stop, critical finding, all secrets must be rotated.
- LetterOpener exposed with live tokens → stop, critical finding.
- Sidekiq accessible with credential-laden job payloads → stop, high finding.
- ActiveRecord SQL injection confirmed beyond simple boolean detection → stop, record finding, do not extract data.
- YAML session serialization confirmed with exposed `secret_key_base` → stop, critical finding.
- Mass-assignment allows privilege escalation → stop, record finding.
- Evidence contains secrets or PII → redact immediately and store only minimal proof refs.

## Evidence — Rails security matrix

For each target, record:

```text
Target: <URL> | Rails version: <detected | estimated>
Version evidence: <Gemfile.lock | /rails/info | response header | error page>

Secrets and config:
  secrets.yml exposed: <yes | no>
  credentials.yml.enc exposed: <yes | no>
  master.key exposed: <yes | no>
  database.yml exposed: <yes | no>
  secret_key_base in client-side: <yes — source | no>

Mass assignment:
  Registration unpermitted fields accepted: <yes — fields | no>
  Profile unpermitted fields accepted: <yes — fields | no>
  permit! misuse detected: <yes — endpoint | no>

SQL injection:
  order() injection vector: <yes — parameter | no>
  raw where() injection vector: <yes — parameter | no>
  Timing differential observed: <yes — query type | no>

Session and cookies:
  Session serialization format: <YAML | JSON | unknown>
  secret_key_base exposed: <yes — path | no>
  Session cookie HttpOnly: <yes | no>
  Session cookie Secure: <yes | no>
  Session cookie SameSite: <Lax | Strict | None>

Dashboard exposure:
  /rails/info accessible: <yes — routes | properties | no>
  Sidekiq accessible: <yes — /sidekiq without auth | requires auth | not found>
  LetterOpener accessible: <yes | not found>
  PgHero accessible: <yes — /pghero without auth | requires auth | not found>

Overall risk: <critical | high | medium | low>
```

Never store: `secret_key_base` values, `secrets.yml` contents, Sidekiq job payloads with credentials, LetterOpener token URLs, raw SQL injection output with database contents, or session cookie values.

## Report handoff

1. `pentest_agent_record_finding` for: exposed `secrets.yml`/`master.key`/`database.yml`, `secret_key_base` in client-side code, mass-assignment accepted, ActiveRecord SQL injection confirmed, YAML session serialization, missing cookie security flags, `/rails/info` exposure, Sidekiq without auth, LetterOpener exposed, and PgHero without auth.
2. Reference the Rails security matrix.
3. Recommend: use Rails encrypted credentials (`rails credentials:edit`) and never commit `master.key`; enforce strong parameters on all controllers — audit for `permit!` and raw `params` usage; whitelist `order()` and `sort` parameters against allowed column names; use JSON session serializer (`Rails.application.config.action_dispatch.cookies_serializer = :json`); set `secret_key_base` via `RAILS_MASTER_KEY` env variable, never in source; disable `/rails/info` routes in production (`config.access_public_info_routes = false` in Rails 7.1+); authenticate Sidekiq web UI (`require 'sidekiq/web'; authenticate :user do; mount Sidekiq::Web => '/sidekiq'; end`); remove LetterOpener and mailer previews from production Gemfile; and upgrade to a supported Rails version.
