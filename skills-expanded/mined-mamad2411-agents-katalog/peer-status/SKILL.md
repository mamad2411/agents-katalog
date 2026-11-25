---
name: peer-status
description: "Query peer agent status and send cross-agent messages via Gateway. Use peer-status to check availability, peer-send to communicate."
---

# Peer Communication Skill

This skill provides two capabilities for inter-agent collaboration:

1. **peer-status** — Query online/busy status of peer agents
2. **peer-send** — Send messages to peer agents via WebSocket

## 1. Query Peer Status

Check which peers are available before initiating collaboration.

### Usage

```bash
node skills/peer-status/scripts/peer-status.mjs --agent-id <your-agent-id>
```

### Output

JSON array printed to stdout:

```json
[
  { "id": "novel-researcher", "name": "Novel Researcher", "status": "busy", "updatedAt": "2026-02-26T14:30:00.000Z" },
  { "id": "worldbuilder", "name": "Worldbuilder", "status": "online", "updatedAt": null }
]
```

**Status values:**
- `busy` — Agent has session activity within the last 5 minutes
- `online` — Agent is registered but not recently active

## 2. Send Cross-Agent Messages

Send a message to a peer agent and optionally wait for their reply.

### Usage

```bash
# Sync mode (default): wait for peer's reply
node skills/peer-status/scripts/peer-send.mjs --from <your-id> --to <peer-id> --message "your message"

# Async mode: send and exit immediately
node skills/peer-status/scripts/peer-send.mjs --from <your-id> --to <peer-id> --message "your message" --no-wait

# Custom timeout (default 120s)
node skills/peer-status/scripts/peer-send.mjs --from <your-id> --to <peer-id> --message "your message" --timeout 180
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--from`  | Yes | Your agent ID |
| `--to`    | Yes | Target peer agent ID (must be in your peers list) |
| `--message` | Yes | Message text to send |
| `--no-wait` | No | Don't wait for reply, exit after send confirmation |
| `--timeout` | No | Max wait time in seconds (default: 120) |

### Output

**Sync mode:** Peer's reply text is printed to stdout.

**Async mode:** JSON confirmation:
```json
{"ok":true,"sessionKey":"agent:peer-id:main","idempotencyKey":"..."}
```

### Peer Validation

The script validates that `--to` is in `--from`'s peers list (from `agent.json`). Attempting to message a non-peer agent will fail with exit code 1.

## Important Rules

- **DO NOT** use `sessions_send` to message other agents — it is blocked by visibility="agent"
- **DO NOT** use `sessions_list` to check peer status — use `peer-status` script instead
- **DO NOT** use `sessions_history` to read other agents' conversations — privacy violation
- Cross-agent messaging **MUST** go through `peer-send` script
- `sessions_send` is only for your own sub-sessions (spawned via `sessions_spawn`)
