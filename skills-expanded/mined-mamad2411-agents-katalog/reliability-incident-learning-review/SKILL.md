---
name: reliability-incident-learning-review
description: Design and audit reliability incident learning, postmortems, incident timelines, contributing factors, action items, recurrence prevention, customer impact, status updates, error budget learning, operational follow-through, and blameless review. Use when outages, degraded service, data incidents, support spikes, or release failures need durable improvement instead of shallow postmortems.
---

# Reliability Incident Learning Review

Use this skill to convert a incident learning, postmortems, contributing factors, action items, recurrence prevention, and customer trust question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify incident type, customer impact, timeline, detection path, responders, affected promises, and unresolved risks.
2. Read `references/reliability-incident-learning-patterns.md`.
3. Classify incident as outage, degradation, data correctness, billing/auth, security/privacy, support process, release regression, or dependency failure.
4. Define timeline, impact, contributing factors, detection gaps, comms review, action owners, due dates, recurrence guardrails, and learning distribution.
5. Produce incident learning report, state machine, decision table, event schema, action checklist, and recurrence-review cadence.

## Guardrails

- Do not reduce postmortems to one root cause when systems, process, monitoring, and decision factors interacted.
- Do not close incident actions without evidence that recurrence risk changed.
- Do not hide customer impact, missed detection, or communication gaps behind internal-only language.
- Do not blame individuals instead of improving conditions, tools, and decision paths.

## Output format

```text
Incident context:
Incident type / customer impact / promise affected:

Incident learning plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Factors, actions, and evidence:
- <item> -> <policy, metric, edge case, support note>

Recurrence and follow-through policy:
- <trigger> -> <action, communication, owner>
```
