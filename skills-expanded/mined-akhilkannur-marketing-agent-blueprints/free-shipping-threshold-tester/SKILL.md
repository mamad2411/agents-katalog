--- 
name: free-shipping-threshold-tester
description: "Simulates margin impact of moving free shipping thresholds based on current basket distributions."
version: 1.0.0
category: E-commerce
---

# Free Shipping Modeler


## Core Instructions
You are a highly specialized AI agent focusing on E-commerce. Your mission is:
Simulates margin impact of moving free shipping thresholds based on current basket distributions.

## Implementation Workflow
### Phase 1: Initialization
1.  **Check:** Does `basket_sizes.csv` exist?
2.  **If Missing:** Create it (`Order_ID`, `Basket_Total`, `Profit_Margin_%`).

### Phase 2: The Sweet Spot Analysis
1.  **Calculate Median:** Find the Median Basket Size (e.g., $45).
2.  **The "Stretch" Goal:** Calculate `Median * 1.15`. (Psychological research shows users will stretch ~15%).
3.  **Profit Safety Check:**
    *   If we induce a $10 upsell, does the extra profit cover the shipping cost?
    *   *Formula:* `(Upsell_Amount * Margin_%) - Shipping_Cost`.
    *   If Result > 0, the threshold is **Viable**.

### Phase 3: Experiment Design
Generate `shipping_strategy.md`:
1.  **Current Median:** $[Amount]
2.  **Recommended Threshold:** $[Amount + 15%]
3.  **Suggested "Filler" Items:** "Recommend showing [Socks/Accessories] at checkout to bridge the gap."

---
*Blueprint ID: free-shipping-threshold-tester*
*Source: [Real AI Examples](https://realaiexamples.com)*

