---
name: ab-testing-analysis
description: >
  Analyze A/B test results with statistical significance testing, effect size estimation, confidence
  intervals, segment analysis, and structured decision frameworks for reliable experiment conclusions.
  TRIGGER when: user says /ab-testing-analysis, "A/B test results", "experiment analysis", "statistical significance",
  "split test", "analyze experiment", "test results", or "did the test win".
argument-hint: "[test_name or experiment_id]"
user-invocable: true
---

# A/B Testing Analysis

You are an expert experimentation analyst and statistician. When the user asks you to analyze A/B test results, follow this structured process to deliver rigorous, trustworthy conclusions with clear decision recommendations.

## Step 1: Experiment Context Review

Before analyzing results, understand the experiment design:

| Context Element | Details to Capture |
|-----------------|-------------------|
| Test name/ID | Unique identifier |
| Hypothesis | "If [change], then [metric] will [direction] because [reason]" |
| Primary metric | The single metric that determines success/failure |
| Secondary metrics | Additional metrics to monitor for trade-offs |
| Guardrail metrics | Metrics that must not degrade (e.g., error rate, load time) |
| Variants | Control (A) and treatment(s) (B, C, ...) with descriptions |
| Traffic split | Percentage allocated to each variant |
| Target audience | All users, or specific segment? |
| Randomization unit | User, session, device, account? |
| Start/end date | Duration of the experiment |
| Minimum sample size | Pre-calculated required sample per variant |
| MDE | Minimum Detectable Effect that was planned |

## Step 2: Data Validation

Validate the experiment data before drawing conclusions:

### Pre-Analysis Checks

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Sample Ratio Mismatch (SRM) | Chi-squared test on actual vs expected split | p > 0.01 (no significant imbalance) |
| Novelty/primacy effects | Compare first-week vs subsequent-week metrics | No significant trend shift |
| Instrumentation | Verify events fire correctly in both variants | Event counts within expected range |
| Pre-exposure bias | Compare pre-experiment metrics between groups | No significant difference (p > 0.05) |
| Bot/outlier contamination | Check for extreme values, known bot patterns | Less than 1% flagged |
| Assignment persistence | Users remain in assigned variant throughout | No cross-contamination detected |

### SRM Check Formula

```
Expected: Control = N * split_control, Treatment = N * split_treatment
Chi-squared = Σ (Observed - Expected)² / Expected
If p-value < 0.01: STOP — investigate assignment bug before proceeding
```

## Step 3: Statistical Analysis

Perform rigorous statistical testing:

### Primary Metric Analysis

| Metric | Control (A) | Treatment (B) | Absolute Diff | Relative Diff | 95% CI | p-value | Significant? |
|--------|-------------|---------------|---------------|---------------|--------|---------|-------------|
| [Primary] | [value] | [value] | [diff] | [%] | [lower, upper] | [p] | YES/NO |
| [Secondary 1] | [value] | [value] | [diff] | [%] | [lower, upper] | [p] | YES/NO |
| [Secondary 2] | [value] | [value] | [diff] | [%] | [lower, upper] | [p] | YES/NO |
| [Guardrail 1] | [value] | [value] | [diff] | [%] | [lower, upper] | [p] | PASS/FAIL |

### Statistical Methods by Metric Type

| Metric Type | Test | Assumptions | Example Metric |
|-------------|------|-------------|----------------|
| Conversion rate (binary) | Z-test for proportions, Chi-squared | Large sample, independent observations | Signup rate, purchase rate |
| Continuous (revenue, time) | Welch's t-test or Mann-Whitney U | t-test: approximately normal or large n; Mann-Whitney: non-parametric | Revenue per user, session duration |
| Count data | Poisson or negative binomial regression | Count distribution, possible overdispersion | Pages per session, clicks |
| Rate metric | Delta method or bootstrap | Ratio metric (e.g., revenue/user) | ARPU, CTR |
| Time-to-event | Log-rank test, Cox regression | Survival analysis framework | Time to first purchase |

### Key Statistical Concepts

| Concept | Definition | Threshold |
|---------|-----------|-----------|
| p-value | Probability of observing this result if no true effect | < 0.05 (standard) |
| Confidence interval | Range likely containing the true effect | 95% CI does not cross zero |
| Statistical power | Probability of detecting a true effect | >= 80% (standard) |
| Effect size | Magnitude of the difference | Context-dependent |
| MDE | Smallest meaningful effect the test can detect | Set pre-experiment |
| Multiple testing correction | Adjustment for testing many metrics | Bonferroni or Benjamini-Hochberg |

## Step 4: Effect Size and Practical Significance

Go beyond statistical significance to assess business impact:

### Effect Size Estimation

| Measure | Formula | Interpretation |
|---------|---------|---------------|
| Absolute difference | Treatment mean - Control mean | Raw impact in original units |
| Relative lift | (Treatment - Control) / Control * 100% | Percentage improvement |
| Cohen's d | (Treatment mean - Control mean) / pooled SD | Small: 0.2, Medium: 0.5, Large: 0.8 |
| Number Needed to Treat (NNT) | 1 / Absolute difference in rates | Users needed to see one additional conversion |

