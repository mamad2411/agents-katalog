---
name: create-and-populate-resource-from-filtered-data
description: Creates a new resource or entity and populates it with data filtered from one or more sources, involving chained API operations.
---
## Overview
This pattern addresses tasks that involve a multi-step process: first, gathering and filtering data from existing sources; second, creating a new container or resource/entity; and finally, populating or modifying that new resource/entity with the previously filtered data. It often requires chaining API calls and managing data flow between distinct operational phases.

## When to Apply
- When an instruction requires filtering or selecting items from a source and then performing an action with them.
- When an instruction implies combining information from multiple API calls to achieve a goal.
- When a task involves creating a new entity and then populating it with previously identified data.
- When data needed for filtering or an action is spread across multiple API endpoints.
- Create a new X and add Y to it.
- Populate a new resource with filtered items.
- Filter data from one source and use it to create and fill another resource.

## Procedure
1. Retrieve initial data from a source, potentially requiring pagination to gather all relevant items.
2. For each item in the initial data, retrieve additional or supplementary details if necessary to gather all required filtering criteria or extract necessary attributes.
3. Filter the collected and combined data based on specified conditions (e.g., attribute value, date range, string comparison), accumulating relevant identifiers and attributes into a structured list.
4. Create the target resource or entity using a dedicated API, providing necessary initial properties (e.g., title, privacy setting).
5. Extract the unique identifier of the newly created resource or entity from the API response.
6. Iterate through the previously filtered and extracted data.
7. For each data point or item, call an API to add it to or modify the newly created resource or entity, using its unique identifier and potentially item identifiers.

## Key Patterns
- **Pagination Loop / Iterative Data Retrieval:** Iteratively fetch data in chunks until an empty response or specific termination condition is met, accumulating all results into a single collection.
- **Data Enrichment via Secondary Calls / Cross-API Data Enrichment:** When initial API responses lack sufficient detail for filtering or processing, make subsequent API calls for each item (e.g., using an ID from the initial response) to retrieve comprehensive information.
- **Multi-criteria Filtering / Conditional Filtering and Accumulation:** Apply a combination of logical conditions (e.g., AND, OR) to filter data based on multiple attributes, potentially involving type conversion or parsing (e.g., date parsing, case-insensitive string comparison), accumulating only the items that satisfy all criteria into a structured list.
- **Resource/Entity ID Extraction:** After creating a new resource or entity, reliably extract its unique identifier from the API response for subsequent operations that require referencing that resource.
- **Inter-Milestone Variable Flow / Chained Data Flow:** Access and utilize outputs from previous milestones (e.g., filtered data, resource/entity IDs) as inputs for current operations, ensuring continuity and data dependency across the task.
- **Create-Then-Populate Workflow:** For tasks involving populating a new container, first create the container entity to obtain its unique identifier, then iterate through the items to be added, performing individual add operations using the container's ID.
- **Direct Action for Creation/Modification:** Perform state-changing API calls (e.g., create, add) directly as instructed, without pre-checking for existence or performing defensive checks, unless explicitly required by the task or API contract.

## Common Pitfalls
- Failing to implement pagination correctly, leading to incomplete data retrieval or infinite loops.
- Attempting to filter data using only the initial, incomplete API response without fetching necessary detailed information for each item.
- Incorrectly parsing or comparing data types (e.g., dates, case-sensitive strings) during the filtering process.
- Not capturing or correctly passing the identifier of a newly created resource or entity to subsequent steps that need to interact with it.
- Not correctly accessing or using variables passed from prior milestones, breaking the data flow between task steps.
- Adding unnecessary defensive checks (e.g., checking if a resource exists before creating it) when the instruction implies direct creation.
- Not iterating through all relevant items when performing bulk actions on a target entity, resulting in partial completion.