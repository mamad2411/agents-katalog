---
name: credentials
description: "Secret and credential lifecycle management via `credentials.*` tools. Use when listing, requesting, creating, rotating, or deleting integration credentials without exposing plaintext secrets."
triggers:
  - credentials
  - credential
  - secret
  - secrets
  - креды
  - секреты
tool_names:
  - credentials.list
  - credentials.request
  - credentials.create
  - credentials.update
  - credentials.delete
preferred_tool_order:
  - credentials.list
  - credentials.request
  - credentials.create
  - credentials.update
  - credentials.delete
requires_env:
  - AFKBOT_CREDENTIALS_MASTER_KEYS
---

# credentials

Manage secrets only via these tools:
- `credentials.request`
- `credentials.create`
- `credentials.update`
- `credentials.delete`
- `credentials.list`

Unified credentials model:
- `app_name` (integration id, e.g. `telegram`, `smtp`, `imap`, `http`)
- `profile_name` (credential profile key, e.g. `default`, `work`)
- `credential_slug` (credential key)
- `value` (secret payload for create/update)

Rules:
- Never output plaintext secret values.
- Never request secrets in normal chat text.
- `credentials.list` returns metadata only (no plaintext).
- Always start from `credentials.list` and reuse existing binding when possible.
- If missing, call `credentials.request` without `value` to return deterministic `credentials_missing` metadata for secure credential prompts.
- Prefer runtime-managed secure recovery over sending `value` through model-planned tool calls.
