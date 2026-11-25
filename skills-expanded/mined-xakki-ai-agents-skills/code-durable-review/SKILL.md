---
name: code-durable-review
description: 'Design or review durable jobs, leases, replay, recovery and ordered external effects. Use when an operation crosses persisted state, queues or scheduled execution. RU: очереди, повтор, восстановление.'
license: MIT
---

# Durable workflows

Use when an operation crosses persisted state, queues, leases, journals, recovery, scheduled execution or external effects. Establish the operation identity, authoritative store, intended state machine, ownership/fence and authorized scope before implementation or read-only review.

Treat `started`, `executed`, `terminal`, external effect and durable finalization as distinct outcomes. Validate exact identity, permitted transition and active ownership before mutation; persist related state atomically when the contract requires it. A lease alone does not make an external effect exactly once. An ambiguous timeout or expired lease is not proof that the external operation did not occur and does not authorize a replay.

Use [lease, replay and effects](references/lease-replay-effects.md), [mirrored-state and recovery](references/mirrored-state-recovery.md) and [independent acceptance](references/acceptance-and-diagnostics.md) as applicable. Apply the actual system's transaction, clock, retry and authorization contracts; test decisive race/failure paths with synthetic fixtures and sanctioned runners. Deployment, real external calls and operator reconciliation require their own authority.
