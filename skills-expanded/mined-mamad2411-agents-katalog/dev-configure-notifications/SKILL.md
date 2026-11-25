---
name: dev-configure-notifications
description: Set up Telegram, Discord, or Slack webhooks for engineering layer alerts — long-running task completion, build failures, security audit alerts.
---

# Dev Configure Notifications

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Configure outbound notifications for engineering layer events: long-running task completion, build failures, critical security findings, etc.

## Use When
- You want to be notified when `dev-autopilot` finishes (it can take minutes)
- You want CI / build failure alerts in Telegram or Discord
- You want `@vault-security` to ping you on CRITICAL findings

## Channels Supported
- **Telegram** — via the existing EvoNexus `int-telegram` integration
- **Discord** — via webhook URL
- **Slack** — via webhook URL

## Workflow

### Step 1 — Pick the trigger
Common triggers:
- `dev-autopilot` completion
- `@vault-security` CRITICAL finding
- `@oath-verifier` FAIL verdict
- `@hawk-debugger` 3-failure circuit breaker

### Step 2 — Pick the channel
- Telegram (uses existing bot via `int-telegram`)
- Discord (needs webhook URL)
- Slack (needs webhook URL)

### Step 3 — Configure
Save webhook config to `.claude/settings.json` or env vars:

```json
{
  "engineeringLayer": {
    "notifications": {
      "telegram": {
        "enabled": true,
        "chatId": "${USER_TELEGRAM_CHAT_ID}",
        "triggers": ["autopilot.complete", "vault.critical", "oath.fail"]
      },
      "discord": {
        "enabled": false
      }
    }
  }
}
```

### Step 4 — Test
Send a test notification via the configured channel. Verify it arrives.

### Step 5 — Document
Save config notes to `workspace/development/research/[C]notifications-config-{date}.md`.

## Output Format

Notification message format:
```
🤖 [EvoNexus Eng] {agent} {event}
{summary}

📁 {path to artifact}
```

## Pairs With
- `int-telegram` (for Telegram delivery)
- `dev-autopilot` (most common notification source)
- `@vault-security` (CRITICAL finding alerts)
- `update-config` (built-in skill for settings edits)
