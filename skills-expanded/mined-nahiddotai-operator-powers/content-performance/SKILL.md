---
name: content-performance
description: Analyze content analytics, traffic, conversions, attribution, audience growth, or published assets to explain performance and choose evidence-based next experiments.
---

# Content Performance

Turn available content results into decisions while separating reach, engagement, conversion, and speculation.

## Job contract

- Owns: diagnosis from performance evidence.
- Does not own: refreshing one asset without metric analysis (`content-refresher`).
- Finished deliverable: normalized scorecard, supported findings, uncertainty, and next experiments.

## Required data disclosure

If no real performance metrics are available, say so at the top of the response before offering any interpretation:

> No real performance data was available. This review uses [name the alternative evidence] instead, so it can assess [what that evidence supports] but not reach, engagement, conversion, revenue, or causality.

Name the result a `Content Evidence Review`, not a performance review. Do not fill the scorecard with invented proxies. If the user needs performance conclusions, list the smallest data export or fields required to produce them.

## Workflow

1. Establish the business goal, period, channels, content set, audience size, distribution, and conversion definition.
2. Validate units, dates, denominators, attribution windows, missing values, and duplicates.
3. Separate reach, attention, engagement, intent, conversion, and revenue.
4. Compare like with like. Use rates and baselines where raw totals mislead.
5. Look for patterns across topic, format, opening, proof, CTA, timing, and distribution.
6. Distinguish confirmed findings, directional indications, and unsupported stories.
7. Recommend a small experiment queue with decision rules.

## Output

```markdown
# Content Performance Review

## Goal And Data Quality
[Objective, coverage, gaps]

## Scorecard
[Comparable metrics and baselines]

## What The Evidence Supports
[Findings with numbers]

## What It Does Not Prove
[Attribution and sample limits]

## Keep, Change, Stop, Test
[Specific decisions]

## Next Experiments
[Hypothesis, asset, metric, threshold, duration]
```

## Guardrails

- Empty attribution is not evidence that reach caused sales or subscribers.
- Do not compare raw counts across unequal audience sizes without noting the bias.
- Never invent missing metrics or causal explanations.
