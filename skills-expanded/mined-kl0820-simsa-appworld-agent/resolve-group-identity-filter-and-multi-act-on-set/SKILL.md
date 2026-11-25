---
name: resolve-group-identity-filter-and-multi-act-on-set
description: Resolves group or abstract identities from an external source to filter a collection of items, then performs one or more distinct actions on the identified set.
---
## Overview
This pattern addresses tasks where an action needs to be performed on a specific set of items within a primary application. The crucial aspect is that the criteria for identifying these target items, particularly their associated identities or group memberships, are not directly available in the primary application. Instead, this essential information must first be resolved or retrieved from an external data source. Once these qualifying identities are established, they are used to filter a broader set of potential target items in the primary application, and then one or more actions are performed on the resulting filtered set.

## When to Apply
- An action is specified for items within a primary application.
- The items must belong to a specific group, relationship category, or be associated with a particular identity.
- The membership of this group, relationship, or the details of the identity are not directly available in the primary application but must be determined from an external source.

## Procedure
1.  Identify the external data source containing the information needed to resolve the qualifying identities or group memberships.
2.  Retrieve the identifying attributes (e.g., names, identifiers, contact details, group IDs) for all relevant entities belonging to the specified group, relationship, or target identity from the external data source.
3.  Identify the primary application and the type of items to be acted upon.
4.  Retrieve all potential target items from the primary application. Ensure that information linking these items to potential identities (e.g., requester, sender, associated group) is included.
5.  Compare the identifying attributes of the potential target items with the resolved qualifying identities to determine which items meet the criteria. This step effectively filters the potential targets based on the external identity information.
6.  Perform the specified action(s) only on the filtered set of items that match the qualifying identities. If multiple distinct actions are required on the same identified set, perform each action sequentially, ideally as separate milestones for clarity and verification.

## Key Patterns
-   **Identity Resolution Pre-computation:** Before acting on items in a target system, resolve the identities of qualifying entities from an external system. This creates a whitelist or blacklist of identifiers to be used for filtering.
-   **Cross-System Filtering:** Filtering criteria for items in one system (the target system) are derived from data in another system (the identity source system). This requires joining or comparing data across different API contexts.
-   **Read-Then-Filter-Then-Act:** The full set of potential target items must be read first, then filtered based on external identity criteria, before the action is applied to the subset. Direct filtering at the read stage might not be possible if the criteria are external.
-   **Separation of Identification and Action:** Distinctly separate the milestone for identifying the target set of items from the milestones that perform actions on those items. This allows for clear verification of the target set before modification.
-   **Multiple Actions on Same Set:** If multiple distinct actions are to be performed on the *same* identified set of items, consider creating a separate milestone for each action, all referencing the common identified set.

## Common Pitfalls
-   Attempting to filter items directly within the primary application without first resolving the external identities.
-   Failing to retrieve sufficient identifying information from either the external source or the primary application to enable accurate matching.
-   Not handling potential mismatches or ambiguities when comparing identities across different systems (e.g., different formats for names, phone numbers, or emails).
-   Performing the action on all items without applying the identity-based filter, leading to unintended consequences.
-   Attempting to use an unresolved or ambiguous identity directly in the target application.
-   Mixing the identity resolution step with the item identification or action steps, leading to less modular and verifiable plans.
-   Failing to account for cases where the identity might not be found in the external source.
-   Performing multiple distinct actions within a single milestone, making verification and error handling more complex.
