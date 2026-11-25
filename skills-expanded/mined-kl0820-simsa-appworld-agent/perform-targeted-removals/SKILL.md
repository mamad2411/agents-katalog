---
name: perform-targeted-removals
description: When a list of items to be removed from one or more collections has been identified in a prior step, this skill performs the actual removal operations.
---
## Overview
This skill addresses the challenge of executing multiple removal operations based on pre-computed lists of targets. It ensures that all specified items are systematically processed and removed from their respective containers or collections, and provides a record of the actions taken.
## When to Apply
- The task requires deleting multiple specific items.
- A prior step has already identified the exact items to be removed.
- The removal operation is a state-changing action.
## Procedure
1. Retrieve the pre-identified list(s) of items to be removed from prior steps.
2. Initialize a structure to record the results of the removal operations.
3. Iterate through each item (or nested structure of items) in the retrieved list(s).
4. For each item, extract the necessary identifiers for the removal API.
5. Call the appropriate removal API with the extracted identifiers.
6. Record the details of the successful removal.
7. Return the accumulated record of all removals performed.
## Key Patterns
- **Pre-identified Targets:** The items to be removed are fully determined by a preceding step, eliminating the need for re-evaluation or filtering within this procedure.
- **Batch Execution:** The procedure involves iterating over a collection of targets and applying a removal action to each, rather than a single, atomic removal.
- **Record Keeping:** A list of successfully removed items or their identifiers is maintained to provide an audit trail or confirmation of the operations.
- **Nested Iteration:** When items are nested within parent containers (e.g., sub-items within a main collection), the procedure involves an outer loop for containers and an inner loop for items within each container.
## Common Pitfalls
- Attempting to re-evaluate removal criteria instead of trusting the pre-identified list.
- Failing to handle cases where the pre-identified list is empty (leading to unnecessary API calls or errors).
- Not accumulating a record of removed items, making it difficult to confirm success or report back.
- Incorrectly extracting identifiers for the removal API.
