---
name: vuln-sensitive-exposure
description: Sensitive data and information disclosure validation — detect credentials in API responses, secrets in client-side JavaScript, exposed debug endpoints, Git repository exposure, cloud storage misconfiguration, and PII leakage in error messages. Redact everything before storing.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Sensitive exposure — secrets, PII, and information disclosure validation

Use this skill to detect inadvertently exposed sensitive data on an authorized, in-scope target. Search for credentials (API keys, tokens, passwords), PII (email addresses, SSNs, credit-card numbers), debug information (stack traces, environment variables, server paths), and misconfigured cloud storage (public S3 buckets, GCP storage, Azure Blob). Focus on confirming exposure and classifying severity — never download, aggregate, or store exposed data beyond what is needed for a redacted finding.

## Required inputs

- Written scope naming the target, authorized surfaces for sensitive-data inspection (API responses, client-side JavaScript, debug endpoints, cloud storage buckets, error pages, configuration files), and explicit permission to assess exposed data.
- Valid authorization cache. This is safe-active: we look at data the application voluntarily serves. But the data itself may be sensitive — redact before storing.
- Known technology stack from recon — helps prioritize which debug endpoints and configuration patterns to check (Spring Boot Actuator, Laravel debug mode, Django debug toolbar, Express error handler, S3 bucket naming conventions).
- Explicit acknowledgment that sensitive-exposure testing may incidentally encounter PII, credentials, or internal documentation. The assessor must stop and redact immediately when sensitive data is found.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools (trufflehog, gitleaks, S3 browser) are used.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` with redaction mandatory → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — API response inspection

Inspect API responses for sensitive fields returned to the client:

1. List all discovered API endpoints from recon and enumeration.
2. For each endpoint returning JSON or XML, inspect the response body.
3. Look for field names suggesting secrets: `password`, `secret`, `key`, `token`, `apikey`, `api_key`, `access_token`, `client_secret`, `private_key`, `hash`, `ssn`, `credit_card`, `dob`, `bank_account`, `pin`, `security_answer`.
4. Look for field values matching patterns: JWT `eyJ...` tokens, AWS key patterns (`AKIA...`), Stripe keys (`sk_live_...`), GitHub tokens (`ghp_...`), database connection strings (`jdbc:`, `mongodb://`), SMTP credentials.
5. If a field name suggests a secret and the value is not obviously redacted → sensitive data exposure confirmed. Stop inspecting that endpoint — do not enumerate all exposed records.
6. Record: endpoint, field name, value type (not the value itself), and whether authentication was required to access the response.

### Phase 2 — client-side secret scanning

Client-side JavaScript often embeds API keys, tokens, and internal URLs:

1. Extract all JavaScript file URLs from the target's HTML pages.
2. For each JS file, fetch the content and search for secret patterns.
3. Use pattern matching (never store the raw JS files if they contain secrets): `apiKey:`, `secret:`, `token:`, `authorization:`, `Bearer`, `AKIA`, `sk-`, `ghp_`, `xoxb-`, `ya29.`, `eyJ`, `-----BEGIN`, `client_secret`, `firebaseConfig`.
4. If a secret is found in client-side code → confirmed sensitive exposure in client bundle. Record the pattern type and the JS file URL — never store the secret value.
5. Check source maps (`.js.map`) availability: source maps can expose original source code with comments, TODOs, and hardcoded credentials.

### Phase 3 — debug and admin endpoint discovery

Check for exposed debug, admin, and infrastructure endpoints:

```text
High-priority endpoints:
/.env, /.env.local, /.env.production, /.env.development
/.git/HEAD, /.git/config
/debug, /debug/vars, /debug/pprof, /_debug
/actuator, /actuator/env, /actuator/health, /actuator/beans, /actuator/mappings
/phpinfo.php, /info.php, /server-status, /server-info
/api/swagger.json, /api/openapi.json, /openapi.yaml, /v3/api-docs
/graphql, /graphiql, /__graphql
/metrics, /prometheus, /stats, /_health, /_status
/package.json, /composer.json, /requirements.txt, /Gemfile.lock
/robots.txt, /sitemap.xml
/backup.sql, /backup.zip, /database.sql, /dump.sql
/wp-config.php.bak, /config.php~, /.htaccess.bak
```

Test procedure:
1. Send a GET request to each endpoint.
2. If the response is not 404 and contains technical data → information disclosure confirmed.
3. For Spring Boot Actuator `/actuator/env`: this can expose environment variables containing database passwords, API keys, and cloud credentials. If accessible → critical finding.
4. For `/.git/HEAD`: if accessible and contains `ref: refs/heads/` → Git repository exposed. Do not dump the repository — document the exposure.
5. For backup files: if a database dump or configuration backup is accessible → critical. Do not download the full file — note the URL, file size, and whether authentication was required.

### Phase 4 — cloud storage misconfiguration

Check for publicly accessible cloud storage buckets:

