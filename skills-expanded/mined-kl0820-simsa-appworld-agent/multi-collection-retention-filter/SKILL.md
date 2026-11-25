---
name: multi-collection-retention-filter
description: Filters and removes items from multiple distinct collections based on retention criteria, processing each collection independently with a read-then-act approach.
---
## Overview
This skill addresses tasks that involve selectively retaining items within various collections while discarding others. It emphasizes a safe, two-phase approach: first, evaluating retention criteria for each item, and then performing the removal actions. Different item types or collections are processed independently to manage complexity and ensure correct application of potentially distinct filtering logic.
## When to Apply
- Cleanup or prune operations on collections.
- Instructions to keep only X or remove everything except Y.
- Multiple distinct categories of items or collections need processing.
- Filtering conditions vary by item category or involve nested checks.
- Explicit exclusions for certain collections.
## Procedure
1. Identify all distinct categories of items or collections that require filtering and modification.
2. For each identified category:
3. Read the current state of the items in that category and evaluate their retention criteria.
4. Based on the evaluation, perform the necessary removal actions for items that do not meet the criteria.
5. Ensure any explicitly excluded categories are not processed.
## Key Patterns
- **Read-then-Act:** Destructive actions (removals) are always preceded by a distinct read step to gather all necessary information and evaluate conditions, ensuring no partial state changes or race conditions.
- **Independent Category Processing:** When multiple distinct types of items or collections need processing, each type is handled in its own read-then-act sequence, allowing for type-specific logic and preventing interdependencies unless explicitly required.
- **Complex Condition Evaluation:** If a retention condition for an item depends on properties of its constituent sub-items, the evaluation of this complex condition is explicitly part of the read step for the parent item.
## Common Pitfalls
- Performing removals without a complete prior evaluation of all items, leading to incorrect deletions.
- Mixing read and write operations within a single milestone for a given category, risking inconsistent state.
- Applying a single, generic filtering logic across all item categories when distinct logic is required.
- Forgetting to explicitly exclude collections marked as do not touch.
