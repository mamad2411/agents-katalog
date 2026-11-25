---
name: ha-api-access
description: |
  Access the Home Assistant REST API using environment variables HA_URL and HA_TOKEN
  exported in ~/.zshrc. Use when: (1) need to query Home Assistant entity states,
  (2) need to call HA services programmatically, (3) need to debug or inspect HA
  integration state, (4) user asks to interact with their Home Assistant instance.
  Covers authentication, common endpoints, and usage patterns.
author: Claude Code
version: 1.0.0
date: 2026-02-19
---

# Home Assistant API Access

## Problem
Need to interact with the user's Home Assistant instance from the CLI for debugging,
testing, or inspecting integration state.

## Context / Trigger Conditions
- User asks to check HA entity states or services
- Need to debug a custom integration by inspecting live state
- Want to call HA services or query the API
- User mentions "HA", "Home Assistant", or "home assistant" API access

## Prerequisites
Environment variables are exported in `~/.zshrc`:
- `HA_URL` — Base URL of the HA instance (e.g., `http://192.168.1.11:8123`)
- `HA_TOKEN` — Long-lived access token for authentication

## Solution

### Verify connection
```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/" | python3 -m json.tool
```

### Get all states
```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states" | python3 -m json.tool
```

### Get a specific entity state
```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states/<entity_id>" | python3 -m json.tool
```

### Call a service
```bash
curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" -H "Content-Type: application/json" \
  -d '{"entity_id": "<entity_id>"}' \
  "$HA_URL/api/services/<domain>/<service>" | python3 -m json.tool
```

### Get config
```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/config" | python3 -m json.tool
```

### Filter states (e.g., area_occupancy entities)
```bash
curl -s -H "Authorization: Bearer $HA_TOKEN" "$HA_URL/api/states" | \
  python3 -c "import json,sys; [print(json.dumps(e, indent=2)) for e in json.load(sys.stdin) if 'area_occupancy' in e['entity_id']]"
```

## Verification
A successful connection returns `{"message": "API running."}` with HTTP 200.

## Notes
- Always use `$HA_URL` and `$HA_TOKEN` env vars — never hardcode credentials
- The token is a long-lived access token created in HA UI under Profile > Security
- Pipe through `python3 -m json.tool` for readable output
- For large responses, pipe through `python3 -c` with filtering logic
- The HA REST API docs: https://developers.home-assistant.io/docs/api/rest/
