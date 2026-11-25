---
name: conditional-resource-upsert
description: This skill applies when a task requires conditionally updating or creating a user-specific resource based on its current state and a target value.
---
## Overview
Many tasks involve modifying user-owned data. This pattern addresses scenarios where the modification is conditional: if the data already meets the target, no action is needed. Otherwise, the agent must first determine if an existing user-specific record can be updated or if a new one needs to be created, using distinct API calls for each case.
## When to Apply
- Instruction specifies a target state for a resource (e.g., 'set to X', 'increase to Y').
- Instruction implies checking the current state before acting (e.g., 'if already Z, leave unchanged').
- APIs include both 'create' and 'update' operations for the same resource type.
- The resource is user-specific, requiring identification of the current user's record.
## Procedure
1. Obtain the list of items to process, typically from a prior milestone.
2. For each item in the list:
3.   Read the item's current state relevant to the target condition.
4.   If the current state already satisfies the target condition, skip to the next item.
5.   If the current state does not satisfy the target condition:
6.     Identify the current user's identifier (e.g., email, ID).
7.     Query for existing user-specific resources related to the current item using the user's identifier.
8.     If an existing user-specific resource is found:
9.       Call the 'update' API for that resource, setting it to the target state.
10.     If no existing user-specific resource is found:
11.       Call the 'create' API for a new resource, setting it to the target state.
12. Accumulate identifiers of items that were modified for reporting purposes.
13. Output a null value, as the primary purpose of this milestone is state change.
## Key Patterns
- **Conditional Execution:** A crucial 'if' condition determines whether any action is needed, based on comparing the current state to the desired target state.
- **Read-Then-Decide:** The agent first reads the current state of the resource and then decides whether to update an existing one or create a new one, using different API calls for each.
- **User-Specific Resource Identification:** When dealing with user-generated or user-owned data, it's necessary to filter or query for resources specifically belonging to the current user before attempting to update or create.
- **Distinct Create/Update APIs:** Often, creating a new resource and updating an existing one are handled by separate API endpoints or methods, requiring a conditional branch.
## Common Pitfalls
- Failing to check the current state, leading to unnecessary updates or creations.
- Using the 'create' API when an 'update' is appropriate, or vice-versa, leading to duplicate or incorrect data.
- Not correctly identifying the current user's specific resource, potentially modifying another user's data or failing to find the correct resource to update.
- Assuming an update is always possible without first checking for the existence of the resource.
- Not handling the case where no existing resource is found and a new one needs to be created.
