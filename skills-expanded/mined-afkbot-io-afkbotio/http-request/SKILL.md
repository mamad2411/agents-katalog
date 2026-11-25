---
name: http-request
description: "Outbound HTTP calls via `http.request` with secure credential reuse. Use when querying or mutating remote HTTP APIs from the agent."
---

# http-request

Use this skill for outbound HTTP API calls via `http.request`.

Tool methods:
- `http.request`
- `credentials.list`
- `credentials.request`
- `credentials.create`
- `credentials.update`

Input checklist:
1. `method` (GET/POST/PUT/PATCH/DELETE)
2. `url`
3. optional `headers`
4. optional `body`
5. optional `auth_credential_name` (for secure auth header)
6. optional `auth_header_name` (default `Authorization`)
7. optional `credential_profile_key` (defaults to `default`)

Credential policy:
- HTTP auth credentials use integration `http` in unified credentials model.
- Recommended sequence:
  1. discover available HTTP credentials with `credentials.list app_name=http`;
  2. if missing, call `credentials.request` (without `value`) to produce deterministic secure credential prompt metadata;
  3. let runtime collect the secure value and store it safely;
  4. reuse `${{CRED:http/profile/slug}}` or `${ENV_KEY}` placeholders in `http.request` params when needed;
  5. call `http.request` with `auth_credential_name=<slug>` or resolved placeholders.
- On `credentials_missing`, collect secret securely and retry.

Safety:
- Respect network allowlist policy.
- Never print plaintext secrets in chat output.
- Runtime routes the correct skill automatically; do not send `skill_name`.
