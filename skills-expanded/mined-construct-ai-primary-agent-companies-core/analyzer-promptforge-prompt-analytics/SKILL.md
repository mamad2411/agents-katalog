---
name: analyzer-promptforge-prompt-analytics
description: >
  Use when analyzing prompt performance data, interpreting success metrics,
  identifying patterns in prompt effectiveness, and generating actionable insights
  from prompt analytics. This skill transforms raw data into prompt engineering intelligence.
---

# Analyzer - Prompt Analytics & Success Metrics

## Overview
Analyzer interprets prompt performance data for PromptForge AI. Raw metrics don't drive decisions—insights do. Analyzer transforms prompt analytics into actionable intelligence that guides prompt engineering strategy.

## When to Use
- When interpreting prompt performance metrics and dashboards
- When identifying patterns in prompt success/failure rates
- When generating analytics reports for stakeholders
- When investigating why a prompt's performance changed
- When building or refining prompt success metrics
- **Don't use when:** Collecting raw data (use automated systems) or setting benchmarks (use quantifier-promptforge-benchmarking)

## Core Procedures

### Step 1: Define Analysis Scope
- What question are we answering? (Why did performance drop? Which prompts are best? What drives success?)
- What data is available? (usage metrics, quality scores, user feedback, cost data)
- What time period? (last week, month, quarter, since launch)
- What segments matter? (by prompt type, by model, by domain, by user)

### Step 2: Collect and Clean Data
Gather relevant data sources:
- Prompt usage statistics (frequency, volume, trends)
- Quality scores (human ratings, automated evaluations)
- User feedback (satisfaction, complaints, suggestions)
- Cost data (token usage, API costs, compute time)
- Error rates (failures, retries, escalations)

### Step 3: Analyze Patterns
Apply analytical techniques:
- **Trend Analysis:** How are metrics changing over time?
- **Correlation Analysis:** What factors correlate with prompt success?
- **Segmentation Analysis:** Do patterns differ by prompt type, model, or domain?
- **Anomaly Detection:** Are there unusual spikes or drops that need investigation?
- **Root Cause Analysis:** For performance changes, what caused them?

### Step 4: Generate Insights
Transform patterns into actionable insights:
```
ANALYTICS INSIGHT
=================
Observation: [what the data shows]
Evidence: [specific data points supporting this]
Interpretation: [what this means]
Impact: [why this matters]
Recommendation: [what should be done]
Confidence: [how certain is this insight]
```

### Step 5: Report and Act
- Create analytics report with key findings
- Prioritize recommendations by impact and effort
- Share with relevant teams (Sage for strategy, Refiner for improvements, Tuner for optimization)
- Track whether recommendations are implemented and their impact

## Success Metrics
- Insight accuracy: >=90% of insights validated by follow-up data
- Actionable output: >=3 specific recommendations per analysis
- Analysis turnaround time: <4 hours for standard analyses
- Stakeholder satisfaction: >=85% find analytics reports useful

## Error Handling
- **Error:** Data is incomplete or unreliable
  **Response:** Note data quality issues, proceed with caveats, recommend data quality improvements
- **Error:** Analysis shows correlation but causation is unclear
  **Response:** Present as correlation only, recommend controlled experiment to establish causation
- **Error:** Insights contradict stakeholder expectations
  **Response:** Present data transparently, walk through methodology, recommend further investigation

## Cross-Team Integration
**Related Skills:** quantifier-promptforge-benchmarking, clarity-promptforge-performance-optimization, tuner-promptforge-ab-testing, predictor-promptforge-outcome-prediction
**Used By:** Quantifier, Clarity, Tuner, Predictor, Sage, ALL agents making data-driven decisions