---
name: quantifier-promptforge-benchmarking
description: >
  Use when establishing performance benchmarks, measuring prompt KPIs, creating
  standardized evaluation datasets, and tracking prompt performance against targets.
  This skill provides benchmarking frameworks for consistent prompt measurement.
---

# Quantifier - Performance Benchmarking & KPIs

## Overview
Quantifier establishes and tracks performance benchmarks for PromptForge AI. Without benchmarks, you can't tell if a prompt is good, bad, or improving. Quantifier creates the measurement standards that make prompt quality objective and comparable.

## When to Use
- When establishing baseline performance for a new prompt
- When creating standardized evaluation datasets for prompt testing
- When defining KPIs for prompt engineering teams or projects
- When comparing prompt performance across time, models, or teams
- When building benchmark reports for stakeholders
- **Don't use when:** Analyzing patterns in data (use analyzer-promptforge-prompt-analytics)

## Core Procedures

### Step 1: Define Benchmark Scope
- What are we benchmarking? (specific prompt, prompt category, entire system)
- What dimensions matter? (quality, speed, cost, reliability, user satisfaction)
- What is the comparison baseline? (previous version, industry standard, competitor)
- What is the target? (what performance level are we aiming for)

### Step 2: Create Evaluation Dataset
Build a representative test set:
- **Size:** Minimum 50 inputs for statistical reliability
- **Diversity:** Cover all input types, edge cases, and common scenarios
- **Difficulty:** Mix of easy, medium, and hard inputs
- **Gold Standard:** Each input has a known correct output or evaluation criteria
- **Versioned:** Dataset is versioned and changes are tracked

### Step 3: Run Benchmark
Execute the prompt against the evaluation dataset:
1. Run prompt on each input (automated where possible)
2. Score each output against gold standard
3. Calculate aggregate metrics (mean, median, std dev, percentiles)
4. Record resource usage (tokens, cost, latency)
5. Document any failures or anomalies

### Step 4: Compare Against Targets
```
BENCHMARK REPORT
================
Prompt: [name and version]
Date: [when benchmark was run]
Dataset: [name and version]
Metrics:
  Quality Score: [X/100] (Target: [Y/100]) [PASS/FAIL]
  Latency (p50): [X ms] (Target: [Y ms]) [PASS/FAIL]
  Cost per Call: [$X] (Target: [$Y]) [PASS/FAIL]
  Reliability: [X%] (Target: [Y%]) [PASS/FAIL]
Overall: [PASS/FAIL]
Comparison to Previous: [improved/same/regressed by X%]
```

### Step 5: Track Benchmark Trends
- Run benchmarks on a regular schedule (weekly, monthly, per release)
- Track metric trends over time
- Alert when metrics drop below targets
- Celebrate when metrics exceed targets

## Success Metrics
- Benchmark coverage: 100% of production prompts have established benchmarks
- Benchmark frequency: All benchmarks run at least monthly
- Target achievement rate: >=90% of prompts meet their quality targets
- Trend visibility: All metrics have visible trend charts with 3+ months of data

## Error Handling
- **Error:** Benchmark results are inconsistent (high variance)
  **Response:** Increase dataset size, check for input quality issues, review scoring criteria for consistency
- **Error:** Benchmark dataset becomes outdated (no longer representative)
  **Response:** Update dataset with new input types, re-run benchmark, note the dataset change
- **Error:** Prompt fails benchmark (below target)
  **Response:** Do not deploy to production, identify root cause, fix and re-benchmark

## Cross-Team Integration
**Related Skills:** analyzer-promptforge-prompt-analytics, tuner-promptforge-ab-testing, clarity-promptforge-performance-optimization, testing-strategy
**Used By:** Analyzer, Tuner, Clarity, Sage, ALL agents who need to measure prompt performance