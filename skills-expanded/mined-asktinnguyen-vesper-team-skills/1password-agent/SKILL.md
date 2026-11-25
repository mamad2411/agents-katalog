---
name: 1password-agent
description: Read and write secrets from the 1Password Vesper vault using a Service Account. No TouchID, no biometrics, no tmux — just op read/write with OP_SERVICE_ACCOUNT_TOKEN.
---

# 1Password Agent Access

Vesper agents have autonomous access to secrets via a dedicated **1Password Service Account** and **Vesper vault**. This eliminates TouchID/biometric prompts entirely.

**This skill replaces the interactive 1Password CLI workflow (tmux + `op signin`) for agent use.** The global `1password` skill is for human-interactive sessions. This skill is for autonomous agent runs.

## Architecture

```
┌──────────────────────────────────────────┐
│  1Password Account: my.1password.com     │
│                                          │
│  ┌─────────────┐   ┌─────────────────┐   │
│  │  Personal    │   │  Vesper         │   │
│  │  (user only) │   │  (agent vault)  │   │
│  │              │   │                 │   │
│  │  - All user  │   │  - Agent-only   │   │
│  │    secrets   │   │    credentials  │   │
│  │  - Requires  │   │  - No biometric │   │
│  │    TouchID   │   │  - Read via     │   │
│  │              │   │    service acct │   │
│  └─────────────┘   └─────────────────┘   │
│                            ▲              │
│                            │              │
│         OP_SERVICE_ACCOUNT_TOKEN          │
│         (read-only, 90-day expiry)        │
└──────────────────────────────────────────┘
```

## Setup Summary

Already configured. Do NOT reconfigure — just use.

| Component | Value |
|-----------|-------|
| Service Account | `<SERVICE_ACCOUNT_NAME>` |
| Access | **Read-only** to Vesper vault |
| Token expiry | 90 days (rotate when expired) |
| Token location | `OP_SERVICE_ACCOUNT_TOKEN` in local shell environment (do not commit) |
| Vault | **Vesper** |
| Account | my.1password.com |

## Reading Secrets

Use `op read` with the `op://Vesper/` URI scheme:

```bash
op read "op://Vesper/<Item Name>/<Field Name>"
```

**Examples:**

```bash
# Generic credentials
op read "op://Vesper/<SERVICE_ITEM>/username"
op read "op://Vesper/<SERVICE_ITEM>/password"

# Or set env vars and keep docs generic
op read "op://${SEESAW_OP_VAULT}/${SEESAW_OP_ITEM}/username"
op read "op://${SEESAW_OP_VAULT}/${SEESAW_OP_ITEM}/password"
```

**No flags needed.** Unlike `op item get`, `op read` does not need `--reveal`, `--vault`, or `--fields` flags. The URI contains everything.

## Current Vault Contents

Avoid publishing real item names in shared/public docs. Keep a private local inventory instead.

| Item | Category | Fields |
|------|----------|--------|
| **<SERVICE_ITEM_A>** | Login | `username` (STRING), `password` (CONCEALED) |
| **<SERVICE_ITEM_B>** | Login | `username` (STRING), `password` (CONCEALED) |

**Keep sensitive item naming in local-only notes, not in git-tracked docs.**

## Adding New Credentials

When the user asks to store new credentials for agent access, write them to the Vesper vault:

### Create a new login item

```bash
op item create \
  --category login \
  --title "<Service Name>" \
  --vault "Vesper" \
  "username=<username>" \
  "password=<password>"
```

### Create with additional fields

```bash
op item create \
  --category login \
  --title "<Service Name>" \
  --vault "Vesper" \
  --url "<service-url>" \
  "username=<username>" \
  "password=<password>" \
  "API Key[password]=<api-key>"
```

### Add a field to an existing item

```bash
op item edit "<Item Name>" --vault "Vesper" \
  "New Field[password]=<value>"
```

### Store an API key (non-login)

```bash
op item create \
  --category "API Credential" \
  --title "<Service Name> API" \
  --vault "Vesper" \
  "credential=<api-key>"
```

After creating or editing, verify the agent can read it:

```bash
op read "op://Vesper/<Item Name>/<Field Name>"
```

Then update the **Current Vault Contents** table in this skill file.

## Important Notes

### op read vs op item get

| | `op read` (use this) | `op item get` (avoid) |
|-|----------------------|-----------------------|
| Auth | Service account token | Desktop app + biometric |
| Syntax | `op read "op://Vault/Item/Field"` | `op item get "Item" --vault "V" --fields "F" --reveal` |
| Concealed fields | Returns value directly | Needs `--reveal` flag or returns help text |
| Agent-friendly | Yes | No — prompts for TouchID |

### Security guardrails

- **Never log or print secrets** in output visible to the user
- **Never commit secrets** to git or write them to non-1Password storage
- **Prefer `op read` inline** in scripts over storing in variables when possible
- The service account has **read-only** access — it cannot delete items or modify the vault structure
- To add/edit items, use `op item create` / `op item edit` which go through the desktop app (requires the user's 1Password to be unlocked)

### Token rotation

The service account token expires every 90 days. If `op read` starts failing with auth errors:

1. Go to: https://my.1password.com → Developer → Service Accounts
2. Generate a new token for the relevant service account
3. Update `OP_SERVICE_ACCOUNT_TOKEN` in your local shell environment
4. Reload your shell or restart terminal

### Relationship to global 1Password skill

The global `1password` skill (at `/Users/tinnguyen/openclaw/skills/1password/`) documents the **interactive** CLI workflow using tmux sessions and desktop app biometric prompts. That workflow is for human-driven sessions.

**This skill** documents the **autonomous** agent workflow using the service account. Use this skill for:
- Scheduled tasks (cron, heartbeat)
- Autonomous agent runs
- Any context where TouchID prompts would block execution

Use the global skill only when interactive biometric auth is acceptable.
