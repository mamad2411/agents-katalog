---
name: resolve-identity-then-categorize-actions
description: When an action needs to be performed on multiple distinct categories of items, all associated with a single, initially un-resolved identifier.
---
## Overview
Many systems require canonical identifiers for operations. When an instruction specifies an action on multiple distinct categories of items, all linked to a single, non-canonical identifier, the identifier must first be resolved. Subsequently, actions are performed separately for each item category, using the resolved identifier as a filter.
## When to Apply
- Instruction specifies an action on items associated with an external identifier (e.g., phone number, email, username).
- Instruction specifies an action on multiple distinct types or categories of items.
- The external identifier needs to be mapped to an internal system ID.
## Procedure
1. Resolve the external identifier to its canonical system identifier.
2. For each distinct category of items specified in the instruction, perform the specified action on items of that category, filtering by the resolved system identifier.
## Key Patterns
- **Identity Resolution:** An external, human-readable identifier must be converted into a system's canonical internal ID before it can be used for filtering or operations.
- **Categorical Action Split:** When an instruction implies actions on multiple distinct types or categories of entities, each category should be handled in a separate, independent action step. This allows for granular control and verification.
- **Resolved ID as Filter:** The canonical ID obtained from the resolution step is passed downstream and used as the primary filter for all subsequent actions.
## Common Pitfalls
- Attempting to act directly on the external identifier without resolving it first.
- Combining actions on different categories of items into a single milestone, leading to ambiguity or inability to verify partial success.
- Failing to pass the resolved identifier to subsequent steps, leading to incorrect filtering or actions.
