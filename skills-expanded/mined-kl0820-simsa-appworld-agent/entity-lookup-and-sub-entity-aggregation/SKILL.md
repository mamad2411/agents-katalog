---
name: entity-lookup-and-sub-entity-aggregation
description: When the task requires finding a primary entity by a descriptive attribute, then retrieving all its associated sub-entities, and finally aggregating information from those sub-entities.
---
## Overview
This pattern addresses tasks that involve a multi-step data retrieval process. It starts by searching for a primary entity, often requiring pagination and exact matching. Once the primary entity's identifier is secured, it proceeds to retrieve all related secondary entities, again employing pagination to ensure completeness. Finally, it processes the collected secondary entities to extract or aggregate specific information.
## When to Apply
- Find X by Y and then Z about X
- What is the [metric] of the [sub-entity] associated with [primary entity]?
- Retrieve all items related to a specific identified item.
- Identify the extreme value (max/min) of a property across a collection of items.
## Procedure
1. Search for the primary entity using a descriptive query.
2. Iterate through search results, potentially across multiple pages, to find an exact match for the primary entity's name.
3. Extract the unique identifier of the matched primary entity.
4. If the primary entity is found, use its identifier to retrieve all associated secondary entities.
5. Paginate through the secondary entity results, accumulating all items into a single collection.
6. Process the collected secondary entities to find the one that meets a specific criterion (e.g., maximum/minimum value of a field).
7. Extract the required information from the identified secondary entity.
8. Handle cases where no entities or sub-entities are found.
## Key Patterns
- **Paginated Search for Exact Match:** Iteratively call a search API, checking each page for an exact match on a specific field, and stopping early if the target entity is found. Ensure case-insensitivity if appropriate.
- **Full Paginated Collection:** Iteratively call an API to retrieve all related items, accumulating them into a single list until no more pages are available (e.g., a page returns fewer items than the page limit or an empty list).
- **Max/Min Aggregation:** Use a built-in function (like `max()` or `min()`) with a `key` argument (often a lambda function) to identify an item within a collection based on the extreme value of one of its properties.
- **Chained API Calls:** The output (e.g., an ID) from one API call is used as a crucial input parameter for a subsequent API call to retrieve related data.
## Common Pitfalls
- Forgetting to paginate for *all* results when a complete collection of secondary entities is needed.
- Not handling the case where the primary entity is not found by the initial search.
- Not handling the case where the primary entity is found but has no associated secondary entities.
- Incorrectly handling case sensitivity or partial matches when an exact match for the primary entity is required.
- Failing to correctly break pagination loops, leading to infinite loops or incomplete data retrieval.
