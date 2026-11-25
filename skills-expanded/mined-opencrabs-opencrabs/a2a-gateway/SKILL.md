---
name: a2a-gateway
description: "Agent-to-Agent (A2A) protocol gateway reference. JSON-RPC 2.0 peer-to-peer agent communication. (/a2a-gateway, a2a, agent protocol)"
---

# A2A Gateway Reference

OpenCrabs exposes an A2A Protocol HTTP gateway for peer-to-peer agent communication.

## What it does

Other A2A-compatible agents send tasks via JSON-RPC 2.0. OpenCrabs processes them using its full tool suite and returns results.

## Endpoints

- `GET /.well-known/agent.json` — Agent Card discovery (skills, capabilities)
- `POST /a2a/v1` — JSON-RPC 2.0 (`message/send`, `tasks/get`, `tasks/cancel`)
- `GET /a2a/health` — Health check

## Setup

Enable in `~/.opencrabs/config.toml`:

```toml
[a2a]
enabled = true
bind = "127.0.0.1"
port = 18790
```

## Bee Colony Debate

Multi-agent structured debate with knowledge-enriched context from QMD memory search. Configurable rounds, confidence-weighted consensus based on ReConcile (ACL 2024).

## Tool: a2a_send

| Param | Required | What |
|-------|----------|------|
| `action` | Yes | `discover`, `send`, `get`, `cancel` |
| `url` | Yes | Base URL of remote agent (e.g. http://127.0.0.1:18790) |
| `message` | For `send` | Text to send |
| `task_id` | For `get`/`cancel` | Task ID to check/cancel |
| `context_id` | Optional | Continue a conversation |
| `api_key` | Optional | Bearer token for authenticated endpoints |
