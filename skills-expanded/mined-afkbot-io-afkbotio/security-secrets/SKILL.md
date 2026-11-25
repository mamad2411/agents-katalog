---
name: security-secrets
description: "Mandatory secret-handling policy skill. Use on every task involving credentials, API tokens, passwords, or other secrets and rely only on `request_secure_field` plus `credentials.*` tools."
---

# security-secrets

Always handle secrets through secure credential prompts and credentials tools.

Strict rules:
- Never ask users to paste plaintext secrets into normal chat.
- Never output plaintext secrets into logs, tool payloads, or assistant messages.
- Use only:
  - `credentials.request`
  - `credentials.create`
  - `credentials.update`
  - `credentials.delete`
  - `credentials.list`

For app integrations (`app.run`):
- always call `credentials.list` first and reuse existing binding if found;
- if runtime returns `credentials_missing` or `credential_binding_conflict`, switch to secure collection flow;
- let runtime collect the secure value instead of sending the secret in a tool payload;
- retry `app.run` after secure value is persisted.
