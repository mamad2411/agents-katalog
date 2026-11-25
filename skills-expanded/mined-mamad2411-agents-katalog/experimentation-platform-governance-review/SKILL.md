---
name: experimentation-platform-governance-review
description: Design and audit experimentation platform governance for A/B tests, holdouts, feature tests, pricing experiments, lifecycle campaigns, marketplace ranking tests, game economy tests, AI experiments, exposure allocation, metrics, guardrails, conflicts, ethics, rollout, and decision review. Use when experiments should create reliable product learning without harming users or corrupting decisions.
---

# Experimentation Platform Governance Review

Use this skill to convert a experimentation governance, A/B tests, holdouts, metrics, guardrails, exposure conflicts, ethics, and decision review question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify experiment type, hypothesis, exposure unit, target population, metrics, risk class, overlapping tests, owner, and decision deadline.
2. Read `references/experimentation-platform-governance-patterns.md`.
3. Classify experiment as UX, pricing, ranking, lifecycle, onboarding, game economy, AI, permission, or infrastructure/product-risk test.
4. Define eligibility, randomization, holdouts, metrics, guardrails, sample plan, conflict policy, ethics review, launch gate, and decision record.
5. Produce governance plan, state machine, decision table, event schema, checklist, and experiment review cadence.

## Guardrails

- Do not test pricing, ranking, safety, privacy, or accessibility changes without risk review and support/comms plan.
- Do not run overlapping experiments that contaminate metrics without conflict policy.
- Do not declare winners without guardrails, segment review, and decision threshold.
- Do not keep long-lived holdouts or experiments without user-impact and cleanup ownership.

## Output format

```text
Experiment context:
Hypothesis / exposure / risk class / conflicts:

Experiment governance plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Metrics, guardrails, and conflicts:
- <item> -> <policy, metric, edge case, support note>

Decision and cleanup policy:
- <trigger> -> <action, communication, owner>
```
