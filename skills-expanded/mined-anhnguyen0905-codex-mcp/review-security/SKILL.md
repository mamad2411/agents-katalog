---
name: review-security
description: Security review checklist for Codex output — secrets, injection, validation, authz, and unsafe operations, with mandatory triggers.
---

# Security Review

## Mandatory triggers (never skip when the diff touches these)

Auth/session logic · user input handling · database queries · file system paths from input · external API calls · crypto · payments · anything reading env/config secrets · a non-code **deliverable** that could embed secrets, credentials, PII, or internal data that must not leave the workspace (check the content, not just code).

## Checklist

- **Secrets**: no hardcoded API keys/passwords/tokens in code or tests; secrets come from env/config; nothing secret in log output or error messages. Grep the diff for `key|token|secret|password` literals.
- **Injection**: SQL via parameterized queries only (no string concatenation); shell commands via arg arrays, never interpolated strings; HTML output escaped or sanitized (XSS); path traversal — user input never joined into file paths without normalization + allowlist.
- **Validation at trust boundaries**: every external input (HTTP body/params, file content, env, third-party API responses) validated before use; server-side validation present even when the client validates.
- **AuthN/AuthZ**: protected routes actually check permissions; object-level access control (user A can't fetch user B's resource by ID); no auth decisions from client-supplied fields.
- **Unsafe patterns**: `eval`/dynamic code execution, pickle/unsafe deserialization of external data, disabled TLS verification, permissive CORS (`*` with credentials), weak or home-rolled crypto.
- **Dependencies**: any dependency Codex added — check it's the package intended (typosquats), reasonably maintained, and actually needed.
- **Error leakage**: stack traces, internal paths, or query details never sent to end users.

## Severity default

A confirmed vulnerability in these categories is CRITICAL or HIGH — it blocks completion and goes back to Codex in the current round, never "noted for later".
