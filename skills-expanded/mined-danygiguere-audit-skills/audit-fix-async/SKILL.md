---
name: audit-fix-async
description: Remediation patterns for correctness findings. Use after a confirmed atomicity, idempotency, or background-work issue — transactions, idempotency keys, outbox.
---

Read `../audit/references/remediation/async-patterns.md` and apply its patterns to fix the
confirmed findings the user referenced. Make the smallest change that restores
the invariant, and keep style consistent with the surrounding code.
