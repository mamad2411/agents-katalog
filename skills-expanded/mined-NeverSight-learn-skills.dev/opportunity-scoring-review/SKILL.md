---
name: opportunity-scoring-review
description: Score, compare, and prioritize product, growth, design, monetization, marketplace, operations, platform, and support opportunities. Use when deciding what to build next, ranking roadmap bets, comparing market opportunities, prioritizing experiments, or balancing impact, confidence, effort, risk, revenue, strategic fit, urgency, and learning value.
---

# Opportunity Scoring Review

Use this skill to prioritize opportunities without pretending a spreadsheet is objective truth.

## Workflow

1. Identify decision context, time horizon, capacity, constraints, and strategic goal.
2. Read `references/opportunity-scoring-systems.md`.
3. Normalize opportunities into comparable user problems or business outcomes.
4. Score impact, confidence, effort, risk, urgency, revenue leverage, strategic fit, and learning value.
5. Produce ranked recommendations plus sensitivity analysis and next validation step.

## Guardrails

- Do not score vague feature ideas before defining the opportunity and target outcome.
- Do not treat low-confidence big numbers as precise.
- Do not ignore dependency, sequencing, support cost, or trust risk.

## Output format

```text
Prioritization goal:
Constraints:

Ranked opportunities:
1. <opportunity> — score, rationale, evidence, next proof

Sensitivity:
- <factor that could change ranking>

Recommended sequence:
- now / next / later / reject
```
