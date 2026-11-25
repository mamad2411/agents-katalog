---
tags: [backend, non, metric, saveraw, null, rule]
name: non-metric-saveraw-null-rule
description: Treat `saveRaw` as tri-state `Boolean` — `null` for non-METRIC types (Availability/Trait), `true`/`false` only for METRIC. Re-apply the rule on every policy mutation path.
category: backend
version: 1.0.0
source_project: lucida-measurement
trigger: Collection policy mixes METRIC and non-METRIC types; boolean `saveRaw` defaults silently overload semantics.
linked_knowledge:
  - policy-edit-saveraw-loss
---

See `content.md`.
