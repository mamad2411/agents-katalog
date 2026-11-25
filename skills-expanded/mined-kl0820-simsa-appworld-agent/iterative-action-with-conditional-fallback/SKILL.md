---
name: iterative-action-with-conditional-fallback
description: When a collection of items requires an action, and a specific failure condition for that action necessitates a predefined fallback strategy.
---
## Overview
This pattern addresses scenarios where a primary API call might fail under specific, anticipated circumstances, requiring an alternative approach. It involves iterating through a set of targets, attempting a default action, and then, based on the API response, executing a fallback action if a particular error state is detected. This ensures robust processing of all items in the collection by handling expected failure modes gracefully.
## When to Apply
- An instruction requires performing an action on multiple entities.
- The primary API call for the action has known, specific failure modes.
- A secondary API call or alternative strategy exists to handle these specific failure modes.
- The task requires ensuring all items in a collection are processed, even if some require a fallback.
## Procedure
1. Read the collection of target items from a prior step or API call.
2. Identify and acquire any necessary resources or parameters for the fallback action once before iterating.
3. Iterate through each item in the collection.
4. For the current item, attempt the primary API action.
5. Inspect the response from the primary API action for specific indicators of a known, recoverable failure condition (e.g., specific error messages, status codes, or field values).
6. If the specific failure condition is detected, attempt the fallback API action using the pre-acquired resources.
7. If the primary action succeeded or the fallback action was attempted, proceed to the next item in the collection.
## Key Patterns
- **Specific Error Detection:** The decision to trigger a fallback is based on parsing the API response for precise error messages, codes, or structural elements that indicate a recoverable failure, rather than a generic error.
- **Pre-computation of Fallback Resources:** Any data or credentials required for the fallback action are fetched or computed once before the main processing loop to optimize performance and ensure availability.
- **Guaranteed Iteration:** The process is designed to attempt an action (primary or fallback) for every item in the input collection, ensuring comprehensive processing.
## Common Pitfalls
- Overly Broad Error Handling: Triggering a fallback for general API errors instead of only the specific, intended failure condition, which might mask other issues or lead to incorrect behavior.
- Redundant Resource Acquisition: Fetching fallback-specific resources inside the iteration loop, leading to unnecessary API calls and performance degradation.
- Premature Termination: Stopping the processing loop after the first failure, rather than attempting to process all remaining items in the collection.
- Ignoring API Response Structure: Not thoroughly understanding how API errors are communicated (e.g., message field, status codes, specific error objects) and thus failing to correctly identify the fallback trigger.
