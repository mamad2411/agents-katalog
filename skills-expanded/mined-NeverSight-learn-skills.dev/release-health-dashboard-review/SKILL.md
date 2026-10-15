---
name: release-health-dashboard-review
description: Design and audit release health dashboards, rollout gates, canary metrics, crash/error monitoring, support signals, store release status, desktop auto-update adoption, rollback triggers, and post-release review for apps, SaaS, games, web, and desktop software. Use when launching releases, patches, experiments, or staged rollouts that need operational confidence.
---

# Release Health Dashboard Review

Use this skill to turn a recurring product-operations problem into a concrete, reviewable artifact instead of generic advice.

## Workflow

1. Identify release type, audience, platform/channel, rollout mechanism, critical user journeys, and rollback capability.
2. Read `references/release-health-patterns.md`.
3. Define leading and lagging health signals across reliability, conversion, payments, support, reviews, and adoption.
4. Set gates for preflight, canary/staged rollout, expansion, hold, rollback, and post-release learning.
5. Produce dashboard spec, alert thresholds, owner rotation, and release decision table.

## Guardrails

- Do not rely on green deploy/build status as user health proof.
- Do not average away platform, version, region, plan, or device-specific regressions.
- Every rollback trigger needs an owner, communication path, and recovery check.
- Use store review and auto-update constraints when release rollback is not instant.

## Output format

```text
Release context:
Platform / rollout / rollback capability:

Dashboard spec:
| Signal | Baseline | Threshold | Segment | Owner | Action |
| --- | --- | --- | --- | --- | --- |

Gate decision table:
- <gate> -> <ship/hold/expand/rollback condition>

Post-release review:
- <learning, follow-up, docs/support update>
```
