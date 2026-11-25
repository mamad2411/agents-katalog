---
name: multi-step-action-with-conditional-fallback
description: When a primary action might fail due to a specific condition, this skill describes how to attempt the action, check for the failure, and then retry with an alternative parameter or method.
---
## Overview
This pattern addresses scenarios where an API call has a primary mode of operation but might require a secondary, fallback approach if the primary fails under specific, identifiable conditions. It involves an initial attempt, parsing the response for a known failure signature, and then executing a modified retry if that signature is found.
## When to Apply
- Perform an action, but if X happens, use Y.
- Accept/process items, using a fallback if the primary method fails.
- When an operation might require an alternative funding source or method.
## Procedure
1. Identify the list of items or actions to process.
2. Retrieve any necessary fallback resources or parameters upfront, if applicable.
3. Iterate through each item/action in the list.
4. Attempt the primary API call for the current item/action.
5. Inspect the API response for a specific failure condition (e.g., an error message indicating a need for fallback).
6. If the specific failure condition is met and a fallback resource/parameter is available, perform a secondary API call for the same item/action, incorporating the fallback.
7. Otherwise, consider the primary attempt as successful or handle other failure types as needed.
8. Optionally, record the outcome of each attempt (primary or fallback).
## Key Patterns
- **Conditional Retry:** An action is retried only if a specific failure message or status is detected from the initial attempt, rather than retrying for all types of failures.
- **Fallback Resource Pre-fetch:** If a fallback resource (e.g., an alternative payment method) is needed for multiple operations, it is efficient to fetch it once before iterating through the actions, rather than repeatedly fetching it inside the loop.
- **Response Message Parsing for Condition:** The decision to use a fallback is based on parsing specific keywords or patterns within an API's error message or status field, rather than just a generic error detection.
## Common Pitfalls
- Not correctly identifying the specific failure condition that warrants a fallback, leading to either unnecessary retries or missed fallback opportunities.
- Retrying for all types of failures, instead of only the specific scenario where a fallback is appropriate.
- Not handling cases where the fallback resource itself is unavailable or fails.
- Creating infinite loops if the fallback also fails or the condition for fallback is misidentified.
- Overlooking the need to fetch fallback resources or parameters once before the main processing loop, leading to redundant API calls.
