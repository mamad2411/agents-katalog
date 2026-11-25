---
name: proxy-mailbox-jsonl-pattern
description: Decouple a local agent from a remote hub by routing every interaction through a local HTTP proxy backed by an append-only JSONL mailbox. Agent only talks localhost; proxy handles auth, retries, background sync.
category: architecture
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [proxy, mailbox, jsonl, ipc, async, hub-sync]
source_type: extracted-from-git
source_url: https://github.com/EvoMap/evolver.git
source_ref: main
source_commit: 4c51382092f9cb125d3ec55475861ead8d1463a6
source_project: evolver
imported_at: 2026-04-18T02:45:00Z
---

# Proxy Mailbox (JSONL) Pattern

## When to use

- An agent/daemon needs to talk to a remote hub but you want no network latency on the hot path, no auth handling in the agent, and clean offline behavior.
- You need an audit trail of every outbound intent and every inbound event.
- Multiple local processes (or future multi-agent) need to share the same hub session.

## Shape

```
Agent --> Local HTTP Proxy (127.0.0.1) --> Remote Hub
              |
          Local Mailbox (messages.jsonl + state.json)
```

- Agent only writes/reads the local mailbox endpoints (`/mailbox/send`, `/mailbox/poll`, `/mailbox/ack`, `/mailbox/status/{id}`, `/mailbox/list`).
- Proxy is the single owner of hub credentials, heartbeat, retries, cursor state.
- Proxy address is published to disk (e.g. `~/.evolver/settings.json` with `{ url, pid, started_at }`) so any local process can discover it.

## Contract (minimum)

| Endpoint | Method | Purpose |
|---|---|---|
| `/mailbox/send` | POST `{type, payload}` | Enqueue outbound message; returns `{message_id, status:"pending"}` |
| `/mailbox/poll` | POST `{type?, channel?, limit}` | Drain inbound messages with optional filter |
| `/mailbox/ack` | POST `{message_ids:[]}` | Mark inbound as consumed |
| `/mailbox/status/{id}` | GET | Lifecycle state for a specific message |
| `/proxy/status` | GET | `{status, node_id, outbound_pending, inbound_pending, last_sync_at}` |

Send is always async: `pending -> synced -> ack'd`. Let the proxy own the transitions; agent only cares about `status` via poll.

## Why JSONL + in-memory index

- Append-only writes survive abrupt kills (no lock file, no partial row rewrite).
- Corrupt lines are skipped on load; intact lines remain readable.
- In-memory maps/lists (`id -> message`, ordered `outbound[]`, ordered `inbound[]`) reconstruct on boot via a single scan.
- Ordering is preserved by file order; cursors are stored in a sibling `state.json`.

## Message IDs

Use UUID v7 (RFC 9562): top 48 bits are `unix_ts_ms`, so IDs sort by time. This makes the JSONL naturally time-ordered and lets the poll filter be a simple forward scan.

## TODO (reader)

- Decide whether the proxy is system-wide or per-user; evolver picks per-user.
- Decide retry policy: exponential on `synced` failures, stay `pending` otherwise.
- Add a `pending_count` introspection endpoint for observability.
