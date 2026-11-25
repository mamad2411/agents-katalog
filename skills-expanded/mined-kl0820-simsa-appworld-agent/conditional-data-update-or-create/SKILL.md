---
name: conditional-data-update-or-create
description: Describes the process of conditionally updating an existing record or creating a new one based on a specific condition and the presence of an existing record.
---
## Overview
This pattern addresses scenarios where an agent needs to modify data, but the modification depends on whether a relevant record already exists and meets certain criteria. It involves checking for an existing record, evaluating its state, and then choosing between an update operation or a creation operation to achieve the desired outcome.
## When to Apply
- Update an existing record if a condition is met, otherwise create a new one.
- Modify a record only if its current state is below a certain threshold.
- Ensure a record has a specific value, creating it if it doesn't exist or updating it if it's different.
- Handle both creation and modification of user-specific data.
## Procedure
1. Retrieve the target items that require potential modification or creation from a prior step or direct API call.
2. Identify any specific identifier or credential needed for user-specific operations (e.g., user email).
3. Iterate through each target item.
4. For each item, evaluate the primary condition to determine if any action is needed at all (e.g., if the item already meets the desired state, skip).
5. If action is needed, attempt to retrieve an existing record associated with the current item and the specific identifier.
6. Check if an existing record was found and if it belongs to the correct entity (e.g., matching user email).
7. If an existing record is found, perform an update operation on that record with the desired new value.
8. If no existing record is found, perform a creation operation to establish a new record with the desired value.
9. Accumulate identifiers of items that were acted upon for reporting or subsequent steps.
## Key Patterns
- **Conditional Action Gate:** Before performing any data retrieval or modification, always check if the primary condition for action is met. This prevents unnecessary operations and ensures adherence to 'no-op' instructions. The data for this condition often comes from a prior step or the initial item being processed.
- **Retrieve-Then-Filter for Specific Records:** When an API returns a collection of records that might belong to various entities, and the task requires action on a *specific* entity's record, retrieve the collection first and then filter it in-memory using the specific entity's identifier (e.g., user ID, email) to locate the correct record.
- **Update-or-Create Logic:** When a task requires ensuring a specific state for an item, and this state might involve either modifying an existing record or creating a new one, implement a clear conditional branch: first attempt to find an existing record; if found, update it; otherwise, create a new one.
- **Prior Milestone Data as Input:** Data generated and stored in `prior_variable_values` from a previous milestone is the primary input for subsequent steps. Always retrieve and utilize this structured data as the starting point for processing.
## Common Pitfalls
- Failing to check the primary condition before attempting any action, leading to unnecessary API calls or incorrect modifications.
- Not correctly identifying the specific user's record when an API returns a list of records from multiple users, leading to updating/creating for the wrong entity.
- Confusing the update and create operations, or attempting to update a non-existent record, or creating a duplicate when an update was intended.
- Ignoring the instruction to leave certain items unchanged if they already meet the desired state.
- Not handling cases where the API for retrieving existing records returns an empty list or an unexpected format.
