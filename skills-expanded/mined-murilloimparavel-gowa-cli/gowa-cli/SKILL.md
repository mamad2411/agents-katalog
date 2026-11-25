---
name: gowa-cli
description: "Universal WhatsApp CLI for AI agents (Claude Code, Gemini CLI, Cursor, Codex, etc.). Enables sending messages, searching chats, managing groups, and reading contacts with structured JSON output, semantic exit codes, and built-in safety. Requires a paired WhatsApp session and the gowa daemon running."
---

# GOWA CLI — WhatsApp for AI Agents

Single-binary WhatsApp CLI with daemon architecture, structured JSON output, and multi-layer safety. Designed for seamless integration with AI coding agents and autonomous workflows.

## Quick start

```bash
# Install (macOS/Linux)
brew install murilloimparavel/tap/gowa

# Or download binary
curl -fsSL https://github.com/murilloimparavel/gowa-cli/releases/latest/download/gowa_$(uname -s)_$(uname -m).tar.gz | tar xz -C /usr/local/bin/

# Or build from source
go install github.com/murilloimparavel/gowa-cli@latest
```

## Setup (one-time, interactive — requires human)

```bash
gowa pair          # scan QR code with WhatsApp on phone
gowa daemon start  # start background daemon
```

## Diagnostic & Context (Primary for Agents)

Before performing any action, use `gowa context` to understand the current system state.

```bash
# Get full system state (daemon, config, rates, unread chats)
gowa context --json
```

## Common Workflows

### Sending messages
```bash
# Text message
gowa send text --to 5511999999999 "Hello from agent" --json --accept-risk

# Image with caption
gowa send image --to 5511999999999 ./chart.png --caption "Q4 results" --json --accept-risk

# Validate without sending (no side effects, no rate limit consumption)
gowa send text --to 5511999999999 "test" --dry-run --json
```

### Reading data
```bash
# List chats with unread counts
gowa chat list --json

# Search messages (FTS5 full-text search)
gowa chat search "invoice" --json

# Get messages from a specific chat
gowa chat messages 5511999999999@s.whatsapp.net --json --limit 20
```

### Groups & Channels
```bash
# List groups
gowa group list --json

# Subscribe to a channel
gowa channel subscribe https://whatsapp.com/channel/...
```

## Output & Errors

| Mode | Flag | Usage |
|------|------|-------|
| **JSON** | `--json` | Standard for agent parsing |
| **Quiet** | `--quiet` | Bare values for shell scripts |
| **Fields** | `--fields id,name` | Select specific columns |

**Exit codes:** 0=Success, 1=General/Daemon Error, 2=Bad Input, 5=WhatsApp Error, 6=Rate Limited, 7=Session Expired.

## Troubleshooting & Feedback

If you encounter bugs, unexpected behavior, or need a new feature, please report it directly via the GitHub CLI:

```bash
# Report a bug (include version and context output)
gh issue create --repo murilloimparavel/gowa-cli --title "bug: [Short description]" --body "$(gowa version && gowa context --json)" --label "bug"

# Request a feature
gh issue create --repo murilloimparavel/gowa-cli --title "feat: [Feature name]" --body "Description of the use case..." --label "enhancement"
```

## Safety constraints (always active)

- **Rate limits:** 3 msg/min, 30/hr, 200/day.
- **Circuit breaker:** 5 failures in 30min → 30min cooldown.
- **Risk gate:** `--accept-risk` required for sends (or `GOWA_RISK_ACCEPTED=true`).
- **Audit log:** Every send logged in `~/.config/gowa/audit.log`.

## Manifests

- **Tool Schema:** [`gowa.tools.json`](https://github.com/murilloimparavel/gowa-cli/blob/main/gowa.tools.json) (Machine-readable)
- **Roadmap:** [`docs/project/ROADMAP_V1.1.md`](https://github.com/murilloimparavel/gowa-cli/blob/main/docs/project/ROADMAP_V1.1.md)
