---
name: system-state-injection
description: Inject live system health into agent context at session open. Cron script checks integrations, disk, gateway status, active sessions — writes compact JSON. Agent reads it before answering any status question. Eliminates stale-recall failures where agents answer from memory instead of live state. Use when setting up always-current system awareness for an autonomous agent.
metadata:
  emoji: 🔬
  category: ops
  platform: macOS, Linux (OpenClaw)
---

# System State Injection

Solves: agents answering "is X working?" from stale memory instead of live state.

Pattern: **cron → JSON → agent reads at session open → always-current answers.**

## Architecture

```
┌─────────────┐  every 30min  ┌────────────────────┐
│  Cron job   │ ────────────▶ │ system_state.json  │
│  checks:    │               │  (compact JSON)    │
│  - gateway  │               └────────┬───────────┘
│  - disk     │                        │
│  - integs   │                        ▼
│  - sessions │               ┌────────────────────┐
└─────────────┘               │ Agent reads at     │
                              │ session open       │
                              │ → always-current   │
                              └────────────────────┘
```

## What It Checks (configurable)

| Check | Method | Output |
|---|---|---|
| Gateway status | `openclaw gateway status` | running / stopped |
| Disk space | `shutil.disk_usage` | GB free, % used |
| Active sessions | `openclaw status` | count |
| Custom integrations | HTTP health check or CLI probe | connected / error |

## Setup

### 1. Configure integrations

Edit `scripts/integrations.json`:

```json
{
  "integrations": [
    {"name": "WhatsApp", "check": "openclaw status | grep WhatsApp"},
    {"name": "Google Drive", "check": "test -f ~/.config/google/token.json && echo ok"},
    {"name": "Twitch Bot", "check": "pgrep -f chatbot.py && echo running || echo stopped"}
  ],
  "output_path": "~/agent-workspace/brain/system_state.json",
  "timezone_offset_hours": 5.5
}
```

### 2. Run manually

```bash
python3 scripts/update_state.py
cat ~/agent-workspace/brain/system_state.json
```

### 3. Cron (every 30 min)

```cron
*/30 * * * * /usr/bin/python3 /path/to/system-state-injection/scripts/update_state.py >> /tmp/state-injection.log 2>&1
```

### 4. Wire into your agent

Add to your agent's system prompt or AGENTS.md:

```
Before answering any question about integration/service/tool status:
read brain/system_state.json first. This is the authoritative source.
Never answer from assumption.
```

## Output Format

```json
{
  "generated": "2026-04-05T22:30:00+05:30",
  "gateway": {"status": "running", "uptime": "3d 14h"},
  "disk": {"free_gb": 142.3, "used_pct": 68},
  "sessions": {"active": 2},
  "integrations": {
    "WhatsApp": "linked",
    "Google Drive": "connected",
    "Twitch Bot": "running"
  }
}
```

## Scripts

- `scripts/update_state.py` — Main script. Runs all checks, writes JSON.
- `scripts/integrations.json` — Configuration for custom integration probes.

## Why This Matters

Without state injection, agents rely on memory for status answers. Memory is often hours or days stale. One cron job eliminates an entire class of wrong answers.

<!-- A·R·E·S 🛡️ | Mumbai | 2026-04-05 | github.com/rushindrasinha -->
