---
name: realtime-systems-engineer
description: "WebSocket, SSE, WebTransport, reconnect, backpressure, Redis pub/sub, fan-out, presence, horizontal scaling, graceful shutdown. Use when building or debugging realtime systems."
---

# Realtime Systems Engineer

## Overview

Design and implement production-grade realtime communication layers: transport selection, connection lifecycle, delivery guarantees, horizontal scaling, and observability. Realtime systems fail in ways that are invisible until they hit production — silent disconnects, message loss under load, thundering-herd reconnects, and fan-out amplification that melts Redis. Every decision made without understanding the failure modes will surface at 3 AM.

**Core principle:** CHOOSE THE DUMBEST TRANSPORT THAT MEETS YOUR DELIVERY REQUIREMENTS, then make it bulletproof.

## The Iron Law

```
NEVER SHIP A PERSISTENT CONNECTION WITHOUT RECONNECT, HEARTBEAT, AND BACKPRESSURE
```

## When to Use

**Use this when:**
- Implementing WebSocket servers, SSE endpoints, or long-poll handlers
- Designing presence, rooms, chat, live dashboards, or collaborative editing
- Adding horizontal scaling to an existing realtime service
- Debugging dropped messages, silent disconnects, or fan-out latency spikes

**Use this ESPECIALLY when:**
- Someone says "just use Socket.IO, it handles all that" (it does not)
- The feature is "just a live counter" (fan-out to 100k connections is not just anything)
- You are adding authentication to an existing WebSocket server
- The service needs to survive a rolling deploy without dropping active connections

**Don't skip when:**
- Under time pressure — missing reconnect logic means your users silently stop receiving updates
- The client is a mobile app — lossy networks make connection hygiene 10x more important

## Workflow

Work through these areas in order. Each must be resolved before writing production code.

**Transport Selection.** Pick WebSocket, SSE, Long-poll, or WebTransport based on direction and use-case. Prefer SSE when clients only consume events — one HTTP/2 connection, automatic browser reconnect, no custom framing. See [REFERENCE.md](REFERENCE.md) for the full transport comparison table.

**Connection Lifecycle.** Every connection must implement handshake validation, heartbeat, and reconnect with resume. Authentication MUST happen in the `upgrade` handler — a connected but unauthenticated socket is an open vulnerability. See [REFERENCE.md](REFERENCE.md) for the WebSocket heartbeat server and HTTP upgrade auth hook code.

**Reconnect with Exponential Backoff and Resume.** Clients must reconnect automatically with jitter to prevent thundering-herd after a server restart. Store `lastEventId` in `localStorage` for cross-tab resume; the server replays from a short-lived ring buffer. See [REFERENCE.md](REFERENCE.md) for the `ReconnectingSocket` implementation.

**Message Delivery Guarantees.** Define at-most-once, at-least-once, or exactly-once before implementation — the wrong default causes silent data loss. At-least-once requires UUID-tagged messages, client acks, and a server-side retry queue with TTL expiry. See [REFERENCE.md](REFERENCE.md) for the delivery guarantee comparison table.

**Backpressure and Flow Control.** A slow client must never block a fast producer. Bound the send buffer; drop the oldest non-critical messages (e.g., presence) before critical ones (e.g., order fills) when the queue is full. See [REFERENCE.md](REFERENCE.md) for the `safeSend` pattern and per-connection queue strategy.

**Horizontal Scaling with Redis Pub/Sub.** Stateless WebSocket servers behind a load balancer require a shared message bus. Redis pub/sub handles < 100k concurrent connections; evaluate NATS or Kafka above that. Prefer stateless fan-out over sticky sessions — sticky sessions break silently on instance failure. See [REFERENCE.md](REFERENCE.md) for the Redis pub/sub broadcast and `joinRoom` implementation.

**Graceful Shutdown and Drain.** Rolling deploys must not force-close active connections. Stop accepting new connections, send close code 1012 to all clients, wait up to 30 s for drain, then clean up pub/sub. Clients receiving 1012 should reconnect immediately with no backoff. See [REFERENCE.md](REFERENCE.md) for the `SIGTERM` drain handler.

**Observability.** Standard HTTP metrics do not capture realtime health. Instrument active connections, message throughput, reconnect rate, heartbeat evictions, send buffer depth, and fan-out latency. See [REFERENCE.md](REFERENCE.md) for the full metrics and structured-log spec.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "We'll add reconnect logic later" — silent disconnects are invisible to users and to you
- "Redis pub/sub can handle any scale" — it cannot; benchmark your fan-out at target concurrency first
- "Authentication can go after the handshake" — this creates an unauthenticated socket window
- "We don't need heartbeats, TCP keepalive is enough" — TCP keepalive does not detect application-layer zombies
- "At-most-once is fine, it's just UI state" — it will not be fine when the UI silently drifts from server state
- No backpressure limit on the send buffer

**ALL of these mean: STOP. Return to the relevant section in [REFERENCE.md](REFERENCE.md).**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Socket.IO handles reconnect automatically" | Socket.IO reconnect does not resume missed messages; you still need a replay buffer. |
| "We only have 1000 users, no need for Redis" | A single deploy event creates a thundering reconnect herd even at 1000 connections. |
| "Heartbeats waste bandwidth" | A 46-byte ping every 30 seconds is cheaper than debugging ghost connections at 2 AM. |
| "Sticky sessions are simpler than pub/sub" | Sticky sessions break silently on instance failure and uneven pod restarts. |
| "We'll add observability after launch" | You cannot diagnose a 10% message-drop rate you cannot measure. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Users are complaining the feed stops updating" — you have no reconnect or heartbeat
- "We're seeing duplicate messages" — at-least-once delivery without idempotency keys
- "The new deploy dropped everyone" — no graceful shutdown drain
- "It works on my machine but not under load" — no backpressure, fan-out untested at scale
- "Why is Redis CPU at 100%?" — fan-out is linear per subscriber; you need channel batching or a broker

**When you see these:** STOP. Return to the relevant section in [REFERENCE.md](REFERENCE.md).

## Related Skills

- **backend-senior-engineer** — API design, database patterns, and service architecture that sit beneath the realtime layer
- **distributed-systems-architect** — consistency models, partition tolerance, and broker selection at scale
- **performance-engineer** — profiling fan-out hot paths, benchmarking Redis pub/sub throughput, and load-testing socket servers
- **observability-pro** — metric instrumentation, alerting on reconnect rate and buffer depth, and distributed tracing across async message paths

## Verification

- [ ] Transport choice is documented with explicit rationale
- [ ] WebSocket server implements ping/pong heartbeat with zombie termination
- [ ] Authentication happens in the `upgrade` handler, not post-handshake
- [ ] Client reconnect uses exponential backoff with jitter
- [ ] Reconnect stores and sends `lastEventId` for resume
- [ ] Message delivery guarantee is explicit (at-most / at-least / exactly once)
- [ ] At-least-once messages have idempotency keys and a server-side ack queue
- [ ] Send buffer depth is bounded; slow clients are disconnected or backpressured
- [ ] Fan-out uses Redis pub/sub (or equivalent broker) — no in-process broadcast across instances
- [ ] Graceful shutdown sends close code 1012 and drains before process exit
- [ ] Active connections, reconnect rate, and fan-out latency are instrumented
- [ ] Load test confirms behavior at 2x expected peak concurrent connections
