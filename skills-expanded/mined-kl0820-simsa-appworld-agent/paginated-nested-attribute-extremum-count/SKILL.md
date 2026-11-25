---
name: paginated-nested-attribute-extremum-count
description: Collects data from a paginated API, extracts and counts occurrences of a specific nested attribute, and identifies the attribute with either the minimum or maximum frequency.
---
## Overview
This skill addresses scenarios requiring the collection of all available data from an API that returns results in pages. It then processes this collected data to extract and count occurrences of a specific nested element. Finally, it determines the element with either the lowest or highest frequency (minimum or maximum count).

## When to Apply
- The task requires processing all available records from an API that supports pagination.
- The task involves counting occurrences of a specific attribute within nested data structures or sub-entities.
- The task asks to identify an item based on either the minimum frequency ('least frequent', 'minimum count') or the maximum frequency ('most frequent', 'most common') of its occurrences.
- Need to aggregate data across multiple API calls.

## Procedure
1. Initialize an empty data structure (e.g., a counter or dictionary) to store aggregated counts for the target attributes.
2. Initialize pagination parameters (e.g., page index, limit).
3. Implement a loop to paginate through the API endpoint:
    a. Make an API call with the current pagination parameters.
    b. Check the response for termination conditions (e.g., empty list, fewer items than limit, error). If met, break the loop.
    c. Iterate through each primary item in the current page's response.
    d. For each primary item, iterate through its nested collection of sub-entities (if applicable).
    e. Extract the relevant attribute from each sub-entity and increment its count in the initialized data structure.
    f. Increment the pagination index for the next call.
4. After the pagination loop completes, check if the aggregated data structure is empty.
5. If not empty, identify the key within the aggregated data structure that has either the minimum or maximum associated count, depending on the task requirement.
6. Handle the case where no attributes were counted.
7. Return the identified key or the formatted result.

## Key Patterns
- **Pagination Loop with Accumulation:** Data is accumulated incrementally within the pagination loop. The loop continues as long as the API returns non-empty results, ensuring all pages are processed before final aggregation.
- **Nested Attribute Extraction and Counting:** When the target attribute is within a list of dictionaries nested inside a primary data object, iterate through the list and extract the specific field from each dictionary to use as a key for counting.
- **Extremum Value Identification:** After aggregating counts, the item with the desired extremum (minimum or maximum) count is identified by iterating through the aggregated counts and using a key function to compare values, ensuring the correct item is selected based on its associated count.

## Common Pitfalls
- Not correctly identifying the termination condition for pagination, leading to infinite loops or incomplete data collection.
- Errors due to incorrect or unsafe access of nested data structures, particularly when attributes might be optional or have varying types (e.g., not using `.get()` or checking for `None`).
- Failure to properly initialize the aggregation data structure before populating it, resulting in runtime errors when attempting to add or update entries.
- Attempting to perform aggregation or extremum calculations on an empty dataset, leading to errors if not explicitly handled.
- Using an inefficient counting method for large datasets.
- Processing data incrementally within the loop when the task requires a global minimum/maximum, which necessitates full accumulation first.