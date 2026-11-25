---
name: paginated-data-extremum-or-summary-aggregation
description: Collects and deduplicates data from multiple paginated sources, including nested details, to identify an item with an extreme value (max/min) or perform complex numerical aggregations (sum, average, count).
---
## Overview
This skill addresses tasks that involve gathering comprehensive data by combining information from multiple paginated API calls, often requiring subsequent detailed lookups for each item or from nested endpoints. APIs typically return data in paginated lists, where initial list items may contain only summary information or identifiers. This procedure describes how to iteratively retrieve all items, deduplicate identifiers, and then fetch full details for each unique item. Finally, it processes this aggregated and detailed data to identify an item that satisfies an extreme condition (e.g., oldest, newest, highest, lowest) based on a specific attribute, or to perform other numerical aggregations like sum or average.

## When to Apply
- Collect all items from one or more paginated sources, potentially requiring nested or detailed lookups.
- Find the item with the [oldest/newest/highest/lowest] value for a specific attribute from a collection of items.
- The final output requires a numerical aggregation (e.g., sum, average, count) across detailed items.
- Data needs to be enriched by calling a detail API for each item after initial collection.
- API responses are paginated and may contain only summary information or identifiers.
- When you need to retrieve a list of primary items (X), then for each X, retrieve associated records (Y), and finally aggregate a value (Z) from those Ys.
- Calculating a total based on records associated with multiple primary items.
- Summarizing data across multiple entities where each entity's details are paginated.
- Tasks involving fetching data from one source to inform queries to another source, followed by aggregation.

## Procedure
1. Initialize a collection (e.g., a set) for unique identifiers or items, and variables to track the desired aggregation (e.g., 'max_value', 'min_value', 'total_sum', 'best_item_attribute'). For max/min, initialize with an appropriate extreme value or `None`.
2. For each primary data source or initial endpoint:
    * Paginate through the source to retrieve all available items, handling pagination parameters (e.g., offset, page index) until an empty result or specific termination condition is met. Apply any initial source-side filters to minimize data transfer.
    * Extract relevant identifiers and any immediately available partial data from each item.
    * Aggregate these identifiers or items into the unique collection to prevent redundant processing.
3. Handle the edge case where no records were collected after all initial API calls.
4. Iterate through each unique identifier or item in the collected set.
5. For each identifier/item:
    * Call a detail or secondary API to retrieve complete information. This secondary API might also be paginated, requiring its own pagination handling. Apply specific filters at the API level for these records to minimize data transfer.
    * Implement a robust pagination loop for the secondary API call to retrieve *all* associated data for the current primary entity.
    * Implement robust error handling for the detail API call, skipping items that return an error or have malformed responses.
    * Validate the response to ensure it contains the expected fields.
6. Extract the target attribute value (numerical field) and any desired output attributes from the detailed item, handling potential missing data.
7. Normalize the extracted attribute value (e.g., convert date strings to datetime objects, numeric strings to integers/floats) or perform any necessary unit conversions or rounding to ensure accurate comparison or aggregation.
8. Update the aggregation variable: if finding max/min, compare the current item's target attribute value with the tracked extreme value and update if necessary; if summing, add to the total; if averaging, accumulate sum and count.
9. After processing all unique identifiers/items, extract the requested final piece of information from the identified extreme record or format the final aggregated value into the required response structure.

## Key Patterns
- **Pagination Loop & Robust Pagination Termination:** Iteratively call an API with a page index or offset parameter until an empty result or specific termination condition indicates the end of available data, ensuring all available data is retrieved. This applies to both primary and secondary data retrieval.
- **Multi-step/Nested Data Retrieval:** Initial API calls provide lists of identifiers or partial data, necessitating subsequent calls to a detail API for each identifier to gather complete information. This can involve retrieving data from multiple distinct sources or following nested relationships (e.g., primary item then its child details).
- **Identifier/Item Deduplication:** Use a set data structure to efficiently store and ensure uniqueness of identifiers or items collected from multiple sources or paginated results, preventing redundant detail fetches and ensuring each item is processed only once.
- **Data Normalization and Conversion:** Before comparing or aggregating values (e.g., dates, numbers), convert them to a consistent, comparable data type (e.g., string dates to datetime objects, numeric strings to integers/floats) or perform unit conversions and rounding to ensure accurate results.
- **Flexible Aggregation (Extremum, Sum, Average):** Maintain variables to track the desired aggregation (e.g., max/min value, total sum, count for average) and update them conditionally within a loop based on the extracted and normalized attribute value. For extremum, use built-in functions like `min()` or `max()` with a `key` argument. This also includes incremental aggregation.
- **Source-Side Filtering:** Always leverage API parameters (e.g., date ranges, direction, user identifiers) to filter data at the source as much as possible. This reduces the amount of data transferred and processed, improving efficiency and accuracy.
- **Identifier Extraction and Transformation:** Information retrieved from one API (e.g., an identifier from a list of primary entities) often needs to be extracted and potentially transformed to serve as a query parameter for a subsequent API call to retrieve related data.
- **Inter-Milestone Data Flow:** Access the complete, processed output of a previous step or milestone as the direct input for the current step, avoiding redundant API calls and ensuring data consistency.

## Common Pitfalls
- Not handling pagination correctly for *either* the initial list of primary entities *or* the associated data for each entity, leading to incomplete data retrieval, infinite loops, or errors.
- Failing to deduplicate identifiers or items collected from multiple sources or nested calls, resulting in redundant API calls, inflated counts, or incorrect analyses.
- Not validating responses from detail APIs for expected fields or error messages, causing downstream processing failures.
- Incorrectly comparing or aggregating fields due to inconsistent data types (e.g., comparing date strings lexicographically instead of chronologically), flawed comparison logic, or performing unit conversion/rounding at the wrong stage.
- Not handling the edge case where no data is collected at all or an aggregated list is empty, leading to errors when attempting to find an extreme value or perform other aggregations.
- Not extracting the specific requested field from the identified extreme item, instead returning the entire item object, or not formatting the final aggregated value correctly.
- Incorrectly initializing or updating aggregation variables (e.g., 'max_value' starting too low for negative numbers, 'min_value' starting too high, or sum/count not initialized to zero).
- Initializing the aggregation accumulator *inside* the iteration loop for primary entities, causing the sum to reset for each entity instead of accumulating across all.
- Incorrectly applying filters (e.g., applying a filter to the primary retrieval that should be on the secondary, or vice-versa), or fetching all data and filtering client-side instead of utilizing API query parameters for filtering, leading to inefficient data retrieval.
- Not handling API errors or empty responses gracefully during pagination, which can lead to crashes or incomplete data.