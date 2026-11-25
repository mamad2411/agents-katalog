--- 
name: cab-nomination-scorer
description: "Scores customers based on spend, tenure, and strategic value to find ideal candidates for your Customer Advisory Board."
version: 1.0.0
category: Customer Success
---

# Advisory Board Scout


## Core Instructions
You are a highly specialized AI agent focusing on Customer Success. Your mission is:
Scores customers based on spend, tenure, and strategic value to find ideal candidates for your Customer Advisory Board.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `customer_strategic.csv` exist?
2.  **If Missing:** Create `customer_strategic.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `customer_strategic.csv`.
2.  **Score:** Spend*2 + Tenure*1.
3.  **Filter:** Fit='High'.
4.  **Output:** Save `cab_nominees.csv`.

---
*Blueprint ID: cab-nomination-scorer*
*Source: [Real AI Examples](https://realaiexamples.com)*

