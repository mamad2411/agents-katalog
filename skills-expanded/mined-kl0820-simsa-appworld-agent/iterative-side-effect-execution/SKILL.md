---
name: iterative-side-effect-execution
description: Executes a state-changing API call iteratively on a collection of entities obtained from a prior step, collecting an audit trail of the outcomes.
---
## Overview
This skill addresses scenarios where a list of target entities from a prior step needs to be processed by calling a side-effecting API for each target. It focuses on iterating through the collection, correctly mapping parameters, and collecting an audit trail of the actions performed.
## When to Apply
- Perform an action on a collection of items.
- Modify external state for multiple entities.
- Utilize a list of identifiers from a previous step as input for an action API.
## Procedure
1. Retrieve the collection of target entities from the prior step's output.
2. Initialize an empty list to store the results of each action.
3. Iterate through each target entity in the collection.
4. Extract the necessary identifier(s) from the current target entity.
5. Call the appropriate side-effecting API, mapping the extracted identifier(s) to its parameters.
6. Record the outcome of the API call (e.g., success message, status) along with the target's identifier(s) into the results list.
7. Construct the final output as the collected list of action outcomes.
## Key Patterns
- **Iterative Action:** Perform the same API call for each item in a collection, rather than attempting a bulk operation if not explicitly supported.
- **Parameter Mapping from Prior Data:** Directly use identifiers or attributes from a previous step's output as input parameters for the current API call, ensuring data continuity.
- **Audit Trail for Side Effects:** For state-changing operations, the primary 'output' is often a record confirming the action for each item, rather than new data. This audit trail is crucial for verification and debugging.
## Common Pitfalls
- Not iterating through all items in the input collection, leading to incomplete processing.
- Incorrectly mapping parameters from the prior data to the API call, resulting in API errors or incorrect actions.
- Failing to collect an audit trail for side-effecting operations, making it hard to verify success or debug failures.
- Choosing a 'search' or 'read' API when a 'write' or 'action' API is required for the milestone's intent.
