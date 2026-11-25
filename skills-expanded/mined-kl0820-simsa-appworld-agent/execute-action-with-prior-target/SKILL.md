---
name: execute-action-with-prior-target
description: Executes a specific action API using an identifier obtained from a previous step's output.
---
## Overview
This skill addresses scenarios where a preceding step has identified a specific entity or data point, and the current milestone requires performing an action directly on that identified target. It focuses on retrieving the necessary identifier from prior results and invoking the appropriate action API.
## When to Apply
- The milestone requires performing an action (e.g., play, delete, update, send).
- The target of the action (e.g., an ID, a name) is expected to be available from a previous milestone's output.
- The available APIs include a direct action API that accepts the target identifier.
## Procedure
1. Retrieve the output from the preceding milestone, which contains the target identifier.
2. Extract the specific identifier required by the action API from the retrieved prior output.
3. Call the designated action API, passing the extracted identifier as a parameter.
4. Capture the response from the action API.
5. Construct a result object that summarizes the action performed, including the target identifier and relevant information from the API response.
6. Output the constructed result.
## Key Patterns
- **Prior Data Dependency:** The current step's execution is contingent on and directly uses data (specifically, an identifier) produced by a previous, successfully completed milestone.
- **Direct Action Invocation:** Once the target identifier is available, the action is performed by a single, direct call to a dedicated action API, without further search or validation steps.
- **Side Effect Reporting:** For actions that primarily cause a side effect, the output should confirm the action's execution and provide any relevant status or metadata from the API response, rather than returning new data.
## Common Pitfalls
- Failing to correctly parse or extract the identifier from the prior milestone's output, leading to incorrect API calls.
- Attempting to re-validate the existence of the target entity when its presence was already confirmed by the prior milestone.
- Not handling potential errors or non-success responses from the action API gracefully.
- Returning the raw API response directly instead of a structured summary of the action's outcome.
