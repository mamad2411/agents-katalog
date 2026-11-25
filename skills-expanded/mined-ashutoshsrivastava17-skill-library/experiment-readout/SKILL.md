---
name: experiment-readout
description: >
  Write experiment result readouts with hypothesis recap, methodology,
  statistical results, business interpretation, and recommendations.
  Structure for stakeholder communication of A/B test and experiment outcomes.
  TRIGGER when: user says /experiment-readout, "experiment readout",
  "experiment results", "A/B test results", or "test readout".
argument-hint: "[experiment name]"
user-invocable: true
---

# Experiment Readout

You are a data scientist preparing an experiment results readout for stakeholders. Present findings clearly, distinguish between statistical significance and practical significance, and deliver actionable recommendations grounded in data.

## Process

### Step 1: Experiment Overview

Summarize the experiment setup:

| Field | Details |
|-------|---------|
| Experiment name | Descriptive name and experiment ID |
| Hypothesis | What we expected to happen and why |
| Primary metric | The key metric being measured |
| Secondary metrics | Supporting metrics and guardrail metrics |
| Test duration | Start date, end date, and total runtime |
| Sample size | Number of users or observations per variant |
| Variants | Control and treatment descriptions |
| Traffic allocation | Percentage of traffic in each variant |
| Target population | Who was eligible for the experiment (segments, regions, platforms) |
| Owner | Who designed and ran the experiment |

### Step 2: Methodology

Document how the experiment was conducted:

| Aspect | Details |
|--------|---------|
| Experiment type | A/B test, multivariate, bandit, switchback, quasi-experiment |
| Randomization unit | User, session, device, region |
| Assignment method | Random, hash-based, stratified |
| Minimum detectable effect (MDE) | Smallest effect size the experiment was powered to detect |
| Statistical power | Target power (typically 80%) and achieved power |
| Significance level | Alpha threshold (typically 0.05) |
| Correction method | Bonferroni, Holm, FDR, or none (and why) |
| Analysis method | Frequentist (t-test, chi-squared), Bayesian, CUPED, regression |

### Step 3: Results

Present results for each metric:

#### Primary Metric

| Metric | Control | Treatment | Absolute Diff | Relative Diff | p-value | CI (95%) | Significant? |
|--------|---------|-----------|:---:|:---:|:---:|:---:|:---:|
| *metric name* | *value* | *value* | *diff* | *%* | *p* | *[lower, upper]* | Yes/No |

#### Secondary Metrics

| Metric | Control | Treatment | Relative Diff | p-value | Significant? | Direction |
|--------|---------|-----------|:---:|:---:|:---:|-----------|
| *metric 1* | *value* | *value* | *%* | *p* | Yes/No | Positive/Negative/Neutral |

#### Guardrail Metrics

| Guardrail Metric | Control | Treatment | Relative Diff | Threshold | Status |
|------------------|---------|-----------|:---:|-----------|--------|
| *e.g., page load time* | *value* | *value* | *%* | < 5% regression | Pass/Fail |
| *e.g., error rate* | *value* | *value* | *%* | < 1% increase | Pass/Fail |

### Step 4: Validity Checks

Verify the experiment ran correctly:

| Check | Result | Status |
|-------|--------|--------|
| Sample ratio mismatch (SRM) | Expected vs. actual split | Pass/Fail |
| Pre-experiment balance | Metric values before treatment | Balanced/Imbalanced |
| Novelty/primacy effects | Trend over experiment duration | Detected/Not detected |
| Interaction effects | Conflicts with concurrent experiments | None/Detected |
| Data quality | Missing data, logging issues, bot traffic | Clean/Issues found |

### Step 5: Interpretation

Translate statistical results into business meaning:

| Question | Answer |
|----------|--------|
| Did the treatment work? | Yes/No/Inconclusive -- with supporting evidence |
| Is the effect practically significant? | Is the observed lift large enough to matter for the business? |
| Who benefited most? | Segment-level analysis (platform, region, user type) |
| Were there negative side effects? | Guardrail metric degradation or segment-level harm |
| What explains the result? | Causal mechanism or behavioral hypothesis |
| What don't we know? | Limitations, confounds, or unanswered questions |

### Step 6: Recommendation

Provide a clear recommendation:

| Decision | Criteria |
|----------|----------|
| **Ship** | Primary metric significantly positive, no guardrail failures, practically significant lift |
| **Iterate** | Directionally positive but not significant, or significant but with guardrail concerns |
| **Do not ship** | No improvement, negative impact, or guardrail failures |
| **Extend experiment** | Insufficient power, inconclusive results, need more data |

## Output Format

Structure the readout for stakeholder consumption:

1. **TL;DR** -- one-paragraph summary: what we tested, what happened, what we recommend (lead with the decision)
2. **Experiment Overview** -- hypothesis, metrics, duration, and population
3. **Results Summary** -- primary and secondary metric tables
4. **Validity Checks** -- confirmation the experiment ran correctly
5. **Segment Analysis** -- how results varied across key dimensions
6. **Interpretation** -- what the results mean for the business
7. **Recommendation** -- ship, iterate, or do not ship, with rationale
8. **Next Steps** -- follow-up experiments, monitoring plan, or rollout strategy
9. **Appendix** -- detailed statistical tables, methodology notes, and raw data references

## Quality Checklist

- [ ] Hypothesis is stated clearly and was defined before the experiment ran
- [ ] Primary metric was pre-registered, not chosen post-hoc
- [ ] Sample size and runtime met the pre-calculated requirements
- [ ] Validity checks (SRM, balance, novelty) have been performed
- [ ] Confidence intervals are reported alongside p-values
- [ ] Practical significance is discussed, not just statistical significance
- [ ] Guardrail metrics are checked and reported
- [ ] Segment analysis looks for heterogeneous treatment effects
- [ ] Recommendation is clear, actionable, and supported by evidence
- [ ] Limitations and caveats are honestly stated

## Edge Cases

- **Under-powered experiments**: Report observed effect size and confidence interval; recommend extending rather than drawing conclusions from noise
- **Multiple testing**: Apply correction methods and report both corrected and uncorrected p-values; be transparent about the number of metrics tested
- **Significant guardrail regression**: Even if the primary metric is positive, flag the guardrail failure prominently and discuss trade-offs
- **Novelty or primacy effects**: If the time-series trend shows decay or ramp-up, note this and recommend waiting for stabilization before deciding
- **Contradictory results across segments**: Report overall and segment results; do not cherry-pick favorable segments unless there is a pre-registered hypothesis for heterogeneous effects
- **Experiments stopped early**: Flag the risk of inflated effect sizes and recommend caution in interpretation
