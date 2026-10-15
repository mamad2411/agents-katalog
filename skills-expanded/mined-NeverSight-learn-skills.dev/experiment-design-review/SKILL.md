---
name: experiment-design-review
description: Design and audit product experiments, A/B tests, feature rollouts, pricing tests, onboarding tests, lifecycle experiments, holdouts, guardrail metrics, sample plans, decision rules, and learning reviews. Use when testing product, UI, growth, monetization, retention, marketplace, or live-ops changes and the agent must avoid false confidence or harmful experiments.
---

# Experiment Design Review

Use this skill to convert a high-stakes product decision into a concrete, measurable, reviewable operating artifact.

## Workflow

1. Identify the decision, user segment, change, expected mechanism, risk, traffic source, and reversible rollout path.
2. Read `references/experiment-design-patterns.md`.
3. Separate hypothesis, primary metric, guardrails, counter-metrics, sample needs, eligibility, exposure, and analysis window.
4. Choose experiment type: A/B, holdout, staged rollout, switchback, pre/post, qualitative pilot, or no-test decision.
5. Produce experiment spec, instrumentation plan, decision rule, launch checklist, and learning review.

## Guardrails

- Do not call an experiment successful from vanity engagement alone.
- Do not test unsafe, deceptive, discriminatory, privacy-invasive, or legally sensitive variants without qualified review.
- Do not ignore novelty effects, seasonality, sample pollution, repeated peeking, or segment imbalance.
- Use product judgment when experiments are underpowered, too risky, or not ethically testable.

## Output format

```text
Experiment context:
Decision / hypothesis / segment:

Experiment spec:
| Field | Value |
| --- | --- |
| Variant | <change> |
| Primary metric | <metric/window> |
| Guardrails | <metric/window> |
| Eligibility | <users/sessions/accounts> |
| Decision rule | <ship/iterate/rollback/no decision> |

Risk and instrumentation:
- <risk> -> <event/check/owner>

Learning review:
- <result, caveat, decision, next action>
```
