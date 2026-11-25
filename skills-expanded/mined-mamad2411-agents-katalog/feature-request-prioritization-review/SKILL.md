---
name: feature-request-prioritization-review
description: Design and audit feature request prioritization from support, sales, customer success, research, app reviews, community, analytics, and strategic accounts; covering evidence quality, segment fit, revenue risk, product strategy, effort, dependencies, fairness, duplicate clustering, communication, and close-the-loop decisions. Use when teams must decide what to build without overreacting to loud requests.
---

# Feature Request Prioritization Review

Use this skill to convert feature request prioritization, evidence quality, duplicate clustering, segment fit, roadmap, and close-the-loop questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify request source, affected users, segment, job/pain, evidence, frequency, revenue/retention impact, strategic fit, current workaround, and delivery constraints.
2. Read `references/feature-request-prioritization-patterns.md`.
3. Classify request as bug, usability gap, workflow blocker, enterprise ask, compliance/security need, pricing/package gap, integration, power-user enhancement, or strategic bet.
4. Define evidence score, clustering, opportunity framing, impact/effort/risk, dependency map, decision owner, communication plan, and revisit trigger.
5. Produce prioritization review, state machine, decision table, event schema, scoring checklist, and stakeholder response.

## Guardrails

- Do not rank by loudest customer, biggest logo, newest ticket, or sales urgency alone.
- Do not promise roadmap dates until ownership, scope, tradeoffs, and delivery confidence are approved.
- Do not merge bugs, support confusion, workflow jobs, and strategic bets into one undifferentiated request list.
- Do not close the loop with vague “maybe later” when the decision and reasoning are known.

## Output format

```text
Request context:
Audience / source of truth / risk boundary:

Prioritization plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Evidence, tradeoffs, decision, and customer response:
- <trigger> -> <policy, metric, edge case, support note>
```
