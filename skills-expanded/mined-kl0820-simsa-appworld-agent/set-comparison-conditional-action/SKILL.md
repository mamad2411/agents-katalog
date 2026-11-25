---
name: set-comparison-conditional-action
description: Compares two distinct paginated entity lists using set operations (e.g., difference) to identify a target subset, then performs a conditional action (e.g., delete, unfollow, update) on entities belonging to that specific subset.
---
## Overview
This pattern addresses tasks requiring an action (e.g., unfollow, delete, update) on a specific group of entities. It involves fetching a primary list of entities, then fetching a secondary list of related entities, processing both to extract relevant identifiers, and finally using set operations to identify the target entities for the action.
## When to Apply
- Perform an action on X based on properties derived from Y and Z.
- Filter a list of A based on attributes found or not found in B.
- Identify items in one collection that are not present in another collection.
- Unfollow/delete/update items that meet certain criteria derived from multiple sources.
## Procedure
1. Retrieve the primary list of entities, handling pagination to ensure all items are collected.
2. Extract key identifiers and any other necessary attributes from each entity in the primary list.
3. Retrieve the secondary list of related entities, handling pagination to ensure all items are collected.
4. For each entity in the secondary list, extract associated identifiers (which may be nested or require further processing).
5. Aggregate and de-duplicate these associated identifiers into a unique set for efficient lookup.
6. Compare the identifiers from the primary list with the aggregated set of identifiers from the secondary list to determine which entities meet the condition for the action.
7. For each identified entity that meets the condition, perform the specified action.
8. Collect and report the results of the action, including details of the entities affected.
## Key Patterns
- **Pagination Loop:** When an API returns paginated results, iterate through `page_index` (or similar pagination parameter) until an empty or partial page is returned, accumulating all results into a single list.
- **Set Difference for Filtering:** To efficiently filter one list of entities based on the presence or absence of their identifiers in another collection, convert the comparison collection into a hash set (e.g., Python `set`) for O(1) average-case lookup.
- **Data Aggregation and De-duplication:** When collecting related entities or attributes from a list of primary entities (e.g., artists from multiple songs), aggregate unique identifiers into a dictionary or set to avoid duplicates and facilitate later lookup.
- **Cross-Milestone Variable Passing:** Results from earlier milestones (e.g., lists of entities or sets of identifiers) are passed as `prior_variable_values` to subsequent milestones for comparison and action, ensuring data continuity.
- **Conditional Mutation:** Perform a mutation action (e.g., unfollow, delete) only on entities that satisfy a specific condition derived from comparing multiple data sources, rather than on the entire initial list.
## Common Pitfalls
- Failing to handle pagination correctly, leading to incomplete data sets or infinite loops.
- Using inefficient comparison methods (e.g., nested loops) instead of set lookups, especially for large datasets.
- Forgetting to de-duplicate identifiers when aggregating from multiple sources, leading to incorrect comparisons.
- Incorrectly identifying the common key or comparison field between different datasets.
- Not gracefully handling empty results from API calls or scenarios where no entities meet the action's condition.
- Performing the mutation action on the wrong subset of entities due to an inverted or incorrect comparison logic.
