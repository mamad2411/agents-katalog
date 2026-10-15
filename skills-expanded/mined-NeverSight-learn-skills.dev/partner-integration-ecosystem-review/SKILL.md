---
name: partner-integration-ecosystem-review
description: Design and audit partner integration ecosystems, APIs, app directories, OAuth flows, webhooks, SDKs, partner onboarding, certification, co-marketing, revenue share, support boundaries, abuse controls, and ecosystem health. Use when a product depends on third-party integrations, platform partners, developer apps, marketplace listings, or strategic distribution channels.
---

# Partner Integration Ecosystem Review

Use this skill to convert a risky product, operations, trust, or marketplace question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify partner types, integration surface, user value, data access, monetization, support boundary, and strategic priority.
2. Read `references/partner-ecosystem-patterns.md`.
3. Map lifecycle: discover, apply, authorize, build, test, certify, publish, support, measure, renew, or remove.
4. Separate product API readiness, business incentives, trust review, documentation, and operational ownership.
5. Produce ecosystem strategy, partner tiers, integration checklist, risk register, and success metrics.

## Guardrails

- Do not expose user data to partners without clear authorization, scopes, logging, and revocation.
- Do not promise partner support or SLAs beyond operational capacity.
- Avoid app-directory vanity if integrations do not create retained user value.
- Keep certification and ranking criteria transparent enough to preserve partner trust.

## Output format

```text
Ecosystem context:
Partner type / integration surface / user job:

Partner matrix:
| Partner type | Value | API/data access | Requirements | Support owner | Metric |
| --- | --- | --- | --- | --- | --- |

Integration lifecycle:
- <state> -> <gate/action/evidence>

Risks and policies:
- <risk> -> <control/review/support>
```
