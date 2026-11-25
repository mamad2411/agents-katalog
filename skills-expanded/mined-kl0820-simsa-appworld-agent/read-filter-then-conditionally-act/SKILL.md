---
name: read-filter-then-conditionally-act
description: Decomposes tasks requiring filtering a collection based on multiple criteria and then conditionally performing an action on each filtered item, potentially based on its current state.
---
## Overview
Many tasks involve identifying a specific subset of items from a larger collection by applying multiple filtering conditions. Once this target subset is identified, actions often need to be applied to each item, potentially with further conditions based on the item's current state. This pattern separates the complex data identification and retrieval from the subsequent iterative, conditional modification, ensuring the action is applied to the correct and complete set.

## When to Apply
- An action is requested on 'some' items from a collection, not 'all' items.
- The specific items to act upon are defined by a condition or state within the collection, or must be dynamically determined from a source.
- The instruction implies a need to first inspect the state of a system or collection before performing an action.
- The task involves a 'read then act' sequence for multiple entities.
- Identify items that meet multiple criteria.
- Perform an action on a subset of items.
- Update items based on their current state.
- Iterate over a filtered collection to apply changes.
- The action is a 'bulk' operation (applies to each item in a collection).

## Procedure
1. Retrieve the full collection of potential target items.
2. Apply the specified filtering criteria or conditions to identify the exact subset of items that meet the task's requirements. This may involve multiple sequential or combined criteria.
3. For each item in the identified subset, retrieve any additional attributes necessary for subsequent conditional actions.
4. Iterate over the identified subset.
5. For each item, perform the specified action, but only if it meets the defined conditional logic based on its retrieved attributes.

## Key Patterns
- **Read-Filter-Act Separation:** Clearly separate the identification and filtering of target entities from the action step. The action step must explicitly depend on and consume the output of the identification/filtering step, ensuring that only the correctly qualified items are processed.
- **Multi-criteria Filtering:** When an item must satisfy multiple independent conditions, combine these conditions to form the final target set before proceeding with actions. This can involve intersection or sequential filtering.
- **Conditional Action Execution:** When an action on an item depends on its current state or attributes, ensure these attributes are read before the action is attempted, and the action is only performed if the condition is met.
- **Condition Fidelity:** The filtering step must precisely implement all conditions specified in the instruction to select the target items.
- **Data Dependency:** The action milestone is entirely dependent on the output (identified entities) of the read/identification milestone.
- **Separation of Concerns:** Reading/identifying data is separated from writing/acting on data, even if both operations occur within the same application.

## Common Pitfalls
- Applying actions to items that do not meet all filtering criteria.
- Executing an action unconditionally when a condition based on the item's current state is required.
- Attempting to perform an action without first accurately identifying the target subset.
- Attempting to perform an action without first retrieving the necessary attributes for its conditional logic.
- Incorrectly applying or interpreting the filtering criteria, leading to actions on the wrong items or an incomplete set.
- Failing to pass the identified subset correctly from the identification step to the action step.
- Acting on the entire collection instead of the specified subset.
- Acting on items before their full identification or retrieval is complete.
- Mixing the identification and filtering of items with their modification, leading to inefficient or incorrect processing.
- Failing to explicitly document when a task's full condition cannot be met due to system limitations, leading to silent reinterpretation of intent.
- Failing to handle cases where no entities are identified for the action.