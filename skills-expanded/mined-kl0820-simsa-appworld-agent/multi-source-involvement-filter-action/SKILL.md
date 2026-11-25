---
name: multi-source-involvement-filter-action
description: Performs an action on entities identified through multi-source identity resolution and complex filtering based on entity involvement across roles, dynamic time windows, and exclusionary conditions, with action parameters derived from collected data.
---
## Overview
This pattern addresses tasks requiring an action on entities whose identity and eligibility are established through a multi-step process involving multiple data sources and diverse filtering criteria. It ensures that all necessary identifiers are available, and that the target entities are precisely identified and filtered based on relationships, time, and exclusionary conditions before the final action is performed.

## When to Apply
- Perform an action for some entities, but not others, based on complex criteria.
- Identify entities from one source, then check their status or involvement in another.
- Combine information from a primary contact list with details from secondary data sources.
- Exclude entities that have already completed a specific interaction or meet certain prior conditions.
- Filter a collection based on relationships to other entities, considering various roles.
- Process items within a specific time window.
- Filter a collection based on a combination of identity, time, and exclusionary criteria.

## Procedure
1.  **Resolve Foundational Identities:** Retrieve a foundational set of entities from a primary source, establishing common identifiers for each. This mapping is crucial for linking data across different systems.
2.  **Determine Time Window (if applicable):** Convert any relative time specifications (e.g., "yesterday", "last week") into concrete, absolute date/time ranges for precise filtering.
3.  **Read Target Collection:** Retrieve the target collection of items or entities from the relevant application or system that will be subject to the action.
4.  **Apply Multi-Criteria Filtering:** Sequentially or in combination, apply the following filtering criteria to narrow down the target collection:
    *   **Time-based Filtering:** Filter the collection by applying the determined absolute time window.
    *   **Entity Involvement Filtering:** Further filter the collection by checking for involvement of any of the resolved foundational entities, considering all possible participation roles (e.g., sender, receiver, participant).
    *   **Exclusionary Filtering:** Query relevant systems (e.g., transactional systems) to identify entities that have already met a specific condition or performed a particular action. Explicitly exclude these entities from the final set of targets.
5.  **Execute Action:** For each entity remaining in the filtered set, perform the required action. The specific parameters for the action should be derived from data gathered in earlier steps and linked via the established common identifiers.

## Key Patterns
-   **Foundational Identity Resolution:** Establish a robust mapping of identifiers from a primary source to serve as a common link across different systems for data integration and filtering.
-   **Multi-Criteria Filtering:** Apply all relevant filtering criteria (time, entity involvement, roles, exclusion status) to precisely narrow down the target collection.
-   **Exclusionary Filtering:** Explicitly identify and remove entities from the target set that have already fulfilled a condition or performed a prior action, preventing redundant or incorrect operations.
-   **Data-Dependent Iteration:** Perform the final action iteratively for each eligible entity, using parameters derived from data gathered in earlier steps.
-   **Relative Time to Absolute Time:** Convert relative time specifications into concrete, absolute date/time ranges for accurate filtering.
-   **Read-Then-Act:** Separate the step of reading and filtering a collection from the step of performing an action on the filtered items.

## Common Pitfalls
-   Failing to establish a robust, common identifier mapping across all relevant systems early in the process.
-   Not explicitly querying for exclusion criteria, leading to redundant or incorrect actions.
-   Attempting to perform actions before all necessary data, including exclusion status and filtering criteria, has been fully gathered and processed.
-   Incorrectly matching entities across systems due to inconsistent identifiers or incomplete foundational mappings.
-   Applying actions to the entire collection before proper filtering.
-   Missing edge cases for entity involvement (e.g., only checking one role like sender, but not receiver).
-   Incorrectly interpreting relative time windows.