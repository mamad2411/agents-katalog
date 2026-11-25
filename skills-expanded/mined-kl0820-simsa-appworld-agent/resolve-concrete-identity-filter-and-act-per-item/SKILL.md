---
name: resolve-concrete-identity-filter-and-act-per-item
description: Resolves specific concrete identifiers (e.g., email, user ID) from an external source to filter individual items in a target application, then performs a single action on each matching item.
---
## Overview
Many tasks require acting on entities related to an abstract identity or group (e.g., 'my family', 'team members') that are not directly available or identifiable in the target application. This pattern addresses tasks where these abstract relationships must first be translated into specific, actionable concrete identifiers from a separate data source. Subsequently, all potential target items are read from the primary application, filtered based on these resolved identifiers (and potentially other constraints), before the final action is performed on the matching subset.

## When to Apply
- The instruction refers to a group or relationship (e.g., 'my family', 'my colleagues', 'my contacts', 'team members').
- The action target requires specific contact information (e.g., email, phone number, user ID) for matching.
- The information needed to resolve the abstract identity or group membership is available in a separate, external data source.
- The task involves filtering items based on an identity that is not natively available in the primary application.
- The action is conditional on an attribute of the target item matching one of the resolved identifiers.

## Procedure
1.  Identify the abstract identity or group mentioned in the instruction that needs resolution.
2.  Determine the external data source capable of resolving this abstract identity into concrete identifiers.
3.  Resolve the abstract identity to a list of concrete identifiers (e.g., email addresses, phone numbers, user IDs) from the identified external source. Ensure all necessary types of identifiers for the target system are extracted and normalized for comparison.
4.  Read all relevant items from the target system, ensuring to capture the attributes needed for matching against the resolved identifiers.
5.  Filter the target items using the resolved concrete identifiers. This filtering may also include any other specified constraints (e.g., date, direction, source). If the target system's API does not support filtering by the resolved criteria, read all potentially relevant items and then perform the filtering locally.
6.  Perform the specified action on each filtered item.

## Key Patterns
-   **Identity Resolution Pre-computation:** Abstract identities (e.g., 'my siblings') must be resolved into concrete identifiers (e.g., email addresses, phone numbers) in a separate, preceding step before they can be used for filtering or matching in a target system.
-   **Data Dependency Ordering:** The milestone that resolves identifiers must always precede the milestone that uses those identifiers for filtering or action.
-   **Cross-App Data Flow/Dependency:** Information obtained from one application (e.g., contacts app) is passed as input to another application (e.g., social media app) to fulfill the task.
-   **Filter-then-Act:** All filtering and identification of target items are completed in preceding milestones before any actions are performed on them.
-   **Cross-System Identifier Normalization:** When filtering items from one system based on entities defined in another, ensure that the identifiers extracted from both systems are normalized or compatible for comparison (e.g., email addresses, phone numbers, unique IDs).
-   **Read All, Then Filter Locally:** If the target system's API does not support filtering by the resolved criteria, read all potentially relevant items and then perform the filtering locally based on the resolved identifiers.

## Common Pitfalls
-   Attempting to filter or act on an abstract identity directly in the target application without first resolving it to concrete identifiers.
-   Failing to identify or extract all possible types of identifiers required by the target system (e.g., only resolving phone numbers when emails are also needed).
-   Not considering alternative data sources for identity resolution if the primary one fails or is incomplete.
-   Performing actions before all filtering criteria, including identity resolution and other constraints, have been applied.
-   Ignoring other constraints (like date ranges, source, or direction) while focusing solely on identity matching.
-   Failing to extract the correct, comparable identifiers from the initial resolution step.
-   Not reading the necessary matching attribute from the target items.
-   Incorrectly matching identifiers across systems due to format differences or missing normalization.
-   Performing the action on items that do not match the resolved criteria.