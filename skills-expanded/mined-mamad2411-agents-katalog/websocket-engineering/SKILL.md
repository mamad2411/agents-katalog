---
name: websocket-engineering
description: Engineer WebSocket features. Use when building realtime bidirectional channels.
metadata:
  tags: websocket, engineering
---

# WebSocket Engineering

## Use this skill when
- Designing message protocols
- Scaling connections and heartbeats
- Handling reconnects and backoffs

## Do not use this skill when
- Periodic polling where SSE suffices
- One-shot requests

## Instructions
1. Define message shapes, types, and error envelopes.
2. Use heartbeats/pings to detect dead connections.
3. Handle partial and binary framing (reassembly) at protocol level.
4. Write idempotent consumers and re-sync state on connect.
5. Backoff reconnects with jitter; cap attempts.
6. Scale with sticky sessions or a pub/sub backend.
7. Secure with auth handshake and message-rate limits.
8. Close cleanly and free server resources on disconnect.

## Checklist
- Heartbeats present
- Reconnect resyncs state
- Auth + rate limits

## Output Format
- Protocol | lifecycle | scaling | reconnect policy

## Common Mistakes
- Reloading lost messages
- No heartbeat detection
- Unbounded connections
