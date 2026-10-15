---
name: product-led-sales-routing-review
description: Design and audit product-led sales routing for signups, trials, freemium workspaces, PQLs, expansion signals, enterprise intent, account matching, owner assignment, sales capacity, suppression, lifecycle messages, CRM sync, handoff, experiments, and conversion-quality guardrails. Use when product usage should trigger the right human or automated sales motion.
---

# Product Led Sales Routing Review

Use this skill to convert product-led sales routing, PQL, account matching, sales capacity, suppression, CRM sync, and conversion-quality questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify signup/trial/freemium model, activation milestones, workspace/account structure, firmographic fit, buying intent, expansion signals, owner rules, sales capacity, lifecycle channels, and CRM state.
2. Read `references/product-led-sales-routing-patterns.md`.
3. Classify route as self-serve, lifecycle nurture, sales-assist, enterprise AE, expansion CS/AE, partner, support assist, disqualified, or suppress.
4. Define PQL/PQA scoring, account matching, ownership, thresholds, routing SLA, message playbook, suppression, CRM sync, experiment guardrails, and feedback loop.
5. Produce routing design, state machine, decision table, event schema, routing checklist, and experiment plan.

## Guardrails

- Do not send every product signal to sales; route only when fit, intent, capacity, and user value justify intervention.
- Do not contact users where consent, account ownership, customer context, support state, or regional rules should suppress outreach.
- Do not optimize meetings or hand-raises without measuring activation quality, paid retention, refunds, support load, and user complaints.
- Do not let product, marketing automation, SDR tasks, and CRM disagree about account owner or lifecycle state.

## Output format

```text
Product-led routing context:
Audience / source of truth / risk boundary:

Routing operating plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Signals, thresholds, ownership, and guardrails:
- <trigger> -> <policy, metric, edge case, support note>
```
