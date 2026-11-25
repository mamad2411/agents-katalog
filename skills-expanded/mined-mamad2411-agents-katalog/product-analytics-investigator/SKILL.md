---
name: product-analytics-investigator
description: Use when a PM, data PM, or analyst needs to investigate product metrics in Amplitude or Mixpanel — diagnosing drops in activation, retention, or funnel conversion, or attributing changes to releases, segments, or experiments. Pulls events, runs cohort/funnel analysis, and writes a root-cause memo.
---

# Product Analytics Investigator

## When to invoke
- "Why did activation drop last week?"
- "Investigate the checkout funnel for mobile users."
- "Compare retention before/after the v4.2 release."

## Inputs needed
1. **Metric or funnel** under investigation (event names + ordering).
2. **Time window** (default: last 14 days vs prior 14 days).
3. **Segments to slice by** (platform, plan, country, cohort).
4. **Hypotheses** (optional) — release dates, experiments, marketing pushes.

If any are missing, ask the user once before running.

## Workflow
1. **Frame** — restate the metric, window, baseline, and segments.
2. **Pull data** — call `investigate.py` (Amplitude/Mixpanel API or warehouse).
3. **Decompose** — break the change by segment, surface, and step.
4. **Correlate** — overlay releases, experiments, incidents.
5. **Report** — produce a memo: TL;DR, evidence, top 3 hypotheses ranked by likelihood, recommended next steps.

## Output format
```
## TL;DR
<one sentence: what changed, by how much, who is affected>

## Evidence
- Funnel step deltas (table)
- Top contributing segments
- Timeline overlay with releases/experiments

## Hypotheses (ranked)
1. <hypothesis> — supporting evidence — confidence
2. ...

## Recommended next steps
- [ ] Owner — Action — ETA
```

## Guardrails
- Never claim causation from correlation alone. Surface confounders.
- Always show absolute counts alongside percentages.
- Flag low-sample segments (n < 100) explicitly.

## Reference code
See `investigate.py` for a runnable funnel + cohort comparison against Amplitude or Mixpanel APIs (or a CSV export).
