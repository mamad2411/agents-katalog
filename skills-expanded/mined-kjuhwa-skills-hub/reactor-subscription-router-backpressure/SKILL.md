---
tags: [backend, reactor, subscription, router, backpressure]
name: reactor-subscription-router-backpressure
description: Per-session, per-destination Reactor Flux router with bounded buffer + DROP_LATEST backpressure and automatic cleanup on session disconnect
trigger: Fanning high-volume upstream events (Kafka, MQTT) out to many WebSocket sessions, where slow clients must not back up the pipeline or OOM the server
category: backend
source_project: lucida-realtime
version: 1.0.0
---

# reactor-subscription-router-backpressure

See `content.md`.
