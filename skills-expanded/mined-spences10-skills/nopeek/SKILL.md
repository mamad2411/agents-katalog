---
name: nopeek
description: "Secret-safe agent sessions via nopeek CLI. Use when user asks about secrets, .env loading, credential safety, or keeping API keys out of conversation context."
metadata:
  last_updated: "2026-04-25"
  verified_against: "current local skill refresh"
---

# nopeek — Secret Safety for Agent Sessions

Secure proxy between coding agents and your secrets. The agent knows key names, never key values. For choosing secret-safety tooling alongside recall, MCP, and database tools, use `ecosystem-guide`.

## Why

Agent tool output can be sent to model providers and retained outside your machine. If a CLI prints a token, that token may enter conversation context or logs. nopeek reduces that risk.

## Quick Start

All nopeek commands are safe inside agent sessions — they never output secret values, only key names.

### 1. Scan and migrate CLIs

```bash
pnpx nopeek init
```

Detects installed cloud CLIs (aws, hcloud, kubectl, etc.), checks their auth config, and migrates to profile-based auth where needed.

### 2. Load .env secrets

```bash
pnpx nopeek load .env
pnpx nopeek load .env --only DATABASE_URL,API_KEY
```

Injects values into the session via `CLAUDE_ENV_FILE` (when available) or outputs a source command. Only key names appear in output — never values.

### 3. Store arbitrary keys

```bash
pnpx nopeek set MY_API_KEY --from-env
pnpx nopeek set STRIPE_KEY --value "sk_live_..."
```

When installed in Claude Code, stored keys auto-load on each session via the SessionStart hook.

### 4. Verify

```bash
pnpx nopeek status
pnpx nopeek list
```

## What the hooks do

| Hook             | Event            | Purpose                                                 |
| ---------------- | ---------------- | ------------------------------------------------------- |
| session-load.sh  | SessionStart     | Loads stored keys + CLI profiles into `CLAUDE_ENV_FILE` |
| redact-output.sh | PreToolUse(Bash) | Wraps cloud CLI output through secret pattern redaction |

## Limitations

- **Redaction is best-effort.** Regex patterns catch known formats (AWS keys, bearer tokens, Stripe keys, private key headers, connection strings) but cannot catch every possible secret.
- **This is a safety net, not a guarantee.** The primary defense is loading secrets via `CLAUDE_ENV_FILE` so they never appear in output at all.
- **No PostToolUse output redaction in Claude Code.** The PreToolUse hook rewrites commands to filter output before the agent sees it.
- **Commands with pipes or redirections are not wrapped.** The redaction hook skips commands containing `|`, `>`, or `<` to avoid breaking complex command semantics.
- **Requires jq.** The redact hook will not fire without jq installed.
- **Waiting on anthropics/claude-code#39882** — PreApiCall/PostApiCall hooks would enable full payload redaction before data leaves your machine.

## Audit .env files

```bash
pnpx nopeek audit
```

Scans current directory for .env files containing secrets and checks .gitignore coverage.

## Troubleshooting

**Keys not loading on session start:**

- Check `pnpx nopeek status` — are keys stored?
- For Claude Code hook installs, verify the plugin is installed: `/plugin list`
- Try `/reload-plugins`

**Cloud CLI still showing secrets:**

- The redaction hook only fires for commands starting with known CLI names (aws, hcloud, kubectl, doctl, gcloud, az, terraform)
- Commands with pipes or redirections are skipped to avoid breaking semantics
- Run `pnpx nopeek load .env` to make secrets available as env vars, then use `$VAR_NAME` in commands
