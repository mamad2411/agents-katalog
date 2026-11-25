---
name: data-enrichment-and-filtered-mutation
description: Applies when a task requires collecting a set of entities, enriching them with additional details (potentially from nested collections), filtering them based on specific criteria, and then modifying or removing the filtered subset.
---
## Overview
This pattern addresses tasks where initial API listings provide insufficient detail for filtering or selection. It involves an initial phase of data collection, followed by enrichment where missing attributes are fetched for each item, potentially across multiple nested collections. This enriched data is then used to filter items, which are subsequently modified or removed using appropriate mutation APIs. Efficiency is emphasized through caching of detailed attributes.

## When to Apply
- Identify, modify, or remove items from a collection based on a condition involving a detailed attribute.
- The initial API call for a collection does not provide all necessary attributes for filtering.
- The task involves processing multiple distinct collections or hierarchical data (e.g., a primary library and secondary nested collections) with similar filtering logic.
- Process all items in a library/account that meet specific criteria.

## Procedure
1.  **Collect Initial Items:** Use a paginated API to retrieve all items from the primary collection, extracting their unique identifiers.
2.  **Collect Nested Items (Optional):** If the task involves hierarchical data, for each primary item, use a paginated API to collect its associated sub-items, extracting their unique identifiers.
3.  **Enrich Item Details & Cache:** For each unique item identifier (from primary or nested collections), check if its detailed attributes are already known (e.g., from a cache). If not, call a detail API using the identifier to retrieve the full attributes. Store these attributes in a cache keyed by the item identifier to avoid redundant calls.
4.  **Compute Conditions:** For each item (primary or sub-item), parse its fetched attributes and compute a boolean condition based on the task's criteria.
5.  **Filter Items:** Select the items (primary or sub-items) that meet the computed condition.
6.  **Mutate Filtered Primary Items:** For each filtered primary item, call the appropriate mutation API to modify it.
7.  **Mutate Filtered Sub-Items (if applicable):** If sub-items were processed, for each filtered sub-item, call its mutation API, providing necessary identifiers (e.g., parent item's ID and sub-item's ID).
8.  **Record Modified Items:** Record identifiers of all items that were modified for traceability.

## Key Patterns
- **Pagination Loop / Paginated List Traversal:** Iteratively call a listing API with incrementing page indices until an empty result set indicates the end of the collection, accumulating all items.
- **Data Enrichment via Detail Calls / Item-Specific Detail Fetch:** When a listing API lacks necessary attributes for filtering, make subsequent detail API calls for each item to retrieve the missing information.
- **Caching for Efficiency / Cross-Milestone Data Cache:** Store and reuse detailed item attributes (e.g., id to attribute_value mapping) in a lookup structure (e.g., dictionary) across different processing stages or milestones to minimize redundant API calls.
- **Conditional Filtering / Attribute-Based Filtering:** Compute a boolean flag for each item based on a specific attribute and a given condition, then use this flag to select items for subsequent actions.
- **Iterative Mutation:** Apply a state-changing operation to each item in a pre-determined list of targets by making individual API calls.
- **Hierarchical Data Processing:** When dealing with nested collections (e.g., playlists containing songs), process the parent collection to identify all sub-items, then enrich and filter sub-items, finally performing mutations that require both parent and sub-item identifiers.
- **Structured Output for Subsequent Milestones:** The output of an enrichment milestone should be a comprehensive data structure that includes all original identifiers, fetched attributes, and computed conditions, making it directly consumable by subsequent filtering and mutation milestones without further API calls.

## Common Pitfalls
- Failing to paginate through all items in a collection, leading to incomplete data processing.
- Not performing detail API calls when initial listings lack critical filtering attributes.
- Making redundant detail API calls for the same item across different collections or processing stages, instead of caching results.
- Incorrectly parsing or extracting the relevant attribute from API responses (e.g., date formats, nested fields) or comparing data types.
- Not structuring the intermediate output data in a way that is easily consumed by subsequent milestones, leading to complex data manipulation or re-fetching.
- Failing to handle API error responses or missing data gracefully during enrichment or mutation.
- Performing actions on the wrong set of items due to incorrect filtering logic.
- Using a single mutation API for all collections when distinct APIs are required for different collection types (e.g., library vs. playlist items).
- Not correctly identifying the join key between list items and detail API calls.