---
name: websocket-realtime
description: "Build realtime features with WebSockets and SSE: connection lifecycle, fan-out and rooms, backpressure, reconnection and horizontal scaling."
type: procedural
category: development
domain: development
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - websocket scaling design
  - sse vs websocket
  - realtime fanout rooms
  - websocket reconnection strategy
  - socket backpressure
keywords:
  - websocket
  - sse
  - realtime
  - fanout
  - rooms
  - backpressure
source: custom
enabled: true
---

# WebSocket and SSE Realtime

## Purpose

Build realtime features with WebSockets and SSE: connection lifecycle, fan-out and rooms, backpressure, reconnection and horizontal scaling.

## When to Use

- Users must see updates without polling.
- Many clients need the same event stream with per-room filtering.
- Connections must survive deploys and network changes.

## When NOT to Use

- Updates are infrequent enough that polling is simpler and cheaper.
- The client only needs server-to-client text (SSE may be enough).
- The platform's load balancer cannot keep long-lived connections.

## Capabilities

- Choose WebSockets versus SSE on requirement, not fashion.
- Manage connection lifecycle with heartbeats and resumable ids.
- Fan out through a shared pub/sub layer so instances stay stateless.
- Apply backpressure and cap per-connection buffers.

## Inputs

- The expected concurrent connections and message rate.
- The load balancer's idle timeout and keepalive settings.
- The consistency requirement: ordered per room or best effort.

## Workflow

1. Confirm the transport against client and infrastructure constraints.
2. Design the message envelope: type, id, payload, and resume cursor.
3. Publish events to a shared bus so any instance can serve any client.
4. Add heartbeats, reconnect with backoff jitter, and resubscribe from a cursor.
5. Load-test connection churn and message fan-out before launch.

## Tools

- ws / Socket.IO / native EventSource
- Redis pub/sub or NATS
- load balancer with sticky/idle config

## Examples

- `allskills route "add live updates to the dashboard"`
- `websocat wss://realtime.example/stream`
- `curl -N https://api.example/events`

## Safety

- Unbounded per-connection queues let a slow client exhaust server memory.
- Authorize each subscription; room names are not security boundaries.
- Long-lived connections must be drained before deploys terminate instances.

## Source

All-Skills canonical library (`skills/development/websocket-realtime`). First-party skill, maintained in this repository.

## Notes

- SSE reconnects natively and works over plain HTTP; use it when only downstream is needed.
- A cursor-based resume makes reconnects lossless.
- Pairs with: `networking/load-balancing`, `development/svelte-development`.
