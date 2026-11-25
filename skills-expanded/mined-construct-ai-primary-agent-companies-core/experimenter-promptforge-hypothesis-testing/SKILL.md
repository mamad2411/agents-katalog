---
name: experimenter-promptforge-hypothesis-testing
description: >
  Use when designing and executing experiments to test hypotheses about prompt
  effectiveness, AI behavior, or technique performance. This skill provides
  scientific experimentation frameworks with controlled variables, measurable
  outcomes, and statistically valid conclusions.
---

# Experimenter - Hypothesis Testing & Innovation

## Overview
Experimenter designs and executes scientific experiments for PromptForge AI. Every claim about prompt effectiveness, technique superiority, or AI behavior should be tested rigorously—not assumed. Experimenter ensures experiments are well-designed, results are valid, and conclusions are evidence-based.

## When to Use
- When testing whether a new prompt technique is better than existing approaches
- When validating claims about AI model behavior or capabilities
- When comparing multiple prompt strategies to find the best one
- When investigating why a prompt works (or doesn't work)
- When building evidence for best practices or recommendations
- **Don't use when:** Making incremental improvements without a testable hypothesis (use refiner-promptforge-version-control)

## Core Procedures

### Step 1: Formulate Hypothesis
Write a clear, testable hypothesis:
```
HYPOTHESIS
==========
Null Hypothesis (H0): [no difference between approaches]
Alternative Hypothesis (H1): [specific expected difference]
Independent Variable: [what we're changing]
Dependent Variable: [what we're measuring]
Control Variables: [what we're keeping constant]
Success Criteria: [what result would reject H0]
```

### Step 2: Design Experiment
- **Control Group:** Baseline approach (current best practice)
- **Treatment Group(s):** New approach being tested
- **Sample Size:** Minimum 30 trials per group for statistical significance
- **Randomization:** Randomly assign inputs to control/treatment groups
- **Blinding:** If possible, evaluators shouldn't know which group produced each output

### Step 3: Execute Experiment
1. Prepare test dataset (diverse, representative inputs)
2. Run control group trials, record all outputs and metrics
3. Run treatment group trials, record all outputs and metrics
4. Ensure identical conditions for both groups (same model, temperature, etc.)
5. Document any anomalies or unexpected behavior

### Step 4: Analyze Results
- Calculate mean, median, standard deviation for each group
- Perform statistical test (t-test for 2 groups, ANOVA for 3+)
- Calculate effect size (Cohen's d) - is the difference practically significant?
- Check for confounding variables that might explain results
- Determine p-value and whether to reject H0

### Step 5: Document and Share
```
EXPERIMENT REPORT
=================
Hypothesis: [what was tested]
Method: [experiment design]
Sample Size: [number of trials per group]
Results: [statistical findings with p-values and effect sizes]
Conclusion: [reject or fail to reject H0]
Confidence Level: [how confident in the conclusion]
Limitations: [what might affect validity]
Recommendation: [adopt, reject, or further test the approach]
```

## Success Metrics
- Experiment completion rate: >=95% (experiments reach conclusion)
- Statistical validity: 100% of experiments meet minimum sample size requirements
- Reproducibility: >=90% of experiments produce same results when repeated
- Actionable conclusions: >=80% of experiments lead to clear recommendations

## Error Handling
- **Error:** Results are statistically insignificant (p > 0.05)
  **Response:** Increase sample size, check for high variance, consider if effect is too small to measure
- **Error:** Results contradict expectations
  **Response:** Don't discard—investigate why, check for confounding variables, this may reveal important insights
- **Error:** Experiment conditions can't be controlled (model behavior changes mid-experiment)
  **Response:** Pause experiment, document the change, restart with stable conditions

## Cross-Team Integration
**Related Skills:** explorer-promptforge-new-techniques, scholar-promptforge-academic-research, tuner-promptforge-ab-testing, quantifier-promptforge-benchmarking, analyzer-promptforge-prompt-analytics
**Used By:** Explorer, Scholar, Tuner, Quantifier, Analyzer, Sage