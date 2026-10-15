---
name: support-escalation-engineering-review
description: Design and audit support-to-engineering escalation workflows covering severity, reproduction, logs, customer impact, ownership, SLAs, bug intake, incident boundary, feature requests, known issues, engineering triage, workaround, customer updates, closure proof, and feedback loops. Use when support needs reliable engineering help without noisy or invisible escalations.
---

# Support Escalation Engineering Review

Use this skill to convert support escalation, engineering triage, bug intake, reproduction, workaround, SLA, and customer-update questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify support channels, issue taxonomy, severity rules, customer segment, reproduction artifacts, logs/traces, owner teams, current queue, SLA promises, and customer communication gaps.
2. Read `references/support-escalation-engineering-patterns.md`.
3. Classify escalation as how-to, known issue, bug, incident, data repair, billing correction, security/privacy, feature request, product gap, or engineering investigation.
4. Define intake requirements, severity, ownership, triage cadence, reproduction standard, workaround policy, customer update cadence, closure proof, and backlog feedback loop.
5. Produce escalation operating model, state machine, decision table, event schema, triage checklist, and support/engineering RACI.

## Guardrails

- Do not escalate vague tickets without customer impact, reproduction detail, environment, logs, and expected/actual behavior when practical.
- Do not bury incidents, security/privacy issues, or data-loss cases in a normal bug queue.
- Do not close engineering escalations without support-visible resolution, workaround, or customer communication.
- Do not let support become the only memory of product defects; route recurring issues into product and quality systems.

## Output format

```text
Escalation context:
Audience / source of truth / risk boundary:

Support-engineering plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Severity, ownership, workarounds, and closure proof:
- <trigger> -> <policy, metric, edge case, support note>
```
