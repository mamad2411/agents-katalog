---
name: feature-flag-management
description: "Roll out changes safely with feature flags: flag taxonomy, targeting, kill switches, stale-flag hygiene and experiment-safe evaluation."
type: procedural
category: development
domain: development
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - feature flag rollout plan
  - kill switch design
  - flag targeting rules
  - stale flag cleanup
  - progressive delivery
keywords:
  - feature-flags
  - rollout
  - kill-switch
  - targeting
  - experimentation
source: custom
enabled: true
---

# Feature Flag Management

## Purpose

Roll out changes safely with feature flags: flag taxonomy, targeting, kill switches, stale-flag hygiene and experiment-safe evaluation.

## When to Use

- A change should be deployable without being visible to everyone.
- A risky path needs an immediate kill switch.
- An experiment needs consistent assignment per user.

## When NOT to Use

- The change is trivially reversible with a deploy.
- The flag would live forever without an owner or removal date.
- You need data backfills, where flags do not help.

## Capabilities

- Classify flags: release, experiment, operational, permission.
- Target by stable identity with deterministic bucketing.
- Wire kill switches that fail closed for sensitive paths.
- Track flag age and remove stale ones.

## Inputs

- The flag provider and its SDK constraints.
- The identity used for bucketing and its stability.
- The success metric and the rollback threshold.

## Workflow

1. Write the flag's purpose, owner and removal date before creating it.
2. Choose the flag type; experiment flags need stable, sticky assignment.
3. Default off in code and roll out by percentage with monitoring.
4. Add a kill switch for the risky path independent of the rollout percentage.
5. Remove the flag once the rollout completes, including dead branches.

## Tools

- flag provider SDK (LaunchDarkly, Unleash, OpenFeature)
- monitoring dashboards
- code search for flag keys

## Examples

- `allskills route "roll out new checkout gradually"`
- `grep -rn "checkout_v2" src/ | wc -l`
- `allskills explain development.feature-flag-management`

## Safety

- A flag that defaults on during an outage removes your ability to disable the path.
- Evaluating flags with unstable identities makes experiments and rollouts inconsistent.
- Never leave permission flags as a permanent authorization mechanism.

## Source

All-Skills canonical library (`skills/development/feature-flag-management`). First-party skill, maintained in this repository.

## Notes

- Flag debt is real: age tracking plus a removal policy keeps evaluation cheap.
- OpenFeature keeps the SDK choice swappable.
- Pairs with: `devops/deployment-patterns`, `testing/load-testing`.
