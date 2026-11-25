---
name: filter-list-by-derived-reference-then-act
description: Retrieves a list, identifies a reference item or value within it, filters the list based on this derived reference, and then performs an iterative action on each item in the filtered subset, optionally passing identifiers across milestones.
---
## Overview
This skill addresses multi-step tasks where an initial data collection needs to be retrieved, a specific subset of items identified through conditional logic, reference point determination, or extreme value identification, and then an action performed on each item in that subset. It covers scenarios where the identification of target items is not a simple direct filter but involves deriving a reference point or applying sequential conditions based on a specific item's property. Once identified, a uniform action is applied to each selected entity, and the outcomes are collected.

## When to Apply
- Find X from a list and then do Y to each X.
- Filter a list of entities based on a property of a specific entity within that list.
- Process items in a collection based on their status, position, or a derived reference.
- Identify specific records and apply an update or action to them.
- Process items in a sequence up to a certain point.
- Identify all items that precede or include a specific reference item based on an ordering property.
- Perform an action on a group of entities whose selection is contingent on a relative condition to another entity.
- Process a sequence of historical records up to and including a current record.

## Procedure
1.  **Retrieve the initial data collection:** Call an API that returns a list of items.
2.  **Identify a "reference item" or "reference point":** Iterate through the retrieved collection to identify a specific item based on a distinguishing property (e.g., 'is_current', 'is_active', specific flags), by finding an extreme value (maximum/minimum) of a specific attribute, or using a primary boolean indicator with a fallback to a secondary boolean indicator if the primary is not found.
3.  **Extract a "reference value" or "reference property":** From the identified reference item, extract a property (e.g., 'position', 'timestamp', 'status', a numerical ordering property) that will be used as the criterion for filtering the rest of the list.
4.  **Filter the original list to create a "target subset":** Apply conditional logic to the original list, using the extracted reference value to determine which items belong to the target subset (e.g., 'item_position <= reference_value', items with a status relative to the reference item's status, or entities whose numerical ordering property is less than or equal to the reference entity's property).
5.  **(Optional) Sort the target subset:** If the order of processing is important, sort the filtered subset based on a relevant sequential property.
6.  **Extract key identifiers:** From each item in the target subset, extract the unique identifier (e.g., 'item_id') needed for the subsequent action API calls.
7.  **Pass identifiers to subsequent milestone (or prepare for current milestone action):** Store the list of key identifiers, typically in a prior milestone variable, to be used as input for the action phase.
8.  **Perform actions on the target subset:** Retrieve the list of identifiers (if applicable, from prior milestone variables). Iterate through this list and for each identifier, call the appropriate action API, passing the identifier as a parameter.
9.  **Collect and report results / Construct the final output:** Format the output according to the task's requirements, including a summary of actions performed, the collected identifiers/responses, or the results of each individual action, including the entity's identifier and the API response.

## Key Patterns
-   **Reference Item Identification:** A 'current' or 'reference' item needs to be identified within a list, often involving checking multiple flags, finding an extreme value (maximum/minimum) of a specific attribute, using a distinguishing property, or locating a specific entity in a list using a primary boolean flag, and if not found, attempting to locate it using a secondary boolean flag.
-   **Reference-Based Filtering:** A specific item in a list is used to establish a filtering criterion (e.g., a position, a status, a timestamp, a numerical ordering property) for other items in the same list.
-   **Positional/Relative/Sequential Filtering:** Items are filtered based on their order, relative position, or a numerical/sequential attribute compared to a reference item's attribute, rather than absolute values, including creating a subset of a list by comparing a numerical ordering property of each entity against a threshold derived from a "reference" entity's corresponding property.
-   **Iterative Action Execution:** Performing the same action on multiple items by iterating through a list of their identifiers, typically obtained from a prior data processing step.
-   **Batch Action Execution with Result Collection:** Iterating through a list of identified entities, performing a uniform API call for each, and accumulating the individual outcomes.
-   **Cross-Milestone Data Flow:** Data (specifically a list of identifiers) generated and stored in one milestone is explicitly retrieved and used as input for a subsequent milestone, ensuring continuity in multi-step tasks.
-   **Identifier Extraction for Action:** Retrieving a specific identifier from each entity in a filtered list to serve as a parameter for an action API.

## Common Pitfalls
-   Not handling empty initial data collections or scenarios where no 'current' or 'reference' item can be found gracefully.
-   Incorrectly identifying the 'current' or 'reference' item, leading to an incorrect target subset for subsequent actions.
-   Failing to extract the specific identifier (e.g., 'item_id') needed for the action API from the filtered items.
-   Incorrectly defining the filtering condition relative to the reference value, including incorrectly applying the comparative relationship (e.g., using strict inequality when inclusive is required).
-   Neglecting to sort the filtered subset when the order of processing is important.
-   Not considering the correct order of operations when identifying the target subset (e.g., finding the reference point before applying filters based on it).
-   Incorrectly accessing or misinterpreting prior milestone variables, leading to errors in subsequent steps.
-   Assuming idempotency of the action API without verification, which can lead to unintended side effects if actions are retried.
-   Not accumulating or reporting the results of individual batch actions, making it difficult to verify success or debug failures.