---
name: benchmark-statistical-analysis
description: Use when BenchmarkDotNet results must be interpreted beyond raw means — covering distributions, effect size, error bounds, outlier decisions, and confidence adequacy for promotion decisions.
---

# BenchmarkDotNet Statistical Analysis

## Specialization

Use this skill to produce distribution-aware, statistically sound interpretations of BenchmarkDotNet results.

This skill is specialized for result interpretation and confidence assessment. It does not design benchmarks or configure CI gates.

## Objective

Produce one deterministic interpretation verdict from BenchmarkDotNet output, with explicit confidence level, effect size assessment, outlier rationale, and recommendation.

## Trigger Conditions

- Raw BenchmarkDotNet output is available and a decision must be drawn from it.
- Claimed performance improvements require statistical validation before acceptance.
- Results have high error or stddev and confidence adequacy is unclear.
- Outliers have been detected and removal rationale must be documented.
- Results from multiple runs must be reconciled into one verdict.

## Scope Boundaries

In scope:

- Distribution analysis: mean, median, standard deviation, error, confidence intervals.
- Effect size assessment and practical significance versus statistical significance.
- Outlier detection, classification, and removal rationale.
- Ratio interpretation (`Ratio` and `RatioSD` columns).
- Allocation and GC column interpretation alongside time metrics.
- Confidence adequacy: when results are strong enough to support a decision.

Out of scope:

- Benchmark design changes and structural improvements (use `benchmark-experiment-design`).
- CI gate configuration and threshold enforcement (use `benchmark-ci-integration`).
- Release promotion sign-off (use `benchmark-quality-gate`).

## Inputs

- BenchmarkDotNet results table (markdown, CSV, or artifact link).
- Baseline method identifier and candidate method identifiers.
- Decision being informed and required confidence level.
- Outlier configuration used during the run.
- Prior results for regression comparison (if available).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Distribution summary: mean, median, stddev, error, and confidence interval per method.
- Ratio analysis: Ratio and RatioSD interpretation with practical significance ruling.
- Allocation verdict: allocation delta and GC pressure assessment.
- Outlier disposition: detected outliers, classification, and removal rationale or rejection.
- Confidence adequacy verdict: strong / weak / insufficient with blocking conditions listed.
- One interpretation recommendation: accept, reject, or inconclusive with explicit rationale.

## Statistical Interpretation Rules

**Treat results as distributions, not single numbers.**

### Primary Signal Priority

1. `Error` (half-width of confidence interval) — if error is large relative to mean, evidence is weak.
2. `StdDev` — spread; high stddev signals environmental noise or benchmark design flaws.
3. `Ratio` and `RatioSD` — relative comparison to baseline; the primary decision signal.
4. `Mean` / `Median` — absolute values; use median when outlier influence is suspected.
5. `Allocated` — allocation delta; a faster method that allocates more may create GC pressure that offsets time gains.

### Effect Size Assessment

| Ratio Range | Practical Significance |
|---|---|
| < 0.85 or > 1.18 | Material difference; strong evidence |
| 0.85–0.95 or 1.05–1.18 | Moderate difference; meaningful but not dramatic |
| 0.95–1.05 | Negligible; within noise band — do not declare a winner |

### Overlap Rule

If confidence intervals of baseline and candidate overlap substantially, the evidence is insufficient regardless of mean difference. Do not declare a winner from overlapping distributions.

### Outlier Policy

- `Default` (BDN default): removes upper and lower outliers automatically.
- `DontRemove`: retains all samples; use when outlier behavior is relevant (e.g., p99 latency).
- `RemoveUpper`: removes upper outliers only; appropriate for throughput-focused benchmarks.
- Rationale for non-default outlier configuration must be stated explicitly.
- Removing outliers without rationale to improve a result is disallowed.

### Confidence Adequacy Verdicts

| Verdict | Condition |
|---|---|
| Strong | Ratio > 1.10 or < 0.90, error < 5% of mean, RatioSD < 0.05, no overlapping CIs |
| Weak | Ratio 0.90–0.95 or 1.05–1.10, or error 5–10% of mean, or mild CI overlap |
| Insufficient | Ratio 0.95–1.05, or error > 10% of mean, or substantial CI overlap |

When confidence is Insufficient, the benchmark must be re-run with environment improvements before a decision is drawn.

## Allocation and GC Interpretation

- Allocation reduction is always positive when accompanied by equivalent or better time.
- Allocation increase requires explicit justification even when time improves.
- Gen0/Gen1/Gen2 column changes must be assessed alongside `Allocated` for GC pressure impact.
- A method with zero Gen0 collections is preferred when both options are otherwise equivalent.

## Result Replication Policy

- Never declare a result from a single run.
- A minimum of two independent runs on the same machine under consistent conditions is required.
- Results that disagree across runs by more than 10% in ratio require investigation before decision.

## Interpretation Report Template

```markdown
## Benchmark: [BenchmarkClassName]
## Run Date: [YYYY-MM-DD]
## Decision: [What this informs]

### Distribution Summary
| Method | Mean | Median | StdDev | Error | Allocated |
|---|---|---|---|---|---|
| Baseline | | | | | |
| Candidate | | | | | |

### Ratio Analysis
- Ratio: [value] (RatioSD: [value])
- Practical Significance: [Material / Moderate / Negligible]
- CI Overlap: [None / Partial / Substantial]

### Outlier Disposition
- Configuration: [Default / DontRemove / RemoveUpper]
- Outliers Detected: [count and direction]
- Rationale: [why removed or retained]

### Allocation Verdict
- Allocated Delta: [+/- bytes]
- GC Pressure Change: [Gen0/Gen1/Gen2 delta]
- Assessment: [Positive / Neutral / Concern]

### Confidence Adequacy
- Verdict: [Strong / Weak / Insufficient]
- Blocking Conditions: [list or None]

### Recommendation
- Decision: [Accept candidate / Reject candidate / Inconclusive — re-run required]
- Rationale: [one sentence]
```

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Distribution-aware interpretation | Statistical Interpretation Rules |
| Effect size and practical significance | Effect Size Assessment |
| Outlier policy and rationale | Outlier Policy |
| Allocation and GC assessment | Allocation and GC Interpretation |
| Confidence adequacy ruling | Confidence Adequacy Verdicts |
| One deterministic recommendation | Interpretation Report Template |

## Sources

- [Andrey Akinshin's Blog](https://aakinshin.net/) — statistical interpretation, effect size, distribution analysis
- [Perfolizer Docs](https://github.com/AndreyAkinshin/perfolizer) — outlier detection and distribution modeling
- [BenchmarkDotNet Docs](https://benchmarkdotnet.org/articles/overview.html) — column definitions and outlier configuration
