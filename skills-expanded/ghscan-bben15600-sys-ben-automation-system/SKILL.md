---
name: vr-income-tracker
description: Tracks Enjoy VR events and income. Trigger on VR/events/income queries.
---

# VR Income Tracker Agent

## Instructions
1. Read VR Events DB for current month
2. Calculate total monthly VR income
3. For each event without invoice text — generate invoice text
4. For events not yet added to Budget DB — create entry (Type: Income, Source: VR)
5. Mark "Added to Budget" checkbox

## Data Sources
- **Read/Write**: VR Events DB (`collection://8d15b9e6-8aed-47fc-97bc-38f1570dea79`)
- **Write**: Budget DB (`collection://295bb07d-d7b9-8176-a6bd-000b6ad23eca`)
