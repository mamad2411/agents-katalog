---
name: conditional-property-update
description: Applies a conditional update to a property of multiple entities based on their current state.
---
## Overview
This skill addresses tasks requiring modifications to a collection of entities where the modification itself depends on the current value of a specific property of each entity. It separates the identification and state-reading phase from the conditional update phase to ensure accurate application of rules.
## When to Apply
- Instructions to modify a collection of items.
- The modification condition depends on an existing property value of each item.
- Instructions to apply a specific value only if the current value meets certain criteria (e.g., 'if lower, increase').
## Procedure
1. Identify the initial collection of entities to be considered.
2. Apply initial filtering criteria to narrow down the target entities.
3. For each filtered entity, read the specific property whose value will determine the update condition.
4. Iterate through the identified entities and their read property values.
5. For each entity, conditionally apply the specified update to a target property based on the previously read property's value.
## Key Patterns
- **Read-Before-Write Conditional Logic:** To perform a conditional update, the current state of the relevant property must be explicitly read *before* attempting the write operation. This prevents overwriting desired states or applying updates incorrectly.
- **Separation of Identification/State-Reading and Action:** The process of identifying the target entities and retrieving their current state should be a distinct step from the actual conditional modification. This ensures all necessary data is gathered before any changes are made.
## Common Pitfalls
- Attempting to update without first reading the current state, leading to incorrect conditional logic application.
- Failing to correctly filter the initial collection, resulting in unintended modifications to entities outside the target scope.
- Applying a blanket update instead of a conditional one, ignoring the 'if lower' or similar constraints.
- Not handling edge cases for the conditional check (e.g., 'unrated' vs. 'rated lower').
