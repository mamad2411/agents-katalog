---
name: collect-filter-deduplicate-and-perform-chained-actions-on-entities
description: Collects entities from paginated sources, extracts, filters, and deduplicates them, then performs a sequence of actions on each processed entity.
---
## Overview
This skill provides a robust strategy for tasks that involve acquiring a potentially large set of entities from paginated sources, applying specific processing steps like extraction, filtering, and deduplication, and then performing one or more sequential actions on each of the processed entities. It emphasizes efficient data acquisition through proper pagination handling, structured data preparation, and ensuring seamless data flow between sequential processing steps and subsequent actions.

## When to Apply
- When an API provides a paginated list of items.
- When items need to be gathered, potentially extracted from nested structures, and deduplicated.
- When items need to be filtered based on specific criteria, including those derived from other data sources or dynamic calculations (e.g., date ranges).
- When one or more distinct, sequential actions need to be performed on each item from a processed list.
- When data from one step needs to be prepared for use in a subsequent step or for efficient lookup during filtering.
- When the task requires reading all items from a collection and then performing an action on each of them.
- When entities need to be identified based on criteria and then modified.

## Procedure
1.  **Prepare Auxiliary Data & Dynamic Parameters:**
    *   If necessary, retrieve auxiliary data (e.g., identifiers) from a prior milestone or API call.
    *   Prepare auxiliary data for efficient lookup (e.g., create a set of identifiers).
    *   Calculate any dynamic parameters, such as date ranges, based on the task context.
2.  **Collect Entities:**
    *   Identify the API endpoint for retrieving the target entities.
    *   Determine if the API supports pagination and how to iterate through pages to collect all entities.
    *   Initialize an empty list to store all raw items and pagination state (e.g., page index, limit).
    *   Iteratively call the primary API to fetch paginated lists of items, accumulating all results until no more pages are available (e.g., an empty response).
3.  **Extract & Deduplicate Entities:**
    *   For each item retrieved across all pages, extract the relevant sub-elements or identifiers, which may involve iterating through nested structures.
    *   Use a data structure (e.g., a set or dictionary) to track unique identifiers for deduplication, ensuring each unique entity is represented only once.
    *   Convert the deduplicated structure into a clean list of unique entities.
4.  **Filter Entities:**
    *   Apply filtering criteria, prioritizing server-side filtering via API parameters to reduce data transfer and processing load.
    *   If server-side filtering is insufficient, perform client-side filtering against the accumulated items, using both direct criteria and auxiliary data prepared in step 1.
    *   Handle the case where no entities are found after filtering.
5.  **Project & Prepare for Action:**
    *   Project the collected, extracted, deduplicated, and filtered entities into a standardized format, extracting only the necessary fields and identifiers for subsequent actions.
    *   Handle the edge case where the processed entity list is empty.
6.  **Perform Chained Actions:**
    *   Iterate over each projected entity in the final list.
    *   For each entity, perform a sequence of API calls or other operations (chained actions), passing the extracted identifiers and any fixed or dynamic parameters.
    *   Handle the output for state-changing actions, typically indicating success rather than returning data.
    *   Accumulate identifiers or summaries of successfully processed items.
    *   Generate the final JSON output, typically setting the `value` field to `null` if the primary outcome is a side effect, and providing a descriptive summary of the actions taken.

## Key Patterns
-   **Pagination Loop:** Repeatedly call an API with an incrementing page index/offset until an empty or short page indicates no more results, accumulating items from each page.
-   **Nested Data Extraction:** Access fields within complex, nested data structures (e.g., a list of dictionaries within a dictionary) to retrieve the target sub-entities.
-   **Deduplication by Key/Identifier:** Using a set or dictionary to store unique identifiers or objects, preventing redundant processing of the same entity, even if it appears multiple times in the source data.
-   **Server-Side Filtering Preference:** Always prefer to use API parameters for filtering data on the server side to reduce data transfer and processing load.
-   **Cross-Milestone Data Join/Filter:** Use data (e.g., a list of identifiers) obtained from a previous milestone to filter or enrich data fetched in the current milestone.
-   **Pre-computation for Efficiency:** Transform a list of identifiers or other auxiliary data into a set or hash map for O(1) average-case lookup during client-side filtering.
-   **Dynamic Parameter Calculation:** Derive parameters like start and end dates for a query window based on a reference date (e.g., task_date) and a duration, rather than hardcoding.
-   **Data Projection for Inter-Milestone Flow:** After collecting and processing data, transform it into a minimal, well-structured format (e.g., a list of dictionaries with only essential keys) that is easy for subsequent milestones to consume.
-   **Inter-Milestone Data Transfer / Milestone Chaining:** Explicitly reading the processed output (specifically the 'value' field) from a preceding step to use as input for the current step's operations.
-   **Chained Actions on Iterated Items / Iterative Mutation:** Looping through a collection of items and performing a predefined sequence of multiple API calls or operations for each item, typically without expecting a significant return value from each individual call, focusing instead on the side effect.
-   **Mutation Output:** When the primary goal of a step is to cause a side effect (e.g., create, update, delete), the `value` field in the final output JSON is typically `null`, and the summary describes the action taken.

## Common Pitfalls
-   Not handling pagination, leading to incomplete data retrieval or infinite loops.
-   Incorrectly identifying the unique key for deduplication, leading to duplicate processing or missed items.
-   Fetching all data and filtering client-side when server-side filtering is available, leading to inefficiency.
-   Failing to correctly extract the necessary parameters from the collected data for the subsequent action API calls, especially from nested structures.
-   Failing to project data into a clean, reusable format for subsequent steps, making downstream processing complex.
-   Not preparing auxiliary data for efficient lookup, resulting in O(N*M) filtering complexity.
-   Hardcoding date ranges or other parameters instead of calculating them dynamically, making the solution non-reusable.
-   Failing to extract the correct identifier from each item for subsequent API calls.
-   Not considering the implications of state-changing operations (e.g., what to return, how to handle errors).
-   Not accumulating results or processed items, losing track of what was done.
-   Expecting a data return from an API call that primarily performs a mutation or side effect.
-   Not correctly accessing the output of a prior milestone.
-   Not handling the edge case where the initial data collection or processed list is empty.
-   Incorrectly formatting the final JSON output, especially for mutation milestones where 'value' is often `null`.