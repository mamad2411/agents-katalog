---
tags: [backend, mongo, timestamp, densification]
name: mongo-timestamp-densification
description: Fill sparse time-series gaps with `$dateTrunc` + `$densify` in Mongo, then a residual Java gap-fill loop for LIVE windows. Partition by series to keep multi-line charts aligned.
category: backend
version: 1.0.0
source_project: lucida-measurement
trigger: Sparse time-series returns missing buckets; chart needs continuous x-axis with per-interval points.
---

See `content.md`.
