---
name: do-release-checklist
version: 1.0.0
description: Build a production release checklist covering pre-flight gates, canary ramp, pre-declared rollback triggers, and stakeholder comms.
author: matrixx0070
tags: [release, deployment, canary, rollback, devops, comms]
capabilities: []
---

# do-release-checklist

## When to use

You are shipping to production and want a repeatable checklist that reduces risk, or you are formalizing an ad-hoc deploy into canary + rollback + communication steps.

**Not for:** the incident response after something breaks (use do-incident-runbook), the CI that produces the artifact (use do-ci-pipeline), or infra changes (use do-terraform).

## Method

1. Pre-flight: confirm CI is green on the exact commit, migrations are backward-compatible, feature flags default safe, config/secrets are in place, and on-call is aware.
2. Choose a progressive strategy. Decision: canary when you can route a fraction of traffic; blue/green when you need instant full cutover and rollback. Define the exposure ramp (1% -> 10% -> 50% -> 100%) with a bake time per step.
3. Pre-declare rollback triggers before you start: the metrics (error rate, latency, SLO burn), their thresholds, and who has authority to call the abort. Decision: any threshold breach at any step aborts — do not renegotiate mid-rollout.
4. Make rollback one action: keep the previous artifact hot, script the revert, and rehearse that migrations and flags roll back cleanly.
5. Communicate: announce start/steps/completion in the agreed channel, note the change window, and record what shipped and the deploy ID.
6. Post-release: watch dashboards through the bake, verify key user journeys, and close with a short release note.

## Example

```yaml
release: checkout v2.4.0 (commit a1b2c3d, deploy-id 2026-07-11-01)
preflight:
  - ci_green_on_commit: a1b2c3d
  - migration_backward_compatible: true
  - flags_default_safe: true
ramp:            # bake + gate at each step
  - { traffic: 1%,   bake: 10m }
  - { traffic: 10%,  bake: 15m }
  - { traffic: 50%,  bake: 15m }
  - { traffic: 100%, bake: 30m }
rollback_triggers:            # any breach -> abort
  - error_rate: "> 1%"
  - p99_latency: "> 400ms"
  authority: on-call lead
rollback_cmd: kubectl rollout undo deploy/checkout
```

## Pitfalls

- Deciding rollback thresholds mid-incident under pressure — you rationalize a bad rollout instead of aborting.
- A non-backward-compatible migration shipped before the code, so the moment you roll back the app the old code hits a schema it cannot read.
- Ramping straight to 100% with no bake time, giving no window to catch regressions on real traffic.
- No comms, so stakeholders and on-call learn about the deploy from the alert page.

## Output format

```
Checklist grouped: Pre-flight / Rollout / Rollback / Comms / Post-release.

Canary ramp:
| step | traffic % | bake time | health gate |

Rollback:
- triggers + thresholds (pre-declared)
- authority: <who calls abort>
- one-line revert: <command>
```
