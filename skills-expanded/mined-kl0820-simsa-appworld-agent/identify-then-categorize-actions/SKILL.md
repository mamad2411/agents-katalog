---
name: identify-then-categorize-actions
description: Applies when a task requires performing distinct actions on different categories of items, all initially identified by a common attribute.
---
## Overview
This pattern addresses tasks where multiple types of entities need to be processed based on a shared initial filter. It separates the initial data gathering from the subsequent type-specific actions, ensuring all relevant items are identified before any modifications occur. This allows for independent verification of actions on each category.
## When to Apply
- Instructions specify actions on multiple distinct types of entities.
- All entities are initially filtered or identified by a single common attribute.
- The actions on different entity types are distinct or have independent success conditions.
- The task involves both identification/reading and subsequent modification/deletion.
## Procedure
1. Identify and gather all relevant items across all specified categories based on a common filtering attribute.
2. For each distinct category of item identified, perform the corresponding category-specific action.
## Key Patterns
- **Initial Broad Identification:** A single initial step is used to identify all items that match a common, broad criterion, regardless of their specific sub-type, to ensure comprehensive data gathering.
- **Type-Specific Action Segregation:** After initial identification, actions are segregated and performed independently for each distinct type or category of item, even if they share a common initial filter.
- **Data Dependency Chain:** Action-oriented milestones are strictly dependent on a preceding identification or data-gathering milestone, ensuring that all necessary data is available before modifications are attempted.
## Common Pitfalls
- Attempting to perform actions on items before fully identifying the complete set of relevant items.
- Mixing actions for different item types within a single milestone, leading to unclear success conditions or recovery paths.
- Failing to use the common attribute for initial identification, leading to redundant filtering or missed items.
- Not separating the read/identification step from the write/action step, which can lead to race conditions or incomplete data processing.
