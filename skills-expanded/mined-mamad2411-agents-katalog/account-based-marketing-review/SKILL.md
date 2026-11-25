---
name: account-based-marketing-review
description: Design and audit account-based marketing motions covering target account selection, buying committee personas, account tiers, intent signals, personalization, ads, events, sales alignment, SDR plays, content offers, attribution, privacy, suppression, pipeline influence, and measurement. Use when B2B growth needs focused account programs instead of broad demand-gen tactics.
---

# Account Based Marketing Review

Use this skill to convert account-based marketing, target account, intent signal, personalization, sales alignment, and pipeline-influence questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify ICP, account tiering, target account source, buying committee, strategic trigger, message wedge, sales owner, channels, privacy constraints, and pipeline goal.
2. Read `references/account-based-marketing-patterns.md`.
3. Classify the motion as one-to-one strategic account, one-to-few segment cluster, one-to-many programmatic ABM, expansion ABM, partner ABM, or reactivation ABM.
4. Define account selection, signal thresholds, personalized offer, channel plan, sales/SDR handoff, suppression rules, measurement model, and learning loop.
5. Produce ABM plan, state machine, decision table, event schema, campaign checklist, and account action plan.

## Guardrails

- Do not call ordinary lead-gen ABM unless account selection, buying committee, personalization, and sales action are explicit.
- Do not personalize with sensitive or creepy signals; respect privacy, consent, and regional marketing rules.
- Do not claim sourced revenue from ABM without separating influence, sourced pipeline, sales activity, and existing momentum.
- Do not target accounts sales cannot follow up or customer success cannot support.

## Output format

```text
ABM context:
Audience / source of truth / risk boundary:

Account program plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Targeting, personalization, sales actions, and measurement:
- <trigger> -> <policy, metric, edge case, support note>
```
