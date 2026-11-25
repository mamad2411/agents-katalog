---
name: multi-collection-recursive-cleanup
description: Cleans up items across multiple distinct collections by interpreting and applying complex, potentially recursive, entity-specific conditions for removal.
---
## Overview
This pattern addresses tasks that involve iterating through different types of collections, applying specific filtering logic to each, and then performing a cleanup action (like removal) on the items that do not meet the criteria. It emphasizes separating the identification of items from their modification and handling complex, nested conditions.
## When to Apply
- Filter items in multiple distinct collections.
- Remove items that do not meet specific criteria.
- Criteria involve multiple conditions (e.g., AND/OR).
- Some criteria are defined recursively or depend on sub-items.
- Certain collections are explicitly excluded from modification.
## Procedure
1. Identify all distinct collections or entity types mentioned in the instruction.
2. For each identified collection or entity type, determine if it is subject to modification or explicitly excluded.
3. For each collection or entity type subject to modification:
4. a. Explicitly enumerate all conditions that define which items should be kept, selected, or removed. Note how these conditions combine (e.g., AND/OR) and if they vary for different entities within the collection.
5. b. If any conditions are complex, recursive, or depend on sub-items (e.g., "all sub-items meet a condition"), define the precise logic for their evaluation.
6. c. Read the collection to identify all items that meet the enumerated criteria.
7. d. Perform the specified action (e.g., remove, update) on items that do not meet the criteria, based on the results of the previous identification step.
## Key Patterns
- **Read-then-Act Separation:** Always read and identify target items based on conditions before performing any destructive or modifying actions. This allows for verification and prevents premature modification.
- **Entity-Specific Condition Evaluation:** Conditions for filtering or selection can vary significantly between different entity types or collections; each must be evaluated independently and precisely.
- **Recursive Condition Definition:** When a condition for a parent entity depends on the state of all its child entities (e.g., "an album is downloaded if all its songs are downloaded"), ensure the definition is correctly interpreted and applied.
- **Exclusion by Instruction:** Explicitly identify and exclude collections or entities that the instruction states should remain untouched.
## Common Pitfalls
- Misapplying conditions across different entity types or collections.
- Failing to correctly interpret and apply complex or recursively defined conditions.
- Executing modifying actions before a complete and verified identification of all target items.
- Modifying entities or collections explicitly designated as out-of-scope.
- Overlooking implicit conditions or inter-entity dependencies.
