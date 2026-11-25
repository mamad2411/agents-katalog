---
name: cross-source-match-and-act
description: Applies when entities from one source need to be filtered or acted upon based on matching identifiers found in another source.
---
## Overview
This skill addresses tasks requiring the identification of a target set of entities from one system, and then filtering or performing an action on a second set of entities from another system, where the condition for action depends on a match between the two sets. It involves careful extraction of identifiers from both sources and a robust matching strategy.
## When to Apply
- Filter or act on items from system A based on criteria from system B.
- Identify a group of entities from one source.
- Identify a group of entities from another source.
- Perform a conditional action on entities from one source, where the condition involves entities from another source.
- Matching entities across different data sources.
## Procedure
1. Retrieve the initial set of entities from the first source, handling pagination and accumulating all results.
2. Extract relevant identifiers and other necessary data fields from each entity in the first set. De-duplicate entities based on a stable unique identifier if they might appear multiple times.
3. Retrieve the target set of entities from the second source, handling pagination and accumulating all results.
4. Extract relevant identifiers and action-specific IDs from each entity in the second set.
5. Prepare the identifiers from the first set for efficient lookup (e.g., by creating a set of normalized identifiers).
6. Iterate through each entity in the target set from the second source.
7. For each target entity, check if its identifier matches any identifier in the lookup structure created from the first set, ensuring identifiers are normalized before comparison.
8. If a match is found, perform the specified action using the target entity's action-specific ID.
9. Collect the action-specific IDs of all entities on which the action was performed.
10. Output the collected action-specific IDs as the final result.
## Key Patterns
- **Pagination Loop:** When an API returns paginated results, repeatedly call the API with incrementing page indices until an empty or partial page indicates the end of the dataset, accumulating all results.
- **Cross-Source Identifier Matching:** To match entities across different data sources, extract a common, reliable identifier (e.g., email, unique ID) from both sources. Convert one set of identifiers into an efficient lookup structure (e.g., a set) for quick membership testing against the other set.
- **Data Accumulation and De-duplication:** When collecting data from multiple API calls or sources, accumulate all results into a single list. If entities might appear multiple times (e.g., due to overlapping categories), de-duplicate them based on a stable unique identifier, retaining all necessary fields from one instance.
- **Conditional Action Execution:** After identifying target entities based on a matching condition, iterate through the target entities and execute a specific API action only for those that satisfy the condition, using their unique action identifier.
- **Identifier Normalization:** Before matching identifiers (especially strings like emails or names), normalize them (e.g., convert to lowercase, strip whitespace) to ensure consistent comparison and prevent mismatches due to case or formatting differences.
## Common Pitfalls
- Failing to handle pagination, leading to incomplete data retrieval.
- Using unreliable or non-unique identifiers for cross-source matching, resulting in incorrect matches.
- Not normalizing identifiers (e.g., case, whitespace) before comparison, leading to missed matches.
- Failing to de-duplicate entities when they can appear in multiple categories or API responses, leading to redundant processing.
- Not gracefully handling empty results from API calls, assuming data will always be present.
- Incorrectly identifying the unique ID required for the action API, leading to failed calls.
- Over-matching or under-matching due to imprecise or overly strict matching logic.
