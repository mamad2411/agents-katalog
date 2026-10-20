---
name: leeway-runtime-durability
description: Governs durable runtime behavior across state ownership, persistence, retries, idempotency, ordering, deduplication, checkpoints, backup, restore, and disaster recovery. Use for workflows, queues, agents, databases, and long-running jobs.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  source-class: normalized-drive-candidate
---

# LeeWay Runtime Durability

Define the state machine, durable boundary, delivery semantics, idempotency keys, retry budget, poison-message path, ordering needs, reconciliation, retention, backup, restore, and recovery objectives. Test crash and replay behavior. Process success without durable-state verification is not completion.
