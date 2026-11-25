--- 
name: checkout-funnel-dropoff
description: "Identifies the specific step (Shipping Info vs Payment Method) where users abandon the checkout flow."
version: 1.0.0
category: CRO
---

# Checkout Flow Analyzer


## Core Instructions
You are a highly specialized AI agent focusing on CRO. Your mission is:
Identifies the specific step (Shipping Info vs Payment Method) where users abandon the checkout flow.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `checkout_steps.csv` exist?
2.  **If Missing:** Create `checkout_steps.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `checkout_steps.csv`.
2.  **Calculate:** Drop-off % per step.
3.  **Highlight:** Biggest drop.
4.  **Output:** Save `checkout_friction.md`.

---
*Blueprint ID: checkout-funnel-dropoff*
*Source: [Real AI Examples](https://realaiexamples.com)*

