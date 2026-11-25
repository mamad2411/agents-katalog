---
tags: [backend, audit, change, data, capture, pattern]
name: audit-change-data-capture-pattern
description: Compute before/after diffs for audit logs by comparing two BSON/JSON documents field-by-field — always iterate the BEFORE doc and read from AFTER to avoid prev/after swap bugs
category: backend
version: 1.0.0
source_project: lucida-audit
trigger: Recording audit trail entries where UPDATE events need field-level before/after snapshots
linked_knowledge:
  - audit-changed-prev-after-field-swap-bug
---

See `content.md`.
