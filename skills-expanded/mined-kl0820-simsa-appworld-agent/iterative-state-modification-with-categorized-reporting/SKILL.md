---
name: iterative-state-modification-with-categorized-reporting
description: Applies when the task requires performing a state-changing action for each item in a collection obtained from a prior step, with detailed outcome categorization.
---
## Overview
This skill addresses tasks that involve iterating over a list of entities, typically sourced from a previous data retrieval step, and applying a specific state-modifying API call to each entity. It emphasizes robust error handling to distinguish between successful operations, operations that indicate a pre-existing state (e.g., "already exists"), and genuine failures, providing a comprehensive summary of all outcomes.
## When to Apply
- Perform an action for each item in a list.
- Update the status of multiple entities.
- Ensure a collection of items meets a certain state.
- Report on the success or failure of individual operations within a batch.
- Synchronize a local collection with an external system's state.
## Procedure
1. Retrieve the collection of entities from the output of a previous milestone.
2. Initialize separate lists or counters to track entities based on their action outcome (e.g., newly created/modified, already in desired state, failed).
3. Iterate through each entity in the retrieved collection.
4. For each entity, extract the necessary identifier(s) or parameters required by the state-modifying API.
5. Execute the state-modifying API call within a try-except block to handle potential errors.
6. Inside the try block, if the API call succeeds, record the entity in the 'newly created/modified' category.
7. Inside the except block, analyze the exception message or API response to determine if the error indicates an "already exists" or "already in desired state" condition.
8. If it's an "already exists" condition, record the entity in that specific category.
9. Otherwise, record the entity in the 'failed' category, including the error details.
10. After processing all entities, compile and report a summary that includes the total number of entities processed and the counts for each outcome category.
## Key Patterns
- **Prior Output Consumption:** The current step's input is directly sourced from the structured output of a preceding milestone, typically a list of dictionaries.
- **Categorized Error Handling:** Distinguishing between different types of API responses or exceptions (e.g., success, idempotent success/already-exists, actual failure) to provide granular reporting on the state-changing operations.
- **Iterative State Change:** Applying the same state-modifying operation repeatedly for each item in a collection, ensuring each item is processed.
- **Comprehensive Outcome Reporting:** Providing a clear breakdown of how many items fell into each outcome category (e.g., newly processed, already processed, failed).
## Common Pitfalls
- Not handling exceptions or specific error messages, leading to premature termination or inaccurate reporting.
- Failing to categorize outcomes, resulting in a vague "success/failure" report instead of detailed status (e.g., distinguishing between "already followed" and a true API error).
- Incorrectly parsing the input collection from the prior step, leading to processing errors.
- Not accumulating results or counts for a final summary, making it difficult to assess the overall task completion.
