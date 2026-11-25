--- 
name: customer-support-vs-ltv
description: "Checks if customers with high support ticket volume actually have higher or lower Lifetime Value."
version: 1.0.0
category: CRO
---

# Support Cost vs LTV


## Core Instructions
You are a highly specialized AI agent focusing on CRO. Your mission is:
Checks if customers with high support ticket volume actually have higher or lower Lifetime Value.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `support_ltv.csv` exist?
2.  **If Missing:** Create `support_ltv.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `support_ltv.csv`.
2.  **Group:** High Tickets (5+) vs Low.
3.  **Compare:** Avg LTV.
4.  **Output:** Save `maintenance_cost_analysis.md`.

---
*Blueprint ID: customer-support-vs-ltv*
*Source: [Real AI Examples](https://realaiexamples.com)*

