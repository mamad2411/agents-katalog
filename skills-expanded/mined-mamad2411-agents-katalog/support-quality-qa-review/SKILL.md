---
name: support-quality-qa-review
description: Design and audit customer support quality assurance, ticket review scorecards, macro quality, escalation correctness, refund/support fairness, tone, evidence handling, coaching loops, calibration, automation QA, and support health metrics. Use when improving support operations for SaaS, apps, games, marketplaces, developer tools, billing, trust, or community products.
---

# Support Quality QA Review

Use this skill to convert a risky product, operations, trust, or marketplace question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify support channels, case types, risk classes, macros, escalation paths, QA owner, and customer outcomes.
2. Read `references/support-quality-patterns.md`.
3. Define QA dimensions: accuracy, empathy, policy, evidence, resolution, escalation, safety, revenue/trust impact, and documentation.
4. Design sampling, calibration, coaching, macro improvement, automation review, and product feedback loops.
5. Produce QA scorecard, review workflow, event schema, and improvement backlog.

## Guardrails

- Do not score agents only on speed when correctness, fairness, or trust is at risk.
- Do not punish support for product gaps; route recurring causes back to product owners.
- Do not let AI/macros send high-impact policy, billing, or safety responses without QA gates.
- Protect customer privacy in QA examples and coaching artifacts.

## Output format

```text
Support QA context:
Channel / case type / risk class:

Scorecard:
| Dimension | Good | Risk | Weight | Evidence | Coaching action |
| --- | --- | --- | --- | --- | --- |

QA workflow:
- <sample/review/calibrate/coach/improve>

Product feedback:
- <recurring issue> -> <owner/artifact/metric>
```
