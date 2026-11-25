---
name: api-rate-limit-quota-review
description: Design and audit API rate limits, quotas, fair-use policy, burst handling, concurrency limits, usage tiers, overages, retry headers, developer dashboards, webhooks, abuse controls, tenant isolation, enterprise overrides, and migration communication. Use when launching APIs, SDKs, developer platforms, AI endpoints, marketplace APIs, or usage-priced products.
---

# API Rate Limit Quota Review

Use this skill to convert a API quotas, rate limits, fair use, developer experience, billing alignment, and abuse controls question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify API consumer, authentication principal, endpoint cost, criticality, tenant blast radius, pricing tier, and abuse pattern.
2. Read `references/api-rate-limit-quota-patterns.md`.
3. Separate rate limit, quota, concurrency cap, payload cap, spend cap, fair-use review, and entitlement gate.
4. Define limit units, headers, error shape, retry/backoff, dashboards, alerts, upgrade path, support override, and migration policy.
5. Produce quota model, state machine, endpoint decision table, event schema, and developer communication checklist.

## Guardrails

- Do not use a single global limit when endpoint cost, tenant size, and abuse risk differ materially.
- Do not return vague 429s without stable headers, retry guidance, documentation, and observability.
- Do not let quota bypass billing, entitlement, security, or tenant isolation controls.
- Do not silently change limits for existing developers without migration notice and support path.

## Output format

```text
API context:
Principal / endpoint cost / tenant blast radius:

Limit and quota plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Developer contract:
- <item> -> <policy, metric, edge case, support note>

Override and migration policy:
- <trigger> -> <action, communication, owner>
```
