---
name: library-item-management-by-status
description: Manages items in a library by retrieving their status from multiple sources, filtering based on criteria, and performing actions.
---
## Overview
This skill addresses tasks requiring the modification of a user's library (e.g., songs, albums) based on specific criteria. It involves fetching all library items, gathering related status information from various APIs, combining this data, and then performing conditional actions like removal.
## When to Apply
- Modify items in a user's library based on their attributes or status.
- Filter library items based on multiple conditions derived from different data sources.
- Determine an item's status by combining information from several API endpoints.
- Perform bulk actions (e.g., add, remove, update) on library items after a filtering step.
## Procedure
1. Retrieve all target library items using a paginated API call, accumulating results.
2. For each relevant status indicator, retrieve all associated identifiers using a paginated API call, accumulating them into a set for efficient lookup.
3. Iterate through the accumulated target library items.
4. For each target item, determine its final status by checking its identifier against the collected sets of status indicators, applying any complex logical rules (e.g., 'all sub-items must have a certain status').
5. Based on the determined status, mark each item for a specific action (e.g., 'keep', 'remove').
6. Filter the target library items to create a list of items designated for the action.
7. Iterate through the filtered list and perform the state-changing API call for each item.
## Key Patterns
- **Pagination Loop:** When an API returns results in pages, use a 'while True' loop with an incrementing page index and a 'break' condition when an empty page is returned to ensure all items are retrieved.
- **Efficient Lookup with Sets:** To quickly check membership (e.g., if an item is 'liked' or 'downloaded') across a large collection of identifiers, aggregate those identifiers into a Python set for O(1) average-case lookup time.
- **Multi-Source Data Aggregation:** Information required to make a decision about a single library item may be spread across multiple API endpoints. Retrieve all necessary data from these distinct sources before attempting to process individual items.
- **Complex Conditional Status Derivation:** When an item's status depends on the status of its sub-items (e.g., an album is 'downloaded' only if *all* its songs are 'downloaded'), use an 'all()' or 'any()' check on the sub-item statuses.
- **Reading Prior Milestone Output:** When a subsequent milestone depends on data computed in a previous one, access it via `prior_variable_values['variable_name']`.
## Common Pitfalls
- Forgetting to implement pagination, leading to incomplete data retrieval.
- Using inefficient data structures (e.g., lists) for membership checks, resulting in poor performance for large datasets.
- Incorrectly combining logical conditions for status determination, especially with 'AND' vs 'OR' or 'all()' vs 'any()'.
- Failing to handle empty responses from paginated APIs, causing infinite loops or errors.
- Performing state-changing API calls inside the main data retrieval or processing loop, which can be inefficient and harder to debug than a separate filtering and action phase.
