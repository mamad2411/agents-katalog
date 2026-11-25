---
name: perform-final-irreversible-action
description: Performs a critical, often irreversible, action after a prerequisite milestone has been successfully completed.
---
## Overview
This pattern applies when the final step of a task involves executing a significant, state-changing operation. The execution is contingent on the successful completion of a prior, dependent milestone, which is confirmed by the system's milestone status. No further validation is performed before executing the action.
## When to Apply
- The task instruction specifies a final, critical, or irreversible action.
- The action is explicitly conditional on the successful completion of a previous step or milestone.
- The available API directly performs the required action without complex parameters.
## Procedure
1. Confirm the successful completion of the prerequisite milestone using the system's milestone status.
2. Call the API that performs the critical action, passing any necessary parameters.
3. Handle the API response, typically by acknowledging the action's completion.
4. Produce a null or empty result as the output, as the action itself is the primary outcome.
## Key Patterns
- **Prerequisite Confirmation:** The success of a prior milestone is confirmed by the system's `milestone_status` variable, eliminating the need for explicit re-validation before proceeding with the critical action.
- **Direct API Execution:** The critical action is performed via a direct call to a single, specific API, often with minimal or no parameters.
- **Side-Effect Output:** The primary outcome is the state change caused by the action, not a data payload; therefore, the output value is typically null or an empty placeholder.
## Common Pitfalls
- Attempting to re-validate the prerequisite milestone instead of trusting the `milestone_status`.
- Expecting a data payload as output when the action's side effect is the intended result.
- Failing to acknowledge the irreversible nature of the action in the summary or description.
