---
name: read-filter-then-act-on-collection
description: Applies when a task requires reading a collection, filtering its entities based on specific criteria or properties, and then performing an action exclusively on the resulting filtered subset.
---
## Overview
This strategy addresses tasks where an action needs to be performed on a specific subset of entities from a larger collection. It ensures that all necessary data is gathered, filtering criteria are fully met, and the target entities are precisely identified before any modifications or actions are executed, preventing unintended operations on non-qualifying entities. This explicit separation of data acquisition, selection, and action allows for independent verification of the selection process and ensures that the action is only applied to the correct, pre-qualified targets.

## When to Apply
- Instructions specify an action to be performed on entities that meet certain criteria within a collection.
- The criteria involve reading one or more attributes or properties of each entity and applying a condition.
- The action is a mutation, write operation, or potentially destructive/irreversible.
- The action is conditional on a property value.
- The source data is a collection of items or entities.
- The task involves collecting items, filtering them, and then performing an operation on the filtered set.

## Procedure
1.  **Read/Collect Collection:** Obtain all items or entities from the initial collection to ensure all relevant source data is available.
2.  **Filter Entities:** Based on the specified criteria and properties, filter the collected items, retaining only those that satisfy the condition(s) and extracting them as the target entities for the action.
3.  **Perform Action:** Iterate through the filtered target entities and perform the designated action on each.

## Key Patterns
-   **Read-Filter-Act Separation:** Explicitly separate the initial data retrieval/collection from the filtering/selection logic, and both from the final action. This is crucial, especially when the action is a mutation, to ensure data dependencies are respected and to prevent premature or incorrect actions. This separation also allows for independent validation of the filtered set.
-   **Data Dependency Ordering:** Always retrieve all necessary data for filtering and action before attempting to apply filters or perform actions. This ensures the filter is comprehensive and accurate, and that the action has all required context.
-   **Filter-then-Act:** Explicitly separate the identification of target entities from the action performed on them. This guarantees the action is only applied to the correct subset.
-   **Conditional Action Pre-computation:** All conditions for performing the final action are evaluated and applied during the data collection and filtering phase, ensuring that the subsequent action only receives pre-qualified targets.

## Common Pitfalls
-   **Premature Actions:** Performing actions on entities before fully evaluating all filtering conditions or before all relevant source data has been collected.
-   **Incomplete Data Retrieval:** Not retrieving all necessary attributes or properties for filtering in the initial read step, leading to inaccurate filtering.
-   **Mixing Logic:** Mixing read/collect, filter, and action logic within the same step, which can make error recovery difficult, lead to race conditions, or result in incomplete data processing.
-   **Incorrect Scope:** Applying the action to the entire collection instead of strictly to the filtered subset.
-   **Inefficient API Calls:** Attempting to perform the action and filter simultaneously, leading to complex or inefficient API calls.
-   **Failing to Pass Filtered List:** Not explicitly passing the filtered list of entities from the filtering step to the action step, leading to incorrect or incomplete operations.
-   **Applying Filter After Action:** Applying the filter *after* performing the action on all entities, leading to unnecessary operations or errors.