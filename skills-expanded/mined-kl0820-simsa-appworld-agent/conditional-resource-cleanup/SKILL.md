---
name: conditional-resource-cleanup
description: This skill applies when resources need to be filtered based on multiple criteria and then conditionally modified or removed.
---
## Overview
The structural problem involves identifying resources from a collection, checking their status against multiple criteria, and then performing a cleanup action (like removal) based on these criteria. This often requires multiple data retrieval steps, data augmentation, and a final conditional action.
## When to Apply
- Filter resources based on multiple conditions.
- Remove or modify resources that do not meet certain criteria.
- Clean up a library or collection.
- Identify items that are 'neither X nor Y'.
- Keep only items that are 'X or Y'.
## Procedure
1. Retrieve the primary collection of resources using a paginated API.
2. Retrieve all necessary auxiliary status information (e.g., liked identifiers, downloaded identifiers) using separate paginated APIs, storing identifiers in efficient lookup structures like sets.
3. Iterate through the primary collection, augmenting each resource with its status by checking against the auxiliary status information. If a status is derived, compute it based on available data.
4. Store the augmented resource data for subsequent steps.
5. Access the augmented resource data from the previous step.
6. Define the logical condition for identifying resources that require mutation (e.g., 'neither X nor Y').
7. Iterate through the resources. For each resource that satisfies the mutation condition, call the appropriate API to perform the action (e.g., removal, update).
8. Collect identifiers or details of mutated resources for reporting.
## Key Patterns
- **Pagination Loop:** Iterate through paginated API results by incrementing a page index until an empty result list is returned, accumulating all items.
- **Bulk Status Retrieval for Efficient Joins:** Instead of making individual API calls for each item's status, retrieve all relevant status identifiers in bulk (e.g., all liked IDs) and store them in a set for efficient O(1) lookup when joining with the main data.
- **Derived Status Calculation:** When a status is not directly available, compute it by combining information from multiple sources or by applying a rule to a collection of sub-items (e.g., 'all sub-items must meet a condition').
- **Conditional Action Logic:** Apply a boolean condition (e.g., 'neither X nor Y', 'X or Y') to each item to determine if a mutation action should be performed.
- **Leveraging Prior Milestone Output:** Access data computed and stored in previous milestones via `prior_variable_values` to avoid redundant API calls and computations.
## Common Pitfalls
- Making N+1 API calls for status checks instead of bulk retrieval and set lookups.
- Incorrectly implementing pagination loops, leading to incomplete data or infinite loops.
- Ignoring data available from prior milestones and re-fetching/re-computing it.
- Misinterpreting or incorrectly implementing the logical conditions for filtering (e.g., confusing 'AND' with 'OR', or 'NOT X AND NOT Y' with 'NOT (X AND Y)').
- Not handling empty initial collections or empty status lists gracefully.
- Adding unnecessary defensive checks (e.g., `if exists()`) before a removal API call when the task implies the item exists and should be removed if it meets criteria.
