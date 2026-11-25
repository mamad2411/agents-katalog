---
name: paginated-data-enrichment-and-optional-action
description: Retrieves all entities from a paginated API, enriches each with details, and then either returns the enriched list or conditionally performs a specified action.
---
## Overview
Many APIs provide paginated lists of summary data, requiring multiple calls to retrieve all items. Often, these summary items lack specific details needed for the task, necessitating individual detail calls for each item. This skill describes the process of combining these two patterns to gather comprehensive data, and then optionally applying conditions and performing actions on the enriched items.

## When to Apply
- When a task requires a complete list of entities from an API that is known to be paginated.
- When the initial list API response provides only summary information for each entity.
- When a separate API call is available to retrieve detailed information for individual entities using an identifier from the summary list.
- When a condition needs to be applied to the detailed information of each item.
- When an action (e.g., removal, update) needs to be performed on items that satisfy the condition, or when the task simply requires returning the fully enriched list.

## Procedure
1. Initialize an empty list to store all collected primary entities.
2. Initialize pagination parameters (e.g., page index, page limit, offset).
3. Enter a loop to repeatedly call the paginated list API:
    a. Make a call to the paginated list API with the current pagination parameters.
    b. Validate the response to ensure it is a list and contains items. If not, or if the number of items is less than the page limit, break the loop.
    c. Extend the collected entities list with the items from the current page.
    d. Increment the pagination parameter for the next page.
4. Initialize an empty list to store the enriched entities, or identifiers/details of entities on which an action is performed.
5. Iterate through each primary entity collected from the paginated list:
    a. Extract the unique identifier for the entity from its summary data.
    b. Make a detail API call using this identifier to retrieve the full, detailed information for that specific entity.
    c. Validate the detail API response to ensure it's in the expected format and contains the required information.
    d. Combine the summary data and the detailed information into a single, comprehensive, enriched entity dictionary, prioritizing detail data where fields overlap.
    e. **If the task requires only an enriched list:** Add the enriched entity to the list of enriched entities.
    f. **If the task requires conditional action:**
        i. From the detailed entity information, extract the specific data point relevant to the task's condition.
        ii. Apply the task's condition to the extracted data point.
        iii. If the condition is met, perform the specified action using the appropriate API, passing the necessary identifiers (e.g., primary entity ID, sub-entity ID if applicable).
        iv. Record the identifiers or relevant details of the entity on which the action was performed.
6. After processing all entities:
    a. **If returning an enriched list:** Return the list of enriched entities.
    b. **If performing conditional actions:** Summarize the total number of actions performed and any other requested output.

## Key Patterns
- **Pagination Loop:** To retrieve all items from a paginated API, use a 'while True' loop, incrementing a 'page_index' or 'offset' parameter with each call, and break the loop when the API returns an empty list or a clear signal of no more data. Accumulate results from each page.
- **Multi-step Data Enrichment (N+1 Detail Fetch):** After collecting summary items from a list API, iterate through each item and make a separate API call to retrieve additional, missing details using an identifier from the summary item.
- **Data Merging/Enrichment:** Combine fields from the initial summary response and the subsequent detail response into a single, comprehensive data structure for each entity, handling potential field overlaps by prioritizing the more detailed source.
- **Defensive Data Access:** Before accessing fields from an API response, especially from detail calls or paginated list calls, check the response type (e.g., 'isinstance(response, list)') and the presence of expected keys to prevent errors.
- **Conditional Action:** After enriching data, apply the task's specific condition to the newly available detailed fields. Only items satisfying this condition should trigger the final action API call.
- **Identifier Mapping/Mismatch:** Be aware that different APIs might use different key names for the same logical identifier (e.g., 'id' vs 'song_id'). Ensure the correct identifier key is used when passing values between API calls.
- **Nested Iteration for Sub-collections:** If primary entities contain sub-collections (e.g., a playlist contains songs), a nested loop may be required to iterate through the sub-collection and apply the same enrichment and conditional action pattern to its members.

## Common Pitfalls
- Forgetting to handle the termination condition for the pagination loop, leading to infinite loops or incomplete data.
- Incorrectly parsing or extracting the relevant data point from the detailed API response (e.g., wrong date format, incorrect key access).
- Failing to extract the correct identifier from the summary list for the detail API call.
- Not validating the API responses (both list and detail), leading to errors when attempting to access non-existent keys or malformed data.
- Overwriting previously collected data instead of accumulating it during pagination.
- Assuming all necessary data is present in the initial list API response, neglecting the need for detail calls.
- Applying the condition to data from the initial, partial API response instead of the enriched, detailed response.
- Using the wrong identifier (e.g., 'id' instead of 'song_id') when calling a subsequent API or performing an action.
- Not handling cases where a detailed API call might fail or return an unexpected structure, potentially causing runtime errors.
- Failing to collect or summarize the results of the actions performed, making it difficult to report task completion.