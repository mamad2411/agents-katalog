---
name: opsecforge
description: Use when a task touches secrets or credentials - reading .env, key or config files, checking changes before a commit, sharing logs, debugging a webhook signature, or inspecting a JWT. Chooses the right local OpsecForge tool so raw secrets stay out of the model context.
---

# OpsecForge: keep secrets out of the context

The OpsecForge MCP tools run on this machine. They take a file path or an environment variable NAME, do the work locally, and return redacted or derived results. Prefer them over reading the raw value yourself.

In this plugin the tools are named `mcp__plugin_opsecforge_opsecforge__<tool>`.

## Pick the tool

| Situation | Tool | How |
| --- | --- | --- |
| You need to see a `.env`, `*.pem`/`*.key`, `credentials`, config or log file | `redact_file` | `{"path": "<file>"}`. Returns the text with secrets replaced by `[REDACTED]` plus a findings summary. |
| You only need to know which variables exist | Read `.env.example` / `.env.sample` / `.env.template` | These are allowed; the guard blocks the real `.env*`. |
| About to commit or open a PR | `scan_secrets` | `{"staged": true}` for the staged diff, or `{"paths": ["src", "config"]}`. Lists file:line, type and a masked preview. |
| You must paste text into an issue, ticket, chat or commit message | `redact_text` | `{"text": "..."}`. Be aware the text was already in your context; this only makes a safe copy to share outward. |
| "Signature mismatch" on a GitHub, Stripe or HMAC webhook | `verify_webhook` | `{"provider": "github", "body_path": "<raw body file>", "secret_env": "MY_WEBHOOK_SECRET", "signature": "<header value>"}`. The secret is read from the named environment variable only. |
| The user gives you a JWT to inspect | `inspect_jwt` | Prefer `{"token_env": "MY_TOKEN"}`. Decoding is not verification; say so when reporting. |
| Verify a download or artifact | `file_checksum` | `{"path": "<file>", "algorithm": "sha256", "expected": "<hex>"}` |

## Rules

- Never ask the user to paste a secret into the chat, and never pass a secret value as a tool parameter. There is no parameter for one; use `secret_env` / `token_env` with the variable NAME.
- If the guard hook blocks a Read, Grep or Bash command on a secret file, do not look for a way around it. Use `redact_file`.
- Do not copy secret values from any tool output into commits, issues, logs or generated files. If a file needs a secret, reference an environment variable.
- Redaction is heuristic and can miss custom formats. A clean result from `redact_file`, `redact_text` or `scan_secrets` is not proof that nothing sensitive is present; say so rather than promising safety.
- `verify_webhook` needs the RAW request body saved byte-for-byte. Re-serialized or pretty-printed JSON, or a trailing newline added by an editor, will not match; the tool reports when it recognises that.
- The guard is best effort. It cannot see what scripts read or what `grep -r` walks into, so keep following these rules even when no hook fires.

More: https://www.opsecforge.com
