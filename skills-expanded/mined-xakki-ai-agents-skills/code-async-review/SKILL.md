---
name: code-async-review
description: 'Design or review deadlines, cancellation, ownership handoffs and asynchronous lifecycles with tests. Use when work crosses async boundaries or must stop cleanly. RU: асинхронность, отмена, завершение.'
license: MIT
---

# Concurrency lifecycle

Use when work, events or processes cross asynchronous boundaries, can outlive an owner, or must be bounded during shutdown. Identify the real production entrypoint, owner identity, child tasks/processes, cancellation semantics, deadline authority and expected terminal effects before changing or reviewing a flow.

Propagate one appropriate monotonic total deadline across retries, fallback and cleanup instead of resetting it at each phase. Classify total, per-attempt, idle and observation deadlines separately. Cancellation, logical revocation, durable settlement and physical termination are different events. An observation deadline is not permission to terminate, restart, discard state or repeat an ambiguous external effect.

For concrete rules, select [deadlines and cancellation](references/deadlines-and-cancellation.md), [ownership and event handoffs](references/ownership-and-events.md), or [subprocess supervision](references/subprocess-supervision.md). Test real coordination paths with deterministic barriers and bounded waits; preserve supported runtime and project policies. Keep independent read-only review distinct from implementation and report only measured evidence.

For asynchronous authenticated interactive state, read [auth state and async work](references/interactive-auth-state.md).
