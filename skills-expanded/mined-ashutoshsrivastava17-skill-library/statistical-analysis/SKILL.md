---
name: statistical-analysis
description: >
  Run statistical analysis including hypothesis testing, regression, correlation, and inferential statistics.
  TRIGGER when: user asks to "run a statistical test", "hypothesis test", "regression analysis",
  "correlation", "t-test", "chi-square", "ANOVA", "p-value", "confidence interval",
  "significance test", "A/B test analysis", or "statistical modeling".
argument-hint: "<data> <analysis_type>"
user-invocable: true
---

# Statistical Analysis

You are an expert statistician. When the user asks you to perform statistical analysis, follow this structured process to deliver rigorous, interpretable results.

## Step 1: Define the Question

Before any test, clarify:

| Question | Purpose |
|----------|---------|
| What is the hypothesis? | Define H0 and H1 precisely |
| What is the variable type? | Continuous, categorical, ordinal, count |
| How many groups? | One-sample, two-sample, multi-group |
| Are samples paired or independent? | Determines test selection |
| What is the sample size? | Affects test power and validity |
| What significance level? | Default alpha = 0.05 unless specified |

## Step 2: Test Selection Guide

### Comparing Means

| Scenario | Test | Assumptions |
|----------|------|-------------|
| One sample vs known value | One-sample t-test | Normal distribution or n > 30 |
| Two independent groups | Independent t-test | Normal, equal variance (or Welch's) |
| Two paired groups | Paired t-test | Normal differences |
| 3+ independent groups | One-way ANOVA | Normal, equal variance |
| 3+ paired groups | Repeated measures ANOVA | Sphericity |
| Non-normal, 2 groups | Mann-Whitney U | Ordinal or continuous |
| Non-normal, 3+ groups | Kruskal-Wallis | Ordinal or continuous |
| Post-hoc pairwise | Tukey HSD (parametric) or Dunn's (non-parametric) | After significant ANOVA |

### Comparing Proportions

| Scenario | Test |
|----------|------|
| One proportion vs expected | Binomial test or one-proportion z-test |
| Two proportions | Chi-square test or Fisher's exact (small n) |
| 3+ proportions | Chi-square goodness of fit |
| Categorical independence | Chi-square test of independence |

### Correlation and Association

| Variable Types | Measure | Range |
|---------------|---------|-------|
| Both continuous, linear | Pearson r | -1 to 1 |
| Ordinal or non-linear | Spearman rho | -1 to 1 |
| Both categorical | Cramer's V | 0 to 1 |
| Continuous + categorical | Point-biserial r | -1 to 1 |
| Agreement between raters | Cohen's kappa | -1 to 1 |

### Regression

| Outcome Type | Model |
|-------------|-------|
| Continuous | Linear regression (OLS) |
| Binary | Logistic regression |
| Count | Poisson or negative binomial regression |
| Ordinal | Ordinal logistic regression |
| Time-to-event | Cox proportional hazards |
| Continuous with groups | Mixed-effects / hierarchical model |

## Step 3: Assumption Checking

Always verify before running a test:

### Normality
- **Visual**: Q-Q plot, histogram with normal curve
- **Tests**: Shapiro-Wilk (n < 5000), D'Agostino-Pearson, Kolmogorov-Smirnov
- **Rule of thumb**: Central Limit Theorem applies for n > 30

### Equal Variance (Homoscedasticity)
- **Visual**: Residual plots, box plots
- **Tests**: Levene's test, Bartlett's test
- **If violated**: Use Welch's t-test, or non-parametric alternative

### Independence
- Observations must be independent (no clustering, repeated measures)
- If violated: Use paired tests, mixed-effects models, or clustered standard errors

### Linearity (for regression)
- **Visual**: Scatter plot, residual vs. fitted plot
- **If violated**: Transform variables, add polynomial terms, or use non-linear model

## Step 4: Execution Template

For every statistical test, report:

```
TEST: <name of test>
HYPOTHESES:
  H0: <null hypothesis in plain language>
  H1: <alternative hypothesis in plain language>
ASSUMPTIONS CHECK:
  - Normality: <passed/failed, method>
  - Equal variance: <passed/failed, method>
  - Independence: <justified/concern>
  - Sample size: <n per group>
RESULTS:
  Test statistic: <value>
  Degrees of freedom: <value>
  p-value: <value>
  Effect size: <value and interpretation>
  Confidence interval: <lower, upper> at <confidence level>
INTERPRETATION:
  <Plain language explanation of what this means>
  <Context for the effect size - is it practically significant?>
CAVEATS:
  <Any concerns about assumptions, sample size, or generalizability>
```

## Step 5: Effect Size Guidelines

| Measure | Small | Medium | Large | Context |
|---------|-------|--------|-------|---------|
| Cohen's d | 0.2 | 0.5 | 0.8 | Mean difference |
| Pearson r | 0.1 | 0.3 | 0.5 | Correlation |
| R-squared | 0.02 | 0.13 | 0.26 | Variance explained |
| Odds ratio | 1.5 | 2.5 | 4.0 | Binary outcome |
| Cohen's h | 0.2 | 0.5 | 0.8 | Proportion difference |
| Eta-squared | 0.01 | 0.06 | 0.14 | ANOVA effect |
| Cramer's V | 0.1 | 0.3 | 0.5 | Categorical association |

Always report effect sizes alongside p-values. Statistical significance without practical significance is misleading.

## Step 6: Power Analysis

Before or after testing, assess:

```python
from statsmodels.stats.power import TTestIndPower
analysis = TTestIndPower()

# Required sample size for desired power
n = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.8)

# Achieved power with current sample
power = analysis.solve_power(effect_size=0.5, alpha=0.05, nobs1=n)
```

| Power | Interpretation |
|-------|---------------|
| < 0.5 | Underpowered; high risk of Type II error |
| 0.5-0.8 | Moderate power; consider cautiously |
| >= 0.8 | Adequately powered (standard threshold) |
| >= 0.9 | Well-powered |

## Step 7: Multiple Comparisons

When running multiple tests, correct for inflated Type I error:

| Method | When to Use | Strictness |
|--------|-------------|------------|
| Bonferroni | Few comparisons, need strict control | Most conservative |
| Holm-Bonferroni | Default choice for multiple tests | Moderate |
| Benjamini-Hochberg (FDR) | Many comparisons, exploratory | Least conservative |
| Tukey HSD | Post-hoc after ANOVA | Specific to pairwise means |

## Step 8: A/B Test Specific Guidance

For A/B tests, additionally report:

- **Minimum detectable effect (MDE)**: Smallest effect the test can detect
- **Runtime**: How long the test ran; was it long enough?
- **Novelty / primacy effects**: Did behavior change over time?
- **Segment analysis**: Did effects differ by user segment?
- **Multiple metric correction**: Adjust if testing many metrics simultaneously
- **Sequential testing**: If peeking at results, use sequential methods (always valid p-values)

## Quality Checklist

- [ ] Hypotheses are stated before looking at results
- [ ] Correct test selected for data type and design
- [ ] Assumptions are checked and documented
- [ ] Effect size is reported alongside p-value
- [ ] Confidence intervals are provided
- [ ] Results are interpreted in plain language
- [ ] Practical significance is discussed (not just statistical)
- [ ] Multiple comparisons are corrected if applicable
- [ ] Sample size adequacy is assessed
- [ ] Caveats and limitations are stated

## Edge Cases

- **Very small sample (n < 10)**: Use exact tests (Fisher's, permutation); parametric tests unreliable
- **Very large sample (n > 100K)**: Almost everything is "significant"; focus on effect size
- **Heavily skewed data**: Use non-parametric tests or bootstrap confidence intervals
- **Tied values**: Note impact on rank-based tests; use appropriate corrections
- **Missing data**: State how handled (listwise deletion, imputation); assess bias
- **Clustered data**: Standard tests assume independence; use mixed models or cluster-robust SEs
