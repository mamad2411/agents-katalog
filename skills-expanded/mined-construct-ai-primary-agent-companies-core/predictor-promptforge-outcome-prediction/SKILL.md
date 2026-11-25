---
name: predictor-promptforge-outcome-prediction
description: >
  Use when forecasting prompt performance, predicting failure modes, assessing risks
  before deployment, and modeling the likely outcomes of prompt engineering decisions.
  This skill provides predictive analytics frameworks for proactive decision-making.
---

# Predictor - Outcome Prediction & Risk Assessment

## Overview
Predictor forecasts outcomes and assesses risks for PromptForge AI. Rather than waiting for problems to occur, Predictor identifies likely failure modes, performance issues, and risks before deployment—enabling proactive mitigation.

## When to Use
- Before deploying a new prompt to predict likely failure modes
- When assessing the risk level of a prompt change
- When forecasting how a prompt will perform at scale
- When evaluating whether a prompt is ready for production
- When modeling the impact of prompt changes on downstream systems
- **Don't use when:** Reacting to an already-occurred failure (use incident-response)

## Core Procedures

### Step 1: Define Prediction Scope
- What outcome are we predicting? (quality, performance, cost, user satisfaction)
- What is the deployment context? (volume, user type, model, environment)
- What time horizon? (immediate, 1 week, 1 month, 1 quarter)
- What confidence level is needed? (rough estimate vs. high-confidence forecast)

### Step 2: Gather Historical Data
Collect relevant historical evidence:
- Similar prompts and their performance history
- Failure modes observed in comparable prompts
- Performance data at different scales
- User feedback patterns for similar use cases
- Model behavior changes over time

### Step 3: Build Prediction Model
Apply prediction techniques:
- **Pattern Matching:** How do similar prompts behave?
- **Trend Analysis:** Is performance improving or degrading over time?
- **Scenario Modeling:** Best case, expected case, worst case
- **Risk Scoring:** Probability × Impact for each identified risk
- **Confidence Intervals:** Range of likely outcomes with confidence levels

### Step 4: Generate Prediction Report
```
PREDICTION REPORT
=================
Prompt/System: [name and version]
Prediction Type: [quality/performance/cost/risk]
Time Horizon: [when this prediction applies]
Expected Outcome: [most likely result with confidence interval]
Best Case: [optimistic scenario]
Worst Case: [pessimistic scenario]
Key Risks: [top 3 risks with probability and impact]
Confidence Level: [how confident in this prediction]
Evidence Base: [what data supports this prediction]
Recommendation: [proceed/proceed with caution/do not proceed]
```

### Step 5: Validate Predictions
After deployment, compare predictions to actual outcomes:
- Were predictions accurate? (within confidence intervals)
- Which risks materialized? Which didn't?
- What was missed in the prediction?
- How can prediction models be improved?

## Success Metrics
- Prediction accuracy: >=80% of predictions fall within confidence intervals
- Risk detection rate: >=90% of significant risks identified before deployment
- False positive rate: <20% (predicted risks that don't materialize)
- Prediction lead time: >=24 hours before deployment for standard predictions

## Error Handling
- **Error:** Prediction confidence is low (insufficient historical data)
  **Response:** Flag as low-confidence, recommend pilot deployment with close monitoring
- **Error:** Prediction contradicts stakeholder expectations
  **Response:** Present evidence base transparently, explain methodology, recommend cautious approach
- **Error:** Actual outcome differs significantly from prediction
  **Response:** Investigate why, update prediction model, document the discrepancy for future improvement

## Cross-Team Integration
**Related Skills:** risk-assessment, integrity-promptforge-ethical-ai, compliance-promptforge-regulatory-compliance, quantifier-promptforge-benchmarking, analyzer-promptforge-prompt-analytics
**Used By:** Integrity, Compliance, Quantifier, Analyzer, Sage, ALL agents before deployment