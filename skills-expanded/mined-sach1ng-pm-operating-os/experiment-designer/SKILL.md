---
name: experiment-designer
description: "Help PMs design rigorous experiments (A/B tests, feature rollouts). Use before any A/B test, feature experiment, pricing test, or phased rollout."
---

# Experiment Designer

Help PMs design rigorous experiments with clear hypotheses, variants, metrics, and decision criteria. Ensures experiments are statistically sound and actionable.

## When to Use

- Before any A/B test
- Feature experiment design
- Pricing or packaging test
- Phased rollout planning
- When asked "how do we test this?"
- Before setting up an experiment in an experimentation platform

## Process / Template

### 1. Capture the Hypothesis

Use format: **"We believe [action] will [outcome] for [segment] because [rationale]"**

- **Action** — what you're changing (feature, copy, flow)
- **Outcome** — expected metric movement
- **Segment** — who you're testing with
- **Rationale** — why you believe this (research, prior data)

### 2. Define Control vs. Treatment

- **Control** — baseline experience (no change)
- **Treatment** — the change being tested
- Be explicit about what differs between variants

### 3. Define Success Metrics

- **Primary metric** — main success signal (one metric)
- **Secondary metrics** — supporting signals
- **Guardrail metrics** — must not regress (e.g., revenue, retention)

### 4. Determine Experiment Type

- **A/B test** — two variants, single change
- **Multivariate** — multiple factors
- **Phased rollout** — gradual % rollout
- **Holdout** — long-term impact test

### 5. Calculate Sample Size and Duration

- **Power** — typically 80%
- **MDE (Minimum Detectable Effect)** — smallest effect you care about
- **Traffic** — daily eligible users
- **Duration** — run until sufficient sample size

### 6. Define Decision Criteria

| Result | Action |
|--------|--------|
| Primary metric improves, guardrails hold | Ship |
| Primary metric flat, secondary improves | Iterate (refine and re-test) |
| Primary metric declines | Kill |
| Inconclusive (low power) | Extend or increase traffic |

### 7. Document Risks

- What could invalidate results? (seasonality, external events)
- Confounding factors?
- Technical implementation risks?

## Output

An **Experiment Design Doc** with:

| Section | Content |
|---------|---------|
| Hypothesis | Full hypothesis statement |
| Variants | Control and treatment definitions |
| Primary Metric | Main success metric |
| Secondary Metrics | Supporting metrics |
| Guardrail Metrics | Metrics that must not regress |
| Sample Size | Required sample per variant |
| Duration | Estimated run length |
| Decision Criteria | Ship / iterate / kill thresholds |
| Risks | What could invalidate results |
