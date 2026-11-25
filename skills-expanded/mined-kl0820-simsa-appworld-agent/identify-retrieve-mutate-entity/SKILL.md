---
name: identify-retrieve-mutate-entity
description: Describes the process of identifying a target entity, retrieving related information, and then performing a mutation based on that information.
---
## Overview
This pattern addresses tasks requiring a multi-step interaction with APIs: first, identifying a primary entity; second, retrieving specific related information using identifiers from the primary entity; and finally, performing a state-changing action (mutation) informed by the retrieved data. It's common when a task involves correcting or reversing a previous action, or acting upon a specific, context-dependent record.
## When to Apply
- When the task requires finding a specific entity and then acting upon a related record.
- When an action needs to be performed based on the details of a previously created or identified item.
- When the instruction implies correcting or undoing a prior transaction or state.
- When a target record needs to be identified by its temporal order (e.g., 'last', 'most recent').
## Procedure
1. Identify the primary target entity using a search query.
2. Filter the search results to precisely match the target entity based on specific criteria (e.g., name, ID).
3. Extract key identifiers and relevant attributes from the matched primary entity.
4. Use these extracted identifiers to retrieve a list of related secondary records.
5. Implement pagination to ensure all relevant secondary records are collected.
6. Filter and sort the secondary records to pinpoint the specific record of interest (e.g., most recent, specific status).
7. Extract the necessary data points from the identified secondary record that are required for a subsequent action.
8. Construct and execute a mutation API call using the extracted data points and primary entity identifiers.
9. Confirm the mutation's success, noting that the primary outcome is the side effect rather than a returned value.
## Key Patterns
- **Chained Entity Resolution:** Information obtained from an initial entity search (e.g., a unique identifier or email) is used as a precise filter or parameter for subsequent API calls to retrieve related data or perform actions, ensuring accuracy and specificity.
- **Comprehensive Retrieval via Pagination:** When searching for a specific item within a potentially large dataset, iterate through all available pages of results to ensure the target item is not missed due to page limits, accumulating all records before filtering.
- **Temporal Selection:** Identifying a specific record based on its temporal order (e.g., 'last', 'most recent') requires sorting all relevant records by a timestamp field and then selecting the appropriate extreme value (maximum or minimum).
- **Mutation as Side Effect:** For API calls that modify state or perform an action, the primary outcome is the successful execution of the operation itself, rather than a returned data structure. The result for the agent is often null or a simple confirmation.
## Common Pitfalls
- Failing to handle pagination, leading to incomplete data retrieval and potentially missing the target record if it's not on the first page.
- Not using precise identifiers (e.g., email, unique ID) from prior steps, instead relying on ambiguous fields like names for filtering, which can lead to incorrect matches.
- Incorrectly identifying the specific record of interest (e.g., 'last' or 'most recent') by neglecting to sort by relevant timestamps or by not considering all available records.
- Attempting a mutation without first confirming the existence and necessary details of the target entity and related records, leading to potential errors or unintended actions.
- Assuming a single API call will always return all necessary data, overlooking the need for iterative searches, filtering, or combining data from multiple sources.
