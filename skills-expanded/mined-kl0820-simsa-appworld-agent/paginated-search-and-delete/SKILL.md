---
name: paginated-search-and-delete
description: When a task requires finding and deleting multiple items that are retrieved through a paginated search.
---
## Overview
This skill addresses tasks that involve identifying and removing multiple entities from a system. It typically requires iterating through paginated search results, filtering them based on specific criteria, and then performing a delete operation on each matching entity.
## When to Apply
- Delete all X from Y
- Remove all Z matching condition C
- The available API for searching returns paginated results.
- The available API for deletion takes a single item identifier.
## Procedure
1. Initialize a list to store identifiers of items to be deleted.
2. Initialize pagination parameters (e.g., page_index, page_limit).
3. Enter a loop to retrieve paginated results:
4. Call the search API with the relevant query and pagination parameters.
5. Check if the returned page is empty or indicates the end of results; if so, break the loop.
6. Iterate through each item in the current page.
7. Apply any necessary filtering or validation to ensure the item matches the deletion criteria.
8. If an item matches, extract its unique identifier and add it to the list of identifiers to be deleted.
9. Increment the pagination parameter for the next iteration.
10. Iterate through the collected list of identifiers.
11. For each identifier, call the delete API.
12. Construct and return a structured output indicating the success and the identifiers of the deleted items.
## Key Patterns
- **Pagination Loop:** Iteratively call a search API with pagination parameters (e.g., 'page_index', 'page_limit') until no more results are returned, typically indicated by an empty list or a list smaller than the 'page_limit'.
- **Defensive Filtering:** Even if the search API accepts filtering parameters, re-validate each returned item against the original criteria within the code to ensure precise matching and prevent unintended actions, especially for 'from X' or 'to Y' conditions.
- **Search-Collect-Delete:** First, gather all relevant unique identifiers from paginated search results into a single list, and then perform individual delete operations using those collected identifiers in a separate loop.
- **Early Exit for Pagination:** Break the pagination loop when the number of results on a page is less than the 'page_limit', as this indicates that the last page of results has been processed.
## Common Pitfalls
- Forgetting to increment the pagination parameter or incorrectly handling the loop termination condition, leading to infinite loops or incomplete results.
- Not defensively checking the filtering criteria (e.g., sender/receiver) on returned items, potentially deleting unintended entities.
- Assuming the search API's filtering is perfectly precise for the instruction's intent and skipping in-code validation.
- Incorrectly handling API response types (e.g., expecting a list but receiving a dictionary for an error or empty result).
- Not collecting all item identifiers before attempting deletion if the deletion logic is outside the pagination loop, or if the API has rate limits that make collecting first more efficient.
