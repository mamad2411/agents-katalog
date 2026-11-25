---
name: retrieve-filter-aggregate-then-mutate
description: Applies when the task requires retrieving a collection of items, aggregating them based on a specific criterion, and then performing a subsequent action on the identified item.
---
## Overview
This pattern addresses tasks that involve a two-stage process: first, identifying a specific item from a larger collection by applying an aggregation or selection logic, and second, using that identified item to perform a subsequent action, often a mutation. It emphasizes efficient data retrieval and careful handling of intermediate results, ensuring the correct item is passed for the final action.
## When to Apply
- Identify an item based on a comparative property (e.g., 'least', 'most', 'oldest', 'newest').
- Perform an action on a specific item after it has been identified from a group.
- The task involves retrieving a list of entities and then selecting one based on a calculated property.
## Procedure
1. Identify the parent entity using a search or list API, filtering by a known attribute.
2. Extract the unique identifier of the parent entity.
3. Retrieve all child entities associated with the parent using a bulk list/search API, ensuring pagination is handled to collect the complete dataset.
4. From the collected child entities, apply the specified aggregation or selection logic (e.g., find the minimum/maximum value of a property) to identify the target item.
5. Extract the unique identifier and relevant properties of the identified target item.
6. Use the identifier of the target item from the previous step (or prior milestone) to call the appropriate mutation or action API.
7. For mutation milestones, ensure the final output's 'value' field is null.
## Key Patterns
- **Paginated Bulk Retrieval:** When retrieving a collection of items, use a bulk list/search API with pagination parameters (e.g., 'page_index', 'page_limit') and loop until no more items are returned, accumulating all results into a single list for complete processing.
- **Efficient Data Collection:** Prioritize bulk APIs that return comprehensive details for each item, avoiding N+1 individual calls to fetch additional properties for each item in a list.
- **Cross-Milestone Data Flow:** Pass essential identifiers and contextual properties from parent entities to child entities, and from one milestone's output to the next milestone's input, to ensure continuity and enable subsequent actions.
- **Mutation Milestone Output:** For milestones that perform a state-changing action (mutation), the final 'value' in the JSON output must be 'null', as there is no data to return, only a side effect.
## Common Pitfalls
- Failing to handle pagination, leading to incomplete datasets and incorrect aggregation results.
- Making N+1 calls to retrieve details for each item in a list when a bulk API could provide all necessary information.
- Not extracting and passing necessary identifiers (e.g., parent ID to child search, selected item ID to action API) between steps or milestones.
- Returning data in the 'value' field for a mutation milestone instead of 'null'.
- Not handling the case where no items are found after filtering or aggregation, leading to errors in subsequent steps.
