---
name: statistical-analysis
description: Applies statistical methods — descriptive statistics, trend analysis, outlier/anomaly detection, hypothesis testing, correlation, distribution analysis — to numeric data. Make sure to use this skill whenever the user says is this statistically significant, what's the trend, are there outliers, detect anomalies, run a t-test, compare these distributions, is this correlated, is this normal/skewed, baseline for [metric], or describes any analytical question that requires more than averaging numbers. For cybersecurity contexts, supports anomaly detection (logins, network traffic, alert volumes), baseline establishment, and signal-vs-noise analysis. Do NOT use for: SQL queries to pull data (use data:sql-queries first), visualization without analysis (use data:create-viz), formal A/B test results writeup (this skill produces inputs; final writeup chains to other skills), or simple averaging/sorting (just do it). Defining characteristic: "the question requires statistical method, not just arithmetic."
---

# Statistical Analysis

Statistical methods for numeric data — descriptive, trend, outlier/anomaly, hypothesis testing, correlation.

## When to use vs. adjacent data skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Question requires statistical method | Just need to pull data → `data:sql-queries` |
| Significance testing, distribution analysis | Just visualize already-analyzed data → `data:create-viz` |
| Outlier or anomaly detection | Profiling a new dataset for shape → `data:explore-data` |
| Trend analysis with confidence intervals | Validating an analysis for stakeholders → `data:validate-data` |

## Statistical methods this skill applies

### Descriptive (the foundation)
- Central tendency (mean, median, mode — and when each is right)
- Spread (range, IQR, variance, standard deviation)
- Distribution shape (skewness, kurtosis)
- Quantiles and percentiles
- Always state n (sample size) — single most-omitted statistic

### Trend
- Linear regression with R² and confidence intervals
- Moving averages (simple, exponential weighted)
- Seasonality detection
- Change point detection
- Rate of change with significance

### Outlier / anomaly detection
- IQR-based (Tukey fences: 1.5× or 3× IQR)
- Z-score based (typically |z| > 3)
- Modified Z-score (MAD-based, robust to existing outliers)
- Isolation Forest for multivariate
- Time-series anomaly: STL decomposition + residual analysis

### Hypothesis testing
- Choose the right test:
  - Compare 2 group means → t-test (independent or paired)
  - Compare 3+ group means → ANOVA
  - Compare proportions → chi-square or Fisher's exact
  - Non-normal distributions → Mann-Whitney U or Kruskal-Wallis
  - Compare distributions → Kolmogorov-Smirnov
- State the null and alternative hypotheses explicitly
- Report effect size, not just p-value (p<0.05 with tiny effect ≠ meaningful)
- Power analysis if requested or if results are null

### Correlation
- Pearson (linear, normal data)
- Spearman (rank, non-parametric)
- Kendall's tau (small samples or many ties)
- Always state: correlation ≠ causation; potential confounders

### Distribution checks
- Normality: Shapiro-Wilk for n<5000, Q-Q plot visual always
- Goodness of fit to other distributions when relevant

## Cybersecurity-specific applications

### Login anomaly detection
- Establish baseline (per user, per role, per geography, per time-of-day)
- Compute z-score on login frequency, time, location, device
- Flag |z| > 3 for review
- Adjust thresholds per role sensitivity (admin accounts tighter)

### Network traffic baselining
- Per-endpoint or per-service baseline
- Detect deviation as unusual traffic pattern
- Seasonality awareness (business hours vs. nights/weekends)

### Alert volume normalization
- Aggregate alerts by source, severity, asset class
- Compare against rolling baseline
- Surface unusual spikes for review (alert-on-alerts)
- Reduce alert fatigue by tuning frequency thresholds

### Compliance metric trending
- Control evidence freshness over time
- Open finding aging
- Time-to-remediation trends

## Output structure

Every analysis produces:

```markdown
# [Question / topic]

## TL;DR
[One sentence with the answer.]

## Method
[What test / method, why this one over alternatives]

## Results
- n: [sample size]
- [statistic]: [value with confidence interval]
- p-value: [if applicable]
- Effect size: [Cohen's d, eta-squared, r — depending on test]

## Interpretation
[What the numbers mean in domain terms]

## Caveats
- Assumptions checked / violated
- Confounders not controlled
- Sample limitations
- What this does NOT tell you

## Recommended next step
[Either a follow-on analysis or a domain action]
```

## Common mistakes this skill avoids

- **p-value worship** — significance without effect size is misleading
- **Multiple comparisons without correction** — Bonferroni or FDR when running many tests
- **Confusing correlation with causation** — flag potential confounders
- **Assuming normality without checking** — test or plot first
- **Tiny n with huge claims** — n=8 doesn't support strong inference
- **Ignoring base rates** — "10 anomalies out of 10,000" reads differently than "10 out of 50"
- **Mean when median is honest** — outliers distort means

## Output

1. Structured analysis above
2. The actual numbers + tests
3. Recommended visualization (chains to `data:create-viz`)
4. Caveats explicit
5. Suggested follow-up analysis or action
