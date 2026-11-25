---
tags: [backend, measurement, grouping, combiner]
name: measurement-grouping-combiner
description: Group rows by `(resourceId, metricId, bucketTs)` into `Map<K, List<T>>`, then a per-granularity pure `combine…ByKey` merges each list into one composite record. One combiner per granularity (raw/1m/5m/hour/day).
category: backend
version: 1.0.0
source_project: lucida-measurement
trigger: Multiple contributing rows per key must merge into one record across several granularities that differ only in merged fields.
---

See `content.md`.
