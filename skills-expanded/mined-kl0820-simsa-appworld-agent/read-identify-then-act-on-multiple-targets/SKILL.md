---
name: read-identify-then-act-on-multiple-targets
description: Applies when a task requires performing an action on items across multiple distinct collections, based on a common filtering condition.
---
## Overview
This strategy addresses tasks where items need to be modified or removed from several different locations or collections. It prioritizes a preliminary read phase to gather all relevant items and apply the filtering condition, ensuring that the subsequent action phases operate on a consistent, pre-identified set of targets. This separation prevents redundant filtering and ensures all affected collections are processed.
## When to Apply
- The instruction specifies an action to be performed on items in multiple distinct collections.
- A filtering or selection condition must be applied to the items before the action.
- The action is destructive or modifies the state of the items.
## Procedure
1. For each distinct collection, read all items and apply the specified filtering condition to identify the subset of items that will be acted upon.
2. Consolidate the identified items from all collections into a single list or set of items to be acted upon.
3. For each distinct collection, perform the specified action on only those items that were identified in the initial read phase as belonging to that collection and meeting the condition.
## Key Patterns
- **Identify-then-Act:** All items subject to an action are first identified by reading their properties and applying a condition, before any modification actions are initiated.
- **Separate Target Processing:** When an action applies to items residing in multiple distinct collections, each collection is processed independently for the action phase, even if the identification phase was consolidated.
- **Condition Pre-evaluation:** The filtering condition is fully evaluated during the read/identification phase, and the results (the identified items) are passed to the action phase, rather than re-evaluating the condition during the action.
## Common Pitfalls
- Attempting to perform the action and evaluate the condition simultaneously for each item, leading to inefficient or inconsistent processing across multiple collections.
- Failing to read all necessary item properties before attempting to apply the filtering condition.
- Not handling each distinct target collection separately during the action phase, potentially leading to incomplete or incorrect updates.
- Re-evaluating the filtering condition for each item during the action phase, rather than using a pre-identified list.
