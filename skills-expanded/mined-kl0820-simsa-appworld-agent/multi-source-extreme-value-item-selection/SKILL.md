---
name: multi-source-extreme-value-item-selection
description: Aggregates and enriches data from multiple paginated sources to identify and return a single item that satisfies an extreme comparative criterion (e.g., oldest, largest, best).
---
## Overview
This skill addresses tasks requiring the collection of a specific type of entity from various library-like sources, where each source might provide partial or differently structured data. It involves iterating through paginated lists, making detail calls for missing information, transforming hierarchical data into flat lists, and finally combining and comparing all collected entities to find a specific one.
## When to Apply
- Collect all X from my Y library.
- Find the oldest/newest/largest/smallest Z across multiple sources.
- Combine information from A, B, and C.
- Retrieve details for items listed in a collection.
## Procedure
1. For each distinct data source:
2. Paginate: Repeatedly call the list-retrieval API for that source, incrementing the page parameter until no more items are returned. Accumulate all items.
3. Extract & Transform: For each item from the paginated list, extract relevant identifiers and attributes. If the source provides hierarchical data (e.g., a parent entity containing child entities), flatten it into individual child entities, propagating relevant parent attributes.
4. Deduplicate (if applicable): If identifiers are collected from multiple items within the same source or across sources, deduplicate them to avoid redundant detail calls.
5. Enrich Details (if necessary): If the initial list API or transformed data lacks required attributes, make individual detail API calls for each unique identifier to fetch the missing information. Handle potential errors or missing items from detail calls.
6. Standardize Schema: Ensure the collected data from each source conforms to a consistent schema (e.g., all items have an identifier, a comparison field, and any required output fields).
7. Consolidate: Combine all standardized data collections from different sources into a single master list.
8. Compare & Select: Identify the target item from the consolidated list based on the specified comparative criterion (e.g., minimum/maximum value of a specific field). This may require parsing data types (e.g., date strings to datetime objects) for accurate comparison.
9. Final Enrichment (if necessary): If the selected target item still lacks a required output field, make a final detail API call using its identifier to retrieve the missing information.
10. Format Output: Present the required information from the selected target item.
## Key Patterns
- **Pagination Loop:** Iteratively call a list-returning API with an incrementing page parameter until an empty or invalid response indicates the end of the collection.
- **Detail Enrichment via ID:** Use an identifier obtained from a list-level API to make a subsequent, more detailed API call for specific attributes of an individual entity.
- **Hierarchical Data Flattening:** Transform data where a parent entity contains multiple child entities into a flat list of individual child entities, often propagating parent attributes to each child.
- **Cross-Source Data Consolidation:** Merge lists of entities obtained from different API endpoints, which may have slightly varying schemas, into a unified collection.
- **Conditional Detail Fetching:** Make an API call to retrieve a missing attribute for a specific entity only if that attribute is not already present in the collected data.
- **Extremum Finding with Key Function:** Use a comparison function (e.g., min() or max() with a key argument) to select an item from a collection based on a specific attribute's value after appropriate type conversion.
## Common Pitfalls
- Forgetting to paginate, leading to incomplete data collection.
- Not handling cases where detail API calls fail or return partial data.
- Comparing raw string representations of dates/times instead of parsed datetime objects.
- Failing to deduplicate identifiers before making detail calls, leading to redundant API requests.
- Assuming all sources provide the same set of fields, leading to errors when accessing missing keys.
- Incorrectly flattening hierarchical data, losing context or duplicating information.
- Not checking for empty collections before attempting to find minimum/maximum.
