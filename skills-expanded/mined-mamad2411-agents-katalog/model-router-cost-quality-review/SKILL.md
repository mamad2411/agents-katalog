---
name: model-router-cost-quality-review
description: Design and audit AI model routers that balance task quality, latency, cost, reliability, safety, privacy, context size, tool use, fallback, caching, evals, budgets, and provider outages. Use when an agent or product must choose models dynamically instead of hard-coding one default model.
---

# Model Router Cost Quality Review

Use this skill to convert AI model routing, provider selection, cost, quality, latency, fallback, eval, and budget questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify task classes, user tiers, quality bar, latency SLO, context size, tool needs, safety/privacy constraints, provider options, budget guardrails, and observability gaps.
2. Read `references/model-router-cost-quality-patterns.md`.
3. Classify routing as fixed, tiered, policy-based, eval-gated, cascade, specialist, fallback, or human-escalated.
4. Define routing inputs, route policy, quality checks, cost budgets, fallback behavior, cache rules, safety escalation, and experiment plan.
5. Produce router design, state machine, decision table, event schema, eval matrix, cost-quality scorecard, and rollback gates.

## Guardrails

- Do not optimize token cost before defining task quality, failure severity, and user promise.
- Do not route sensitive, regulated, or customer-confidential inputs to providers without privacy and contract review.
- Do not let fallback silently lower safety, correctness, or tool-call capability.
- Do not use aggregate satisfaction as the only quality signal; include task-specific evals and failure samples.

## Output format

```text
Router context:
Audience / source of truth / risk boundary:

Cost-quality routing plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Routes, fallback, evals, and budget gates:
- <trigger> -> <policy, metric, edge case, support note>
```
