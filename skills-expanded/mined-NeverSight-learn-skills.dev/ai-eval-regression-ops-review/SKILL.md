---
name: ai-eval-regression-ops-review
description: Design and audit AI eval regression operations, golden datasets, prompt/model release gates, rubric governance, judge drift, safety cases, quality monitoring, cost/latency guardrails, failure triage, provider/model changes, human review, and rollback. Use when AI features, agents, copilots, recommendations, or automation need reliable improvement without silent regressions.
---

# AI Eval Regression Ops Review

Use this skill to convert a AI eval regression operations, datasets, rubrics, judge drift, release gates, monitoring, and rollback question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify AI job, autonomy level, harm if wrong, datasets, eval owners, model/provider dependencies, release cadence, and user-facing acceptance criteria.
2. Read `references/ai-eval-regression-ops-patterns.md`.
3. Classify eval types: golden cases, adversarial/safety, rubric judge, human review, offline replay, live canary, cost/latency, and task-success metrics.
4. Define dataset governance, rubric versioning, judge calibration, release thresholds, failure triage, monitoring, rollback, and review cadence.
5. Produce eval ops plan, state machine, decision table, event schema, regression checklist, and model-change policy.

## Guardrails

- Do not ship AI changes on aggregate score alone when critical slices regress.
- Do not use model-as-judge without calibration, drift checks, and human spot review for high-impact cases.
- Do not leak private customer data into eval datasets or vendor prompts without policy review.
- Do not treat a passed offline eval as proof that live cost, latency, safety, and fallback behavior are acceptable.

## Output format

```text
AI eval context:
Job / autonomy / harm / release cadence:

Eval regression ops plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Datasets, rubrics, and gates:
- <item> -> <policy, metric, edge case, support note>

Failure triage and model-change policy:
- <trigger> -> <action, communication, owner>
```
