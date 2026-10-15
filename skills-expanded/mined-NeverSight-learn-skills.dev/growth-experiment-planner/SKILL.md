---
name: growth-experiment-planner
description: Use when planning A/B tests in LaunchDarkly, Optimizely, or similar platforms. Sizes the experiment (sample size, MDE, runtime), drafts hypothesis + success metrics + guardrails, and produces a launch checklist + rollback plan.
---

# Growth Experiment Planner

## When to invoke
- "Plan an A/B test for the new onboarding flow."
- "How long do we need to run this experiment?"
- "Draft an experiment brief for the pricing page test."

## Inputs needed
1. **Hypothesis** — what change, expected effect, why.
2. **Primary metric** — name, baseline rate or mean, variance if known.
3. **Traffic** — daily users hitting the surface.
4. **MDE** — minimum detectable effect (relative).
5. **Variants** — control + N treatments.
6. **Guardrails** — metrics that must NOT regress (revenue, errors, latency).

## Workflow
1. **Frame** — restate hypothesis in one sentence.
2. **Size** — call `plan.py` to compute sample size and runtime.
3. **Spec** — generate experiment brief: metrics, segments, allocation, stopping rules, guardrails.
4. **Checklist** — pre-launch QA, holdout, instrumentation, rollback path.
5. **Hand off** — output a Markdown brief ready for LaunchDarkly/Optimizely.

## Output format
A complete experiment brief with: Hypothesis, Variants, Metrics, Sample size, Runtime, Allocation, Guardrails, Stopping rules, QA checklist, Rollback plan.

## Guardrails
- Always require a primary metric defined before launch (no metric fishing).
- Require explicit guardrails — at minimum: error rate, p95 latency, revenue per user.
- Flag if runtime exceeds 4 weeks (novelty + seasonality risk).

## Reference code
`plan.py` computes two-proportion sample size (Evan Miller formula) or two-sample t-test sample size.
