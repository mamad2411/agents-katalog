---
name: conditional-destructive-action-by-absence
description: Applies a destructive action to a set of entities based on their absence from a reference set.
---
## Overview
Many tasks require modifying a collection of items by removing those that do not meet a specific positive criterion. This often involves identifying items that are present in one list but absent from another, which serves as a whitelist or positive condition. The strategy ensures that the destructive action is only applied to the truly unwanted items after a clear comparison.
## When to Apply
- Instruction implies removing items from a collection.
- The condition for removal is based on the absence of a relationship or property defined by another set of data.
- The task involves a destructive operation (e.g., delete, unfollow, revoke).
## Procedure
1. Read the full list of primary entities that are candidates for the destructive action.
2. Read the full list of related entities that define the positive condition or 'whitelist'.
3. Identify the subset of primary entities that are NOT present in, or do NOT satisfy the condition defined by, the related entities.
4. Perform the destructive action ONLY on the identified subset of primary entities.
## Key Patterns
- **Separate Read for Comparison:** Always read all necessary data for comparison into distinct sets or lists before attempting any filtering or action, especially when the comparison involves multiple data sources.
- **Negative Condition for Destructive Action:** When a destructive action is conditional, explicitly define the *negative* condition (what to remove) by identifying items *not* meeting a positive criterion, rather than trying to define what *to keep*.
- **Pre-computation of Target Set:** Before executing a destructive action, fully compute the exact set of items that will be affected. This ensures accuracy and prevents unintended modifications.
## Common Pitfalls
- Attempting to filter and act in a single step, leading to incomplete data for comparison.
- Incorrectly defining the comparison logic, e.g., acting on items that *are* present in the reference set instead of those that are *absent*.
- Performing the destructive action without first confirming the exact set of targets, risking unintended data loss.
- Not handling pagination or large datasets when reading the primary or reference entities, leading to incomplete lists for comparison.
