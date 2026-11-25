---
name: multi-source-intersection-enrich-and-mutate
description: Identifies common items across multiple paginated sources, enriches them with additional details, then conditionally creates or updates these items based on specific criteria derived from their enriched attributes.
---
## Overview
This pattern addresses tasks that involve a multi-step process: first, identifying a specific subset of entities by combining information from different data sources and enriching them with additional details; second, iterating through this enriched subset and performing conditional update or creation operations based on the retrieved details. It often involves pagination for initial data retrieval and careful selection of API calls for mutation.
## When to Apply
- Filter X from Y based on Z
- Update/Set/Change A for all B that satisfy C
- For each item in a filtered list, perform an action based on its current state
- Combine data from multiple sources to identify target items
## Procedure
1. Retrieve and aggregate identifiers from a primary paginated source.
2. Retrieve and aggregate identifiers from a secondary paginated source.
3. Identify target items by computing the intersection of aggregated identifiers.
4. For each target item, retrieve additional, specific details via an API call.
5. Structure the collected and enriched data for subsequent processing.
6. Load the structured data from the previous step.
7. Iterate through each item in the loaded data.
8. Apply conditional logic based on the item's enriched details:
9. If a condition for skipping is met, record the item as skipped.
10. If a condition for creating a new record is met, call the appropriate API.
11. If a condition for updating an existing record is met:
12. If necessary, retrieve the specific identifier for the record to be updated.
13. Call the appropriate API to update the record.
14. Summarize the outcome of the operations.
## Key Patterns
- **Paginated Data Aggregation:** Iteratively call an API with pagination parameters (e.g., page_index, page_limit), collecting all results into a single aggregated structure until an empty page is returned.
- **Set-Based Filtering:** Use set operations (e.g., intersection, union, difference) to efficiently identify common or unique elements across multiple collections of identifiers.
- **Conditional API Dispatch:** Select and call different APIs (e.g., create, update, delete) based on the current state or specific attributes of an item being processed.
- **Dependent Identifier Retrieval:** When an update or modification API requires a specific identifier (e.g., a record ID) that is not directly available from prior steps, perform an additional API call to fetch that identifier before proceeding with the modification.
- **Inter-Milestone Variable Passing:** Explicitly load and utilize structured data (e.g., a list of dictionaries) that was generated and passed as a variable from a preceding milestone.
## Common Pitfalls
- Not handling pagination correctly, leading to incomplete data retrieval.
- Incorrectly computing the intersection or other filtering criteria, resulting in an incorrect target set.
- Using a 'create' API when an 'update' API is required, or vice-versa, leading to errors or duplicate records.
- Failing to retrieve necessary identifiers (e.g., a specific record ID) before attempting an update operation.
- Not handling the 'no data' or 'empty list' case gracefully at any stage of the process.
- Confusing aggregate data (e.g., average ratings) with user-specific data when enriching items.
