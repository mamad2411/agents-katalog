---
name: tuner-promptforge-ab-testing
description: >
  Use when running A/B tests on prompts, comparing prompt variants, statistically
  validating performance differences, and optimizing prompts through experimental
  testing. This skill provides rigorous A/B testing frameworks for prompt engineering.
---

# Tuner - Performance Optimization & A/B Testing

## Overview
Tuner runs A/B tests for PromptForge AI. When you need to know which of two prompt variants performs better, Tuner designs and executes statistically valid experiments that produce actionable answers.

## When to Use
- When choosing between two or more prompt variants
- When testing whether a prompt change improves performance
- When optimizing prompt parameters (temperature, max tokens, structure)
- When validating that a new prompt is genuinely better (not just different)
- When fine-tuning prompt elements through systematic testing
- **Don't use when:** Designing experiments with hypotheses (use experimenter-promptforge-hypothesis-testing)

## Core Procedures

### Step 1: Define Test Parameters
```
A/B TEST DESIGN
===============
Test Name: [descriptive name]
Variant A (Control): [current prompt]
Variant B (Treatment): [new prompt]
Metric: [what we're measuring - quality score, task success, user satisfaction]
Sample Size: [calculated based on expected effect size]
Significance Level: [alpha = 0.05]
Power: [1 - beta = 0.80]
Duration: [how long to run the test]
```

### Step 2: Calculate Sample Size
Use power analysis to determine required sample size:
- Expected effect size (small=0.2, medium=0.5, large=0.8)
- Significance level (typically 0.05)
- Statistical power (typically 0.80)
- Result: minimum samples per variant

### Step 3: Run the Test
- Randomly assign inputs to Variant A or B
- Ensure equal distribution across input types
- Run until minimum sample size is reached
- Don't peek and stop early (inflates false positive rate)
- Monitor for technical issues (one variant failing, data collection errors)

### Step 4: Analyze Results
- Calculate mean metric for each variant
- Run statistical test (t-test for continuous metrics, chi-square for categorical)
- Calculate p-value and confidence interval
- Calculate effect size (Cohen's d)
- Determine winner: statistically significant AND practically significant

### Step 5: Decide and Act
- **A Wins:** Keep control, document why B failed, archive B
- **B Wins:** Deploy B, document improvement, update baseline
- **No Difference:** Either variant is fine, choose simpler/cheaper one
- **Inconclusive:** Increase sample size, check for implementation issues

## Success Metrics
- Test completion rate: >=95% of tests reach conclusion
- Statistical validity: 100% of tests meet minimum sample size
- False positive rate: <5% (tests that declared winner incorrectly)
- Average test duration: <24 hours for standard tests

## Error Handling
- **Error:** Test results are not statistically significant
  **Response:** Check if sample size was sufficient, if effect size was overestimated, consider running longer or accepting no difference
- **Error:** One variant has technical failures
  **Response:** Fix the technical issue, restart the test, don't compare broken vs working
- **Error:** Results show B is worse than A (regression)
  **Response:** Document what made B worse, this is valuable information—keep A, learn from the failure

## Cross-Team Integration
**Related Skills:** experimenter-promptforge-hypothesis-testing, clarity-promptforge-performance-optimization, quantifier-promptforge-benchmarking, analyzer-promptforge-prompt-analytics
**Used By:** Experimenter, Clarity, Quantifier, Analyzer, Sage, ALL agents comparing prompt variants