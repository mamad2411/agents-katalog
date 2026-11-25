---
tags: [backend, websocket, stomp, channel, pool, config]
name: websocket-stomp-channel-pool-config
description: Spring WebSocket STOMP config with separate inbound/outbound task executors and raised transport buffer limits, sized for burst notification fan-out to many role-filtered subscribers.
trigger: STOMP endpoint fans out notifications to many subscribers (role-filtered); default shared channel pool stalls during burst broadcasts.
source_project: lucida-alarm
version: 1.0.0
category: backend
---

# WebSocket STOMP Channel Pool Config

## Shape

Override `WebSocketMessageBrokerConfigurer` to provide two independently-sized thread pools (inbound small, outbound larger) and bump transport buffer limits. Authenticate on CONNECT via a channel interceptor that stashes identity/role into session attributes for later routing.

## Steps

1. Implement `WebSocketMessageBrokerConfigurer`.
2. `configureClientInboundChannel` (CONNECT/SUBSCRIBE/DISCONNECT, lightweight):
   - `core=2, max=4, queue=50, keepAlive=30s`.
3. `configureClientOutboundChannel` (per-subscriber sends, heavy due to authorization filtering):
   - `core=4, max=8, queue=200, keepAlive=120s`.
4. `configureWebSocketTransport`:
   - `messageSizeLimit ≈ 10 MB`, `sendTimeLimit ≈ 1000 s`, `sendBufferSizeLimit ≈ 1.5 MB`.
5. Register a `StompChannelInterceptor` that validates JWT on `CONNECT`, extracts `orgId`, `loginId`, `roleIds`, and stores them in STOMP session attributes.
6. Track sessions via a `SessionTrackerConfig` bean for metrics and forced disconnect.
7. Use role/org-scoped destinations so broker filtering runs before fan-out work.

## Counter / Caveats

- Inbound pool can stay small — outbound is where fan-out cost lives. Don't "scale both the same".
- Raising `sendBufferSizeLimit` delays dropping slow clients — monitor and force-disconnect to protect the broker.
- External STOMP broker relay (RabbitMQ) has different tuning; these values target the simple in-memory broker.
- Without the interceptor attaching identity to the session, downstream filtering re-does JWT work on every message.
