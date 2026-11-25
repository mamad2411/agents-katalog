---
name: multi-source-entity-aggregation-and-extremum-finding
description: Aggregates entities from multiple sources, potentially requiring detail fetches, and identifies an extremum based on a specific attribute.
---
## Overview
This skill addresses tasks requiring the collection of entities from various library-like sources, where initial API calls might not provide all necessary details. It involves strategies for efficient data retrieval, deduplication, and subsequent aggregation to find a specific entity based on a comparative attribute.
## When to Apply
- Instruction asks to gather items from multiple distinct collections or libraries.
- Required data for each item is not fully available in initial listing APIs.
- The final goal involves comparing items across all collected data to find a specific extremum (e.g., newest, oldest, largest, smallest).
## Procedure
1. For each distinct source (e.g., library, collection):
2. Retrieve a list of primary entities from the source, handling pagination.
3. If the primary entities are containers (e.g., albums, playlists), iterate through them to extract identifiers for their contained sub-entities (e.g., songs).
4. If necessary, make additional API calls for each sub-entity (or a batch of them) to fetch missing details (e.g., release date, title), optimizing to avoid redundant calls by first collecting unique identifiers.
5. Accumulate all sub-entities with their complete details into a temporary list, ensuring deduplication if entities can appear in multiple containers or sources.
6. Combine all temporary lists of entities from different sources into a single master list.
7. Parse the comparative attribute (e.g., date string to datetime object) for each entity in the master list.
8. Identify the entity with the extreme value (e.g., maximum, minimum) for the comparative attribute.
9. Extract the required final output from the identified extreme entity.
## Key Patterns
- **Paginated List Retrieval:** Iteratively call a list API with pagination parameters (e.g., page_index, page_limit) until no more results are returned (e.g., an empty list or fewer items than page_limit).
- **N+1 Detail Fetch Optimization:** When initial list APIs lack full details, collect all unique identifiers first, then make detail calls for only those unique identifiers, or seek a more efficient API that provides details for multiple items or richer data in one call.
- **Multi-Source Entity Consolidation:** Gather entities from distinct API endpoints or prior results, then merge them into a single collection for unified processing.
- **Deduplication by Identifier:** Before processing or making detail calls, ensure entities are unique based on a primary identifier (e.g., song_id) to prevent redundant work or skewed results.
- **Extremum Finding:** Identify an item in a collection that has the maximum or minimum value for a specific attribute, often after data type conversion (e.g., string to datetime) for accurate comparison.
## Common Pitfalls
- Forgetting Pagination: Not handling APIs that return results in pages, leading to incomplete data.
- Inefficient N+1 Calls: Making a detail API call for *every* item from a list without first consolidating unique identifiers or checking for more efficient batch/richer APIs.
- Missing Deduplication: Including duplicate entities from different sources, leading to incorrect counts or skewed extremum results.
- Incorrect Date/Attribute Comparison: Comparing strings instead of parsed date objects, or using the wrong comparison logic (e.g., min instead of max).
- Ignoring Empty Results: Not gracefully handling cases where a library or source returns no items, leading to errors in subsequent steps.