```text
AWS S3 naming patterns:
https://<target>.s3.amazonaws.com/
https://s3.amazonaws.com/<target>/
https://<target>-dev.s3.amazonaws.com/
https://<target>-staging.s3.amazonaws.com/
https://<target>-backup.s3.amazonaws.com/

GCP Storage:
https://storage.googleapis.com/<target>/
https://<target>.storage.googleapis.com/

Azure Blob:
https://<target>.blob.core.windows.net/
```

Test procedure:
1. Send a GET request to each bucket URL.
2. If the response contains `ListBucketResult` (S3) or a list of objects → bucket is publicly listable. Critical finding.
3. Do not enumerate all objects in the bucket. Note the bucket name and accessibility status.
4. If the bucket is not listable but objects are accessible (e.g., you can guess a known object key) → document the difference between listable and accessible.

### Phase 5 — error-message credential leakage

Trigger error conditions to check for credentials in error responses:

1. Send malformed requests: SQL injection probes (`'`, `"`), type errors (string where number expected), missing parameters, invalid JSON.
2. Inspect error responses for: database connection strings (`jdbc:mysql://`, `mongodb://`), stack traces with file paths (`/var/www/`, `/home/`, `C:\inetpub\`), environment variable values, API endpoint URLs with credentials, debug SQL queries with table/column names.
3. If an error response contains credentials or sensitive paths → information disclosure confirmed. Record the error trigger and the type of exposed data — never store the credential value.

## Decision points

- **Stop at first confirmed secret in each category**: one API response with a password field, one JS file with an API key, one exposed .git directory — each is a separate finding. Do not continue searching the same category after confirmation.
- **Spring Boot Actuator `/env` without authentication is critical**: this exposes all environment variables. Report immediately.
- **Public S3 bucket listing is critical**: if a bucket is listable, assume all objects are accessible. Document the bucket name and stop.
- **Git repository exposure is high severity**: `.git/HEAD` accessible means source code, configuration, and possibly credentials are exposed. Document without dumping.
- **Not all debug endpoints are vulnerabilities**: `/actuator/health` returning `{"status":"UP"}` is normal. Only flag endpoints that return configuration, environment variables, secrets, or sensitive paths.

## Prohibited behavior

- Downloading or storing exposed credentials, API keys, tokens, PII, or database dumps. Redact before storing any evidence.
- Using discovered credentials to authenticate to external services (AWS console, GitHub, APIs).
- Enumerating all objects in exposed S3 buckets beyond confirming accessibility.
- Dumping exposed Git repositories, database backups, or configuration files. Note their existence and stop.
- Testing cloud storage buckets that clearly belong to third parties (CDN, analytics, external services).
- Probing error conditions at high volume — rate-limit requests to avoid triggering alerts.

## Stop conditions

- API response contains a field named `password`, `secret`, `key`, or `token` with a non-redacted value → sensitive data in API response confirmed, stop that endpoint.
- Client-side JS contains an API key or secret pattern → secret in client code confirmed, stop scanning that JS file.
- Spring Boot Actuator `/env` accessible without authentication → critical, stop and report immediately.
- Public S3 bucket listable or `.git/HEAD` accessible → critical, stop and report.
- Error response contains database credentials or environment variables → information disclosure confirmed, stop triggering errors on that endpoint.
- All surfaces checked and no exposure found → negative result, document.

## Evidence — redaction requirements

All evidence must be redacted before storage. Replace:
- API keys: `sk_live_XXXX` → `sk_live_REDACTED`
- Tokens: `eyJ...` → `eyJ_REDACTED`
- Passwords: any value in a `password` field → `[REDACTED]`
- Database URLs: `jdbc:mysql://user:pass@host/db` → `jdbc:mysql://REDACTED@host/db`
- PII: email addresses → `user@REDACTED`, SSN → `XXX-XX-REDACTED`
- File paths: `/home/user/project` → `/home/REDACTED/project` (redact username only)
- AWS account IDs: `123456789012` → `REDACTED_ACCOUNT`

For each finding, record the exposure type (API field, JS secret, debug endpoint, cloud bucket, error-message leak), the endpoint or location, whether authentication was required, and the data classification (credential, PII, infrastructure detail, source code). Never store the actual secret.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with exposure type, location, redacted evidence, CVSS estimate (5.0–6.5 for debug endpoint exposure, 7.0–8.5 for credential leakage, 8.0–9.5 for public cloud storage or Git repository with secrets), and remediation guidance.
2. Reference the redacted evidence log.
3. Recommend: audit API response serialization to exclude sensitive fields, remove secrets from client-side code (use server-side API proxy), disable debug endpoints in production or require authentication, use `.gitignore`-based deployment (never deploy `.git/`), configure cloud storage with block-public-access enabled and bucket policies, suppress detailed error messages in production, and run secret-scanning tools (trufflehog, gitleaks) in CI.
