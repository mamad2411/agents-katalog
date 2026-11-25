---
name: change-plan-builder
description: 'Turn Google Ads findings into an ordered, approval-ready change plan with dependencies, evidence, rollback, and measurement. Use when the analysis is done and the next move needs to be clear.'
---

# Change Plan Builder

## Doctrine

A good change list is not a pile of recommendations. It respects dependencies, names the exact entity and current state, separates investigation from execution, and tells you how to undo each move. Tracking comes before bidding, query evidence comes before negatives, and a low CPA does not make every extra dollar profitable.

## When to use

- After one or more Google Ads skills have produced findings.
- Before making account changes, especially goals, negatives, ads, bids, budgets, or structure.
- Use a connected Google Ads MCP for a fresh read, or paste findings with exact entity names, IDs, current settings, recent changes, and business constraints.

## Run it

```
Build a READ-ONLY Google Ads change plan. Use live account data for current state if connected; otherwise use what I paste. Execute nothing.

1. Confirm the scope, exact entities and IDs, current settings, primary business goal, approval policy, and recent change history.
2. Convert each finding into one label: keep, investigate, exclude, rewrite, restructure, or test.
3. For every item show: priority, entity, current state, proposed state, evidence, expected direction, confidence, risk, dependency, preflight check, approval required, rollback, success measure, and review date.
4. Order dependencies before impact:
   - verify conversion integrity before bid, target, budget, or scaling changes;
   - run negative-keyword collision checks before exclusions;
   - verify page claims and URLs before ad rewrites;
   - stabilize serving before judging efficiency.
5. Use directional expectations unless the user supplies a validated model. Do not invent CTR lifts, CPC savings, conversion counts, or monthly forecasts.
6. Keep investigations separate from mutations. "May be duplicated" becomes a verification step, not "delete the duplicate".
7. Require item-level approval and a fresh preflight read before any later execution. Grouping items in one plan is not blanket approval.

Return: do first, do next, hold, and keep. End with "Plan only. No changes were made."
```

## Guardrails

- Never delete or demote a conversion action from a similarity in names or totals alone.
- Never turn a few bad queries into broad one-word negatives without match-type, scope, and collision checks.
- A campaign below target and limited by budget is a candidate for investigation, not an automatic budget increase.
- Every executable item needs exact current and proposed state, approval, rollback, and measurement.
- Do not bundle unrelated changes into one test. If the result would be impossible to attribute, split the plan.

## Good output looks like

An ordered dry run where the safest dependency comes first, every proposed change is inspectable and reversible, forecasts stay honest, and nothing happens without item-level approval.
