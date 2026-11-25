---
name: service-level-slo-review
description: Design and audit service levels, SLIs, SLOs, SLAs, error budgets, maintenance windows, incident status, support response promises, uptime claims, API latency targets, data freshness targets, recovery objectives, and customer communication. Use when a product needs reliability promises that engineering, support, sales, and customers can trust.
---

# Service Level SLO Review

Use this skill to convert a SLOs, SLIs, SLAs, error budgets, uptime, latency, freshness, recovery objectives, and customer reliability promises question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify critical user journeys, customers, contractual promises, measurement sources, failure modes, support commitments, and business risk.
2. Read `references/service-level-slo-patterns.md`.
3. Separate internal SLO, external SLA, support target, uptime claim, freshness objective, latency objective, and recovery objective.
4. Define SLIs, windows, exclusions, error budget policy, alerting, status page behavior, maintenance windows, and customer communications.
5. Produce service-level plan, state machine, decision table, event schema, reliability checklist, and promise-review cadence.

## Guardrails

- Do not promise an SLA if monitoring, incident response, support process, and credit/remedy policy cannot support it.
- Do not measure availability only from server uptime when the user journey depends on dependencies, auth, billing, DNS, or queues.
- Do not hide planned maintenance or partial degradation behind green status.
- Do not treat SLO burn as an engineering-only metric when customer promises or sales claims are affected.

## Output format

```text
Service-level context:
Journey / customer promise / measurement source:

SLO and service-level plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

SLIs, windows, and promises:
- <item> -> <policy, metric, edge case, support note>

Error budget and communication policy:
- <trigger> -> <action, communication, owner>
```
