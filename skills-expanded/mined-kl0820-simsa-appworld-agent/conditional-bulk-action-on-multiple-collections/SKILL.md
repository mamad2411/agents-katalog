---
name: conditional-bulk-action-on-multiple-collections
description: Applies when a conditional bulk action needs to be performed across multiple distinct data collections, some of which may be nested.
---
## Overview
This pattern addresses tasks requiring a filter-and-act operation on items distributed across different organizational structures within an application. It necessitates iterating through each structure, retrieving items, evaluating a condition based on item attributes, and then performing the action. The core challenge is managing distinct top-level collections and potentially nested structures within them, ensuring comprehensive and accurate processing.
## When to Apply
- Perform an action on items in multiple distinct locations.
- Apply a condition to items before acting.
- Process all items within a collection, and all items within sub-collections.
- Remove/modify/add items based on a specific attribute.
## Procedure
1. Identify all distinct primary data sources or top-level containers that need processing.
2. For each identified primary data source or container:
3. If the container holds items directly:
4. Retrieve all items from the container.
5. For each item, read the necessary attribute(s) to evaluate the condition.
6. Filter the items based on the specified condition.
7. Perform the specified action on the filtered items.
8. If the container holds secondary containers (e.g., a list of folders, each containing files):
9. Retrieve all secondary containers.
10. For each secondary container:
11. Retrieve all items from the secondary container.
12. For each item, read the necessary attribute(s) to evaluate the condition.
13. Filter the items based on the condition.
14. Perform the specified action on the filtered items within that secondary container.
## Key Patterns
- **Distinct Collection Processing:** Decompose the task into separate sub-tasks for each distinct top-level data collection or organizational unit, even if the action and condition are identical across them.
- **Read-Then-Act:** Always retrieve all necessary attributes for condition evaluation *before* performing any destructive or modifying action on an item.
- **Nested Iteration:** When a primary collection contains secondary collections, iterate through the primary collection, and for each secondary collection, perform a further iteration over its contained items.
- **Exhaustive Retrieval:** Ensure all items are retrieved from a collection, potentially requiring handling of pagination or other mechanisms for large datasets, to guarantee completeness.
## Common Pitfalls
- Mixing processing logic for fundamentally different collection types (e.g., a flat list vs. a list of containers) into a single, undifferentiated loop.
- Performing an action on an item before fully evaluating its attributes against the condition, leading to incorrect modifications or deletions.
- Failing to retrieve all items from a collection, especially when pagination is involved, resulting in incomplete processing.
- Missing entire sub-collections when iterating through a nested structure, leading to partial task completion.
- Assuming a single bulk operation can span across distinct collection types or nested structures, which often requires separate API calls or processing flows.
