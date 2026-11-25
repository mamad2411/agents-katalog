---
name: enumerate-transform-delete-sequence
description: When a task requires enumerating a set of source entities, performing a non-destructive transformation on each, and then deleting the original source entities.
---
## Overview
This pattern addresses tasks involving a sequence of operations on a collection of items: first identifying them, then applying a transformation that often creates new artifacts, and finally cleaning up the original items. It emphasizes careful ordering to ensure data integrity and prevent premature deletion.
## When to Apply
- Instruction specifies processing 'each' item in a collection.
- Instruction specifies creating new artifacts based on existing items.
- Instruction specifies deleting the original items after processing.
- Instruction implies a dependency where the deletion must occur after the creation/transformation.
## Procedure
1. Identify and enumerate the source entities from the specified location, capturing any necessary identifiers or attributes from each.
2. Filter the enumerated list to exclude any entities that should not be processed or deleted (e.g., output directories, special files), ensuring this exclusion happens before any iterative processing.
3. For each entity in the filtered list, perform the specified non-destructive transformation, using the captured identifiers for naming or targeting new artifacts.
4. After all transformations are complete, for each entity in the *same filtered list*, perform the specified destructive action (e.g., deletion).
## Key Patterns
- **Read-then-Act Dependency:** All subsequent actions (transformation, deletion) depend on the initial enumeration of source entities, ensuring consistency and preventing re-enumeration.
- **Destructive Action Last:** Destructive operations are always placed after all non-destructive operations that rely on the original state of the entities.
- **Exclusion Pre-processing:** Any entities that should be excluded from processing or deletion are filtered out during the initial enumeration step, ensuring they are not included in subsequent iterative steps.
- **Identifier Preservation:** Key identifiers or attributes from the source entities are captured during enumeration and reused consistently across all subsequent steps (e.g., for naming output artifacts).
## Common Pitfalls
- Performing destructive actions before all necessary non-destructive operations are completed.
- Failing to enumerate the target entities once and reusing that list, leading to inconsistencies or re-enumeration.
- Not explicitly excluding output or protected entities from the initial enumeration or the final destructive step, particularly when output entities are co-located with source entities.
- Deleting the output directory or other unintended targets due to insufficient filtering or incorrect scope definition for the destructive action.
- Failing to capture and reuse the exact identifiers from the source entities for naming or targeting new artifacts, leading to incorrect associations.
