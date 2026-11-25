---
name: ab-experiment-design
description: When the agent needs to design an A/B test, split test, feature experiment, or growth test — hypotheses worth testing, sample-size honesty, and designs that produce decisions instead of noise.
department: Product
source: helm
---

# A/B Experiment Design

You design experiments like a growth team with a statistician on staff: strong hypotheses from real evidence, power math done BEFORE launch, and pre-committed decision rules that make peeking pointless.

## Operating principles

1. **A hypothesis is a causal sentence with a stake**: "Because [evidence — 62% of drop-off happens on the plan page], we believe [change — leading with the annual-discount toggle] will [effect — raise plan-page conversion] for [segment], measured by [metric], and we'll ship if [threshold]." No evidence clause → it's a guess; go get evidence first.
2. **Power math before launch, always.** Required sample per arm ≈ 16σ²/δ² (or for proportions: n ≈ 16·p(1−p)/δ² at 80% power, α=0.05, two-sided). Practical translation: detecting a 2-pt lift on a 10% baseline needs ~3,600/arm; on 500 visitors/week that's a 15-week test — meaning DON'T run it; test something bigger or on a higher-traffic step. Underpowered tests aren't "directional", they're random number generators with branding.
3. **One primary metric, pre-registered.** Decided before launch: primary metric, minimum detectable effect you care about, run length (full weeks, ≥ 1 and enough for the sample), guardrails (latency, churn, support contacts). Post-hoc metric shopping across 20 metrics guarantees a false "win" (at α=0.05, ~1 in 20 lies to you).
4. **No peeking, no early stopping on excitement.** Check for BREAKAGE daily (sample-ratio mismatch, error spikes); evaluate RESULTS once at the pre-set end. A "significant" day-3 result that dies by day 14 is regression to the mean doing its job.

## Workflow

1. Source the hypothesis from evidence (funnel data, session replays, research findings) — rank candidate tests by expected-impact × evidence-strength ÷ runtime.
2. Do the power math with REAL traffic numbers; if runtime > 4 weeks, escalate the change's boldness or move upstream in the funnel.
3. Pre-register: hypothesis card (the sentence above), primary + guardrails, MDE, dates, decision rule (ship / iterate / kill thresholds), segment.
4. Implementation checks: random assignment at the right unit (user/account — account for B2B to avoid contamination), sticky bucketing, both arms deployed simultaneously, sample-ratio check at 24 h (a 50/50 split showing 47/53 = instrumentation bug, halt).
5. Readout: effect size with confidence interval (not just p-value), guardrail status, segment sanity-cuts (pre-declared only). Decision per the rule. Log it in the experiment registry — including losers (a killed bad idea is ROI).

## Output contract

Deliver: the hypothesis card · power calculation with real numbers and the runtime verdict · pre-registration block · implementation checklist (assignment unit, SRM check) · readout template with the decision rule filled in · registry entry.

## Quality bar

- No test launches without power math and a pre-registered decision rule.
- Effect sizes reported with intervals; "trending toward significance" is banned language.
- The registry accumulates: every test ends in ship/iterate/kill with the learning captured in one sentence.
