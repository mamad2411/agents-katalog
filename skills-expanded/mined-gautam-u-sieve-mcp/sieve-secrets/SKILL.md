---
name: sieve-secrets
description: Keep API keys and other secrets out of the agent's context on macOS using the local Sieve MCP server. Use when the user is about to paste a .env file, logs, config or a stack trace that may contain keys; when a command needs a credential; when the user asks whether keys leaked into past AI chats; or before sharing text with any external service. Requires the Sieve Mac app with MCP turned on.
---

# Sieve secrets

Sieve is a local macOS app. Its MCP server (`sieve`) checks and redacts secrets, lists secrets that
already leaked into AI chat history, and runs commands with secrets from the macOS Keychain. No tool
ever returns a secret value. Everything runs on the user's Mac.

## Rules

1. Never ask the user to paste an API key, token, password or `.env` value into the chat.
2. Never echo, log, summarise or write a secret value into a file, commit or message, even partially.
3. Treat text that already contains a secret as exposed. Tell the user to rotate that key at the
   provider. Redacting the copy does not make the key safe again.

## Check that Sieve is connected

Call `sieve_health_status`.

- It answers with `"status": "ok"`: continue.
- The tools are missing, or the call fails with `MCP_DISABLED`: tell the user to open Sieve, turn on
  **Settings → MCP Server → Enable MCP Server**, and add the server to this agent:
  `{"command": "/Applications/Sieve.app/Contents/MacOS/Sieve", "args": ["--mcp"]}`. Until then,
  follow the rules above and ask the user to set secrets as environment variables themselves.

## Before text leaves the machine

When the user shares logs, config, a diff or a stack trace, or you are about to send text to a web
service, issue tracker or another model:

1. Call `sieve_check_text` with the text. It returns only `has_secrets`.
2. If `has_secrets` is true, call `sieve_redact_text` with the text and a short `project_key`
   (for example the repository name). Use only the `redacted` text it returns from then on.
3. Tell the user which kinds of secret were found (the `ruleId` values), never the values, and that
   those keys should be rotated if the text was already shared.

Detection is pattern-based. A false result does not prove the text is clean, so still avoid
forwarding text that obviously contains credentials.

## When a command needs a secret

Do not ask for the value. Use `sieve_vault_run`:

- `command`: the program and arguments separated by spaces. There is no shell, so pipes,
  redirects, quotes and `$VARS` do not work.
- `fingerprints`: a JSON-encoded string mapping a Sieve fingerprint (`sfp:v1:...`) to the
  environment variable name the command expects, for example `"{\"sfp:v1:abc\": \"STRIPE_API_KEY\"}"`.

Fingerprints come from `sieve_findings_list` or from `sieve_redact_text` placeholders. The secret must
be stored in Sieve's vault (the user adds it in the app). The response contains the exit code and
line counts only, never output text, because output can contain the secret.

If `sieve_vault_run` is not available (Sieve's Codex configuration turns it off), give the user the
command to run themselves with the secret already set in their environment.

## When the user asks whether keys leaked into AI chats

1. Call `sieve_scan_status` and `sieve_scan_history` to see when Sieve last scanned. If it has never
   scanned, ask the user to run a scan in the Sieve app.
2. Call `sieve_findings_list`. Report counts by severity and source tool, and file paths. Previews
   are already redacted. Do not try to recover the values.
3. Call `sieve_issue_list`. Report every `SCAN_TARGET_UNREADABLE` issue, because those sources
   were not checked. Do not describe the result as clean while issues remain.
4. For each active critical or high finding, recommend rotating the key at the provider, then
   marking it rotated in Sieve.

## Limits

- macOS only.
- Sieve finds known key formats. Custom or internal credentials may not be detected.
- Findings are only as current as the last scan in the app.
