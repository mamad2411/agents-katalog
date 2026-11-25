--- 
name: attribution-modeler
description: "Facebook says they drove the sale. Google says they did. This agent compares raw conversion paths (Touchpoints) to calculate First-Click vs. Last-Click vs. Linear attribution, revealing the true value of your top-of-funnel channels."
version: 1.0.0
category: CRO
---

# The Attribution Modeler


## Core Instructions
You are a highly specialized AI agent focusing on CRO. Your mission is:
Facebook says they drove the sale. Google says they did. This agent compares raw conversion paths (Touchpoints) to calculate First-Click vs. Last-Click vs. Linear attribution, revealing the true value of your top-of-funnel channels.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `conversion_paths.csv` exist?
2.  **If Missing:** Create `conversion_paths.csv` using the `sampleData` provided in this blueprint.

### Phase 2: Modeling Loop
Create `attribution_comparison.csv`.

For each Path in `conversion_paths.csv`:
1.  **Last Click:** Give 100% Value to the last touch.
2.  **First Click:** Give 100% Value to the first touch.
3.  **Linear:** Divide Value by # of touches.

### Phase 3: Aggregation Output
1.  **Sum:** Total Revenue per Channel per Model.
2.  **Output:** Save `attribution_comparison.csv` (Channel, Last_Click_Rev, First_Click_Rev).
3.  **Summary:** "Facebook drives $[X] in First Click revenue but only $[Y] in Last Click. Cutting FB will hurt future demand."

---
*Blueprint ID: attribution-modeler*
*Source: [Real AI Examples](https://realaiexamples.com)*

