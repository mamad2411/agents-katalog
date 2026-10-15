---
name: partner-risk-due-diligence-review
description: Design and audit partner risk due diligence for integrations, resellers, agencies, affiliates, marketplace partners, creators, data-sharing partners, AI providers, and co-marketing. Covers strategic fit, security/privacy, legal, operational dependency, brand risk, support burden, incentives, exit plans, and monitoring. Use when committing to partner ecosystems or joint go-to-market.
---

# Partner Risk Due Diligence Review

Use this skill to convert a partner risk due diligence, integrations, data sharing, brand fit, incentives, legal/privacy/security exposure, and exit plans question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify partner type, user value, data exchanged, dependency depth, commercial terms, brand exposure, support impact, and exit cost.
2. Read `references/partner-risk-due-diligence-patterns.md`.
3. Classify partner motion: integration, reseller, agency, affiliate, marketplace supply, creator, data partner, AI provider, or co-marketing.
4. Define risk review, evidence, data boundaries, contract terms, support model, monitoring, incentives, escalation, and termination/exit path.
5. Produce partner due diligence plan, state machine, decision table, event schema, checklist, and ongoing review cadence.

## Guardrails

- Do not integrate or co-market before data-sharing, support, brand, legal, privacy, and security responsibilities are explicit.
- Do not let revenue upside hide dependency risk, customer confusion, or misaligned incentives.
- Do not share customer data or leads without consent, minimization, and legal basis.
- Do not launch a partner dependency without degradation, offboarding, and customer communication paths.

## Output format

```text
Partner risk context:
Partner type / data / dependency / brand exposure:

Due diligence plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Evidence, terms, and monitoring:
- <item> -> <policy, metric, edge case, support note>

Exit and escalation policy:
- <trigger> -> <action, communication, owner>
```
