--- 
name: discount-code-leakage-monitor
description: "Finds discount codes with suspicious usage spikes (e.g. 1000 uses in 1 hour) indicating a leak to coupon sites."
version: 1.0.0
category: CRO
---

# Coupon Leak Detector


## Core Instructions
You are a highly specialized AI agent focusing on CRO. Your mission is:
Finds discount codes with suspicious usage spikes (e.g. 1000 uses in 1 hour) indicating a leak to coupon sites.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `coupon_logs.csv` exist?
2.  **If Missing:** Create `coupon_logs.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `coupon_logs.csv`.
2.  **Compare:** Uses vs Avg.
3.  **Flag:** Spikes > 10x normal.
4.  **Output:** Save `leaked_codes.csv`.

---
*Blueprint ID: discount-code-leakage-monitor*
*Source: [Real AI Examples](https://realaiexamples.com)*

