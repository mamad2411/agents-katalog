---
name: paginated-data-filter-create-mutate
description: Applies when the task involves acquiring paginated data, filtering it, creating a new resource, and then populating that resource with the filtered data.
---
## Overview
This skill addresses tasks that require a multi-stage data flow: first, gathering data from a paginated source, enriching it with per-item detail calls, and filtering it based on specific criteria. Second, it involves creating a new resource with a given identifier. Finally, it populates that newly created resource by adding the previously filtered items to it.
## When to Apply
- Acquire data from a paginated API.
- Filter items based on specific criteria (e.g., attribute values, date ranges).
- Create a new resource (e.g., a playlist, a document, a record).
- Add multiple items to an existing resource.
- Combine data from multiple API calls to form a single filtered list.
## Procedure
1. Initialize an empty list to accumulate items from a paginated source.
2. Loop through pages of the initial data acquisition API, accumulating all items until no more data is returned.
3. For each item obtained from the initial acquisition, call a detail API to retrieve additional attributes.
4. Filter the detailed items based on specified criteria (e.g., matching an attribute value, comparing a date).
5. Store the filtered items as a list of dictionaries, each containing necessary identifiers and attributes, for subsequent use.
6. Call an API to create a new resource, providing required parameters like a name or type.
7. Extract the unique identifier of the newly created resource from the API response.
8. Iterate through the previously filtered list of items.
9. For each filtered item, call a mutation API to add it to the newly created resource, using the resource's identifier and the item's identifier.
10. Output 'None' as the final result for the mutation phase, indicating a side effect completion.
## Key Patterns
- **Pagination Loop:** Iteratively call a list-fetching API with an incrementing page index or token until an empty result or specific termination condition is met, accumulating all results into a single list.
- **Per-Item Detail Fetch:** After an initial list fetch, for each item in the list, make a separate API call to retrieve more detailed attributes for that specific item, often using an identifier from the initial list.
- **Chained Filtering:** Apply multiple filtering conditions sequentially (e.g., first by one attribute, then by another, then by a date range) to refine a dataset, often after enriching items with detail calls.
- **Resource Creation and ID Extraction:** Call an API to create a new resource and immediately extract its unique identifier from the successful response for use in subsequent operations.
- **Bulk Mutation via Iteration:** Perform a mutation operation (e.g., adding items, updating properties) by iterating over a pre-filtered list of items and making a separate API call for each item.
- **Intermediate Data Structure:** Store processed data from one milestone (e.g., filtered items with enriched details) in a structured format (e.g., list of dictionaries) to be consumed as input by a subsequent milestone.
## Common Pitfalls
- Not handling pagination correctly, leading to incomplete data acquisition or infinite loops.
- Failing to extract the necessary identifier from an API response for subsequent calls, causing downstream failures.
- Incorrectly applying filtering logic or data type conversions (e.g., date parsing, string comparisons), resulting in incorrect filtered data.
- Not checking for API call failures (e.g., empty responses, error messages, non-dict results) at each step, leading to unexpected errors.
- Attempting to add items to a resource before it has been successfully created or its identifier extracted.
- Not passing the correct identifiers (e.g., resource ID, item ID) to mutation APIs, causing operations to fail or target the wrong resource.
