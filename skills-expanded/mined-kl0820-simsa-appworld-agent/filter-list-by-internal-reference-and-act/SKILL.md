---
name: filter-list-by-internal-reference-and-act
description: Filters a list of items using a condition derived from a 'reference' item within that same list, then performs an action on each item in the filtered subset.
---
## Overview
This skill addresses tasks that involve a two-stage process: first, identifying a subset of items from a larger collection by establishing a filtering criterion based on an item within that collection; second, iterating through this filtered subset to perform a specific action on each item.

## When to Apply
- Identify X from a list, then do Y to each X.
- Filter a collection of items and then perform a specific operation on the filtered set.
- Filter a list of entities based on a property of a specific entity within that list.
- Process items that are 'current' or 'active' and related items.
- Apply an operation to all items that meet a dynamic condition derived from another item in the list.

## Procedure
1. Call an API to retrieve a collection of items.
2. Handle potential empty or error responses from the API.
3. Identify a 'reference' item within the collection based on a specific flag, property, or characteristic that defines a boundary or key for subsequent filtering.
4. Extract a key attribute or value from this reference item.
5. Filter the original collection, keeping only items that satisfy a condition relative to the extracted key value and any additional criteria.
6. Extract unique identifiers and relevant metadata from each item in the filtered list, ensuring proper ordering if necessary.
7. Store these identifiers (and metadata) as the output of the current milestone, or prepare them for the next step.
8. In a subsequent step or milestone, retrieve the stored identifiers from the prior output.
9. Iterate through the retrieved identifiers.
10. For each identifier, call an action API, passing the identifier (and any necessary metadata) as a parameter.
11. Record the outcome of each action, such as collecting success/failure messages, acknowledging completion, or constructing a structured result including per-item action outcomes.

## Key Patterns
- **Two-Stage Processing:** The overall task is naturally split into an identification/filtering stage and an action stage, often corresponding to separate milestones or distinct logical blocks.
- **Reference-Based/Contextual Filtering:** A list is filtered not by a static value, but by a value dynamically extracted from a 'current' or 'reference' item found within that same list.
- **Iterative Action on Filtered Subset:** After identifying a subset of items, a single-item action API is called repeatedly for each item in that subset.
- **Milestone Chaining for Data Flow:** The structured output (e.g., a list of unique identifiers and metadata) from a previous milestone serves as the direct input for a later milestone's iterative actions.
- **Action Outcome Logging:** When performing multiple actions, it's crucial to accumulate and report the individual success or failure messages for each action, rather than just a single overall status.

## Common Pitfalls
- Applying the action to the entire initial list instead of the correctly filtered subset.
- Failing to handle cases where the 'reference' item is not found in the initial collection.
- Incorrectly identifying the filtering criteria or deriving the filtering condition from the reference item's properties.
- Not handling empty collections or API errors gracefully at any stage.
- Not correctly passing the unique identifier (or necessary metadata) from the filtered list to the subsequent action API calls.
- Attempting to perform actions before the identification and filtering steps are fully completed, leading to race conditions or incomplete data processing.
- Not accumulating individual action results when multiple actions are performed, leading to a loss of per-item status.