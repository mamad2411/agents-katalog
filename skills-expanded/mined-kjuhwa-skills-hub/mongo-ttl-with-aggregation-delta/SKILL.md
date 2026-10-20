---
tags: [backend, mongo, ttl, with, aggregation, delta]
name: mongo-ttl-with-aggregation-delta
description: Store short-lived counter snapshots in MongoDB with a TTL index for auto-expiry and compute delta-from-previous at read time via an aggregation $subtract pipeline.
category: backend
version: 1.0.0
source_project: lucida-health
trigger: You sample a monotonic counter (GC bytes, requests total) on an interval and need rate/delta without storing history forever.
---

See `content.md`.
