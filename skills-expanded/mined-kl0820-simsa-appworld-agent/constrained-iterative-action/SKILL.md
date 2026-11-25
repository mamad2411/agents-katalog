---
name: constrained-iterative-action
description: When a task requires performing an action on a subset of items, where the subset is defined by external constraints or relationships.
---
## Overview
This pattern addresses tasks where the target items for an action are not immediately obvious but depend on filtering against a pre-defined set of allowed entities. It involves first identifying the allowed entities from an external source, then using this information to filter the potential target items within the primary application, and finally iterating through the filtered items to perform the required action, potentially with conditional sub-actions.
## When to Apply
- Instruction specifies an action on items from specific groups or certain relationships.
- The identity of the specific groups or certain relationships needs to be resolved from an external source.
- The action needs to be performed on multiple items that match the criteria.
- The action might have conditional requirements (e.g., checking resource availability).
## Procedure
1. Identify and collect unique identifiers for entities belonging to specified constraint categories from an external identity source.
2. Retrieve all potential actionable items from the primary application.
3. Filter the retrieved actionable items, retaining only those associated with the unique identifiers collected in the first step.
4. Iterate through the filtered actionable items, performing the primary action on each.
5. During iteration, if a resource check is required, perform it and execute a conditional sub-action if the primary resource is insufficient.
## Key Patterns
- **Pre-computation of Whitelist/Blacklist:** Resolve the set of allowed or disallowed entities from an external source before querying the primary application, to use as a filter.
- **Filter-then-Act:** Separate the step of reading all potential items from the step of filtering them based on pre-computed constraints, and then from the step of acting on the filtered set.
- **Iterative Conditional Action:** When performing an action on multiple items, iterate through them, and for each item, check for necessary conditions (e.g., resource availability) and execute alternative steps if conditions are not met.
## Common Pitfalls
- Attempting to filter items without first resolving the identities of the constraining entities.
- Not handling cases where the primary resource for an action is insufficient, leading to partial task completion or errors.
- Performing actions on all items without applying the specified constraints, leading to unintended side effects.
- Failing to collect all necessary unique identifiers from the external source, resulting in an incomplete filter.
