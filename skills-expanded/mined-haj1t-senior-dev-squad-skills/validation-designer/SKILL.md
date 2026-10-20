---
name: validation-designer
description: "Design validation experiments, Lean Canvas, MVP scoping, success metrics, statistical analysis. Use when designing experiments to validate a product hypothesis."
version: 1.0.0
platforms: [linux, macos]
---

# Validation Designer

## What It Does
Designs rigorous validation experiments to test product hypotheses before committing significant resources. Generates Lean Canvases, scopes MVPs to the minimum necessary for learning, defines success metrics (North Star Metric, OKRs), and designs statistically valid experiments (A/B tests, feature flags, prototype tests, concierge tests).

## Iron Laws (NEVER violate)
1. **Learning over building** — The goal of validation is to learn, not to ship. Build the minimum necessary to answer the hypothesis.
2. **Falsifiable hypothesis** — Every experiment must have a hypothesis that can be proven wrong. "Users will like this" is not falsifiable.
3. **Success criteria before data** — Define what success looks like BEFORE running the experiment. No post-hoc goalpost moving.
4. **Fail fast, fail cheap** — Design experiments to fail in days, not months. The cost of being wrong should approach zero.

## Red Flags (STOP immediately)
- **Confirmation bias in design** — Experiment designed to prove the hypothesis right, not to test it honestly
- **MVP scope creep** — "Just one more feature" before testing → you're building, not validating
- **Vanity metric as success** — Using signups/pageviews when the hypothesis is about retention/engagement
- **No false-positive control** — No way to distinguish real signal from noise/novelty effect

## Common Rationalizations (self-deception)
- "We already know this will work" → If you already know, why test? The discomfort of testing reveals uncertainty.
- "A proper experiment takes too long" → A week of validation is cheaper than 6 months of building the wrong thing.
- "We'll learn as we build" → Building without hypothesis is expensive guessing. Experiments are cheap learning.

## When To Use
- User has a product idea and wants to validate before building
- Need to define MVP scope for a new feature
- Setting up success metrics for a product initiative
- Designing an A/B test with proper statistical rigor
- Evaluating whether a prototype test is sufficient vs full MVP

## Human Partner Signals (escalate to human)
- **Ethical experiment** — Experiment involves user data or behavior manipulation → ethics review
- **Revenue risk** — Experiment could impact paying customers → stakeholder approval
- **Statistical complexity** — Experiment requires advanced design (multi-arm bandit, factorial) → data science support
- **Scope decision** — MVP scope involves cutting features stakeholders expect → alignment meeting

## Pipeline
1. Frame: articulate the hypothesis in falsifiable form — "We believe [X] will cause [Y] for [segment], measured by [metric]"
2. Design: select experiment type (A/B, feature flag, prototype, concierge, wizard-of-oz, landing page)
3. Scope: define MVP — what's the absolute minimum to test the hypothesis? Cut everything else.
4. Metricize: define primary success metric, secondary metrics, and guardrail metrics (must not degrade)
5. Power: calculate required sample size and experiment duration for statistical significance
6. Execute: run experiment without peeking, collect data, analyze results
7. Decide: Pivot (hypothesis false), Persevere (hypothesis true), or Iterate (ambiguous, refine and retest)

## Verification Checklist
- [ ] Hypothesis is falsifiable (can be proven wrong by the experiment)
- [ ] Success criteria defined BEFORE experiment launch
- [ ] MVP scope contains only what's necessary to test the hypothesis (nothing extra)
- [ ] Sample size calculation completed with power analysis (α=0.05, β=0.2)
- [ ] Guardrail metrics identified to detect negative side effects
- [ ] Experiment duration set and no-peeking rule enforced

## Related Skills
- `opportunity-solver` — Opportunities identified feed into validation experiments
- `growth-engineer` — Growth experiments use the same validation methodology
- `roadmap-prioritizer` — Validated hypotheses get prioritized on the roadmap
- `spike` — Lightweight technical validation for implementation feasibility
