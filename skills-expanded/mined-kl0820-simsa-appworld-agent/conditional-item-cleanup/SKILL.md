---
name: conditional-item-cleanup
description: Describes the strategy for filtering and conditionally removing items from a collection based on multiple status checks.
---
## Overview
This skill addresses tasks requiring the cleanup or modification of a primary collection where items are retained or removed based on complex, often multi-source, conditions. It involves fetching the main collection, gathering auxiliary status data, correlating this data, and then performing conditional actions like removal.
## When to Apply
- Keep only X that are Y or Z
- Remove the rest
- An A is B if all C in it are D
- Cleanup my libraries
- Leave [entity] library as is
## Procedure
1. Identify the primary collection to be processed and the criteria for retention/removal.
2. Retrieve all items from the primary collection using a paginated API, accumulating them into a comprehensive list.
3. Retrieve all necessary auxiliary status data (e.g., 'liked' status, 'downloaded' status) for items and related entities using paginated APIs. Store relevant identifiers in efficient lookup structures (e.g., sets).
4. For each item in the primary collection, evaluate its retention/removal status based on the retrieved auxiliary data and any specified complex rules (e.g., aggregation across sub-items).
5. Construct an intermediate data structure containing the unique identifier of each item and its computed retention/removal status (e.g., boolean flags for 'liked', 'downloaded', 'keep').
6. Filter the intermediate data structure to identify items designated for removal based on the computed status.
7. For each identified item, invoke the appropriate API to perform the removal action.
8. Generate a final output detailing the identifiers of the items that were removed.
## Key Patterns
- **Pagination Loop:** Repeatedly call a listing API with an incrementing page parameter (e.g., 'page_index') until an empty list is returned, indicating all items have been fetched.
- **Set for Efficient Lookup:** Store identifiers from auxiliary status listings (e.g., 'liked_ids', 'downloaded_ids') in a set data structure for O(1) average-case membership testing, significantly improving performance over list lookups.
- **Intermediate Status Object:** Create a structured intermediate output (e.g., a list of dictionaries) that combines original item data with computed boolean flags (e.g., 'liked', 'downloaded', 'keep'). This object serves as a clear, reusable input for subsequent milestones, avoiding redundant computations.
- **Aggregated Status Evaluation:** When a parent item's status (e.g., 'album downloaded') depends on the status of all its children (e.g., 'all songs in album downloaded'), use an 'all()' or equivalent logical check across the child identifiers against the relevant status set.
- **Explicit Exclusion Handling:** Identify and explicitly exclude entities or collections from processing if the task instruction specifies they should be left unchanged.
- **Prior Milestone Variable Usage:** Leverage results from previous milestones, accessed via 'prior_variable_values', to avoid re-fetching data or re-computing statuses, ensuring efficiency and consistency across the task.
- **Conditional Action Execution:** Perform state-changing actions (e.g., removal) only on items that precisely match the specified removal criteria, derived from the computed statuses.
## Common Pitfalls
- Failing to handle pagination, leading to incomplete data retrieval.
- Using inefficient data structures (e.g., lists) for frequent membership checks instead of sets.
- Redundantly calling APIs or re-computing statuses that were already determined in a previous milestone.
- Incorrectly implementing aggregation logic for complex conditions (e.g., misinterpreting 'all' for 'any').
- Modifying entities or collections that were explicitly stated to be left unchanged.
- Not gracefully handling empty results from API calls, leading to errors.
- Performing removal actions on the wrong type of entity (e.g., removing songs instead of albums).
- Failing to pass comprehensive intermediate results to subsequent milestones, forcing re-computation.