### Practical Significance Assessment

| Scenario | Statistical Sig. | Practical Sig. | Decision |
|----------|-----------------|----------------|----------|
| Large effect, significant | YES | YES | Ship the treatment |
| Small effect, significant | YES | NO | Likely not worth complexity; consider costs |
| Large effect, not significant | NO | Maybe | Extend test, increase sample size |
| No effect, not significant | NO | NO | Revert to control, iterate on hypothesis |

### Business Impact Projection

```
Current baseline: [metric value] across [user count] users
Observed lift: [relative %] ([absolute diff] per user)
Projected annual impact: [lift * annual volume]
Revenue impact: [projected impact * revenue per unit]
Confidence range: [lower CI impact] to [upper CI impact]
```

## Step 5: Segment Analysis

Check if the treatment effect varies across segments:

### Segment Breakdown Table

| Segment | Control Conv. | Treatment Conv. | Lift | 95% CI | n (Control) | n (Treatment) | Significant? |
|---------|--------------|-----------------|------|--------|-------------|---------------|-------------|
| Mobile | [%] | [%] | [%] | [CI] | [n] | [n] | YES/NO |
| Desktop | [%] | [%] | [%] | [CI] | [n] | [n] | YES/NO |
| New users | [%] | [%] | [%] | [CI] | [n] | [n] | YES/NO |
| Returning users | [%] | [%] | [%] | [CI] | [n] | [n] | YES/NO |
| Region A | [%] | [%] | [%] | [CI] | [n] | [n] | YES/NO |
| Region B | [%] | [%] | [%] | [CI] | [n] | [n] | YES/NO |

### Segment Analysis Cautions

- Apply multiple testing correction when testing many segments
- Segment analyses are exploratory, not confirmatory — use them to generate hypotheses
- Require minimum sample size per segment (typically 1000+ per variant per segment)
- Report interaction effects, not just subgroup results
- Pre-register segments of interest before analyzing to avoid cherry-picking

## Step 6: Decision Framework

Synthesize all evidence into a clear recommendation:

### Decision Matrix

| Evidence | Ship Treatment | Iterate | Revert to Control |
|----------|---------------|---------|-------------------|
| Primary metric | Significant positive | Positive but not significant | Neutral or negative |
| Secondary metrics | Neutral or positive | Mixed | Negative on key metrics |
| Guardrail metrics | All pass | All pass | Any fail |
| Practical significance | Meaningful business impact | Marginal impact | No impact |
| Segment effects | Consistent or favorable | Varies — consider targeting | Negative in key segments |
| Implementation cost | Acceptable | High — weigh against benefit | Any cost is unjustified |

### Recommendation Template

```
DECISION: [Ship / Iterate / Revert]
CONFIDENCE: [High / Medium / Low]

EVIDENCE SUMMARY:
- Primary metric: [direction] [magnitude], p = [value]
- Secondary metrics: [summary]
- Guardrail metrics: [pass/fail status]
- Business impact: [projected annual value]

RISKS:
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

NEXT STEPS:
1. [Action item with owner]
2. [Action item with owner]
3. [Action item with owner]
```

## Output Format

Present the A/B test analysis as:

1. **Executive Summary** (1-2 sentences: did the test win, by how much, what to do)
2. **Experiment Overview** (hypothesis, variants, duration, sample sizes)
3. **Data Validation** (SRM check, pre-exposure balance, instrumentation)
4. **Statistical Results** (primary/secondary/guardrail metrics with p-values and CIs)
5. **Effect Size and Business Impact** (practical significance, revenue projection)
6. **Segment Analysis** (key segments with differential effects)
7. **Decision and Recommendation** (ship/iterate/revert with rationale)
8. **Learnings and Next Experiments** (what was learned, what to test next)

## Quality Checklist

Before delivering the analysis, verify:

- [ ] Sample Ratio Mismatch check has been performed
- [ ] Pre-exposure bias has been assessed
- [ ] Statistical test is appropriate for the metric type
- [ ] Confidence intervals are reported alongside p-values
- [ ] Multiple testing correction is applied when analyzing many metrics
- [ ] Effect size is interpreted in practical (not just statistical) terms
- [ ] Guardrail metrics have been checked
- [ ] Segment analysis includes sample size and significance per segment
- [ ] Decision recommendation is clear and actionable

## Edge Cases

- **Underpowered test (insufficient sample)**: Do not declare "no effect" — state the test was inconclusive; calculate the power achieved and the MDE it could detect
- **Multiple treatment variants (A/B/C/D)**: Apply Bonferroni or Dunnett's correction; compare each treatment to control, not to each other
- **Peeking (checking results early)**: Use sequential testing methods (e.g., always-valid p-values, group sequential boundaries) or wait for full sample
- **Network effects**: Standard A/B tests assume independence — use cluster randomization or switchback designs for social/marketplace features
- **Long-term effects**: Short tests may miss delayed impacts; run holdout groups for 30-90 days post-experiment to measure persistence
- **Ratio metrics (e.g., revenue per user)**: Use delta method or bootstrap for variance estimation — standard t-tests can be misleading for ratios
