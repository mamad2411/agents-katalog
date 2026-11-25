---
name: read-filter-act-on-collections
description: Filter items from one or more collections based on criteria, then perform a uniform action on the filtered subset.
---
## Overview
Many tasks require identifying a subset of items from one or more collections based on specific conditions, and then applying a consistent modification to only those identified items. This pattern ensures all necessary data for both filtering and the subsequent action is gathered upfront, preventing redundant reads or incomplete information during the action phase. The action itself might be conditional based on the item's current state, but the target state is uniform. When dealing with multiple collections, each is processed systematically and independently.

## When to Apply
- Modify items in one or more collections based on their attributes.
- Filter a list of entities using multiple conditions.
- Perform an action on a subset of items after checking their current state.
- A task involves both reading collection(s) and then writing to a subset of it.
- The items are located in multiple distinct, independently manageable collections or data sources, and the filtering condition is consistent across all of them.

## Procedure
1. **Identify Target Collections:** Determine all distinct collections that need to be processed.
2. **For each target collection:**
    a. **Read Data:** Retrieve all items from the current collection, ensuring all attributes relevant for filtering and subsequent action are gathered. This includes attributes needed for conditional logic within the action step.
    b. **Filter Items:** Iterate through the retrieved entities, applying the specified filtering conditions to identify the subset of entities that require modification.
    c. **Perform Action:** For each identified entity, perform the specified uniform action. This action may use the previously retrieved attributes to confirm its necessity or specific parameters, ensuring the final state is consistent across all acted-upon items.

## Key Patterns
- **Read-Before-Write Separation:** Separate the initial data retrieval of all relevant attributes for a collection from the subsequent filtering and modification steps. This ensures all necessary information is available before any mutations occur.
- **Pre-emptive Data Collection:** Gather all attributes that might be needed for any filtering condition or any conditional action in the initial read step, even if not all attributes are used for every item.
- **Uniform Action on Filtered Set:** After filtering, the action applied to each selected item is consistent, even if the reason for applying it (e.g., unrated vs. rated higher) varies. The final state is uniform.
- **Collection Isolation:** When processing multiple collections, each distinct collection is treated as an independent unit for the read-filter-act sequence. This ensures that operations on one collection do not interfere with or depend on the state of another, allowing for modular processing and error handling.

## Common Pitfalls
- Attempting to filter items without first reading all necessary attributes.
- Performing actions on items without confirming they meet all filtering criteria.
- Mixing read and write operations within the same milestone, leading to inefficient or incomplete data processing.
- Failing to retrieve all attributes needed for conditional logic within the action step during the initial read.
- Applying the filtering condition inconsistently across different collections when processing multiple sources.
- Failing to process all specified collections, or mixing items from different collections during the action phase.