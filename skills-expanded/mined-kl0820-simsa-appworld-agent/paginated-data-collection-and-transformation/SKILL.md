---
name: paginated-data-collection-and-transformation
description: Systematically retrieves, filters, and transforms data from paginated APIs, including chained detail lookups, to produce a comprehensive, structured dataset or extract specific items for general processing.
---
## Overview
This skill addresses the challenge of gathering a complete dataset or finding specific items from an API that returns results in pages. It involves systematically requesting all pages, accumulating the results, applying robust filtering both server-side (if available) and client-side, and finally structuring, transforming, or extracting specific information from the complete dataset. This ensures all qualifying items are found, processed accurately, and presented in a usable format, or that a specific item is efficiently located. It also covers scenarios where initial paginated calls provide identifiers for subsequent detailed retrieval. This pattern can be applied once for a single objective or iteratively for multiple targets, often sourced from a previous task, with the data then aggregated across these targets.

## When to Apply
- The task requires retrieving a comprehensive list of entities from an API that supports pagination.
- You need to find all items that meet specific criteria from a source, or find a single specific item within a large dataset.
- The API documentation indicates support for pagination (e.g., 'page_index', 'page_limit', 'offset', 'next_page_token', 'has_more' flag).
- Filtering criteria need to be applied to the retrieved items, potentially both at the API level and client-side.
- The retrieved data needs to be transformed or structured into a specific format for later use or as a final output.
- The data might exceed a single API response limit.
- A search API might not return all relevant results on the first page.
- A summary API provides identifiers, and a detail API provides full content, requiring chained calls.
- The instruction mentions 'all', 'every', 'total', 'sum', 'count' for data that might be paginated.
- Task requires processing a list of items obtained from a previous step, where each item requires further API calls.

## Procedure
1.  Initialize an empty list or collection to store all accumulated results or found items, or an accumulator for the final aggregated result (e.g., a sum, a count).
2.  If applicable, retrieve a list of targets or identifiers from a prior milestone's output.
3.  For each target (or if no targets, directly proceed with a single iteration):
    4.  Initialize pagination parameters (e.g., `page_index = 0`, `page_limit`, `offset`, or a `next_page_token`), starting from the first page.
    5.  Enter a loop that continues until all pages are retrieved or a specific item is found.
    6.  Inside the loop, call the data retrieval API, providing current pagination parameters, the current target (if applicable), and any available server-side filtering parameters.
    7.  Validate the API response: if it's an error or indicates no more data, terminate the pagination loop.
    8.  Process the items received on the current page:
        *   Iterate through each item received in the current page's response.
        *   Apply client-side filtering to each item based on the task's specific criteria. This acts as a safeguard even if server-side filters were used, ensuring all criteria are strictly met.
        *   If the objective is to find a specific item: if an item passes all filters and matches the target, store it, and terminate the pagination loop immediately.
        *   If the objective is to collect all items or perform incremental aggregation: if an item passes all filters, extract the necessary fields, transform data, and add the processed item to the accumulated results list (e.g., using `list.extend()` for the whole page or appending individual processed items), or perform immediate aggregation (e.g., sum, count).
    9.  Check the API response to determine if it's the end of the results. This can be indicated by:
        *   An empty list of items in the response.
        *   A specific `has_more` flag being `false`.
        *   The number of items returned on the current page being less than the `page_limit`.
        If any of these conditions are met, break the pagination loop.
    10. Increment the `page_index` or update the `next_page_token` for the next API call.
4.  After the outer loop (or single iteration) completes:
    *   If identifiers were collected (e.g., from a summary API), perform subsequent detailed retrieval for each relevant identifier using a separate API call.
    *   Apply any final filtering, transformation, or aggregation to the collected or found data to produce the desired output.
    *   If necessary, apply deduplication (e.g., using a set) to ensure unique items in the final collection.
    *   Format the final collected and filtered data into the required output structure (e.g., a list of dictionaries with specific keys).
    *   Return the final aggregated or processed result.

## Key Patterns
-   **Pagination Loop Control:** Implement a `while True` loop that continues fetching pages until an explicit end-of-results condition is met (e.g., an empty list, a `has_more` flag is false, or fewer items than `page_limit` are returned), or a specific target item is found. Use `page_index`, `offset`, or `next_page_token` to manage progression.
-   **Iterating Prior Results:** When a task requires processing multiple entities, obtain the list of entities (e.g., IDs, emails) from a prior step's output and iterate over them, performing API calls for each.
-   **Data Accumulation & Incremental Aggregation:** Maintain a single list or collection outside the pagination loop to collect and store all items retrieved across all pages, typically using `extend()` to add items from each new page, or incrementally aggregate results (e.g., sum numerical values, append items to a list) within the pagination loop and potentially across multiple target iterations.
-   **Targeted vs. Broad Retrieval:** Distinguish between iterating to find a single specific item (and stopping early) versus iterating to collect all items that meet certain criteria.
-   **Dual Filtering (Server-side & Client-side):** Utilize API parameters for initial filtering to reduce data transfer and processing load. Always include explicit client-side checks on the received data to ensure all criteria are strictly met and to guard against API inconsistencies or partial filtering.
-   **Data Structuring/Transformation:** Selectively pull out, rename, and transform only the required fields from the raw API response objects, discarding unnecessary data, and formatting the final dataset into a specific structure required by subsequent steps or for the final output. This can also involve content-based data extraction from raw text.
-   **Summary-Detail API Chaining:** A common pattern where a 'list' or 'search' API provides high-level information (often just IDs), requiring subsequent calls to a 'get' or 'show' API for each item to retrieve full details.
-   **Result Deduplication:** Employing a mechanism (e.g., a set) to ensure that extracted or collected items are unique, especially when multiple sources or parsing methods might yield duplicates.

## Common Pitfalls
-   **Incomplete Data:** Forgetting to implement pagination, leading to only the first page of results being processed, or incorrectly handling the loop break condition, resulting in missing the last page.
-   **Inefficient Filtering:** Not utilizing available server-side filtering parameters, resulting in fetching more data than necessary, or filtering data client-side after retrieving all results, instead of using API-provided filters, which can be inefficient.
-   **Incorrect Filtering Logic:** Relying solely on server-side filtering without client-side validation, which can lead to including items that don't fully meet the criteria if the API's filtering is imperfect or incomplete.
-   **Infinite Loop:** Incorrectly defining the loop termination condition for pagination (e.g., forgetting to initialize or increment pagination parameters), causing the agent to request pages indefinitely.
-   **Data Overwrite:** Not accumulating results correctly, leading to each new page overwriting the previous one instead of adding to a growing list, or failing to initialize accumulators or resetting them incorrectly within loops.
-   **Not Handling Errors:** Failing to gracefully handle empty responses or errors from the API within the loop.
-   **Excessive Detailed Retrieval:** Performing detailed retrieval for all items when only a subset or a single item's details are needed, leading to unnecessary API calls.
-   **No Deduplication:** Not using a set or similar mechanism for deduplication when unique items are required, leading to redundant data.
-   **Incorrect Termination for Specific Item Search:** Failing to break the pagination loop immediately once a specific target item is found, leading to unnecessary API calls.