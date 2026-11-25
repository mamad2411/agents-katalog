---
name: resolve-group-filter-and-iterate
description: This skill applies when a task requires performing an action on multiple items within a collection, where the items must satisfy multiple filtering conditions, including involvement with a pre-resolved group of entities.
---
## Overview
Many tasks require acting on a subset of items from a larger collection. This pattern addresses scenarios where the subset is defined by multiple criteria, one of which involves a group of related entities that must first be identified or resolved from a separate source. The strategy involves resolving the target group, then reading the primary collection, applying all necessary filters, and finally iterating to perform the specified action on each matching item.
## When to Apply
- Instructions that specify an action on 'all X from Y involving any of my Z'.
- Tasks requiring an action on a collection of items that are filtered by both a temporal constraint and a relationship to a dynamic group.
- When a group of related entities needs to be identified before being used as a filter for another operation.
## Procedure
1. Identify and resolve the target group of entities from its source.
2. Read the primary collection of items from the relevant system.
3. Filter the collection of items based on all specified criteria, including the resolved group of entities and any temporal constraints.
4. For each item remaining in the filtered collection, perform the specified action.
## Key Patterns
- **Pre-computation of Target Group:** Before acting on items related to a specific group, that group must first be explicitly identified and resolved from its authoritative source. This resolved set then serves as a parameter for subsequent filtering.
- **Multi-criteria Filtering:** When multiple conditions (e.g., temporal, relational) define the target items, all conditions must be applied sequentially or in combination to narrow down the collection before any action is taken. The resolved target group is one such critical filter.
- **Iterative Action on Filtered Results:** If the instruction implies an action on 'all' or 'each' matching item, the action must be performed iteratively over every item that satisfies all filtering criteria, rather than a single, bulk operation or an action on only one item.
- **Data Dependency:** The output of the entity resolution step (the identified group) is a direct input dependency for the filtering step of the primary collection. This ensures that the action is performed only on items relevant to the specified group.
## Common Pitfalls
- Attempting to filter by an unresolved or ambiguous group identifier.
- Performing the action on the entire collection without applying all necessary filters.
- Applying filters incorrectly or in the wrong order, leading to an incorrect set of target items.
- Executing a single action instead of iterating over all matching items when the instruction implies multiple actions.
- Ignoring temporal constraints specified in the instruction.
