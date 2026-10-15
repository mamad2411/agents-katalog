---
name: trial-conversion-sales-assist-review
description: Design and audit sales-assisted trial conversion for SaaS and developer tools covering activation signals, PQL scoring, usage intent, sales routing, in-product nudges, demo offers, procurement readiness, upgrade prompts, trial extension, nurture, handoff, experiment guardrails, and trust-preserving outreach. Use when free trials or freemium users should convert without spam or dark patterns.
---

# Trial Conversion Sales Assist Review

Use this skill to convert trial conversion, product-qualified lead, sales-assist, activation, upgrade prompt, and nurture questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify trial model, activation events, value milestones, user/account identity, firmographic fit, usage signals, buying intent, routing capacity, pricing page path, and current conversion friction.
2. Read `references/trial-conversion-sales-assist-patterns.md`.
3. Classify users as not activated, self-serve ready, PQL, sales-assist, enterprise intent, procurement-ready, nurture, extension-needed, or bad-fit.
4. Define PQL scoring, routing rules, message triggers, upgrade offers, demo/CS handoff, trial extension policy, suppression, experiment metrics, and support path.
5. Produce trial conversion plan, state machine, decision table, event schema, conversion checklist, and experiment/guardrail plan.

## Guardrails

- Do not route every trial to sales; protect sales capacity and user trust with fit and intent thresholds.
- Do not use misleading scarcity, hidden cancellation, surprise billing, or aggressive outreach as conversion tactics.
- Do not optimize conversion without tracking activation quality, retention, refunds, support load, and complaint signals.
- Do not contact users in ways that violate consent, privacy, regional rules, or enterprise account ownership.

## Output format

```text
Trial conversion context:
Audience / source of truth / risk boundary:

Sales-assist conversion plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Signals, routing, nudges, and guardrails:
- <trigger> -> <policy, metric, edge case, support note>
```
