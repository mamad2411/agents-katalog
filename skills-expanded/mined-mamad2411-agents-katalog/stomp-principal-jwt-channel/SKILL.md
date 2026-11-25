---
tags: [backend, stomp, principal, jwt, channel]
name: stomp-principal-jwt-channel
description: STOMP ChannelInterceptor that validates a JWT on CONNECT and binds a multi-tenant Principal (orgId + userId + sessionId) for downstream routing
trigger: Multi-tenant real-time service where each WebSocket session must be scoped to one tenant, and downstream handlers need tenant context without re-parsing the token
category: backend
source_project: lucida-realtime
version: 1.0.0
---

# stomp-principal-jwt-channel

See `content.md`.
