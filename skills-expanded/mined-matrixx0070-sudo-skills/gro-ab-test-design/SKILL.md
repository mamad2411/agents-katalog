---
name: gro-ab-test-design
version: 1.0.0
description: Design a rigorous A/B test with a falsifiable hypothesis, one primary metric, MDE, sample size, and guardrails.
author: matrixx0070
tags: [growth, experimentation, ab-testing, statistics, causal]
capabilities: []
---

## When to use

Use this before shipping any change where you need *causal proof* it helped — pricing, onboarding, copy, layout, algorithm changes. Use it whenever a wrong decision is expensive or the effect is too small to see by eyeballing a chart.

**Not for:** prioritizing which idea to test first (use gro-growth-experiment / ICE), no-brainer bug fixes, or changes with too little traffic to ever reach significance — there, ship and monitor, or run a holdout. Also not for measuring long-run retention shifts without a long enough horizon.

## Method

1. Write a falsifiable hypothesis: "Because [insight], changing [X] will improve [primary metric] for [population]." One primary metric only.
2. Choose the primary metric at the decision altitude (e.g. activation rate, not clicks). Pick guardrail metrics that must NOT regress (revenue, latency, refunds, unsubscribes).
3. Set the MDE (minimum detectable effect) = the smallest lift worth shipping, from a cost/benefit view — not a guess. Decision point: if the MDE is smaller than plausible reality, the test is underpowered; widen scope or accept a longer run.
4. Compute sample size per arm. Two-proportion rule of thumb: n ≈ 16 × p(1−p) / (MDE_absolute)². Use α=0.05, power=0.80. Decision point: if required runtime > 4 weeks, reduce arms, raise MDE, or target a higher-traffic surface.
5. Define assignment (unit = user, sticky, hashed), split, and duration covering ≥1 full business cycle (usually 1–2 weeks) to avoid day-of-week bias.
6. Pre-register the stop rule: fixed horizon OR a sequential test. Decision point: never peek-and-stop on a fixed-horizon test. Pre-declare how you'll handle a guardrail breach (auto-rollback).

## Example

Hypothesis: adding social proof to signup lifts signup completion. Baseline p=20%, MDE=+2pp (to 22%). n ≈ 16 × 0.2 × 0.8 / 0.02² = 16 × 0.16 / 0.0004 = 6,400 per arm → 12,800 total. At 1,000 signups/day that's ~13 days; round to 14 to cover two weekly cycles. Guardrails: paid-conversion and support tickets flat.

## Pitfalls

- Tracking many metrics and celebrating whichever wins (multiple comparisons → false positives). One primary, pre-declared.
- Peeking daily and stopping at first significance — inflates false-positive rate massively.
- Running less than a full weekly cycle, so weekday/weekend mix skews the result.
- Ignoring a guardrail regression because the primary metric won.

## Output format

```
Hypothesis: Because <insight>, <change> will improve <primary metric> for <population>.
Primary metric:  <metric> | Baseline: <p>
Guardrails:      <m1 flat/up>, <m2 flat/up>
MDE:             <+X pp / +Y%> (rationale: <cost/benefit>)
Sample size:     <n>/arm, <total> total
Assignment:      unit=<user>, split=<50/50>, sticky, hashed
Duration:        <days> (≥1 business cycle)
Stop rule:       <fixed horizon N | sequential>; rollback if <guardrail breach>
Decision rule:   ship if primary +≥MDE at p<0.05 AND guardrails intact
```
