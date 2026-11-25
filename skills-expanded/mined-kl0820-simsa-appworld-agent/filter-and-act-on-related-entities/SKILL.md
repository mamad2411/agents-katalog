---
name: filter-and-act-on-related-entities
description: Applies when the task requires filtering a collection of entities based on their relationship to another set of entities and then performing an action on the filtered subset.
---
## Overview
This skill addresses tasks that involve identifying a target group of entities by cross-referencing information from multiple sources. It typically involves retrieving a primary set of related entities, then a secondary set of action-eligible entities, and finally performing a specific action only on those secondary entities that match the primary set.
## When to Apply
- Filter entities based on a relationship to other known entities.
- Perform an action only on a specific subset of items.
- Combine information from multiple data sources to identify target items.
## Procedure
1. Identify the API and parameters to retrieve the primary set of related entities.
2. Iteratively call the API, handling pagination, to collect all relevant primary entities, extracting all necessary identifiers and attributes.
3. Consolidate and deduplicate the collected primary entities.
4. Identify the API and parameters to retrieve the secondary set of action-eligible entities.
5. Iteratively call the API, handling pagination, to collect all relevant secondary entities, extracting all necessary identifiers and attributes, especially those needed for cross-referencing.
6. Load the collected primary and secondary entities from previous steps.
7. Prepare efficient lookup structures (e.g., sets of identifiers) from the primary entities for matching.
8. Iterate through each secondary entity.
9. For each secondary entity, extract its relevant identifier(s) for comparison.
10. Check if the secondary entity's identifier(s) match any in the lookup structure derived from primary entities.
11. If a match is found, call the designated action API with the secondary entity's unique identifier.
12. Accumulate the identifiers of all entities on which the action was successfully performed.
13. Report the outcome, including the count and identifiers of the acted-upon entities.
## Key Patterns
- **Pagination Loop:** When an API returns results in pages, implement a loop that continues calling the API with incrementing page indices until an empty or partial page is returned, indicating all data has been retrieved. Ensure all items from each page are accumulated.
- **Cross-referencing Identifiers:** To link entities from different sources, create efficient lookup structures (e.g., hash sets) from the identifiers of one set of entities. When processing the second set, check for membership in these lookup structures. Consider multiple potential matching fields (e.g., email, full name) and normalize them (e.g., lowercase, strip whitespace) for robust matching.
- **Comprehensive Data Extraction:** From each API response, extract not only the fields used for filtering or matching but also all unique identifiers and other attributes that might be required for subsequent steps or the final output. The deduction agent should inspect the API's response structure to determine these fields.
- **Conditional Action Execution:** Perform the final action API call only on those entities that satisfy the filtering or matching criteria established in prior steps. Do not act on entities that do not meet the conditions.
- **Accumulation of Action Results:** Maintain a list or other collection to store the identifiers or relevant details of each entity on which an action was successfully performed. This allows for a consolidated report of the operation's outcome.
## Common Pitfalls
- Failing to handle pagination, leading to incomplete data retrieval for either the primary or secondary entity sets.
- Not extracting all necessary fields (especially unique identifiers) from API responses required for subsequent matching or action steps.
- Using inefficient matching techniques (e.g., nested loops) instead of optimized lookup structures (e.g., hash sets) when cross-referencing entities.
- Overlooking alternative identifiers (e.g., both email and name) for cross-referencing, leading to missed matches.
- Re-fetching data that has already been retrieved and stored in a prior milestone's variable.
- Not accumulating the results of the final action, making it difficult to report what was done.
