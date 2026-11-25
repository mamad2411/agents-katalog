---
name: identify-and-act-on-target-and-complement
description: Apply one action to a specific identified item(s) within a collection, and a different action to all other items in that same collection.
---
## Overview
This pattern addresses tasks where a collection of similar entities needs to be processed, but with one or more specific entities singled out for a particular action, and all other entities receiving a different, often complementary, action. It emphasizes the importance of reading the full state first to enable accurate identification of both the target(s) and the complementary set, and then applying distinct modifications.

## When to Apply
- A task requires modifying a specific item(s) and applying a different action to all other items in the same collection.
- An action needs to be applied to a target entity, and a distinct action to 'the rest' or 'all others except X'.
- A target entity needs a relative update (e.g., '20 minutes later' or 'increase by 1 unit').

## Procedure
1.  **Read All Entities:** Retrieve the full state of all relevant entities in the collection. This ensures you have current data for identification and subsequent modifications.
2.  **Identify Target(s) and Complement:** Based on the given criteria, identify the specific target entity(s) within the collection. Simultaneously, identify the complementary set of all other entities by excluding the target(s) from the original collection. Extract any necessary attributes from the target(s) (e.g., current values for relative updates).
3.  **Act on Target(s):** Perform the specific action or modification on the identified target entity(s). If the modification is relative, calculate new properties based on the attributes extracted in the previous step.
4.  **Act on Complement:** Perform the distinct action or modification on the complementary set of entities (all items except the target(s)).

## Key Patterns
-   **Read-Before-Act:** Always retrieve the full state of a collection and identify targets before attempting any modifications. This prevents errors from stale data or incorrect identification.
-   **Target vs. Complementary Set:** Explicitly define both the target entity(s) and the complementary set of entities in an initial read step.
-   **Differential/Distinct Actions:** Separate actions that apply to the specific target entity(s) from actions that apply to the remaining entities, even if they are part of the same overall task.
-   **Relative Property Calculation:** If a new property value is defined relative to an existing one (e.g., '20 minutes later', 'increase by 10%'), the existing value(s) must be read first to calculate the new value(s) before the update.

## Common Pitfalls
-   Attempting to modify entities without first reading their current state or confirming their identity.
-   Applying a bulk action to all entities without correctly excluding the specific target entity(s).
-   Failing to correctly identify the target entity(s) or its complement set.
-   Mixing the two distinct modification steps into a single, complex action, leading to errors.
-   Not extracting necessary attributes (e.g., current value) before attempting a relative modification, resulting in incorrect updates.