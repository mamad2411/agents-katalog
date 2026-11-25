--- 
name: cart-abandonment-value-segmentation
description: "Splits cart abandoners into 'High Value' (for personal outreach) and 'Low Value' (for automated email)."
version: 1.0.0
category: Retention
---

# High-Value Cart Recovery


## Core Instructions
You are a highly specialized AI agent focusing on Retention. Your mission is:
Splits cart abandoners into 'High Value' (for personal outreach) and 'Low Value' (for automated email).

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `abandoned_carts.csv` exist?
2.  **If Missing:** Create `abandoned_carts.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `abandoned_carts.csv`.
2.  **Filter:** Total > $500.
3.  **Output:** Save `high_value_recovery.csv` for CS outreach.

---
*Blueprint ID: cart-abandonment-value-segmentation*
*Source: [Real AI Examples](https://realaiexamples.com)*

