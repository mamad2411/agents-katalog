---
name: data-statistical-analysis
version: 1.0.0
description: Run descriptive stats, trend, outlier, correlation, and hypothesis tests with correct method selection and honest effect sizes.
author: matrixx0070
tags: [statistics, hypothesis-testing, correlation, trend, outliers, effect-size]
capabilities: []
---

# data-statistical-analysis

## When to use

Use this when a decision rides on whether an effect is signal or noise: "is this difference real?", "are these correlated?", "is the trend significant?", "which points are outliers?" Reach for it instead of eyeballing a chart.

**Not for:** the raw business answer without rigor (use data-analyze), profiling data quality (use data-explore), or building the chart itself (use data-create-viz).

## Method

1. **Frame the question statistically:** estimation, comparison, association, or trend. State the population and unit of analysis.
2. **Describe first.** Report n, center (mean/median), spread (SD/IQR), and shape. Visualize the distribution before testing.
3. **Choose the test by data type and assumptions:**
   - Two-group means → t-test (Welch if variances differ); non-normal/small → Mann-Whitney.
   - >2 groups → ANOVA / Kruskal-Wallis.
   - Categorical association → chi-square / Fisher (small cells).
   - Numeric association → Pearson (linear) or Spearman (monotonic).
   - Trend → regression, test the slope.
   Decision point: check normality, independence, and variance; if an assumption fails, drop to the nonparametric option.
4. **Report effect size and confidence interval,** not just p. A significant p with a trivial effect is not actionable.
5. **Outliers:** detect (IQR or z-score), investigate cause, decide keep/exclude with justification — never drop silently.
6. **Correct for multiple comparisons** (Bonferroni/BH) when running many tests.

## Example

A/B test: control 4.0% conversion (n=5,000), variant 4.6% (n=5,000). Two-proportion z-test → p=0.03. But the 95% CI on the lift is [+0.05pp, +1.15pp] — the effect could be near-zero. Verdict: statistically significant, practically marginal; ship only if the +0.6pp point estimate clears the cost of the change.

## Pitfalls

- Reporting p<0.05 with no effect size, implying an important result from a trivial one.
- Running a t-test on skewed or tiny samples where its normality assumption fails.
- Reading correlation as causation, ignoring a confounder.
- Testing 20 metrics, celebrating the one that hits p<0.05, and not correcting for multiplicity.

## Output format

```
Question:      hypothesis in plain + statistical terms
Descriptives:  n, center, spread, distribution shape
Test:          method + why + assumption checks
Result:        statistic, p-value, effect size, confidence interval
Interpretation: what it means for the decision, plain language
Caveats:       sample size, violated assumptions, confounders
```

Distinguish statistical from practical significance. Say when the sample is too small to conclude anything.
