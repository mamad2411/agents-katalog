---
name: batch-action-on-list
description: Applies a single, state-changing action to each item in a previously identified list of entities.
---
## Overview
This skill addresses scenarios where a uniform action needs to be performed on multiple entities. It involves iterating through a collection of previously identified items, extracting a unique identifier for each, and then calling a specific API with that identifier and any required action parameters. The key is to ensure all items are processed and the action is applied directly without re-validation.
## When to Apply
- Perform an action on 'all' identified entities.
- Apply a specific operation to 'each' item in a collection.
- Iterate through a list to perform a uniform update or modification.
## Procedure
1. Retrieve the list of target entities from a prior milestone's output.
2. Extract the unique identifier for each entity from the list.
3. Define any static parameters required for the action (e.g., a specific message or status).
4. Iterate through the extracted identifiers.
5. For each identifier, call the relevant API to perform the action, passing the identifier and any static parameters.
6. Collect the identifiers of the entities on which the action was successfully performed.
## Key Patterns
- **Iterative API Call:** The core pattern involves looping through a collection of entities and making a separate API call for each entity to perform a uniform action.
- **Identifier Extraction:** Before calling the action API, extract the specific unique identifier (e.g., 'id', 'transaction_id') from each entity object in the input list.
- **Verbatim Parameter Usage:** If the action requires a specific string or value (e.g., a comment, a status), use it exactly as provided in the instruction, without modification or paraphrasing.
- **Direct Action Execution:** Once the target entities are identified and validated in a prior step, execute the state-changing API call directly for each, without adding further conditional checks for existence or validity.
## Common Pitfalls
- Failing to iterate through all items in the input list.
- Incorrectly extracting the unique identifier from each entity.
- Modifying or paraphrasing required verbatim parameters for the action.
- Adding redundant validation or existence checks before performing the action, slowing down execution or introducing unnecessary complexity.
- Not collecting the identifiers of the items that were successfully acted upon for downstream use or confirmation.
