---
name: resolve-entity-then-process-data-and-act
description: Resolve an entity's identity, then retrieve and process relevant data based on specific criteria (from request or task) before performing a final action.
---
## Overview
This pattern addresses tasks where an action needs to be performed for a specific named entity or target, but its canonical identifier is not directly provided. The details of the action depend on specific data associated with that entity, which must be located, extracted, and potentially processed based on criteria from the entity's request or the task itself. It ensures all necessary identifiers and data points are resolved and retrieved before attempting the final action, preventing errors due to ambiguous targets or missing parameters.

## When to Apply
- An action is to be performed for a specific named entity or target.
- The instruction refers to an entity by a human-readable name, not a canonical identifier.
- The specifics of the action depend on a request or criteria provided by that entity, OR the task specifies conditions to identify a unique record (e.g., 'the last one', 'the approved one').
- The information needed to fulfill the request or perform the action must be sourced from internal records, a prior transaction, or an external system.
- The action requires a specific value (e.g., an amount, a date) or multiple parameters that are not explicitly given but are implied by context.

## Procedure
1. Identify and resolve the human-readable name of the target entity or recipient to its unique canonical identifier.
2. Determine the specific criteria or parameters required for data retrieval and processing. This could be derived from the entity's explicit request, communication, or from the task's explicit conditions (e.g., 'the last one', 'the approved one').
3. Retrieve relevant data or a collection of records associated with the identified entity. This data might come from internal systems, prior transactions, or external data sources.
4. Filter, select, and extract the necessary data points from the retrieved data based on the criteria identified in the previous step. This step transforms raw data into actionable information or specific parameters.
5. Perform the final action using the resolved entity identifier and the processed/extracted data points.

## Key Patterns
- **Identity Resolution First:** Always resolve a human-readable entity name to its canonical identifier (e.g., email, ID) as the first step, as this identifier will be a critical parameter for subsequent operations.
- **Criteria-Driven Data Processing:** The criteria for filtering, selecting, or transforming data are directly derived from either the entity's explicit request or the task's specific conditions, ensuring relevance and accuracy of the final output.
- **Specific Data Selection:** When a task refers to 'the last X' or 'X that meets condition Y', retrieve all relevant X, then apply filtering and sorting to precisely identify the single target record or specific data points.
- **Sequential Data Dependency:** The output of an earlier step (e.g., entity identifier, processing criteria) is a mandatory input for a subsequent step, establishing a clear execution order and preventing critical inputs from being omitted.

## Common Pitfalls
- Attempting to use a human-readable name directly or interact with an entity without first resolving its unique canonical identifier, leading to incorrect targeting or failure.
- Gathering or processing data without first fully understanding the specific request or criteria from the entity or the task, resulting in irrelevant or inaccurate outputs.
- Performing the final action before all necessary data has been retrieved, processed, and confirmed according to the criteria, leading to incomplete or incorrect task fulfillment.
- Failing to correctly filter or sort a collection of records to identify the *specific* one required by the task, leading to acting on the wrong data.
- Combining data retrieval and action steps into a single milestone when the retrieved data is a critical input for the action, obscuring dependencies.