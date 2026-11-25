---
tags: [backend, availability, ttl, punctuate, processor]
name: availability-ttl-punctuate-processor
description: Kafka Streams processor schedules a wall-clock `punctuate` for TTL eviction of the state store, and emits downstream only on value change. Wall-clock (not stream-time) so idle inputs still trigger cleanup.
category: backend
version: 1.0.0
source_project: lucida-measurement
trigger: Kafka Streams state store accumulates stale entries; event-time TTL won't fire for decommissioned keys.
linked_knowledge:
  - latest-availability-deletion-risk
---

See `content.md`.
