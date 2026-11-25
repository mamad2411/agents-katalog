---
name: websocket-patterns
description: Build real-time WebSocket/Socket.IO systems — auth at the handshake, rooms/namespaces, presence, reconnection, Redis pub/sub scaling. Use for bidirectional messaging, live updates, chat, or notifications.
license: MIT
metadata:
  author: https://github.com/Jeffallan
---

# WebSocket Patterns

You are building stateful, long-lived connections — a different discipline from request/response HTTP. Every decision (auth, scaling, cleanup) must account for connections that persist, drop, and reconnect.

## Core Workflow

1. **Analyze requirements** — connection scale, message volume, latency needs.
2. **Design architecture** — clustering, pub/sub, state management, failover.
3. **Implement** — WebSocket server with authentication, rooms, events.
4. **Validate locally** — test auth rejection, room join/leave, and delivery before scaling (e.g. `npx wscat -c ws://localhost:3000`).
5. **Scale** — verify the Redis pub/sub round-trip before enabling the adapter; configure sticky sessions and confirm across instances.
6. **Monitor** — connections, latency, throughput, error rates; alert on connection-count spikes.

## Invariants

- Sticky sessions for load balancing — WebSocket connections are stateful; requests must route to the same instance.
- Heartbeat/ping-pong to detect dead connections — TCP keepalive alone is insufficient.
- Rooms/namespaces for message scoping, never filtering in application logic.
- Queue messages during disconnection windows (silent data loss otherwise); jittered exponential backoff on reconnect.
- Connection state lives in Redis/external store, never only in instance memory; always clean up on disconnect (presence, room membership, timers).
- Load-test before production — connection-count spikes behave nothing like HTTP traffic spikes.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/implementation.md` — working Socket.IO server (auth middleware, rooms, presence, Redis adapter) and client (reconnection, backoff, message queue), plus the output template · read when writing server or client code.
- `references/protocol.md` — WebSocket handshake, frames, ping/pong, close codes · read when working at the raw protocol level.
- `references/scaling.md` — horizontal scaling, Redis pub/sub, sticky sessions · read when going multi-instance.
- `references/patterns.md` — rooms, namespaces, broadcasting, acknowledgments · read when designing message flows.
- `references/security.md` — authentication, authorization, rate limiting, CORS · read when securing endpoints (for offensive testing, see the sibling `websocket-security` skill).
- `references/alternatives.md` — SSE, long polling, when WebSockets are the wrong choice · read when validating the transport decision.
