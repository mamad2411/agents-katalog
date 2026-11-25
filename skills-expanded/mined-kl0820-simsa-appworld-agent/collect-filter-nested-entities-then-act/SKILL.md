---
name: collect-filter-nested-entities-then-act
description: Performs an action on a specific set of entities by traversing nested data structures, applying filters at multiple levels, and collecting unique targets before execution.
---
## Overview
This skill addresses tasks requiring an action on specific entities that are nested within hierarchical data structures. The process involves systematically traversing these structures, applying filtering conditions at appropriate levels, collecting all unique target entities, and then performing the desired action. This approach ensures that all conditions are met and targets are uniquely identified before any state-changing operations occur.

## When to Apply
- An action needs to be performed on a specific type of entity.
- The target entities are nested within other entities or associated with them.
- The entities are part of a broader collection or hierarchical data structure.
- Filtering conditions must be applied based on attributes of the target entities, their parent entities, or any other relevant associated entities.
- The action should be applied to all unique instances of the identified target entities.

## Procedure
1.  **Retrieve Top-Level Collection:** Read the initial collection of parent or top-level entities.
2.  **Traverse and Extract Nested Entities:** Iterate through the top-level entities. For each, retrieve its nested sub-entities, and potentially further nested entities or their attributes.
3.  **Apply Filtering Conditions:** Apply specified filtering criteria based on the attributes of the sub-entities, their parents, or any other relevant associated data. This step refines the dataset, progressively narrowing down to potential targets.
4.  **Collect Unique Target Entities:** From the filtered sub-entities, extract and collect all unique instances or identifiers of the ultimate target entities for the action. Ensure deduplication to prevent redundant operations.
5.  **Perform Action:** Execute the specified action on each of the collected unique target entities.

## Key Patterns
-   **Read-Then-Act Separation:** All data gathering, filtering, and collection operations are completed and verified before any modifying action is performed on the target entities. This ensures conditions are met and data is prepared.
-   **Hierarchical Data Traversal:** The process involves navigating through multiple levels of nested entities (e.g., collection -> item -> sub-item -> attribute) to reach the desired level for filtering or extraction.
-   **Sequential Data Refinement:** The task is broken down into a series of steps where each step refines the dataset produced by the previous step, progressively narrowing down to the final set of target entities.
-   **Filter-Extract-Deduplicate:** After traversing and filtering, specific identifiers needed for the final action are extracted and ensured to be unique, preparing for efficient batch operations.

## Common Pitfalls
-   **Premature Actions:** Performing actions immediately upon finding a matching sub-entity, without collecting all potential targets first. This can lead to incomplete or incorrect results.
-   **Lack of Deduplication:** Failing to deduplicate target entities before performing the final action, leading to redundant or inefficient operations.
-   **Incorrect Filter Level:** Applying filtering criteria at an incorrect level of nesting or after the relevant data has already been processed, resulting in an incorrect set of target entities.
-   **Incomplete Search:** Failing to exhaustively search all parent entities or handle all nested levels, leading to an incomplete set of target entities.
-   **Ignoring Pagination/Large Collections:** Not handling pagination or large collections when retrieving entities or sub-entities, which can lead to incomplete data processing or performance issues.