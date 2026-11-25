---
name: cross-app-identity-filter-multi-action
description: When a task requires acting on items filtered by an identity resolved from a different application, and involves multiple distinct actions.
---
## Overview
This pattern addresses tasks where a target set of items needs to be identified based on criteria that include an identity or relationship defined in a separate system. After identifying the target items, multiple distinct operations must be performed on each.
## When to Apply
- Instruction specifies filtering items based on a relationship or identity from a different application.
- Instruction requires performing more than one distinct action on the same set of filtered items.
- The filtering criteria include a dynamic list of external identifiers.
## Procedure
1. Resolve the external identities or relationships from the source application.
2. Retrieve the target items from the primary application, applying all filtering criteria, including the resolved identities.
3. For each distinct action required, create a separate milestone to perform that action on the filtered target items.
## Key Patterns
- **Cross-Application Identity Resolution:** An identity or relationship needed for filtering in one application is first explicitly retrieved from another.
- **Filter by Resolved Identity:** The retrieved identities are used as a dynamic filter for the main data retrieval.
- **Separate Actions on Same Target:** If multiple distinct actions are required on the same set of target items, each action is performed in its own milestone.
## Common Pitfalls
- Attempting to resolve identities and filter items within a single, complex step.
- Failing to explicitly retrieve the external identities before attempting to use them as filters.
- Combining multiple distinct actions into a single milestone, leading to unclear success conditions or retry logic.
- Not ensuring all filtering criteria are applied during the data retrieval step.
