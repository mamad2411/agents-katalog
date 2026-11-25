---
name: chained-paginated-data-aggregation
description: Retrieves a primary collection (potentially paginated), then for each item, performs a secondary paginated API call, aggregating the results.
---
## Overview
This pattern addresses tasks that involve a two-stage data retrieval and processing flow, culminating in an aggregated sum or summary. First, a primary collection of items or entities is obtained. Then, for each item in this primary collection, a secondary API call is made. Both the initial and secondary API calls might return paginated results. The data from these nested, paginated calls is then extracted, filtered, and accumulated into a final sum or aggregate value.

## When to Apply
- Calculate a total sum, count, or aggregate value across multiple records or entities.
- Retrieve a list of items or entities, then for each item, query another system or API for related data.
- The initial list of items may come from a prior step or require its own paginated API call.
- The related data API call supports pagination.
- Filter data by criteria such as date range, direction, or specific identifiers.
- Perform an action on a set of entities identified through an initial search, where the action involves aggregating data.

## Procedure
1.  **Obtain Primary Collection:**
    a.  If the primary collection is from a prior milestone's output, load it.
    b.  If the primary collection needs to be fetched via an API: Call the initial API to retrieve a collection of primary entities, applying specific filters. Implement pagination to ensure all primary entities are collected.
2.  Extract the unique identifier(s) or necessary context from each primary entity in the collection.
3.  Initialize an accumulator variable (e.g., `total_sum`, `count`, `result_list`) to its starting value (e.g., zero, empty list).
4.  For each entity/identifier in the primary collection:
    a.  Construct parameters for the secondary API call, using fields from the current entity/identifier and other task constraints (e.g., date ranges, direction, specific filters).
    b.  Initialize a page index for the secondary API call (e.g., `page = 1`).
    c.  Perform a paginated loop for the secondary API call:
        i.   Call the API with the constructed parameters and the current page index.
        ii.  Check the API response for error messages; if an error is present, or if the response indicates no data, treat it as no data for the current entity/page and break the pagination loop.
        iii. If the response is a list of records:
            *   For each record in the response list:
                *   Extract the relevant data point (e.g., numerical field).
                *   If aggregating numerical data, convert the extracted field to the appropriate data type (e.g., float).
                *   Add this value to the accumulator variable.
            *   If the number of records returned is less than the page limit, break the pagination loop (indicating no more pages).
            *   Increment the page index for the next iteration.
        iv.  Else (if response is not a list, e.g., empty or unexpected format), break the pagination loop.
5.  Perform any final processing on the accumulator (e.g., rounding, formatting).
6.  Store the final aggregated value as the milestone's result.

## Key Patterns
-   **Chained/Nested Iteration & Comprehensive Pagination:** The core pattern involves an outer loop iterating over a list of entities (e.g., recipients), and an inner loop handling pagination for API calls related to each individual entity. The page index for the inner loop *must be reset for each new entity*. Both the initial primary collection retrieval and the subsequent API calls may involve pagination.
-   **Dynamic Parameter Construction:** API parameters for the inner/subsequent call are dynamically constructed using data extracted from the current entity in the outer loop (e.g., an identifier or email).
-   **Incremental Aggregation with Filtering:** Data points are extracted from API responses and added to a running total or collection. Crucially, multiple filtering parameters (e.g., direction, date, specific entity ID) are applied to the API calls to ensure only relevant data contributes to the aggregation.
-   **Prior Milestone Data Extraction:** The list of identifiers or primary entities used for iteration can be sourced directly from the output of a preceding milestone, demonstrating inter-milestone data dependency and flow.
-   **Robust API Call Handling:** API responses are checked for specific error indicators (e.g., a 'message' key in a dictionary) to gracefully handle failures or empty results, distinguishing them from valid empty lists or successful data.
-   **Filtering at Source:** Apply filters (e.g., date ranges, direction) directly in the API call parameters to reduce the amount of data fetched and processed.

## Common Pitfalls
-   Forgetting to initialize the accumulator variable before the loops, leading to errors or incorrect sums.
-   Not resetting the page index for each new identifier in the outer loop, causing incomplete data retrieval or infinite loops.
-   Overlooking pagination for any of the API calls (initial or subsequent), leading to incomplete data.
-   Incorrectly handling pagination termination conditions for the inner/subsequent API calls.
-   Failing to convert extracted numerical fields to the correct data type (e.g., float) before accumulation, leading to type errors or incorrect string concatenation.
-   Incorrectly applying or omitting necessary filters in the API calls, resulting in an over- or under-inclusive sum.
-   Failing to dynamically pass entity-specific parameters to the inner/subsequent API call.
-   Not handling API errors or empty responses gracefully, leading to crashes or incorrect assumptions about data availability.
-   Performing aggregation logic outside the loops, leading to incorrect results.
-   Not applying filters at the API call level when possible, leading to over-fetching and inefficient processing.
-   Making multiple API calls when a single, well-parameterized call could achieve the same result.
-   Incorrectly parsing or extracting the required data fields from API responses.
-   Not correctly reading and utilizing the output from a preceding milestone.