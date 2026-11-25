---
name: select-single-item-from-collection-then-act
description: Applies when an action needs to be performed on a single item selected from a collection based on a specific criterion, often comparative or superlative.
---
## Overview
This skill addresses tasks where a target item for an action is not directly provided but must be identified from a larger set of items. It involves first retrieving all relevant items, then applying a selection logic to pinpoint the single desired item, and finally executing the primary action on that identified item.

## When to Apply
- An action is requested on an item that is part of a collection.
- The specific item for the action is determined by a comparative or filtering criterion (e.g., 'least', 'most', 'highest', 'lowest', 'specific property').
- The item's identity is not directly provided but must be discovered by comparing a property across multiple candidates.
- The instruction implies iterating through a collection to find a specific member.

## Procedure
1. Retrieve the collection of items relevant to the task's scope.
2. For each item in the retrieved collection, read or extract the property required for the selection criterion.
3. Apply the selection criterion to identify the single target item from the collection. This often involves comparing property values across all items to find the one that meets the specified condition (e.g., superlative).
4. Perform the requested action on the identified target item.

## Key Patterns
- **Read-then-Filter/Computed Selection:** The target item is not directly named but is the result of an aggregation, comparison, or filtering operation performed on a property across a set of items.
- **Data Dependency Ordering:** The identification step must precede the action step, as the output of identification (the target item) is a direct input to the action.

## Common Pitfalls
- Attempting to perform the action without first identifying the specific target item.
- Failing to retrieve all items in the collection, leading to an incomplete or incorrect selection.
- Failing to read the necessary property for comparison on all relevant items.
- Incorrectly applying the selection or comparison logic (e.g., finding the 'least' instead of 'most', or using the wrong filter).
- Not preserving the exact identity of the selected item for the subsequent action.
- Not handling cases where multiple items might share the superlative property, if the task requires a unique selection.