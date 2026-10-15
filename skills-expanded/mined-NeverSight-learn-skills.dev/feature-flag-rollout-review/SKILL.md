---
name: feature-flag-rollout-review
description: Design and audit feature flags, staged rollouts, kill switches, targeting rules, exposure plans, holdouts, rollout gates, rollback paths, flag cleanup, and operational ownership for SaaS, apps, games, AI features, marketplaces, and desktop software. Use when releasing risky changes gradually or when a product needs safe experimentation, canaries, or emergency disablement.
---

# Feature Flag Rollout Review

Use this skill to convert a risky product, operations, trust, or marketplace question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify feature owner, risk class, user segments, dependencies, exposure unit, rollout channel, and rollback mechanism.
2. Read `references/feature-flag-rollout-patterns.md`.
3. Separate release flag, experiment flag, permission flag, ops kill switch, migration flag, and configuration flag.
4. Define targeting, metrics, guardrails, rollout gates, support/comms, and cleanup deadline.
5. Produce flag plan, rollout state machine, decision table, event schema, and cleanup checklist.

## Guardrails

- Do not use feature flags as permanent product architecture without ownership and cleanup.
- Do not target sensitive groups in ways that create unfairness, privacy risk, or unsupported claims.
- Do not roll forward after guardrails fail just because deploy checks are green.
- Every high-risk flag needs an owner, rollback path, monitoring, and support note.

## Output format

```text
Feature flag context:
Risk / owner / exposure unit:

Rollout plan:
| Stage | Audience | Gate metric | Guardrail | Decision | Owner |
| --- | --- | --- | --- | --- | --- |

Flag inventory:
- <flag> -> <type, default, dependencies, cleanup date>

Rollback and cleanup:
- <trigger> -> <disable/rollback/comms/remove>
```
