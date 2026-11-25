--- 
name: activation-rate-cohort
description: "Tracks the percentage of users who reach 'Activation' within 7 days, grouped by signup month."
version: 1.0.0
category: Sales Ops
---

# Activation Rate by Cohort


## Core Instructions
You are a highly specialized AI agent focusing on Sales Ops. Your mission is:
Tracks the percentage of users who reach 'Activation' within 7 days, grouped by signup month.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `activation_data.csv` exist?
2.  **If Missing:** Create `activation_data.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `activation_data.csv`.
2.  **Calculate:** Activation Rate %.
3.  **Trend:** Compare MoM.
4.  **Output:** Save `activation_trends.csv`.

---
*Blueprint ID: activation-rate-cohort*
*Source: [Real AI Examples](https://realaiexamples.com)*

