---
name: iterative-action-with-idempotent-handling
description: Applies a state-changing API action to each item in a collection, robustly handling idempotent success conditions.
---
## Overview
Many tasks require performing the same action on multiple entities. This pattern ensures that such operations are executed for all target entities, gracefully managing scenarios where the action might have already been completed for some entities, treating these as successful idempotent operations rather than errors.
## When to Apply
- For each X in Y, do Z.
- Ensure all X are in state S.
- Apply action A to all items.
- Follow all artists.
## Procedure
1. Obtain the collection of items to process, typically from a prior step's output.
2. Initialize empty lists or counters to track successfully processed items, items for which the action was already completed (idempotent success), and items that resulted in actual errors.
3. Iterate through each item in the collection.
4. Within the loop, use a try-except block to wrap the API call that performs the action on the current item.
5. In the try block, make the API call. If successful, add the item to the list of successfully processed items or increment its counter.
6. In the except block, catch general exceptions. Inspect the error message (e.g., by converting the exception to a string) to identify specific phrases indicating an idempotent success condition (e.g., 'already exists', 'already followed').
7. If an idempotent success condition is detected, add the item to the list of already-completed items or increment its counter.
8. Otherwise, if it's a different error, add the item and its error details to the list of error items or increment its counter.
9. After the loop, summarize the results, reporting counts for newly processed, already completed, and error items.
10. Construct a structured output that reflects the outcome of the bulk operation, including counts and potentially lists of affected items.
## Key Patterns
- **Idempotent Error Handling:** Distinguish between true errors and conditions where the desired state is already achieved, treating the latter as a successful idempotent operation rather than a failure.
- **Iterative Application:** Apply a single API call repeatedly across a collection of inputs, ensuring each item is processed.
- **Categorized Outcome Reporting:** Separate and report results into distinct categories (e.g., newly processed, already completed, failed) for clear and comprehensive feedback on the bulk operation.
## Common Pitfalls
- Not using try-except blocks, leading to early termination of the entire process on the first error.
- Treating idempotent success conditions as actual errors, leading to incorrect reporting or unnecessary retries.
- Failing to collect and report on the different categories of outcomes, providing an incomplete picture of the operation's success.
- Not handling cases where the input collection is empty, potentially leading to unnecessary loop iterations or incorrect summary reporting.
