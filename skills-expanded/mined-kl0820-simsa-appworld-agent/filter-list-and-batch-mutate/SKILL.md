---
name: filter-list-and-batch-mutate
description: Filters a list of items based on a reference item's property and then performs a batch mutation on the filtered subset.
---
## Overview
This strategy addresses tasks requiring the selection of a subset of items from a larger collection, often based on their relative position or state to a 'current' item, followed by applying a uniform action to each item in the selected subset. It involves initial data retrieval, precise filtering, and subsequent iterative API calls for mutation.
## When to Apply
- Identify a subset of items from a collection based on a condition.
- Perform an action on all items that meet certain criteria.
- Process items relative to a 'current' or 'active' item.
- Apply a bulk operation to a dynamically determined list of entities.
## Procedure
1. Call an API to retrieve a list of structured items.
2. Handle cases where the retrieved list is empty or indicates an error.
3. Identify a specific 'reference item' within the list based on a distinguishing property (e.g., a boolean flag or unique identifier).
4. Extract a relevant scalar property (e.g., an index, position, or timestamp) from the identified reference item.
5. Filter the original list of items, retaining only those whose corresponding scalar property meets a specified condition relative to the reference item's property.
6. From each item in the filtered list, extract a unique identifier.
7. Store this list of unique identifiers for subsequent use.
8. Retrieve the list of unique identifiers from the previous step.
9. Iterate through each identifier in the retrieved list.
10. For each identifier, call a mutation API, passing the identifier as a parameter.
11. Report the outcome as a mutation, indicating no specific return value.
## Key Patterns
- **Reference Item Identification:** Identifying a single, special item within a list (e.g., 'current', 'active') using a boolean flag or unique attribute.
- **Relative Filtering:** Filtering a list of items based on a comparison of a scalar property (e.g., position, timestamp) against the same property of a previously identified reference item.
- **Identifier Projection:** Transforming a list of complex objects into a list of their unique identifiers for use in subsequent API calls.
- **Iterative Mutation:** Performing a series of identical API calls, each targeting a different item from a pre-determined list of identifiers.
- **Mutation Milestone Output:** For milestones that primarily perform side effects, the 'value' field in the final output JSON should be 'null'.
## Common Pitfalls
- Failing to handle an empty initial list or an API error response, leading to downstream errors.
- Incorrectly identifying the reference item or extracting the wrong property from it.
- Applying an incorrect comparison logic for filtering (e.g., using '<' instead of '<=').
- Attempting to use the entire item object instead of just its identifier in the mutation API call.
- Expecting a meaningful return value from a mutation API call and not setting 'value' to 'null'.
