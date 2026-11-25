---
name: paginated-filtered-iterative-action
description: Retrieves and filters paginated entities (potentially across multiple types and using cross-milestone data), then performs an action on each qualifying one, providing a summary of actions.
---
## Overview
This skill addresses tasks requiring a multi-stage process: first, efficiently identifying and gathering a list of target entities that meet specific criteria. This often involves retrieving data from paginated APIs, potentially across different entity types, and applying complex filtering conditions that may incorporate data from prior steps or multiple sources. Second, iterating through this collected and filtered list to perform a designated state-changing action on each qualifying entity. The output of the first stage serves as the direct input for the second, covering robust data collection, validation, multi-condition filtering, and sequential execution of actions, culminating in a structured summary of the actions taken.

## When to Apply
- The task requires retrieving a list of entities that might exceed a single API call's return limit, necessitating pagination.
- Filtering criteria need to be applied to the retrieved entities, potentially both server-side and client-side.
- Filtering criteria include data obtained from a previous milestone or other sources.
- An action needs to be performed on each entity that satisfies the filtering criteria.
- The task involves a sequence of finding/filtering data and then acting upon it.
- The task may involve identifying and acting on entities of one or more types based on common filtering criteria.
- The task involves a mutation or side-effect on the filtered items.
- The final output should summarize the items on which the action was performed.

## Procedure
1.  **Prepare Filtering Criteria:**
    *   Retrieve necessary filtering criteria or identifiers from prior milestone variables or other sources.
    *   Pre-process retrieved criteria for efficient lookup (e.g., create a set for O(1) average-case lookups).
    *   Determine any dynamic criteria, such as the current date or time, and compute target date strings if needed.
2.  **Retrieve All Paginated Data:**
    *   Initialize an empty list to store identifiers and minimal data of items to be acted upon.
    *   For each entity type relevant to the task (if multiple types are involved, otherwise proceed for a single type):
        a.  Identify the API endpoint for retrieving the target entities of this type, noting any pagination parameters (e.g., `page_limit`, `page_index`, `continuation_token`).
        b.  Consult API documentation to determine available filters that can narrow down results according to the specified criteria, applying all possible filters directly at the API level to minimize client-side processing.
        c.  Implement a pagination loop: repeatedly call the retrieval API, incrementing the page offset/index or using continuation tokens, and accumulating all results until an empty page is returned or a partial page indicates the end of the dataset. Check the API response for error indicators (e.g., a 'message' key). If an error is present, handle it (e.g., break the loop or log the error).
        d.  After collecting all potential entities for the current type, apply any necessary client-side filtering to ensure all criteria are met, especially if server-side filtering was insufficient, inconsistent, or for nested fields. This includes applying all specified filtering conditions (e.g., date comparisons, string matching, membership checks against pre-processed prior data). Ensure conditions are applied with logical AND.
        e.  From the accumulated and filtered results, extract only the minimal necessary identifiers and relevant data points for subsequent steps, adding them to the master collected list.
3.  **Perform Conditional Action and Summarize:**
    *   Identify the API endpoint(s) for performing the required action(s) on a single entity. If different entity types require different action APIs, note these.
    *   Iterate through the collected list of qualifying entities/identifiers.
    *   For each entity, call the appropriate action API using its extracted identifier and minimal data. If identifiers from different types are present, ensure the correct API is called for each type.
    *   Accumulate the results or status of each action for reporting, extracting specific fields from the item and the action's result to construct a summary object for the action performed.
4.  **Construct Final Output:**
    *   Construct the final output as a JSON object containing the list of processed items, a summary string describing the actions, and a description of the overall outcome.
    *   If the milestone is primarily for side-effects and no specific data needs to be returned, the 'value' field of the output contract should typically be 'null', with 'summary' and 'description' providing context about the action performed and its results.

