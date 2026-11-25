---
name: conditional-collection-pruning
description: Applies when a task requires conditionally modifying multiple distinct collections of items based on specific retention criteria.
---
## Overview
This pattern addresses tasks involving the selective removal of items from multiple distinct collections. It emphasizes processing each collection independently, first evaluating retention conditions for all items, then performing the removal. Complex conditions, including those requiring nested data evaluation, are resolved during the evaluation phase.
## When to Apply
- The task specifies multiple distinct collections or entity types to be processed.
- Each collection/entity type has its own set of conditions for retention or removal.
- The operation involves destructive modification (e.g., removal, deletion).
- Some conditions may require evaluating properties of constituent sub-items.
- Specific collections or entity types are explicitly excluded from modification.
## Procedure
1. Identify all distinct target collections or entity types that are subject to modification, and any explicitly excluded collections or entity types.
2. For each identified target collection/entity type:
3. Identify the specific retention conditions that apply to items within this collection, including any complex or nested conditions that require evaluating properties of sub-items.
4. Read all items from the current target collection.
5. For each item, evaluate its retention conditions, resolving any nested conditions by first evaluating the properties of its constituent sub-items.
6. Compile a list of items that do not meet the retention conditions.
7. Perform a bulk removal of the identified non-retained items from the target collection.
8. Verify that all explicitly excluded collections or entity types remain untouched.
## Key Patterns
- **Separate Collection Processing:** When multiple distinct collections or entity types are involved, process each independently with its own read and action phases, even if the overall goal (e.g., cleanup) is similar across them. This ensures type-specific rules and dependencies are handled correctly.
- **Read-Then-Act for Destructive Operations:** Before performing any destructive modification (e.g., removal), first read the entire state of the target collection and evaluate all conditions to determine the full set of items to be acted upon. This prevents partial state changes, allows for a single, informed action, and avoids issues with modifying a collection while iterating it.
- **Nested Condition Resolution:** If a retention condition for an item depends on the state or properties of its constituent sub-items, resolve the sub-item states first to accurately determine the parent item's overall status against the condition.
## Common Pitfalls
- Attempting to modify items while iterating through a collection, leading to unpredictable behavior or missed items.
- Applying a single set of retention rules across all collections, ignoring type-specific conditions or exclusions.
- Failing to resolve complex, nested conditions before making removal decisions, leading to incorrect item retention.
- Accidentally modifying collections explicitly marked for exclusion.
