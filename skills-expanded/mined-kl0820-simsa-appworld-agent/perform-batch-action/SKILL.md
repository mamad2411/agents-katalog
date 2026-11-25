---
name: perform-batch-action
description: Applies a single, state-changing API action to each item in a collection of previously identified entities.
---
## Overview
This skill addresses scenarios where a set of entities has been identified in a prior step, and a uniform, state-changing operation needs to be applied to all of them. It involves iterating through the collection and invoking a specific API for each item, assuming the validity of the identifiers from upstream processing.
## When to Apply
- Instructions to perform an action on 'all' or 'each' of a previously identified set of items.
- The action is a single, atomic operation per item (e.g., comment, like, update, delete).
- The items to act upon are available as a collection from a prior milestone's output.
## Procedure
1. Retrieve the collection of target entities or their identifiers from a prior milestone's output.
2. Extract the necessary identifier for each entity from the collection.
3. Define any static parameters required for the action (e.g., the comment text, the status to set).
4. Iterate through the extracted identifiers.
5. For each identifier, call the appropriate state-changing API with the identifier and any static parameters.
6. Accumulate the identifiers of the entities on which the action was successfully performed.
7. Construct the final result as a list of these accumulated identifiers.
## Key Patterns
- **Unconditional Batch Execution:** Actions are performed directly on all provided identifiers without re-validation or conditional checks, relying on the correctness of prior identification steps. Any API errors are expected to surface as exceptions.
- **Identifier Extraction:** The input from a prior step might be a complex object; only the minimal necessary identifier (e.g., an ID string or integer) is extracted for use in the current API call.
- **Confirmation Output:** The output of this skill is typically a list of the identifiers that were successfully acted upon, serving as a confirmation rather than new data for subsequent steps.
## Common Pitfalls
- Attempting to re-validate or filter the input collection, duplicating work already done in prior milestones.
- Failing to correctly extract the unique identifier from each item in the input collection.
- Not handling potential API errors gracefully (e.g., logging failures, collecting failed IDs).
- Modifying static parameters (e.g., comment text) instead of using them verbatim as instructed.
