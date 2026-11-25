---
name: watch-monitor
description: Canonical watch/monitor pack for meaningful change detection across web sources, connectors, repo activity, or triggers, with false-positive suppression and alert summaries.
tags: [watch, monitor, alert, webhook, trigger, repo activity, change detection]
keywords:
  - watch
  - monitor
  - alert
  - webhook
  - trigger
  - repo activity
  - change detection
triggers:
  - monitor changes
  - watch a source
  - notify on change
  - trigger summary
context_tags:
  - observability
  - workflow
canonical_pack: true
delivery_modes:
  - manual
  - routine
  - trigger
prerequisite_hints:
  - "Web source monitoring can use browser/fetch tooling without connectors."
  - "Connector-backed monitoring depends on the relevant connector readiness."
  - "Trigger-driven workflows should use packaged webhook/trigger flows where available."
source_links:
  - docs/operating/routines.md
  - skills/zorai-mcp/operating/observability.md
mobile_safe: true
approval_behavior: "Read-only monitoring is allowed; any remediation or external write-back spawned from a watch result requires separate approval."
---

# Watch / Monitor

## User story

I want to define a watch that only notifies me on meaningful changes, whether the source is a webpage, connector-backed resource, repo activity, or trigger event.

## Pack contract

### Prerequisites and readiness

- Manual web/source monitoring works without connectors
- Connector-backed monitors require the relevant connector
- Trigger-driven use should be routable via routines or triggers when available

### Inputs and configuration fields

- `watch_source`: webpage / connector resource / repo / webhook family
- `threshold`: significance threshold or rule set
- `suppression_rules`: optional false-positive suppression criteria
- `delivery_channel`: in-app or chat channel

### Outputs and delivery targets

- concise change summary
- why it fired
- what changed
- source reference(s)
- suppression / noise notes when relevant

## Manual run recipe

1. Read the source snapshot or event.
2. Compare to the prior relevant state when available.
3. Apply suppression rules.
4. Emit only meaningful change summaries.

## Example routine wiring

`Run the Watch/Monitor pack every hour for the chosen source and notify only when the threshold is exceeded.`

## Example trigger wiring

Use as the target logic behind a packaged trigger that ingests webhook events and converts them into operator-safe summaries.

## Example prompt

`Set up the Watch/Monitor pack for repo activity with stale-noise suppression and mobile-safe alerts.`

## Failure and recovery behavior

- Missing prior state -> emit a baseline snapshot instead of a spurious alert.
- Missing connector -> fail closed with setup hint.
- Trigger noise -> report suppression decision and avoid alert spam.

## Verification checklist

- [ ] Manual proof on a web/source input passes.
- [ ] Routine-oriented proof passes.
- [ ] Trigger-oriented proof passes.
- [ ] False-positive suppression behavior is documented.
- [ ] Alerts are mobile-safe and source-linked.
