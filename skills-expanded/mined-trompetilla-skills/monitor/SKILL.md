---
name: Monitor
description: Create flexible monitoring scripts with structured logs, alerts, and intelligent insights for any target.
metadata: {"clawdbot":{"emoji":"📡","os":["linux","darwin","win32"]}}
---

## Directory Structure

```
.monitors/
├── config.json          # Global settings (alert defaults, retention)
├── monitors/            # One script per monitor
│   ├── web-mysite.sh
│   ├── twitter-elonmusk.py
│   └── api-stripe-health.sh
├── logs/                # Structured logs per monitor
│   ├── web-mysite/
│   │   └── 2024-03.jsonl
│   └── twitter-elonmusk/
│       └── 2024-03.jsonl
└── alerts/              # Alert history
    └── 2024-03.jsonl
```

## Monitor Scripts

- Each monitor is a standalone script (bash, python, node) in `.monitors/monitors/`
- Script must exit 0 for success, non-zero for failure
- Script outputs JSON to stdout: `{"status": "ok|warn|fail", "value": any, "message": "human readable"}`
- Keep scripts simple and fast — they run on schedule, not continuously
- Name pattern: `{type}-{target}.{ext}` (e.g., `web-api-prod.sh`, `content-competitor-blog.py`)

## Log Format

- One JSONL file per monitor per month: `logs/{monitor-name}/YYYY-MM.jsonl`
- Entry: `{"ts": "ISO8601", "status": "ok|warn|fail", "value": ..., "latency_ms": N, "message": "..."}`
- Append-only — never modify past entries
- Retention: keep 12 months by default, configurable in config.json

## Creating Monitors

When user requests monitoring, create appropriate script:

**Web uptime**: curl with timeout, check status code
```bash
#!/bin/bash
START=$(date +%s%3N)
STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$URL")
LATENCY=$(($(date +%s%3N) - START))
if [ "$STATUS" = "200" ]; then
  echo "{\"status\":\"ok\",\"value\":$STATUS,\"latency_ms\":$LATENCY}"
else
  echo "{\"status\":\"fail\",\"value\":$STATUS,\"message\":\"HTTP $STATUS\"}"
  exit 1
fi
```

**Content changes**: hash page content, compare to last
**API health**: call endpoint, validate response schema
**Social media**: fetch latest posts, check for new content
**Custom metrics**: run any command, parse output

## Running Monitors

- Monitors run via cron or scheduled task — agent sets up schedule on user request
- Suggested intervals: critical (1m), important (5m), standard (15m), daily (24h)
- Runner script reads all monitors, executes each, appends to logs, triggers alerts
- Log runner output: `logs/runner.log` for debugging schedule issues

## Alert Configuration

Store in `config.json`:
```json
{
  "alerts": {
    "default": {"type": "log"},
    "channels": {
      "pushover": {"token": "...", "user": "..."},
      "agent": {"enabled": true},
      "webhook": {"url": "..."}
    }
  },
  "monitors": {
    "web-mysite": {"alert": ["pushover", "agent"], "interval": "5m"}
  }
}
```

Alert types:
- **log**: Write to alerts/YYYY-MM.jsonl only
- **agent**: Flag for agent to mention in next conversation
- **pushover/ntfy**: Push notification
- **webhook**: POST to URL
- **email**: Send via configured SMTP

## Alert Logic

- Alert on status change (ok→fail, fail→ok) — avoid spam on repeated failures
- Include consecutive failure count in alert
- Recovery alerts: "Monitor X back to OK after 3 failures (12 minutes)"
- Configurable thresholds: alert only after N consecutive failures

## Insights (Agent Analysis)

When user asks about monitoring:
- Parse recent logs, calculate uptime percentage
- Identify patterns: "Site slower on weekends", "API fails every Monday 9am"
- Suggest new monitors based on what user cares about
- Generate weekly summary if requested: uptime stats, incidents, trends

## Efficient Patterns

- Don't store full response bodies — only status, latency, relevant extracted values
- For content monitoring, store hash + diff summary, not full content
- Compress logs older than 30 days if storage is concern
- Index by status for quick "show all failures" queries
