---
name: aggregate-and-find-extremum
description: This skill applies when the task requires combining data from multiple sources and identifying an item with an extremum value based on a specific criterion.
---
## Overview
Tasks often require gathering related data that is spread across several API endpoints, each potentially returning different schemas or requiring further detail calls. This pattern addresses the challenge of aggregating this disparate information, standardizing it, and then performing a comparison across all collected items to find a specific extremum (e.g., oldest, newest, largest, smallest) based on a designated field.
## When to Apply
- The instruction mentions combining information from multiple libraries or collections.
- The instruction asks to find the 'oldest', 'newest', 'first', 'last', 'minimum', or 'maximum' item based on a specific attribute.
- Data needed for comparison or display is not available directly from initial API calls and requires subsequent detail fetches.
## Procedure
1. For each distinct data source identified in the task:
2.   Paginate through the source API to retrieve all available items.
3.   If the initial response lacks necessary comparison or display fields, make subsequent detail API calls for each item (or a deduplicated set of items) to enrich the data.
4.   If the source provides nested data (e.g., a list of items within another item), flatten the structure and apply relevant parent attributes to the child items.
5.   Standardize the collected items into a common format (e.g., a list of dictionaries, each containing a unique identifier, the comparison field, and the display field).
6. Combine all standardized lists from different sources into a single master list.
7. Parse the comparison field of each item in the master list into a comparable data type (e.g., datetime objects for dates, numbers for numerical comparisons).
8. Identify the item with the extremum value (minimum or maximum) of the parsed comparison field across the entire master list.
9. If the identified extremum item lacks the required display field, make a final detail API call using its unique identifier to retrieve the missing information.
10. Return the display field of the identified extremum item as the final result.
## Key Patterns
- **Pagination Loop:** Repeatedly call an API endpoint with an incrementing page index or offset until an empty result or a result indicating no more pages is returned, ensuring all data is collected.
- **Data Enrichment/Detail Fetch:** When an initial API response provides only summary information or IDs, iterate through these items (or a deduplicated set of their IDs) and make individual API calls to a detail endpoint to retrieve missing attributes required for comparison or final display.
- **Schema Transformation/Flattening:** Convert complex or nested API responses (e.g., an album containing multiple song IDs) into a flat list of individual records, ensuring that relevant attributes from the parent object are propagated to each child record.
- **Deduplication of Identifiers:** When collecting identifiers from multiple sources, use a set or similar structure to store unique IDs before making detail API calls, preventing redundant fetches for the same item.
- **Extremum Finding with Key:** After combining and standardizing data, use a min() or max() function with a lambda key to efficiently find the item with the earliest/latest date, smallest/largest number, etc., ensuring the comparison is based on the correctly parsed data type.
- **Conditional Display Field Retrieval:** After identifying the extremum item, check if its display field is already present. If not (because some sources might not provide it), make a targeted API call to retrieve only that specific field for the final output.
## Common Pitfalls
- Failing to paginate completely, leading to incomplete data and potentially incorrect extremum identification.
- Comparing raw string representations of dates or numbers instead of parsing them into appropriate data types, which can lead to lexicographical rather than chronological/numerical comparisons.
- Not handling cases where some data sources do not provide all necessary fields, especially the final display field for the extremum item.
- Making redundant API calls for the same item when it appears in multiple sources without prior deduplication.
- Incorrectly combining data from different schemas, leading to missing fields or type mismatches in the aggregated list.
- Not handling empty results from API calls or prior variables, which can cause errors when attempting to process non-existent data.
