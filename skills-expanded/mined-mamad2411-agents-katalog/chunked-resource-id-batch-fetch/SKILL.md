---
tags: [backend, chunked, resource, batch, fetch]
name: chunked-resource-id-batch-fetch
description: Split large ID lists into ~1000-item chunks before querying DB or Elasticsearch to avoid bind-parameter limits (MSSQL 2100, Oracle 1000) and OOM on bulk responses
version: 1.0.0
source_project: cygnus
source_ref: cygnus@cbb96a6dfff
category: backend
triggers:
  - `WHERE id IN (?, ?, …)` with thousands of IDs
  - ES `terms` query near 65536-item ceiling
  - monitor/report accepts an unbounded target ID list
---

# Chunked Resource ID Batch Fetch

See `content.md`.