## Key Patterns
-   **Pagination Loop/Exhaustion:** Repeatedly call a list-retrieval API, incrementing an offset or page index, or using a continuation token, and accumulating results until an empty response indicates no more data.
-   **Comprehensive & Defensive Filtering:** Leverage API parameters to filter data at the source (API-level filtering) and apply additional client-side filtering on the collected data to ensure robustness, handle potential API inconsistencies or limitations, and re-verify exact criteria. This includes applying a logical AND of multiple conditions, such as date comparisons, string matching, and membership checks.
-   **Cross-Milestone Data Dependency/Flow:** Data extracted and processed in an earlier milestone (or from other sources) is used as a filtering criterion or parameter in a subsequent milestone, often pre-processed into an efficient lookup structure (e.g., a set) using stable identifiers.
-   **Minimal Data Extraction:** After an API call, extract only the specific fields required for subsequent steps or the final answer, discarding irrelevant data to maintain efficiency and clarity.
-   **Chained Operations (Collect then Act):** The output of one logical step (e.g., data collection and filtering) directly serves as the input for a subsequent logical step (e.g., performing actions on collected data). Collect all target item identifiers first, then iterate through this collection to perform individual actions, rather than acting immediately within the search loop.
-   **Iterative Action/Conditional Action Execution:** When a task requires performing an action on multiple items, iterate through the collection of items and call the relevant action API for each, passing the item's unique identifier. An API call that modifies state (a mutation or side-effect) is only executed for items that satisfy a predefined set of filtering conditions.
-   **Cross-Type Aggregation:** When the task involves multiple entity types, identify and collect identifiers from each type based on common criteria, then aggregate them into a single list for subsequent action, ensuring the correct action API is called for each type.
-   **Set-Based Lookup for Efficiency:** Converting lists of identifiers from prior steps into a set for O(1) average-case lookup during filtering.
-   **Action Milestone Output:** For milestones that perform state-changing or destructive actions, the 'value' field of the output contract should typically be 'null', with 'summary' and 'description' providing context about the action performed and its results.

## Common Pitfalls
-   **Incomplete Pagination:** Not exhausting pagination, leading to incomplete data processing, or incorrectly implementing pagination termination conditions (e.g., infinite loops or missing the last page).
-   **API Error Handling:** Not handling API error responses or empty lists gracefully during pagination or action calls.
-   **Filtering Issues:** Filtering data client-side when API-level filters are available, or conversely, relying solely on server-side filtering without client-side validation for edge cases or nested fields. Incorrectly applying filtering conditions (e.g., using OR instead of AND, or not handling date/time comparisons correctly), leading to over- or under-filtering.
-   **Inefficient Prior Data Usage:** Failing to pre-process prior milestone data or external data for efficient lookup, resulting in slow or incorrect filtering.
-   **Incorrect Data Extraction/Structuring:** Failing to correctly extract the unique identifier or necessary data points from the retrieved items for the subsequent action, or not correctly extracting and structuring data from one milestone for efficient use in the next.
-   **Unnecessary Data Passing:** Extracting and passing along unnecessary data fields between steps, impacting efficiency.
-   **Unstable Identifiers:** Using unstable identifiers (like names) for cross-milestone joins instead of stable unique keys (like IDs or normalized emails).
-   **Unconditional Action:** Performing the action unconditionally instead of only on filtered items.
-   **Incorrect Output Structure:** Incorrectly setting the 'value' field for action-oriented or destructive milestones (should often be 'null'), or not extracting all required fields for the final output or structuring it incorrectly.
-   **No Matches Handling:** Not handling the case where the initial retrieval yields no results gracefully, or where no items match the filtering criteria (e.g., attempting to call an action API on an empty list).
-   **Not Accumulating Batch Action Results:** Failing to accumulate results or status messages from iterative action calls for proper reporting, making it difficult to audit or confirm which specific actions succeeded or failed.
-   **Acting within Search Loop:** Attempting to perform actions directly within the search loop, which can be inefficient or problematic if the search API has rate limits or if the action itself affects subsequent search results.
-   **Incomplete Target Identification:** Not identifying all targets comprehensively before initiating actions, potentially missing items or performing actions on incorrect items.