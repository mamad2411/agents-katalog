---
tags: [backend, mongo, aggregation, filter, optimization]
name: mongo-aggregation-filter-optimization
description: Replace `$unwind`+`$match` on array sub-documents with inline `$filter` so array elements are pruned before any downstream stage — avoids N× document explosion.
category: backend
version: 1.0.0
source_project: lucida-measurement
trigger: MongoDB aggregation uses $unwind immediately followed by $match on the unwound field; pipeline cost grows with outer-doc count × array length.
linked_knowledge:
  - topn-unwind-match-to-filter
---

See `content.md`.
