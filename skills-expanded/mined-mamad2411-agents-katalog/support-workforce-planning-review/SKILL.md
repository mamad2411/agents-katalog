---
name: support-workforce-planning-review
description: Forecast and audit customer support workforce plans across channels, languages, queues, SLAs, severity tiers, launches, incidents, seasonality, shrinkage, occupancy, escalation, QA, macros, deflection, BPO/vendor coverage, and burnout risk. Use when support demand must be staffed without sacrificing quality or trust.
---

# Support Workforce Planning Review

Use this skill to convert support staffing, capacity, queue, SLA, coverage, escalation, QA, and deflection questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify channels, issue taxonomy, volume history, seasonality, languages, time zones, severity tiers, SLA promises, backlog, launches/incidents, support tooling, and team constraints.
2. Read `references/support-workforce-planning-patterns.md`.
3. Classify demand as steady state, launch spike, incident surge, seasonal peak, migration wave, abuse burst, enterprise queue, or long-tail support debt.
4. Define forecast, coverage model, schedule assumptions, escalation lanes, QA sampling, macro/knowledge updates, deflection plan, and hiring/vendor triggers.
5. Produce workforce plan, state machine, decision table, event schema, staffing checklist, and risk register.

## Guardrails

- Do not staff only from average ticket volume; account for arrival patterns, handle time, shrinkage, backlog, and severity mix.
- Do not improve deflection metrics by hiding human support for high-risk billing, account, safety, or incident issues.
- Do not treat all agents as interchangeable across language, domain expertise, enterprise promises, abuse, and technical escalation.
- Do not let burnout, QA drift, or backlog aging become invisible capacity debt.

## Output format

```text
Support capacity context:
Audience / source of truth / risk boundary:

Workforce plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Coverage, escalation, and quality controls:
- <trigger> -> <policy, metric, edge case, support note>
```
