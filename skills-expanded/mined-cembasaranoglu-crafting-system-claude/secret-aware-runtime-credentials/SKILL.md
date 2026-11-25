---
name: secret-aware-runtime-credentials
description: Classify and handle secrets, credentials, runtime config, env vars, CI secrets, Kubernetes secret references, and redaction without exposing real secret values.
---
# Secret-Aware Runtime Credentials

Use when the user request involves credentials, database URLs, API keys, tokens, certificates, `.env`, cloud credentials, CI secrets, Kubernetes secrets, secret managers, or runtime configuration.

Load or follow `prompt-system/prompts/158_secret_and_runtime_credentials.md`.

Required behavior:

1. Classify secret context before work.
2. Do not ask for real secret values.
3. Do not repeat or transform real-looking secrets.
4. Use env var names, placeholders, fake local values, and secret references.
5. Require approval for integration execution with preconfigured runtime secrets.
6. Block `.env` reads, secret printing, and credential-bearing artifacts.
7. Produce `secret_handling_report`.

Task scope:

```text
$ARGUMENTS
```
