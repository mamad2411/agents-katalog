---
name: filtered-action-with-identity-resolution
description: When a primary action needs to be performed on a subset of entities, requiring identity resolution and filtering based on external state.
---
## Overview
This pattern addresses tasks where a core action must be executed for specific entities, but only after their identifiers are resolved and they are filtered against a set of already-completed or excluded items. It ensures all necessary auxiliary data is gathered and processed before the final action.
## When to Apply
- Perform an action for a specific group of individuals.
- The target individuals are identified by names or partial information, requiring lookup for full contact details.
- The action should only apply to individuals who meet certain criteria or have not already completed a related step.
- The action involves a fixed descriptive parameter.
## Procedure
1. Identify the primary set of entities for which the action might be performed, along with their initial identifying information (e.g., names) and any associated data (e.g., amounts).
2. Retrieve auxiliary contact information (e.g., email addresses, phone numbers) for these entities from a separate source, resolving any ambiguities or partial matches to obtain system-usable identifiers.
3. Identify and retrieve a set of entities that should be excluded from the action, based on a specific condition or prior completion of a related step, ensuring their identifiers are also resolved for comparison.
4. Filter the primary set of entities, using the resolved contact information, to exclude those identified in the previous step.
5. For each remaining, filtered entity, perform the specified action using their resolved contact information and any associated data, applying any fixed parameters.
## Key Patterns
- **Identity Resolution:** Mapping a human-readable identifier (e.g., a name) from a primary data source to a system-usable identifier (e.g., an email address or unique ID) by consulting an auxiliary data source (e.g., a contact list) before any action is taken.
- **Exclusionary Filtering:** Creating a distinct set of items or entities that must be explicitly *removed* from a primary list of potential targets, based on external state or conditions, before the main action is executed.
- **Pre-computation of Constraints:** All filtering, identity resolution, and data aggregation steps are completed entirely before the iterative action begins, ensuring the action loop operates on a fully prepared and validated dataset.
## Common Pitfalls
- Attempting to perform identity resolution or filtering dynamically within the action loop, leading to inefficiency or errors due to repeated lookups.
- Failing to account for multiple potential identifiers for the same entity (e.g., different names for the same person) during resolution.
- Not handling cases where an entity from the primary list cannot be resolved in the auxiliary contact source, leading to skipped actions or errors.
- Incorrectly matching exclusion criteria, leading to over-filtering (excluding valid targets) or under-filtering (including invalid targets).
- Not retrieving all necessary intermediate data points or auxiliary data sources required for identity mapping or transformation, even if not explicitly mentioned in the primary instruction.
