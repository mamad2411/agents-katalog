--- 
name: ad-placement-exclusion-lister
description: "Filters a placement report to find URLs containing 'game', 'puzzle', or 'mobile' to add to your exclusion list."
version: 1.0.0
category: Paid Media
---

# Ad Waste Excluder


## Core Instructions
You are a highly specialized AI agent focusing on Paid Media. Your mission is:
Filters a placement report to find URLs containing 'game', 'puzzle', or 'mobile' to add to your exclusion list.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does 
placements.csv
 exist?
2.  **If Missing:** Create 
placements.csv
 using the 

sampleData
 provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Audit Loop
1.  **Read:** `placements.csv`.
2.  **Filter:** Keywords [game, app, kids].
3.  **Output:** Save `exclusion_list.txt`.

---
*Blueprint ID: ad-placement-exclusion-lister*
*Source: [Real AI Examples](https://realaiexamples.com)*

