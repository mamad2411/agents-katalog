---
name: ai-feature-product-risk-review
description: Design and audit AI feature product risks across user value, model limitations, hallucination, automation boundaries, human review, privacy, safety, evals, latency, cost, transparency, abuse, fallback, rollout, and support. Use when adding AI assistants, copilots, generators, classifiers, recommendations, agents, or automated decisions to a product.
---

# AI Feature Product Risk Review

Use this skill to convert a risky product, operations, trust, or marketplace question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify AI job, user harm if wrong, model/input/output boundary, autonomy level, data sensitivity, and business metric.
2. Read `references/ai-feature-risk-patterns.md`.
3. Map quality, safety, privacy, cost, latency, abuse, support, transparency, and fallback requirements.
4. Separate assistive suggestions, generated content, classification, ranking, automation, and agentic actions.
5. Produce risk matrix, eval plan, UI guardrails, rollout gates, and support/incident paths.

## Guardrails

- Do not hide uncertainty or present generated output as verified fact when it is not.
- Do not automate irreversible, financial, legal, safety, account, or privacy-impacting actions without appropriate gates.
- Do not use user/private data beyond stated purpose, retention, and consent boundaries.
- AI feature launch needs evals, monitoring, fallback, and support playbooks before broad rollout.

## Output format

```text
AI feature context:
Job / autonomy / data / harm:

Risk matrix:
| Risk | Failure mode | User impact | Control | Eval/metric | Owner |
| --- | --- | --- | --- | --- | --- |

UI and rollout gates:
- <transparency/fallback/review/flag>

Support/incident path:
- <case type> -> <triage/evidence/recovery>
```
