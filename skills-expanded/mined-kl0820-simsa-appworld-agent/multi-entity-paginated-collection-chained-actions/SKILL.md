---
name: multi-entity-paginated-collection-chained-actions
description: Collects primary and auxiliary data from multiple distinct paginated sources, applies complex multi-attribute filtering across these sources, and performs multiple sequential actions on each filtered item.
---
## Overview
This skill addresses tasks that involve a multi-stage process: first, iteratively collecting primary items and potentially auxiliary/external data from multiple paginated sources; second, combining this data or using criteria derived from prior steps to filter the collection based on complex, multi-attribute conditions (e.g., date ranges, related entities, participant roles); and finally, iterating through the filtered data to perform specific actions, which may involve multiple API calls per item.

## When to Apply
- Filter a collection based on multiple attributes from different sources or related entities.
- Identify items for retention or removal based on complex logical conditions, including those derived from prior steps.
- Perform an action on a subset of items determined by cross-referencing multiple data points or criteria.
- Tasks involving 'keep only X that meet criteria A and B' or 'remove items that do not satisfy conditions C and D'.
- Process all items in a feed/list that meet certain conditions.
- Apply an action to specific records based on multiple attributes.
- Retrieve data, then filter it based on related entities.
- Iterate through a list of filtered entities to apply an update or action.
- Combine data from multiple sources to identify targets for an action.
- Filter items based on a date condition (e.g., 'today', 'this week').
- Filter items based on participant roles or relationships, cross-referencing with external data.
- The task involves processing a 'feed' or 'stream' of events/data.

## Procedure
1. Retrieve necessary filtering criteria or initial data from prior milestone variables or API calls, handling pagination and extracting necessary identifiers. Prepare external/auxiliary data into an efficient lookup structure (e.g., a set).
2. Initialize an empty list to accumulate all primary items from the paginated feed(s).
3. Implement a pagination loop for each primary data source: Call the API to get a page of items, add the retrieved items to the accumulator list, and continue looping, incrementing the page index, until a page returns fewer items than the page limit or is empty.
4. Iteratively collect all auxiliary data (e.g., status flags, related entities, participant identifiers) from their respective paginated APIs, storing relevant identifiers in efficient lookup structures like sets. Normalize identifiers (e.g., lowercasing emails) if they will be used for comparison.
5. For each primary item, cross-reference its unique identifier with the collected auxiliary/external data and apply any required data transformations (e.g., date calculations, parsing date fields into comparable objects) to prepare for filtering.
6. Apply all specified filtering conditions (which may be multi-stage, multi-criteria, or involve conditional aggregation) to each primary item, marking it for retention or removal based on the combined criteria. This may involve sequential checks (e.g., date match, then participant match), short-circuiting if an item fails an early filter.
7. Initialize a list to store identifiers of items on which an action is performed.
8. Perform the designated action(s) on the items identified in the previous filtering step, potentially executing multiple distinct API calls sequentially for each item, leveraging intermediate results from prior computations if available.
9. Add the unique identifier of each acted-upon item to the list initialized in step 7.
10. Collect relevant details of the items on which the action was performed and construct the final output, including a summary of the action performed and the identifiers of the affected items.

## Key Patterns
- **Pagination Loop / Paginated Feed Accumulation:** To ensure all data is collected from an API that returns results in pages, repeatedly call the API with an incrementing page index until an empty result or a specific error response indicates the end of the data stream, accumulating all results.
- **Set for Efficient Lookup / External Data Lookup Set:** When checking for the presence of an item's unique identifier within a large collection of auxiliary/external identifiers or a list of identifiers from a prior step, convert the collection into a set. This allows for average O(1) lookup time, significantly improving performance compared to list iteration. Normalize identifiers (e.g., lowercasing) before adding to the set if comparisons will be case-insensitive.
- **Intermediate Data Structure for Annotation:** Create a temporary data structure (e.g., a list of dictionaries) to store primary items along with computed flags (e.g., 'liked', 'downloaded', 'keep'). This centralizes all relevant information for subsequent filtering and action steps.
- **Conditional Aggregation for Complex Criteria:** For criteria that depend on the status of related sub-items (e.g., an aggregate item is 'downloaded' only if ALL its constituent sub-items are 'downloaded'), use an 'all()' check over the sub-items' statuses. Ensure to handle edge cases like empty sub-item lists.
- **Separation of Identification and Action:** First, identify all items that meet the criteria for an action. Then, in a separate loop or step, perform the action on the identified items. This improves clarity, allows for review, and prevents issues like modifying a collection while iterating over it.
- **Multi-stage and Multi-criteria Filtering:** Combine multiple conditions (e.g., date match, membership in a set) using logical operators, potentially using results from a previous API call to inform subsequent filtering criteria. Apply sequential filtering conditions, short-circuiting further processing if an item fails an early filter.
- **Iterative or Sequential Action Execution / State-Changing Action with Accumulation:** Perform one or more state-changing API calls for each item that passes the filtering criteria. Simultaneously accumulate identifiers of affected items for reporting.
- **Date Range Calculation:** Dynamically calculate start and end dates for filtering based on the current task date and a specified duration (e.g., 'last 7 days'). Parse date strings into comparable date objects before comparison.
- **Verbatim String Pass-through:** Use a literal string value directly as an API parameter when the instruction specifies exact text (e.g., a comment message).

## Common Pitfalls
- Not handling pagination correctly, leading to incomplete data retrieval, not accumulating all paginated results before filtering, or not checking for empty/error responses.
- Using inefficient data structures (e.g., lists instead of sets) for frequent membership checks, leading to poor performance.
- Incorrectly applying complex logical conditions (e.g., misinterpreting 'AND' vs. 'OR', or 'all' vs. 'any' for aggregated criteria, incorrect date/time or date range comparisons, timezone issues, off-by-one errors).
- Failing to account for API error responses or edge cases during data collection (e.g., empty lists, error dictionaries), which can prematurely terminate pagination and result in incomplete datasets.
- Re-fetching large datasets in subsequent steps or milestones when the necessary information has already been computed and can be passed as an intermediate result.
- Not collecting the results of the actions performed or the identifiers of affected items.
- Forgetting to extract necessary identifiers from prior steps, making subsequent filtering impossible.
- Hardcoding values that should be derived from task context (e.g., task_date) or prior variables.
- Not normalizing (e.g., lowercasing) string identifiers before comparison, leading to missed matches.
- Not handling missing or null fields gracefully (e.g., using `.get()` with default values, or explicit 'if not' checks).
- Failing to check all relevant participant roles (e.g., only checking sender, not receiver) when filtering by participants.
- Not parsing date strings into comparable date objects before comparison.