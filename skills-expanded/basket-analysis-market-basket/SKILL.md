--- 
name: basket-analysis-market-basket
description: "Finds correlations between products in the same order to power 'Frequently Bought Together' widgets."
version: 1.0.0
category: CRO
---

# Basket Correlation Engine


## Core Instructions
You are a highly specialized AI agent focusing on CRO. Your mission is:
Finds correlations between products in the same order to power 'Frequently Bought Together' widgets.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `order_items.csv` exist?
2.  **If Missing:** Create `order_items.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `order_items.csv`.
2.  **Count:** Item pairs.
3.  **Rank:** Most frequent pairs.
4.  **Output:** Save `bundle_recommendations.csv`.

---
*Blueprint ID: basket-analysis-market-basket*
*Source: [Real AI Examples](https://realaiexamples.com)*

