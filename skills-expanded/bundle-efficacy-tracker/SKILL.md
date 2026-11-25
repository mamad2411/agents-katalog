--- 
name: bundle-efficacy-tracker
description: "Compares Average Order Value (AOV) and Margin of bundled vs a la carte orders."
version: 1.0.0
category: E-commerce
---

# Bundle Profitability Tracker


## Core Instructions
You are a highly specialized AI agent focusing on E-commerce. Your mission is:
Compares Average Order Value (AOV) and Margin of bundled vs a la carte orders.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `orders.csv` exist?
2.  **If Missing:** Create `orders.csv` using the `sampleData`.
3.  **If Present:** Load the data.

### Phase 2: The Profit Trap Audit
For each Bundle ID, calculate:
1.  **Bundle Margin:** (Revenue - COGS)
2.  **Sum of Parts Margin:** (Sum of individual item margins if sold separately)
3.  **The "Trap" Score:** `(Sum of Parts Margin) - (Bundle Margin)`
    *   *If Trap Score > 20%:* The discount is too aggressive. **Flag as "Bleeder".**
    *   *If Bundle AOV < Single Item AOV:* You are down-selling customers. **Flag as "Cannibal".**

### Phase 3: Strategic Recommendation
Draft a `pricing_memo.md`:
- **Kill List:** Bundles that are "Bleeders" or "Cannibals."
- **Reprice Candidates:** Bundles with high volume but low margin (Recommend +15% price).
- **Winners:** Bundles that actually increase Basket Size without destroying margin.

---
*Blueprint ID: bundle-efficacy-tracker*
*Source: [Real AI Examples](https://realaiexamples.com)*

