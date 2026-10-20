---
name: feature-flag-lifecycle
description: "Implement and retire a feature flag safely after the rollout mechanism has been chosen. Use when wiring a flag into request, client or worker code, making subject assignment sticky, choosing safe behaviour when configuration is unavailable or stale, exercising a kill switch, proving the off path, or deleting a flag without breaking older deployed clients. Specify owner and removal condition at creation, test on/off and failure states including side effects, and verify mixed-version compatibility before cleanup. A flag off stops future execution; it cannot reverse charges, sent messages, deleted data or schema changes. For deciding rings, percentages, bake times and promotion guardrails use release-strategy; for schema expand/contract use db-migration. Not for selecting a flag vendor."
allowed-tools: "Read, Grep, Glob"
---

# Feature Flag Lifecycle

Implement the off path as a working product state, not an exception handler. A switch is useful only if its effective state and propagation are known under failure.

## Workflow

1. Record flag type, owner, removal ticket/date or durable review cadence, subject identity, default, storage authority and propagation bound. Separate a release flag from an enduring operational kill switch. For percentages use stable subject-based cohorts (and an explicit missing-subject policy), not per-request random assignment. Keep authorization checks independent of the flag.
2. Define behaviour for missing, unreachable and stale configuration and verify actual platform cache/TTL and evaluation semantics. Choose a safe, explicit fallback for each failure mode; never assume the last cached value is indefinitely safe. Ensure a kill switch remains reachable when the dependency it guards fails; document on-call owner and time to effective off.
3. Implement and test both branches under current and older deployed clients/workers. Exercise on, off, missing config, stale config, mixed-version traffic and overlapping flag combinations. Test an off flip under load and measure propagation; the bound only stops new evaluations from seeing on, so confirm no new work is admitted after it. Work admitted before the flip (an in-flight request, a queued job) can still reach its side effect later: where off must also stop that, cancel or drain it, or re-check the flag immediately before the side effect. Off does not undo irreversible effects already committed: give charges, messages and destructive writes separate idempotency or compensation plans.
4. Hand ring design, percentages, promotion and rollback thresholds to `release-strategy`. Before deletion inventory old client binaries, queued jobs, workers and external readers; prove none requires the old value or off branch, or keep a compatible response. Remove evaluation and dead branch only after this evidence, then delete config and update on-call documentation; re-test the surviving path.

## Output

Write a lifecycle record with owner, subject key, fallback matrix, on/off and failure test evidence, kill-switch propagation time, irreversible-effects boundary, older-version inventory, removal gate and cleanup result. Hold if the off path or compatibility cannot be verified.

## Anti-patterns

**Deleting after 100% rollout.** An offline mobile client or queued worker can still require the old path long after the server reached 100%.
