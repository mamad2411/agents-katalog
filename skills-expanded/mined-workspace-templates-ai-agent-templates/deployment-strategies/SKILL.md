---
name: deployment-strategies
description: Picks blue-green, canary or rolling for a service from its risk and state, then writes the rollout, verification and rollback steps.
---

# Deployment strategies

Choose the strategy from the risk, then write down how to stop it.

## Steps

1. Gather facts: statelessness, traffic volume, database or message-format changes, how fast bad behavior shows in metrics, infrastructure available (Kubernetes, load balancer, feature flags).
2. Choose:
   - **Rolling**: stateless, backward-compatible change, cheap to repeat. Set `maxUnavailable` and `maxSurge` and require readiness before the next batch.
   - **Blue-green**: needs instant switch and instant revert, and you can afford two full environments. Warm the green side before the cutover.
   - **Canary**: risk is in real traffic. Send 1, 5, 25, then 100 percent, pausing at each step.
   - **Feature flag**: when code can ship dark and be enabled per cohort; separate deploy from release.
3. Handle data: use expand and contract. Release 1 adds the new column or format while old code still works; release 2 switches over; release 3 removes the old one. Never ship code that cannot run against the previous schema.
4. Define go and stop signals per step: error ratio, p95 latency, a business metric, with numbers and a minimum observation time.
5. Write the rollback: the exact command, the expected time, and what state it leaves. Test it in staging.
6. Output a runbook with the steps, owners and communication points.

## Rules

- Never plan a rollback that depends on a destructive migration.
- Do not execute the deploy; produce the plan.

## Report

Chosen strategy and why, step table with signals and thresholds, rollback command, and risks left.
