---
name: bridge-twin
description: Send messages to Hermes (Brian) via the JSONL bridge. Use when user says "tell Brian", "message Brian", "ask Brian", "send to Brian", "/twin", or wants inter-AI communication. Also handles reading messages from Hermes and testing bridge connectivity.
---

# Bridge Twin — Buck ↔ Hermes Communication

Send messages to Hermes (Brian) via the JSONL + webhook bridge.

## Architecture

- **Buck → Hermes:** Write JSONL to Hermes inbox + webhook push (primary) + SSH trigger (fallback)
- **Hermes → Buck:** Write JSONL to Buck inbox + webhook push → inotify watchdog + `openclaw cron wake`
- **HMAC Secret:** Stored in config — rotate regularly
- **Webhook endpoints:**
  - Buck receiver: `http://<buck-host>:8644/webhooks/bridge-push`
  - Hermes receiver: `http://<hermes-host>:8644/webhooks/bridge-push`
- **Health checks:** `http://<host>:8644/health`
- **Systemd service:** `bridge-webhook.service` (user unit, enabled)

## Quick Commands

### Send a message to Brian

```bash
python3 ~/.openclaw/workspace/scripts/bridge_write_hermes.py --type <TYPE> --payload '<JSON>'
```

Types: `command`, `query`, `response`, `event`, `ack`, `heartbeat`, `error`

Examples:
```bash
# Simple message
python3 ~/.openclaw/workspace/scripts/bridge_write_hermes.py --type query --payload '{"text": "Hey Brian - status check?"}'

# Response with correlation
python3 ~/.openclaw/workspace/scripts/bridge_write_hermes.py --type response --payload '{"text": "Got it!"}' --correlation_id abc123
```

This writes to inbox + pushes webhook + falls back to SSH trigger automatically.

### Read messages from Brian

```bash
python3 ~/.openclaw/workspace/scripts/bridge_read.py
```

Or inline:
```python
import json, subprocess
result = subprocess.run(["python3", "~/.openclaw/workspace/scripts/bridge_read.py", "--json"], capture_output=True, text=True)
messages = json.loads(result.stdout)
```

### Test connectivity

```bash
# Test push to Brian
python3 ~/.openclaw/workspace/scripts/bridge_push_hermes.py --test

# Test local webhook
curl -s http://<buck-host>:8644/health
curl -s http://<hermes-host>:8644/health
```

### Webhook receiver management

```bash
systemctl --user status bridge-webhook.service
systemctl --user restart bridge-webhook.service
```

## Message Format

All messages are JSONL with this structure:
```json
{
  "id": "uuid",
  "ts": "ISO-8601",
  "sender": "buck",
  "seq": 1234567890000,
  "type": "query|response|command|event|heartbeat|ack|error",
  "correlation_id": "optional-id",
  "ttl_seconds": 300,
  "payload": {"text": "message content"}
}
```

## Fallback Chain

Webhook push → SSH trigger → 5-min heartbeat (Hermes) / 30-min liveness cron (Buck)

If webhook returns 401, check HMAC secret rotation. If SSH fails, check your bridge SSH key config.