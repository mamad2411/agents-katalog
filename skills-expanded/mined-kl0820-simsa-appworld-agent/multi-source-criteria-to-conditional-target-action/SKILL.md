---
name: multi-source-criteria-to-conditional-target-action
description: Aggregates data from multiple sources to derive criteria, then uses these criteria to conditionally perform actions on items within a separate, distinct target dataset.
---
## Overview
This skill addresses tasks that require gathering comprehensive information from various API endpoints, often involving iterative calls to handle pagination or different categories. The collected data is then processed and cross-referenced with another dataset to identify specific items that meet defined criteria, leading to targeted, conditional API calls.
## When to Apply
- Collect all X from Y and Z.
- Find items in A that are related to items in B.
- Perform an action on a subset of items based on external criteria.
- Aggregate data from multiple paginated endpoints.
## Procedure
1. Initialize an empty collection to store aggregated data from the first set of sources.
2. For each distinct category or source required for the first dataset:
3. Implement a pagination loop: repeatedly call the relevant API, incrementing page parameters until no more results are returned or an error is encountered.
4. Accumulate and, if necessary, de-duplicate the items retrieved from each page into the main collection.
5. Extract and standardize key identifiers from these items for later comparison.
6. Initialize an empty collection for the second dataset, which will be acted upon.
7. Implement a pagination loop for the API providing the second dataset, similar to step 2a.
8. Accumulate all items from the second dataset into its dedicated collection.
9. Transform the key identifiers from the first aggregated dataset into an efficient lookup structure (e.g., a set).
10. Iterate through each item in the second dataset.
11. For each item, check if its relevant identifier exists in the lookup structure created in step 6.
12. If a match is found, perform the specified action API call using the item's unique identifier.
13. Record the identifiers of all items on which the action was successfully performed.
14. Return the list of recorded identifiers.
## Key Patterns
- **Pagination Loop with Termination Conditions:** A 'while True' loop makes repeated API calls, breaking when the response is empty, contains an error message, or returns fewer items than the requested page limit, indicating the end of available data.
- **Multi-Category Data Aggregation and De-duplication:** Collect data from different categories (e.g., 'friend', 'roommate') into a single structure (e.g., a dictionary keyed by a unique ID) to automatically handle de-duplication and consolidate information.
- **Cross-Dataset Lookup Optimization:** Convert a list of identifiers from one dataset into a 'set' (after normalization like '.strip().lower()') to enable highly efficient O(1) average-case membership checks when iterating through another dataset.
- **Conditional API Execution:** Use an 'if' statement to gate state-changing API calls, ensuring they are only made when specific matching criteria between datasets are met.
## Common Pitfalls
- Incomplete Data Retrieval: Failing to implement or correctly terminate pagination loops, leading to only partial data being collected.
- Inefficient Data Comparison: Performing linear searches or nested loops for matching items between large datasets instead of using optimized lookup structures like sets or hash maps.
- Data Normalization Issues: Not standardizing comparison fields (e.g., case, whitespace) before attempting to match identifiers across different sources, leading to missed matches.
- Ignoring API Error Responses: Not checking for and handling error messages or unexpected response formats during data retrieval, which can cause the agent to crash or proceed with invalid data.
- Missing Action Accumulation: Forgetting to collect and return the identifiers of items on which an action was performed, making it difficult to summarize the task's outcome.
