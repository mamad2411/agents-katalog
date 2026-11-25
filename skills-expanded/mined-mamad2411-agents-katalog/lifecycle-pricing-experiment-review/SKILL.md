---
name: lifecycle-pricing-experiment-review
description: Design and audit lifecycle pricing experiments across trials, coupons, intro offers, upgrade prompts, expansion nudges, renewal discounts, winback offers, annual conversion, regional pricing, usage thresholds, grandfathering, holdouts, guardrails, revenue measurement, and customer trust. Use when testing monetization changes without corrupting retention or brand trust.
---

# Lifecycle Pricing Experiment Review

Use this skill to convert lifecycle pricing experiment, offer test, upgrade nudge, renewal discount, winback, annual conversion, and monetization guardrail questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify target lifecycle stage, customer segment, offer, control group, pricing surface, eligibility rules, billing mechanics, success metric, guardrails, and customer-communication risk.
2. Read `references/lifecycle-pricing-experiment-patterns.md`.
3. Classify the situation as trial experiment, intro discount, upgrade prompt, annual conversion, expansion offer, renewal save, winback, regional price test, usage threshold test, or holdout measurement.
4. Define hypothesis, eligibility, randomization, holdout, revenue and retention metrics, support/legal constraints, abuse controls, billing QA, and stop conditions.
5. Produce pricing experiment brief, state machine, decision table, event schema, guardrail checklist, rollout plan, and readout template.

## Guardrails

- Do not optimize conversion while hiding churn, refund, support, downgrade, margin, or trust damage.
- Do not expose unfair pricing differences without eligibility logic, communication policy, and support handling.
- Do not run pricing tests that billing, taxes, invoices, entitlements, or analytics cannot prove.
- Do not let sales or support override experiment cohorts without an auditable exception path.

## Output format

```text
Lifecycle pricing context:
Audience / source of truth / risk boundary:

Pricing experiment plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Hypothesis, cohorts, guardrails, billing proof, and readout:
- <trigger> -> <policy, metric, edge case, support note>
```
