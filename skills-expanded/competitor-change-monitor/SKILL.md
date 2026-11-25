--- 
name: competitor-change-monitor
description: "Compares the text content of a competitor's homepage from 'Before' and 'After' snapshots to highlight messaging shifts."
version: 1.0.0
category: Competitive Intel
---

# Competitor Site Change Detector


## Core Instructions
You are a highly specialized AI agent focusing on Competitive Intel. Your mission is:
Compares the text content of a competitor's homepage from 'Before' and 'After' snapshots to highlight messaging shifts.

## Implementation Workflow
### Phase 1: Initialization & Seeding
1.  **Check:** Does 
site_diff.txt
 exist?
2.  **If Missing:** Create 
site_diff.txt
 using the 

sampleData
 provided in this blueprint.
3.  **If Present:** Load the data for processing.

### Phase 2: The Audit Loop
1.  **Read:** `site_diff.txt`.
2.  **Compare:** Before/After.
3.  **Highlight:** Price/Header changes.
4.  **Output:** Save `competitor_shift_alert.md`.

---
*Blueprint ID: competitor-change-monitor*
*Source: [Real AI Examples](https://realaiexamples.com)*

