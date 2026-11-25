--- 
name: cross-sell-recommender
description: "Identifies customers who bought a specific primary product (e.g., Tent) but have NOT yet bought the accessory (e.g., Footprint)."
version: 1.0.0
category: Retention
---

# Cross-Sell Recommender


## Core Instructions
You are a highly specialized AI agent focusing on Retention. Your mission is:
Identifies customers who bought a specific primary product (e.g., Tent) but have NOT yet bought the accessory (e.g., Footprint).

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `purchase_history.csv` exist?
2.  **If Missing:** Create `purchase_history.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `purchase_history.csv`.
2.  **Filter:** Bought 'Tent' AND NOT 'Footprint'.
3.  **Output:** Save `cross_sell_footprint.csv`.

---
*Blueprint ID: cross-sell-recommender*
*Source: [Real AI Examples](https://realaiexamples.com)*

