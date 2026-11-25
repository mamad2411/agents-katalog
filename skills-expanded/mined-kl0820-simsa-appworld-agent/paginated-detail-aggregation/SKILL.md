---
name: paginated-detail-aggregation
description: Describes how to aggregate data from detailed records retrieved through paginated primary records.
---
## Overview
This skill addresses scenarios where a primary API provides a paginated list of high-level records, and a secondary API is needed to fetch detailed information for each of these records. The goal is to perform an aggregation or calculation based on the detailed data across all records. It involves handling pagination, iterating through primary records, making individual detail calls, and then processing the collected data.
## When to Apply
- Retrieve all X and then process their Y details.
- Find the Z of all items, where Z requires detailed information.
- Calculate a metric across a collection of entities, where the collection is paginated and the metric requires individual entity details.
## Procedure
1. Initialize a container for all primary entities.
2. Implement a pagination loop to retrieve all primary entities from a listing API, adding them to the container. The loop should terminate when an empty or partial page is received.
3. Initialize a container for aggregated results, often a list of tuples or dictionaries.
4. Iterate through each primary entity collected.
5. For each primary entity, call a detail API using its identifier to retrieve comprehensive information.
6. Extract specific data points from the detailed entity response.
7. Perform an intermediate calculation or aggregation based on the extracted data for the current entity.
8. Store the intermediate result, associating it with the primary entity's identifier if needed.
9. After processing all primary entities, perform a final aggregation or selection across all intermediate results.
10. Apply any required final transformations, such as unit conversions or rounding.
11. Construct the final output in the specified format.
## Key Patterns
- **Pagination Loop Termination:** A while True loop with a page_index increment and break conditions for an empty page or a page containing fewer items than the page_limit ensures all paginated data is retrieved.
- **Iterative Detail Retrieval:** When a high-level listing API provides insufficient detail, iterate through each item from the listing and make a separate API call to a detail endpoint using the item's identifier.
- **Robust Data Access:** Before accessing nested data or iterating over collections within an API response, always check the response type and the existence of expected keys to prevent errors.
- **Handling Empty Collections Gracefully:** Implement explicit checks for empty initial data sets or aggregated result sets to provide default values or handle edge cases without errors, especially before operations like max() or sum().
- **Incremental Aggregation:** Accumulate partial sums or counts within a loop for each detailed item, then use these partial results for a final overall aggregation.
## Common Pitfalls
- Forgetting to handle pagination, leading to incomplete data.
- Not checking for empty lists or null responses from API calls before processing, causing runtime errors.
- Assuming all necessary data is available in the initial paginated list, neglecting to call detail APIs.
- Incorrectly accumulating or aggregating data across iterations.
- Off-by-one errors or infinite loops in pagination logic.
- Not handling the case where no primary records are found.
