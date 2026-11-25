---
name: paginated-list-detail-extremum-aggregation
description: Aggregates a numerical value from detailed information of items retrieved from a paginated list, then identifies an extremum (max/min) among these aggregated values.
---
## Overview
This skill addresses scenarios where a primary list of entities is paginated, and each entity requires a subsequent API call to retrieve detailed attributes. The goal is to aggregate a specific numerical attribute from these detailed entities, often involving nested data structures, and then compare these aggregated values to identify an extremum (maximum or minimum) for final processing.

## When to Apply
- Retrieve a potentially long, paginated list of items.
- Calculate a metric or aggregate a value based on detailed information for each item in a list.
- Find the item with the maximum or minimum of a certain aggregated attribute.
- Perform a calculation on a sum of attributes from detailed sub-items.

## Procedure
1.  **Identify Primary List Endpoint:** Determine the API endpoint that returns a paginated list of primary entities.
2.  **Handle Pagination:** Identify pagination parameters (e.g., page index, page limit, offset, next token) and the stopping condition (e.g., empty page, no next token). Loop through the paginated API calls, accumulating all primary entities into a single collection.
3.  **Fetch Detailed Information:** For each primary entity in the accumulated collection:
    a.  Identify the unique identifier needed to fetch its detailed information.
    b.  Identify the API endpoint that returns detailed information for a single primary entity, using its unique identifier.
    c.  Call the detail API to retrieve its full attributes.
4.  **Perform Nested Aggregation:** From the detailed entity's response, locate any nested collection of sub-items and the specific numerical attribute within each sub-item that needs to be aggregated. Sum or aggregate this numerical attribute across all relevant sub-items for the current primary entity to get its total aggregated value.
5.  **Track Extremum:** Store the aggregated results, associating them with their respective primary items. Keep track of the primary entity that yields the maximum (or minimum, depending on the task) total aggregated value.
6.  **Final Processing:** Perform any required unit conversions, rounding, or other final calculations on the identified extremum.
7.  **Format Result:** Format the final numerical result into the specified output structure.

## Key Patterns
-   **Paginated List Accumulation:** Iterate through pages of a list-fetching API using identified pagination parameters until a termination condition is met, accumulating all results into a single list.
-   **Nested Detail Fetching:** After obtaining a list of primary identifiers, make a subsequent API call for each identifier to retrieve comprehensive details, which may include nested data structures relevant for aggregation.
-   **Nested Attribute Aggregation:** To calculate a sum or other aggregate for a primary entity, traverse a nested list within its detailed response and sum a specific numerical attribute from each item in that nested list.
-   **Extremum Selection/Tracking:** After aggregating values for multiple items, identify and track the item corresponding to the maximum or minimum aggregated value throughout the iteration.
-   **Unit Conversion and Rounding:** Apply arithmetic operations and rounding functions to transform a numerical result into the desired unit and precision.

## Common Pitfalls
-   Forgetting to handle pagination correctly, leading to incomplete data retrieval.
-   Not identifying the correct unique identifier to link primary entities to their detailed information API calls.
-   Failing to make detail calls for each item when necessary, resulting in missing information for aggregation.
-   Incorrectly parsing nested data structures or summing/aggregating values from them.
-   Failing to initialize the maximum/minimum tracking variable correctly (e.g., with a value that can never be exceeded/undercut).
-   Not handling the edge case where the initial list of primary items is empty.
-   Off-by-one errors or incorrect rounding during final unit conversion.
-   Assuming all necessary data is available in the initial paginated list response, overlooking the need for detail-fetching API calls.