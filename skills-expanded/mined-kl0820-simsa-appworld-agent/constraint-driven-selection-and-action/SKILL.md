---
name: constraint-driven-selection-and-action
description: Applies when an action needs to be performed on an item selected from a collection, where the selection criterion is derived from an external information source.
---
## Overview
This pattern addresses tasks requiring an action on a specific item from a set, where the item's suitability is determined by a constraint value obtained from a separate, distinct information source. It involves a multi-step process of identifying the constraint, gathering potential targets, evaluating them against the constraint, and finally executing the action.
## When to Apply
- An action needs to be performed on an item from a collection.
- The selection of the item depends on a specific value or condition.
- This specific value or condition is not immediately available and must be retrieved from a separate information source.
- The action requires a target that meets a minimum or maximum threshold derived from the external source.
## Procedure
1. Identify and locate the external information source containing the constraint.
2. Extract the specific constraint value from the identified source, potentially requiring context-dependent processing.
3. Retrieve a collection of potential target items from the action-performing application.
4. For each potential target item, compute or derive the property relevant to the constraint.
5. Select the first target item from the collection that satisfies the extracted constraint, and perform the specified action on it.
## Key Patterns
- **Cross-Application Data Dependency:** A critical value (the constraint) for an operation in one application is sourced entirely from another, distinct application.
- **Constraint Pre-computation:** The constraint value is fully resolved and available before any iteration or selection process begins on the target collection.
- **Derived Property for Selection:** The selection criterion for target items is not a direct property but one that must be computed or aggregated from sub-elements of each item.
- **First-Match Action:** The action is performed on the first item encountered that satisfies the selection criteria, implying an ordered or prioritized search.
## Common Pitfalls
- Attempting to perform the action before fully resolving the constraint value.
- Failing to account for context-dependent extraction of the constraint (e.g., current day, user preferences).
- Not computing the necessary derived properties for target items before attempting selection.
- Ignoring the 'first-match' or specific ordering requirement for selection, leading to suboptimal or incorrect choices.
- Not handling cases where no target item satisfies the constraint.
