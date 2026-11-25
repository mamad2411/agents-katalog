---
name: differentiated-entity-actions
description: Applies when a task requires different actions on a specific entity versus other entities of the same type.
---
## Overview
This pattern addresses tasks where a collection of similar entities exists, but the instruction specifies a unique action for one or a subset of these entities, and a different action for the rest. It ensures that all entities are first understood, then categorized, and finally acted upon distinctly.
## When to Apply
- Instructions specify an action for 'the X' and a different action for 'the rest'.
- A collection of similar items needs to be processed with varying operations based on their properties or identity.
- A task involves identifying a specific item within a list and then treating other items differently.
## Procedure
1. Retrieve all relevant entities and their current states or properties.
2. Identify the specific target entity or subset of entities based on the task's criteria.
3. Perform the first specified action on the identified target entity or subset.
4. Perform the second specified action on all other entities that were not part of the target subset.
## Key Patterns
- **Read-then-Act Separation:** Always read the current state of all relevant entities before attempting any modifications, especially when modifications depend on current values or classifications.
- **Differentiated Entity Processing:** When a task requires distinct actions for different subsets of entities, first classify all entities, then apply the specific actions to their respective groups.
- **Derived Value Computation:** If an action requires a value that is a modification of an existing property (e.g., 'X minutes earlier'), compute this new value based on the read property before applying the action.
## Common Pitfalls
- Attempting to modify an entity without first reading its current state or properties.
- Applying a single action uniformly to all entities when the instruction implies differentiated treatment.
- Failing to correctly identify the specific target entity, leading to incorrect actions.
- Not accounting for all entities in the collection, leaving some unprocessed.
