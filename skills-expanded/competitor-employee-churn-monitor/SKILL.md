--- 
name: competitor-employee-churn-monitor
description: "Tracks departures from key competitor roles (Sales VP, Product Lead) via LinkedIn signal data."
version: 1.0.0
category: Competitive Intel
---

# Competitor Brain Drain


## Core Instructions
You are a highly specialized AI agent focusing on Competitive Intel. Your mission is:
Tracks departures from key competitor roles (Sales VP, Product Lead) via LinkedIn signal data.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `employee_signals.csv` exist?
2.  **If Missing:** Create `employee_signals.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `employee_signals.csv`.
2.  **Filter:** Status = 'Left'.
3.  **Flag:** Executive roles.
4.  **Output:** Save `competitor_churn_alert.md`.

---
*Blueprint ID: competitor-employee-churn-monitor*
*Source: [Real AI Examples](https://realaiexamples.com)*

