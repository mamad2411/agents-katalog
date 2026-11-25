---
name: post-memory
description: Log a significant action to a personal activity feed. Optional skill — works only if you have ACTIVITY_FEED_URL configured. EXAMPLE.
---

# Post Memory (example)

> **EXAMPLE.** Demonstrates the optional-external-logging pattern. Original called Brad's Supabase; this version uses an env-gated POST URL so you can plug in any endpoint (Supabase, Airtable, your own API, plain webhook, etc.).

## When to invoke

Call from any skill after completing a meaningful action — heartbeat alert, deal updated, cron complete, etc. Logs to:

1. An external activity feed (HTTP POST) — IF `ACTIVITY_FEED_URL` env var is set
2. Today's local memory file (`memory/YYYY-MM-DD.md`)

If `ACTIVITY_FEED_URL` is not set, only writes to local memory and exits — no error.

## Procedure

### STEP 1 — POST to external activity feed (if configured)

```python
import os, urllib.request, json
url = os.environ.get("ACTIVITY_FEED_URL")
if url:
    token = os.environ.get("ACTIVITY_FEED_TOKEN", "")
    data = json.dumps({"action_type": "ACTION_TYPE", "description": "DESCRIPTION"}).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=10) as r:
        r.read()
```

Replace `ACTION_TYPE` and `DESCRIPTION` with the actual values. Common action types: `cron-fired`, `email-sent`, `deal-updated`, `meeting-prep-done`, `research-complete`.

### STEP 2 — Append to today's memory file

```
echo "$(date '+%H:%M') — ACTION_TYPE: DESCRIPTION" >> memory/$(date '+%Y-%m-%d').md
```

### STEP 3 — Done

No Telegram. This is silent logging.

## Setting up your activity feed

Pick any HTTP endpoint that accepts POST. Examples:

- **Supabase**: create a table, get the REST URL, set `ACTIVITY_FEED_URL=https://<project>.supabase.co/rest/v1/your_table`. Token = anon key.
- **Airtable**: use their REST API.
- **Zapier webhook**: free webhook URL, no token needed.
- **Your own service**: any URL that accepts JSON POST.

Add to `~/.zshenv` or wherever you store env vars:

```bash
export ACTIVITY_FEED_URL="https://your-endpoint.example.com/log"
export ACTIVITY_FEED_TOKEN="your-secret"
```
