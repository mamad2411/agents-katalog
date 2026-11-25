---
tags: [backend, cache, variance, ttl, jitter]
name: cache-variance-ttl-jitter
description: Add ±N% random jitter to cache TTLs so keys written together don't all expire in the same tick, avoiding synchronized recompute storms
trigger: In-memory or distributed cache where many entries are populated together (batch load, cold start, scheduled refresh) and simultaneous expiry causes a thundering herd
category: backend
source_project: lucida-realtime
version: 1.0.0
---

# cache-variance-ttl-jitter

See `content.md`.
