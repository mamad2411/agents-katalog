---
name: partner-support-enablement-review
description: Design and audit partner support enablement across partner tiers, implementation roles, support access, escalation paths, training, certification, runbooks, knowledge bases, customer handoffs, co-sell motions, SLAs, sandbox environments, release updates, feedback loops, and quality metrics. Use when partners need to support customers without creating hidden operational risk.
---

# Partner Support Enablement Review

Use this skill to convert partner support enablement, implementation partner, reseller support, co-sell handoff, partner training, escalation, certification, and partner runbook questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify partner type, customer segment, supported product scope, access model, escalation path, training level, certification requirement, SLA promise, and shared success metric.
2. Read `references/partner-support-enablement-patterns.md`.
3. Classify the situation as referral partner, reseller, implementation partner, support partner, marketplace partner, systems integrator, technology partner, or strategic alliance.
4. Define partner roles, support boundaries, escalation tiers, knowledge assets, training, certification, sandbox access, release update cadence, customer communication, and quality monitoring.
5. Produce partner support enablement plan, state machine, decision table, event schema, readiness checklist, escalation map, and partner QA loop.

## Guardrails

- Do not give partners customer-impacting support access without permission boundaries, audit logs, training, and revocation paths.
- Do not let partners promise unsupported SLAs, roadmap items, pricing terms, security controls, or custom implementation behavior.
- Do not create partner support channels that bypass product feedback, incident communication, or customer success ownership.
- Do not certify partners without outcome evidence and renewal or revocation criteria.

## Output format

```text
Partner support context:
Audience / source of truth / risk boundary:

Partner enablement plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Roles, access, escalation, training, quality, and feedback loops:
- <trigger> -> <policy, metric, edge case, support note>
```
