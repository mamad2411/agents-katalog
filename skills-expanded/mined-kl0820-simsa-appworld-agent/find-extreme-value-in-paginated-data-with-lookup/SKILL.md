---
name: find-extreme-value-in-paginated-data-with-lookup
description: Retrieves a complete dataset using paginated API calls, optionally after an initial entity search, then identifies a specific item within that dataset based on an extreme value (min/max) of one of its attributes.
---
## Overview
This skill addresses scenarios where a target item needs to be identified from a large, potentially paginated, dataset. It involves an optional initial lookup to scope the search, followed by iterative data retrieval to gather all relevant items, and finally, an aggregation step to pinpoint the desired item based on a quantitative criterion (minimum or maximum value of a specific attribute).

## When to Apply
- Find the X with the least/most Y.
- Identify the top/bottom Z based on A.
- Get the item that has the highest/lowest value for a certain property.
- Process all items related to a primary entity to find a specific one.
- You need to find an entity by an exact name or identifier first.
- You need to retrieve all associated records for an identified entity, handling paginated API responses.
- Examples: "Find the customer named 'XYZ Corp' and then identify their order with the largest total amount.", "List all products in category 'Electronics' and find the one with the lowest price."

## Procedure
1.  **Initial Entity Resolution (Optional):** If the target entity for the main data retrieval needs to be identified first (e.g., by name), perform a paginated search for this entity. Iterate through the results until an exact match is found and extract its unique identifier. If no match is found after exhausting all search pages, terminate the process gracefully.
2.  **Paginated Data Accumulation:** Using the identifier obtained from the previous step (or directly if no initial resolution was needed), perform a paginated search to retrieve all relevant items or records associated with the target. Initialize an empty list and, in a loop, call the API with increasing page indices or offsets, accumulating all results until an empty page or an explicit end-of-data signal indicates all data has been retrieved.
3.  **Extreme Value Selection:** From the accumulated list of items, identify the single item that possesses the minimum or maximum value for a specified quantitative attribute. This typically involves using a built-in function (e.g., `min()` or `max()`) with a `key` argument (often a `lambda` function) to specify the attribute for comparison.
4.  **Extract and Output:** Extract the required information or specific output field(s) from the identified item. Construct a structured output containing the unique identifier and relevant attributes of the identified item, ensuring it's in a format suitable for subsequent steps or as a final output.
5.  **Error Handling:** Ensure graceful handling for scenarios where no items are found at any stage, or if the initial entity search yields no results.

## Key Patterns
-   **Entity Lookup and Filtering / Target Entity Resolution:** Search for a primary entity by a descriptive string and then filter the results to find an exact match, often requiring case-insensitive comparison or handling of partial matches. The extracted identifier becomes crucial input for subsequent steps.
-   **Pagination Loop / Paginated Accumulation:** Repeatedly call an API with an incrementing page index or offset until no more results are returned, accumulating all data from each page into a single, complete collection.
-   **Extremum Finding / Max/Min Item Selection:** Iterate through a collection of items to identify the single item with the minimum or maximum value for a specific numeric attribute, often using `min()` or `max()` with a `key` function (e.g., a `lambda` function).
-   **Result Structuring / Chained Data Flow:** Create a dictionary or object with specific keys (e.g., ID, title, value) for the identified item. The output of one API call or processing step becomes the crucial input for a subsequent API call or processing step, with subsequent steps executing only if preceding steps successfully yield necessary data.

## Common Pitfalls
-   **Incomplete Pagination:** Failing to implement a complete pagination loop, leading to partial data retrieval and potentially incorrect extreme value selection.
-   **Incorrect Entity Matching:** Incorrectly matching the primary entity from search results (e.g., not handling case sensitivity, partial matches, or multiple similar results).
-   **Missing Entity Handling:** Not handling cases where the initial entity search yields no results, causing subsequent API calls to fail or leading to runtime errors.
-   **Empty List Errors:** Failing to handle empty search results for the primary entity or empty paginated collections of sub-entities, which can lead to runtime errors when attempting to find a maximum or minimum value.
-   **Incorrect Identifier Extraction:** Incorrectly extracting the unique identifier from the identified entity for subsequent API calls.
-   **Incorrect Key for Min/Max:** Incorrectly specifying the `key` for `min()`/`max()` operations, leading to incorrect results or errors.
-   **Attribute Confusion:** Confusing the attribute used to determine the maximum/minimum with the attribute that needs to be extracted as the final answer.
-   **Incorrect Value Comparison:** Incorrectly comparing values when finding the extremum (e.g., comparing strings instead of numbers, or not handling missing values gracefully).