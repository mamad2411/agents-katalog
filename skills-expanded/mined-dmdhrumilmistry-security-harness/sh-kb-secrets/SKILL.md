---
name: sh-kb-secrets
description: "Knowledge base for finding hardcoded secrets and sensitive-data exposure - API keys, passwords, tokens, private keys, and connection strings embedded in source/config, or secrets leaked to logs/errors/URLs. Use when hunting secret exposure. CWE-798/259/312/532, OWASP A05/A02:2021."
---

# Hardcoded Secrets & Sensitive Exposure - Hunter Knowledge Base

Credentials embedded in code/config or leaked through logs, errors, or client-visible responses. High
value: a single leaked key can defeat every other control.

## What to hunt
- **Hardcoded credentials** (CWE-798/259): API keys, passwords, tokens, private keys, DB connection
  strings, cloud keys committed in source, config, Dockerfiles, CI files, or client bundles.
- **Secrets in client-shipped code**: keys in frontend JS/mobile apps (extractable by anyone).
- **Secrets to logs/errors** (CWE-532): logging tokens, passwords, PII, full request bodies; verbose stack
  traces returned to users; secrets in URLs (query strings get logged/cached/Referer-leaked).
- **Weak storage** (CWE-312): sensitive data stored plaintext at rest.

## Detection patterns (grep targets)
- Assignment patterns: `password\s*=`, `passwd`, `api[_-]?key`, `secret`, `token`, `access[_-]?key`,
  `client_secret`, `Authorization: Bearer <literal>`, `-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----`.
- High-entropy string literals assigned to those names (not `os.environ[...]`/`process.env.*`/vault calls).
- Provider prefixes: `AKIA` (AWS), `AIza` (Google), `ghp_`/`gho_` (GitHub), `sk-` / `sk_live_` (OpenAI/Stripe),
  `xox[baprs]-` (Slack), `-----BEGIN`.
- Connection strings: `mongodb://user:pass@`, `postgres://user:pass@`, `Data Source=...Password=`.
- Log/error sinks with secrets: `logger.*(... token/password ...)`, returning exception detail to clients.

## Detection recipe
1. `graft grep "(api|secret|access|private)[_-]?(key|token)|password|BEGIN [A-Z ]*PRIVATE KEY|AKIA|sk_live|xox[bp]-" --json`
   (and native Grep across config/CI/Docker/`.env` committed files).
2. Confirm the value is a real literal, not a placeholder (`changeme`, `xxx`, `example`) or an env lookup.
3. For client bundles, check what ships to the browser/app.
4. For logs/errors, trace whether secret/PII values reach log or client-facing error sinks.
5. If in git history, note it may still be exposed even if removed from HEAD (recommend rotation).

## PoC / evidence
- The literal at `file:line` (mask the value in the report: `AKIA****`). For a live key, the "PoC" is
  demonstrating it authenticates - describe rather than actually using third-party creds without authorization.
- For log leak: show the code path where the secret enters the log/response.

## False-positive filters
- Placeholders/examples/test fixtures/`*.example`; obviously fake values.
- Values loaded from env/secret managers/vault (`os.environ`, `process.env`, AWS Secrets Manager, Vault, KMS).
- Public/publishable keys meant to be client-side (Stripe publishable `pk_`, OAuth client_id, public certs).
- Non-secret high-entropy strings (UUIDs, hashes of public data) - confirm meaning before flagging.

## CWE / OWASP / severity
CWE-798/259 (hardcoded creds), CWE-312 (cleartext storage), CWE-532 (log exposure), CWE-522. OWASP
A05:2021 (Misconfiguration) / A02:2021 (Cryptographic Failures). Live production credential -> **critical**;
test/limited-scope or client publishable-by-design -> low/info.

## Chaining hints
A leaked key is often the *first* link: DB creds -> full data access; cloud key -> infra takeover; JWT
secret -> forge tokens (`auth`); pairs with `path-traversal`/`sqli` reads that surface config files.

## Mitigation
Remove secrets from code; load from env/secret manager/vault; rotate any exposed secret (and purge from
git history); never log secrets/PII (redact); return generic errors to clients; keep keys server-side;
add pre-commit secret scanning (gitleaks/trufflehog) to prevent recurrence.
