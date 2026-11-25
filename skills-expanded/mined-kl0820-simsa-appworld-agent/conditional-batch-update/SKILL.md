---
name: conditional-batch-update
description: Applies when a task requires reading a collection of items, identifying a subset based on a condition, performing an action on that subset, and then performing a different action on the remaining items.
---
## Overview
This pattern addresses tasks that involve a multi-stage process: first, retrieving a list of entities; second, identifying specific entities within that list based on certain criteria; and finally, applying different modifications to the identified entities versus the remaining ones. It ensures proper data flow and conditional logic across multiple mutation steps.
## When to Apply
- Read all X items.
- Identify Y items among X based on a condition.
- Perform action A on Y items.
- Perform action B on the remaining X items.
## Procedure
1. Call a 'list' or 'show all' API to retrieve a collection of items, handling pagination to accumulate all available items.
2. From the accumulated items, extract relevant properties (e.g., identifier, mutable fields, identifying properties).
3. Identify the 'target' item(s) by applying a specific condition to their identifying properties (e.g., label match, ID comparison).
4. Store the full list of items and the identifier(s) of the target item(s) for subsequent milestones.
5. Retrieve the stored identifier(s) and relevant data for the target item(s) from the previous milestone.
6. Perform any necessary data transformations (e.g., time calculations, status changes) to determine the new values for the target item(s).
7. Call an 'update' or 'modify' API for each identified target item with its new values.
8. Output 'None' as the value for this mutation-only milestone.
9. Retrieve the stored identifier(s) of the target item(s) and the full list of items from the initial read.
10. Optionally, re-fetch the full list of items using the 'list' API to ensure the data is current and complete, especially if the prior milestone's output might have been truncated.
11. Iterate through the full list of items. For each item whose identifier does NOT match any of the target item identifiers, call an 'update' or 'modify' API with the specified action (e.g., disable, set to default value).
12. Output 'None' as the value for this mutation-only milestone.
## Key Patterns
- **Pagination Loop:** When an API returns a paginated list, repeatedly call the API with incrementing page indices until an empty or partial page is returned, accumulating all results into a single list.
- **Conditional Identification:** Identify specific items within a collection by iterating through them and applying a condition (e.g., case-insensitive string match, property value comparison) to a designated identifying property.
- **Cross-Milestone Data Flow:** Pass the full collection of items and the identifiers of specifically identified items from an initial read milestone to subsequent milestones for targeted and conditional updates.
- **Mutation-Only Output:** For milestones that primarily perform state-changing operations (updates, deletions), the 'value' field in the output should be 'None', indicating no data is returned for subsequent processing.
- **Robust Data Retrieval:** In later milestones, consider re-fetching the complete list of items from the source API, even if a list was passed from a prior milestone, to ensure data freshness and completeness, especially if the prior data might be truncated or stale.
## Common Pitfalls
- Failing to handle pagination, leading to incomplete data retrieval.
- Incorrectly identifying target items due to case sensitivity, partial matches, or flawed comparison logic.
- Not passing the necessary full item list or target item identifiers between milestones, requiring redundant API calls or leading to incorrect logic.
- Applying the same action to all items instead of conditionally applying different actions to target vs. remaining items.
- Incorrectly parsing or formatting data (e.g., time strings, boolean values) when preparing for an update API call.
- Not handling API errors or empty responses gracefully during data retrieval or updates.
- Forgetting to output 'None' for mutation-only milestones, potentially causing issues for downstream processing expecting a specific data structure.
