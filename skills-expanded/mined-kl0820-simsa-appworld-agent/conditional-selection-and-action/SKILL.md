---
name: conditional-selection-and-action
description: This skill applies when an agent needs to select a single item from a collection based on criteria derived from another source, and then perform an final action on the selected item.
---
## Overview
The core problem involves a multi-stage process: first, identifying a reference point or threshold from one data source; second, processing a list of potential target items, often requiring further API calls for each item to compute relevant properties; and finally, using the reference/threshold to filter and select a single target item on which to perform a final action.
## When to Apply
- Find an item in a list that meets a condition.
- Select the first item from a collection that satisfies a calculated criterion.
- Perform an action on a specific item after filtering a larger set.
- Use information from one API response to filter results from another API.
## Procedure
1. Retrieve a primary reference entity or value, potentially involving search, pagination, and filtering.
2. Extract a key criterion or threshold from the primary reference entity, possibly using contextual information.
3. Retrieve a collection of secondary entities, potentially involving pagination.
4. For each secondary entity in the collection, compute a derived property, which may require additional API calls for its sub-components.
5. Filter the collection of secondary entities based on the extracted criterion/threshold and their computed derived properties.
6. Select the first entity from the filtered collection that meets all conditions.
7. Perform a final action using the identifier of the selected entity.
## Key Patterns
- **Pagination Loop:** Iteratively call an API with an incrementing page index until no more results are returned, accumulating all items into a single list.
- **Nested Data Retrieval and Aggregation:** For each item in a primary list, make further API calls to retrieve details of its sub-components, then aggregate these details to compute a property for the primary item.
- **Contextual Data Extraction:** Parse structured text content from a retrieved entity to extract specific values based on current contextual information (e.g., current weekday).
- **First Match Selection:** Iterate through a list of candidates and select the very first one that satisfies the specified conditions, then stop processing the rest of the list.
- **Cross-Milestone Variable Flow:** Store and retrieve intermediate results (e.g., IDs, calculated values, processed lists) from prior milestones to inform subsequent steps.
## Common Pitfalls
- Failing to implement complete pagination, leading to incomplete data sets.
- Not robustly parsing structured text, especially when dependent on dynamic context.
- Inefficiently making redundant API calls or failing to aggregate data correctly from nested calls.
- Not handling the edge case where no item in the collection meets the selection criteria.
- Incorrectly applying the 'first match' rule, potentially selecting a suboptimal item or continuing to process after a match is found.
- Forgetting to pass necessary data from one milestone's output to another's input.
