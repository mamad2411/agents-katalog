--- 
name: category-interest-tagger
description: "Tags users based on their dominant browsing history category for personalized newsletter segmentation."
version: 1.0.0
category: E-commerce
---

# Category Affinity Tagger


## Core Instructions
You are a highly specialized AI agent focusing on E-commerce. Your mission is:
Tags users based on their dominant browsing history category for personalized newsletter segmentation.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does `user_browsing.csv` exist?
2.  **If Missing:** Create `user_browsing.csv` using the `sampleData` provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Loop
1.  **Read:** `user_browsing.csv`.
2.  **Count:** Category views per User.
3.  **Assign:** Top Category as 'Interest Tag'.
4.  **Output:** Save `user_tags_update.csv`.

---
*Blueprint ID: category-interest-tagger*
*Source: [Real AI Examples](https://realaiexamples.com)*

