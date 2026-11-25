---
name: filter-and-act-on-collection
description: Applies when a task requires filtering a collection of items based on multiple criteria and then performing an action on the filtered subset.
---
## Overview
This skill addresses tasks that involve a two-stage process: first, identifying a subset of items from a primary collection based on complex, multi-source criteria, and second, performing a specific action (e.g., removal, update) on the identified subset. It emphasizes efficient data retrieval, logical combination of conditions, and clear separation of identification from action.
## When to Apply
- Filter a collection based on multiple conditions.
- Identify items for subsequent action.
- Remove items from a library/collection based on criteria.
- Keep only certain items in a collection.
## Procedure
1. Fetch the primary collection of items using a paginated API.
2. Fetch all auxiliary data (e.g., liked items, downloaded items) relevant to the filtering criteria, also using paginated APIs.
3. Process auxiliary data into efficient lookup structures (e.g., sets of identifiers).
4. For each item in the primary collection, apply the filtering logic using the auxiliary data to determine a 'keep' or 'action_needed' flag.
5. Augment the primary collection with these flags and create a separate list of identifiers for items that meet the 'keep' criteria (or 'action_needed' criteria, depending on the task).
6. If an action is required in a subsequent milestone: Read the augmented collection and the list of identifiers from the prior milestone.
7. Identify the specific items to act upon (e.g., items *not* in the 'keep' list, or items *in* the 'action_needed' list).
8. For each identified item, call the relevant state-changing API.
9. Accumulate the identifiers of items on which the action was successfully performed.
## Key Patterns
- **Pagination Loop:** Repeatedly call a list-fetching API with an incrementing page index until an empty list is returned, accumulating all results.
- **Set-based Lookup for Efficiency:** Collect identifiers from auxiliary data sources into sets to enable O(1) average-case lookup when checking conditions for items in the primary collection.
- **Inter-Milestone Data Contract:** When a milestone identifies items for subsequent action, its output must include the original collection augmented with all derived flags (e.g., 'liked', 'downloaded', 'keep'), AND a separate list of identifiers for the items identified for action. This prevents re-fetching or re-deriving data in later steps.
- **Derived Flag Logic:** Combine multiple boolean conditions (e.g., 'is_liked' AND 'is_downloaded') to create a final 'keep' or 'action_needed' flag for each item in the primary collection.
- **Action Execution vs. Output Construction:** Clearly distinguish between API calls that modify state (e.g., 'remove_item') and the final construction of the output JSON. Perform state-modifying actions once and accumulate their results; the final output should only reference these accumulated results.
## Common Pitfalls
- Not handling pagination correctly, leading to incomplete data retrieval.
- Re-fetching data in subsequent milestones that was already retrieved and processed in a prior milestone.
- Inefficiently checking conditions (e.g., iterating through lists instead of using sets for lookups).
- Failing to pass the augmented original collection (with flags) to the next milestone, forcing re-computation of flags.
- Confusing the logic for 'items to keep' versus 'items to remove' when applying filters.
- Not accumulating the identifiers of items successfully acted upon by state-changing APIs.
