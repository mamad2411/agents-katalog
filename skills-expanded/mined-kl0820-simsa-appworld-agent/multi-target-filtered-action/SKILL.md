---
name: multi-target-filtered-action
description: When an instruction requires performing a common action on multiple distinct item types, all constrained by the same filter.
---
## Overview
A single instruction can imply multiple distinct operations across different data categories, even if they share a common filtering condition. Decomposing these into separate milestones ensures each operation can be independently executed and verified, while maintaining the necessary filtering context.
## When to Apply
- The instruction specifies an action to be performed on multiple distinct types of entities or data.
- A common filtering or selection criterion applies uniformly across all specified entity types.
- The actions on each entity type are logically independent.
## Procedure
1. Identify all distinct entity types or data categories targeted by the instruction.
2. Identify the common filtering criterion that applies to all identified targets.
3. For each distinct target, create a separate milestone that specifies the action and explicitly includes the common filtering criterion.
## Key Patterns
- **Distinct Target Decomposition:** Decompose a single instruction into separate milestones when it targets multiple distinct types of entities for the same action.
- **Filter Criterion Propagation:** Ensure the common filtering criterion is explicitly included in each milestone derived from the decomposition.
- **Action Implies Selection:** An action like 'delete' or 'modify' implicitly requires a preceding 'find' or 'select' step, which must incorporate the filtering criterion.
## Common Pitfalls
- Attempting to perform a single, undifferentiated action across disparate entity types.
- Failing to explicitly carry over the filtering criterion to each decomposed milestone.
- Treating distinct entity types as a single homogenous set, leading to incorrect or incomplete operations.
