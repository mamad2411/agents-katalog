---
tags: [backend, multi, resource, batch, query]
name: multi-resource-or-batch-query
description: Collapse N per-resource Mongo queries into one pipeline using `Criteria.orOperator` (or `$in`) over resourceId, projecting a synthetic `key` field for service-side de-multiplexing. Chunk at ~200 for index-friendly `$or`.
category: backend
version: 1.0.0
source_project: lucida-measurement
trigger: Multi-line chart / tabular export would issue N Mongo round-trips for N resources; need single-pipeline batch.
---

See `content.md`.
