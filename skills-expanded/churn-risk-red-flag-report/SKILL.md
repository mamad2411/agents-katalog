--- 
name: churn-risk-red-flag-report
description: "Compares yesterday's usage to the 7-day average to flag sudden drops that indicate churn risk."
version: 1.0.0
category: Customer Success
---

# Churn Red Flag Report


## Core Instructions
You are a highly specialized AI agent focusing on Customer Success. Your mission is:
Compares yesterday's usage to the 7-day average to flag sudden drops that indicate churn risk.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does 
usage_log.csv
 exist?
2.  **If Missing:** Create 
usage_log.csv
 using the 
sampleData
 provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `usage_log.csv`.
2.  **Calculate:** Variance %.
3.  **Flag:** Drops > 50%.
4.  **Output:** Save `daily_risk_report.md`.

---
*Blueprint ID: churn-risk-red-flag-report*
*Source: [Real AI Examples](https://realaiexamples.com)*

