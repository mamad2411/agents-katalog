---
name: filtered-collection-mutation
description: Applies when a task requires modifying a subset of items within a larger collection, often excluding a specific item.
---
## Overview
This skill addresses tasks that involve identifying one or more specific items from a collection, performing a targeted modification on them, and then performing a different, often inverse, modification on the remaining items in the collection. It typically involves multiple API calls: one or more to fetch the collection, and then individual update calls for each item to be modified.
## When to Apply
- Modify a specific item and then process the remaining items differently.
- Update all items except a designated one.
- Iterate through a list and apply a condition-based action to some items while excluding others.
- Identify an item by a descriptive label and then perform an action on it and its peers.
## Procedure
1. Fetch the complete collection of items, handling pagination if necessary.
2. Identify the primary target item(s) from the collection based on specific criteria (e.g., label matching, ID).
3. Extract relevant identifiers and current values from the identified target item(s).
4. If no target item is found, handle this case gracefully (e.g., return None).
5. Calculate any new values or states required for the primary target item(s) based on the instruction.
6. Call the update API for the primary target item(s) with the new values/states, ensuring all required parameters are passed.
7. Fetch the complete collection of items again (or use a cached version if freshness is guaranteed).
8. Identify the item(s) to be excluded from the secondary modification (typically the primary target item(s)).
9. Iterate through the entire collection. For each item that is NOT among the excluded item(s), call the update API to perform the secondary modification (e.g., disabling, setting a default state).
10. Collect identifiers of all items that were modified in the secondary step for reporting.
## Key Patterns
- **Pagination Loop:** Repeatedly call a list-fetching API with an incrementing page index until an empty or partial page is returned, accumulating all results into a single list.
- **Conditional Item Selection:** Filter items from a fetched collection based on a string match (e.g., case-insensitive substring search) or other attribute comparisons to identify specific targets.
- **Derived Value Calculation:** Compute a new attribute value (e.g., a new time, a new status) for an item based on its current attribute value and a specified delta or rule.
- **Exclusion Logic for Mass Update:** When performing an action on 'all but one' or 'all except X', iterate through the collection and apply a conditional check (e.g., `if item_id != excluded_id`) before calling the update API for each item.
- **Multiple Individual Updates:** To modify multiple items in a collection, it's common to call a single-item update API repeatedly within a loop for each item that needs modification.
## Common Pitfalls
- Failing to handle pagination when fetching a collection, leading to incomplete data.
- Incorrectly parsing or calculating new attribute values (e.g., not handling time rollovers or edge cases).
- Forgetting to exclude the specific item(s) from the 'update all others' step, leading to unintended modifications.
- Assuming the collection state remains static between initial fetching and subsequent mass updates; always refetch if freshness is critical.
- Not handling the case where the primary target item is not found in the initial collection.
- Failing to pass all necessary parameters (e.g., 'enabled' status) when calling update APIs, leading to partial or incorrect state changes.
