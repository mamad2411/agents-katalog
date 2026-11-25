---
name: conditional-resource-mutation
description: When the task requires identifying and modifying specific resources based on detailed attributes, often involving nested data structures and pagination.
---
## Overview
This skill addresses tasks where a collection of primary resources needs to be iterated, their detailed attributes fetched (potentially from a secondary API), filtered by a condition, and then a state-changing action performed on the qualifying resources. It often involves handling paginated lists and nested resource structures.
## When to Apply
- Iterate through a collection of items.
- Filter items based on a condition.
- Perform an action on filtered items.
- The initial listing API does not provide all necessary details for filtering.
- Resources are organized in a nested structure (e.g., items within containers).
- The primary list of resources is paginated.
## Procedure
1. Repeatedly call the primary listing API with pagination parameters until all primary resources are collected.
2. For each primary resource:
3. If the primary resource itself contains sub-resources, iterate through them.
4. For the current resource (either primary or sub-resource):
5. If necessary, call a detail API using an identifier from the current resource to fetch its full attributes.
6. Extract the relevant attribute(s) from the detailed resource.
7. Apply the task's filtering condition to the extracted attribute(s).
8. If the condition is met, perform the specified state-changing action using the resource's identifier(s).
9. Record the identifiers of the resources on which the action was performed.
10. Aggregate and return the recorded identifiers.
## Key Patterns
- **Pagination Loop:** Repeatedly call a listing API, incrementing an offset or page number, until an empty result indicates the end of the collection, ensuring all items are retrieved.
- **Summary-to-Detail Fetch:** An initial API provides a list of resource identifiers or summary data, requiring subsequent calls to a detail API for each resource to obtain full attributes needed for processing or filtering.
- **Nested Resource Traversal:** Iterating through a collection of primary resources, and for each primary resource, iterating through its own collection of sub-resources to access all relevant items.
- **Conditional Action Execution:** Applying a specific condition to resource attributes and only executing a state-changing API call if the condition evaluates to true, preventing unnecessary or incorrect modifications.
## Common Pitfalls
- Forgetting to handle pagination, leading to incomplete data processing.
- Not realizing that a separate detail API call is needed for filtering attributes, resulting in missing data for conditions.
- Incorrectly parsing or extracting attributes from API responses, leading to faulty filtering or actions.
- Failing to handle nested data structures correctly, causing some resources to be overlooked.
- Assuming all necessary data is available in the initial listing, when a detail fetch is required.
- Not collecting identifiers of modified resources for the final output or subsequent steps.
