---
name: find-extreme-value-in-related-paginated-collection
description: This skill applies when the task requires finding an item with an extreme (minimum or maximum) value for a specific attribute within a collection of items, where the collection needs to be retrieved based on a prior search and may be paginated.
---
## Overview
This strategy addresses tasks that involve identifying a primary entity, then retrieving a potentially large, paginated list of related items, and finally processing this list to find an item that satisfies an extreme (minimum or maximum) condition on one of its attributes. It combines searching, pagination, and data aggregation with a final selection step to extract the desired information.

## When to Apply
- The task requires finding an item with the minimum or maximum value of a specific attribute (e.g., "find the item with the most/highest/maximum [attribute]", "identify the item that has the largest [attribute]", "what is the [attribute] of the item with the most [other_attribute]?").
- The target items are part of a collection associated with another entity.
- The collection of items might be paginated and requires multiple API calls to retrieve completely.
- An initial search is needed to identify the primary entity by a human-readable identifier.

## Procedure
1.  Identify the primary entity using a search API, filtering by a specific identifier (e.g., name). Ensure an exact match, often case-insensitive, to extract its unique identifier.
2.  If the primary entity is not found, handle this empty result scenario.
3.  Using the extracted primary entity's identifier, query for related items. Implement a pagination loop to collect all items across all available pages until an empty list or a specific termination condition is met.
4.  Accumulate all retrieved items into a single list, extracting all necessary attributes (e.g., the attribute to be extremized, and any attributes needed for the final output).
5.  If the accumulated list of related items is empty, handle this empty result scenario.
6.  Iterate through the complete list of accumulated items to identify the single item that possesses the extreme (minimum or maximum) value for the specified attribute.
7.  Extract the required output attribute from the identified extreme item and format the final result as specified by the task.

## Key Patterns
-   **Entity Resolution with Exact Match Filtering:** Search for an entity by a human-readable name, then iterate through the search results to find an exact, case-sensitive or case-insensitive match, extracting its unique identifier for subsequent API calls.
-   **Pagination Loop for Full Collection:** Repeatedly call an API with an incrementing page index (or offset) until an empty list or a specific termination condition is met, accumulating results from all pages into a single comprehensive list.
-   **Deferred Aggregation / Extreme Value Selection:** All relevant data (e.g., all secondary items with their attributes) must be fully collected and accumulated into a single structure before any aggregation operation (like finding the minimum or maximum) is performed. Then, iterate through this complete collection to identify the single object that possesses the extreme value for a designated numeric attribute.
-   **Chained API Calls / Identifier Chaining:** The output (e.g., an ID) from one API call is used as a crucial input parameter for a subsequent API call to retrieve related or more detailed information.

## Common Pitfalls
-   Not handling pagination, leading to incomplete data and potentially incorrect results due to only processing the first page.
-   Failing to correctly filter search results for the primary entity or not performing an exact match check, leading to using the wrong identifier for subsequent queries.
-   Attempting to find the extreme value incrementally during pagination instead of after all data has been collected (deferred aggregation).
-   Incorrectly handling the edge case where no primary entity is found or where the primary entity has no associated related items.
-   Failing to extract all necessary attributes from each item during collection, which might be needed for the final selection or output.
-   Case-sensitivity issues when matching entity names during the initial search and filtering step.