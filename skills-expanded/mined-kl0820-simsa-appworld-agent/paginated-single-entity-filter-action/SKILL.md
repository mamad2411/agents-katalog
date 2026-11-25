---
name: paginated-single-entity-filter-action
description: Collects all paginated data for a single entity type (potentially across categories), filters it using internal or prior milestone data, and performs a single, designated action on each filtered item.
---
## Overview
This pattern addresses tasks involving comprehensive data collection from paginated APIs, potentially across multiple categories or using different filter parameters. It then applies sophisticated filtering logic, which may involve cross-referencing with other retrieved data or data from prior milestones, to identify specific items for a subsequent conditional action. The process ensures all relevant data is processed, actions are performed on the correct subset, and includes robust error handling and an audit trail.

## When to Apply
- The task requires collecting 'all' or 'every' relevant entity from a paginated API.
- Data collection needs to be performed across distinct categories or using different filter parameters.
- Filtering items based on attributes, relationships, time-based criteria (e.g., 'yesterday', 'today'), or multi-criteria matching.
- Cross-referencing data from multiple sources or using data from prior milestones for filtering or action triggers.
- Performing a specific action on a subset of retrieved items.
- API documentation indicates pagination for data retrieval endpoints.

## Procedure
1.  **Identify Collection Parameters:** Determine distinct categories or filter parameters for initial data collection, if applicable.
2.  **Initialize Accumulator & Pagination:** For each category/filter (or a single collection if no categories), initialize an accumulator (list or dictionary) and pagination parameters (e.g., `page_index`, `page_limit`, `offset`).
3.  **Paginated Data Collection Loop:**
    *   Repeatedly call the data retrieval API with current category/filter and pagination parameters.
    *   Implement robust API response handling: check for API error responses and break if an error occurs. Check for indicators of completion (e.g., empty page, fewer items than limit) and break the loop if found.
    *   If the API returns a list of items, append them to the accumulator. If using a dictionary, handle deduplication and merging of attributes for existing keys.
    *   Update pagination parameters for the next iteration.
4.  **Prepare Filtering Data:**
    *   Read any necessary filtering or matching data from prior milestone variables or retrieve additional entities (paginated if necessary).
    *   Transform this filtering data into an efficient lookup structure (e.g., sets of identifiers).
    *   Define time-based criteria if required by the task (e.g., calculate relative dates).
5.  **Filter Collected Data:**
    *   Iterate through the primary collected dataset.
    *   Apply filtering logic, potentially checking multiple fields against the lookup structure and time-based criteria. Consider both server-side and client-side filtering efficiency.
    *   For each selected item, extract and store the specific identifiers and relevant attributes needed for subsequent actions.
6.  **Perform Conditional Action:**
    *   Initialize an empty container to record the outcomes of the actions and an audit trail.
    *   Iterate through the list of selected target items.
    *   For each target item, extract its unique identifier(s).
    *   Call the designated action API using the extracted identifier(s).
    *   Record the response or outcome of the action in the action outcomes container, accumulating an audit trail.
7.  **Format Output:** Format the accumulated action results for the final output, including a summary of actions performed and recorded outcomes, preserving relevant fields and potentially nesting related information.

## Key Patterns
-   **Pagination Loop:** Iteratively call a data retrieval API with incrementing page parameters (e.g., page index, offset) until no more data is returned, indicated by an empty or incomplete page.
-   **Data Accumulation:** Build a complete dataset by extending an accumulator list or container with results from each paginated API call.
-   **Categorical Iteration:** Iterate through distinct categories or filter parameters, performing a full paginated retrieval for each to ensure comprehensive data collection.
-   **Deduplication and Attribute Merging:** When collecting data from multiple sources or categories, store items in a dictionary keyed by a unique identifier. Merge attributes (e.g., lists of relationships) for items with the same key rather than overwriting.
-   **Data Transformation and Selection:** Extract specific fields and apply filtering criteria to raw API responses, potentially combining server-side and client-side filtering to identify target items.
-   **Efficient Lookup Set Creation:** Create hash-based collections (e.g., sets of emails, IDs) from reference datasets for O(1) average-case lookup time during filtering.
-   **Date-Based Filtering:** Calculate relative dates (e.g., 'yesterday', 'today') from a `task_date` and use them to filter items based on their timestamp.
-   **Multi-Criteria Matching:** Apply filtering logic that checks multiple fields (e.g., email OR name) against lookup sets to ensure robust matching.
-   **Prior Variable Consumption:** Directly access and use data stored in `prior_variable_values` from previous milestones as input for subsequent processing.
-   **Iterative Action Execution:** Perform a state-changing operation or a specific action for each item in a previously identified and filtered list, often using an identifier extracted from the item.
-   **Robust API Response Handling:** Check the type and content of API responses (e.g., `isinstance(resp, dict)`) to guard against unexpected formats or errors before processing.
-   **Structured Output Construction:** Construct the final output as a list of dictionaries, preserving relevant fields and nesting related information as required.

## Common Pitfalls
-   **Incomplete Pagination:** Failing to implement a complete pagination loop, resulting in partial data collection.
-   **API Error Handling:** Not handling API error responses or empty results gracefully during data retrieval, leading to crashes or infinite loops.
-   **Data Merging Issues:** Overwriting data instead of merging attributes when deduplicating items collected from multiple categories.
-   **Inefficient Filtering:** Using inefficient data structures for lookups (e.g., lists instead of sets), leading to performance issues.
-   **Date Parsing Errors:** Incorrectly parsing or comparing dates, especially across time zones or formats.
-   **Prior Variable Mismatches:** Incorrectly extracting or transforming data from prior milestone variables, causing errors in subsequent steps.
-   **Filtering Edge Cases:** Missing edge cases in filtering logic, such as null values or variations in identifier formats (e.g., case sensitivity, leading/trailing spaces).
-   **Lack of Audit Trail:** Failing to collect an audit of actions performed, making it hard to verify task completion.
-   **Data Structure Assumptions:** Not verifying data structure or content from one milestone to the next.
-   Failing to extract the correct unique identifiers from selected items for subsequent actions.
-   Not handling the edge case where no items are found or selected, leading to errors in subsequent action steps.