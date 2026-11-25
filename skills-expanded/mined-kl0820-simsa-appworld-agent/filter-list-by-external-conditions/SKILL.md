---
name: filter-list-by-external-conditions
description: Filters an existing primary list of items by applying conditional inclusion or exclusion logic based on lookup data from multiple external sources or prior processing, then performs an iterative action on the refined subset.
---
## Overview
This skill addresses tasks that require combining information from multiple, disparate data sources or prior processing steps to build a precise list of targets for a final, iterative action. It involves retrieving initial entities, gathering specific details for the action, identifying exclusions or inclusions, structuring this combined data for efficient lookups, and then performing an action on the filtered set.

## When to Apply
- When an instruction requires combining information from multiple prior milestones or disparate data sources.
- When an instruction specifies excluding or including certain items based on data from another source.
- When an instruction requires performing an action for each item that satisfies specific conditions.
- When an instruction involves mapping identifiers or attributes between different datasets.
- When a base list of entities comes from one source, and exclusion criteria or action details from another.
- When you need to perform an action on a filtered list of items.

## Procedure
1.  **Retrieve all necessary data:** Gather the initial list of potential target entities, details required for the final action, and any exclusion or inclusion criteria from various data sources or prior milestone variables. This may involve iterative pagination for large datasets.
2.  **Prepare data for efficient lookups:** Transform relevant data into efficient lookup structures (e.g., dictionaries for key-value mapping, sets for quick membership checking of unique identifiers).
3.  **Normalize and reconcile identifiers:** Establish a consistent mapping or join key to link entities across different data sources. Ensure identifiers and attributes are in a consistent format (e.g., all lowercase, stripped of whitespace) to prevent mismatches.
4.  **Iterate and apply conditional logic:** Iterate through the primary dataset that will drive the actions. For each item, use its attributes to look up corresponding information in the other prepared data structures. Apply conditional logic (e.g., exclusion, inclusion) based on the combined information.
5.  **Perform the specified action:** If an item meets the conditions, perform the specified API action using the relevant associated details.
6.  **Collect results:** Collect the results or identifiers of each successful API action into a list for the final output.

## Key Patterns
-   **Multi-source Data Integration:** Combine information from several distinct API calls, data structures, or prior milestones to build a complete picture of entities, their associated details, and any exclusion/inclusion criteria.
-   **Lookup Table Creation & Identifier Reconciliation:** Transform lists of records into dictionaries (mapping a key attribute to an entire record or another attribute) or sets (for quick membership checks of unique identifiers) to efficiently join or cross-reference data.
-   **Exclusion/Inclusion Set Construction & Conditional Iteration:** Build a set of identifiers for entities that should be excluded or included, allowing for efficient O(1) lookup during the filtering phase. Iterate over a primary set of items, applying conditions derived from other data sources.
-   **Data Normalization for Comparison:** Before comparing identifiers or attributes across different data sources, ensure they are in a consistent format (e.g., all lowercase, stripped of whitespace) to prevent mismatches.
-   **Iterative Pagination:** Repeatedly call a list-returning API with incrementing page indices and a fixed page limit until all available data has been retrieved.
-   **Structured Content Parsing:** Extract specific data points from a larger block of unstructured text by splitting on delimiters, stripping whitespace, and converting data types.
-   **Date-based Filtering:** Use date/time parameters (e.g., 'since yesterday', 'created_at') to narrow down search results or filter retrieved data, often requiring date string formatting.

## Common Pitfalls
-   **Failing to normalize data:** Mismatched or inconsistent identifiers (e.g., case sensitivity, leading/trailing whitespace) when attempting to join or cross-reference data, leading to missed matches.
-   **Inefficient data structures:** Using linear searches in lists for frequent lookups instead of dictionaries or sets, especially with larger datasets.
-   **Incorrect conditional logic:** Applying exclusion or inclusion logic incorrectly, leading to either over-inclusion (acting on entities that should be excluded) or under-inclusion (missing entities that should be acted upon).
-   **Missing data handling:** Not handling cases where a lookup key might not exist in a dictionary (use `.get()` or explicit checks) or empty results from intermediate data retrieval steps.
-   **Pagination errors:** Failing to correctly paginate and retrieve all relevant data from list-returning APIs.
-   **Parsing errors:** Errors in parsing structured information from free-form text due to unexpected formats or missing delimiters.
-   **Data type mismatches:** Ignoring the need for data type conversions (e.g., string to number for amounts) before performing calculations or API calls.
-   **Forgetting to collect results:** Not collecting the results of iterative API calls, making it impossible to report on the actions taken.