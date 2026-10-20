---
name: claude-data-use-cases
description: Five high-value Claude data analysis use cases — Anomaly Investigation, Cohort Analysis, Funnel Diagnosis, Scenario Modeling, and Insight Extraction — with ready-to-use prompt templates for each. Use when the task is to analyse data and decide which analytical frame to apply.
---

# 5 Claude Data Use Cases

Source: iCloud Photos content analysis
Workflow: Raw Data → Patterns → Anomalies → Explanations → Decisions

---

## Use Case 1 — Anomaly Investigation

**What it does:** Finds unusual patterns worth investigating in your data.
**When to use:** Metrics moved unexpectedly and you don't know why.

```
Analyse this dataset and identify anomalies:

Data: [PASTE DATA OR DESCRIBE IT]
Time range: [RANGE]
Expected range / baseline: [WHAT NORMAL LOOKS LIKE]

1. Flag any values that fall outside expected range.
2. Identify the time, segment, or dimension where the anomaly appears.
3. List 3–5 possible causes, ranked by likelihood.
4. Suggest the next data slice to investigate each cause.
```

---

## Use Case 2 — Cohort Analysis

**What it does:** Compares groups across time to identify behavioural differences.
**When to use:** You want to understand retention, LTV, or engagement by user group.

```
Run a cohort analysis on this data:

Data: [PASTE DATA]
Cohort definition: [WHAT DEFINES A COHORT — signup week, acquisition channel, plan type, etc.]
Metric to track: [RETENTION / REVENUE / ENGAGEMENT / OTHER]
Time periods: [WEEKLY / MONTHLY / QUARTERLY]

1. Group users by cohort.
2. Calculate [METRIC] for each cohort at each time period.
3. Identify which cohorts perform best/worst.
4. Suggest 2–3 hypotheses that explain the difference.
```

---

## Use Case 3 — Funnel Diagnosis

**What it does:** Finds exactly where users disappear in your conversion funnel.
**When to use:** Conversion rate is lower than expected and you need to find the leak.

```
Diagnose this conversion funnel:

Funnel steps: [LIST STEPS IN ORDER]
Data: [STEP → USERS / CONVERSION RATE AT EACH STEP]
Goal: [FINAL CONVERSION EVENT]

1. Calculate the drop-off rate at each step.
2. Identify the biggest drop-off point.
3. List 3 possible reasons users exit at that step.
4. Suggest one experiment to test each hypothesis.
```

---

## Use Case 4 — Scenario Modeling

**What it does:** Stress-tests plans against optimistic, base-case, and pessimistic assumptions.
**When to use:** You need to pressure-test a forecast or decision before committing.

```
Build a scenario model for this decision:

Decision / plan: [DESCRIBE THE PLAN]
Key variables: [LIST THE INPUTS THAT DRIVE THE OUTCOME]
Outcome metric: [REVENUE / USERS / COST / OTHER]

Build three scenarios:
- Optimistic: [BEST-CASE ASSUMPTIONS]
- Base case: [MOST LIKELY ASSUMPTIONS]
- Pessimistic: [WORST-CASE ASSUMPTIONS]

For each scenario:
1. State the assumptions.
2. Project the outcome metric.
3. Identify the single biggest risk.
4. Suggest one mitigation.
```

---

## Use Case 5 — Insight Extraction

**What it does:** Finds the few numbers that actually matter out of all your data.
**When to use:** You have a large dataset or report and need to surface the signal.

```
Extract the key insights from this data:

Data / report: [PASTE OR DESCRIBE]
Business context: [WHAT DECISIONS THIS DATA INFORMS]
Audience: [WHO WILL READ THE INSIGHTS]

1. Identify the 3–5 most important findings.
2. For each, state: what it is, why it matters, what action it suggests.
3. Flag any data quality issues or gaps that might affect reliability.
4. Suggest one follow-up question worth investigating.
```

---

## Quick Selector

| Situation | Use case |
|---|---|
| "Something looks off" | Anomaly Investigation |
| "Are new users better than old users?" | Cohort Analysis |
| "Why isn't our funnel converting?" | Funnel Diagnosis |
| "What if the market turns?" | Scenario Modeling |
| "What does this data actually mean?" | Insight Extraction |
