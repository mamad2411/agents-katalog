---
name: do-incident-runbook
version: 1.0.0
description: Produce a clear on-call runbook mapping symptoms to checks and mitigation-first steps so a tired responder acts fast and safely.
author: matrixx0070
tags: [incident, oncall, runbook, sre, reliability, mitigation]
capabilities: []
---

# do-incident-runbook

## When to use

You need an on-call runbook for a service, are turning tribal knowledge into a document a tired responder can follow at 3am, or are capturing what to do when a specific alert fires.

**Not for:** defining the alerts or SLOs themselves (use do-observability), the planned release/rollback procedure (use do-release-checklist), or debugging cluster internals (use do-kubernetes).

## Method

1. State the service's purpose, owners, dependencies, and criticality up front, plus links to dashboards, logs, and deploy history.
2. For each known failure mode, write a symptom -> diagnosis -> mitigation entry: the alert or user report, the exact commands/queries to confirm the cause, and the ordered steps to mitigate.
3. Lead with mitigation over root cause. Decision: if service is down, restore first (roll back, scale out, failover, drain, flag off), then investigate — never debug a live outage before stabilizing it.
4. Include escalation: when to page the next tier, who owns each dependency, and the severity ladder with response-time expectations. Decision: escalate when a mitigation fails or the blast radius grows, not after an arbitrary delay.
5. Add safety rails: mark destructive commands, changes needing a second approver, and the rollback for each mitigation.
6. Keep it current: reference the last incident, note gaps, and prompt the reader to update the runbook after use.

## Example

```markdown
### Symptom: checkout 5xx rate > 5% (alert: CheckoutErrorBudgetFastBurn)
Confirm:
  - dashboard: https://grafana/checkout (error rate panel)
  - recent deploy? `kubectl rollout history deploy/checkout`
Mitigate (in order):
  1. If a deploy shipped < 30m ago -> roll back:
     `kubectl rollout undo deploy/checkout`   [safe, reversible]
  2. If DB saturated -> scale read replicas (see db runbook).
  3. Still failing after 10m -> escalate to Tier 2 (@payments-oncall).
Do NOT: flush the Redis cache — cold cache amplifies the outage. [DESTRUCTIVE]
```

## Pitfalls

- Leading with root-cause analysis while the service is down — the responder debugs while users bleed instead of restoring first.
- Vague steps ("check the database") instead of the exact command/query a half-awake responder can paste.
- No escalation trigger, so an overwhelmed responder struggles alone past the point they should have paged.
- Unmarked destructive commands (cache flush, data delete) with no "do not / needs approval" rail.

## Output format

```
Header: service | owners | dependencies | dashboards | severity ladder.

Per failure mode:
### Symptom: <alert or user report>
Confirm: <exact commands/queries>
Mitigate (in order): 1... 2... 3...
Escalate when: <trigger> -> <who>
Do NOT / needs approval: <destructive steps>

Post-incident: update-this-runbook checklist.
```
