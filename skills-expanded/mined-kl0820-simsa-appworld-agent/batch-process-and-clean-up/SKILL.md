---
name: batch-process-and-clean-up
description: This skill applies when a list of resources needs to be processed sequentially, with each processing step involving a mutation and a subsequent cleanup action.
---
## Overview
This structural pattern addresses tasks requiring the iterative processing of a collection of items, where each item undergoes a transformation or modification, followed by a cleanup or deletion of the original item. The challenge is to correctly identify the items, perform the operations robustly, and ensure all items are processed and their originals handled as specified.
## When to Apply
- For each item in a collection, perform an action and then remove the original item.
- Transform a set of source resources into a new format or location, then delete the original sources.
- Iterate through a list of entities, applying a modification and a subsequent cleanup operation.
- Process all identified resources and ensure their original forms are no longer present.
## Procedure
1. Identify the source collection of items to be processed, typically by listing resources in a specified location.
2. Filter the identified items to exclude any that are targets of the operation or otherwise irrelevant.
3. For each relevant item, extract all necessary identifiers and paths required for subsequent API calls.
4. Store the extracted information as a structured list for the next processing stage.
5. Read the structured list of items from the previous step.
6. Iterate through each item in the list.
7. For each item, construct the target path or identifier for the transformed/mutated resource.
8. Call the primary mutation API, ensuring that any required cleanup action (e.g., deletion of the original item) is performed, ideally as part of the same API call if supported.
9. Include parameters for robustness, such as overwriting existing target resources if applicable.
10. Record the identifier of the successfully processed item for summary purposes.
11. Confirm that all items from the initial list have been processed.
12. Produce a null value as the output, as the primary outcome of this stage is the side effect of the mutations and cleanups.
## Key Patterns
- **Combined Mutation and Cleanup:** Look for API parameters that allow combining multiple logical steps (e.g., transform and delete) into a single atomic operation for efficiency, consistency, and reduced error surface.
- **Verbatim Identifier Extraction:** When extracting identifiers or names from resource paths, preserve their exact casing and formatting unless the instruction explicitly requires modification or normalization.
- **Exclusion of Output Target:** When listing resources that serve as input, explicitly filter out any resources or directories that are designated as the *output* location for the process, to prevent self-referential issues or unintended processing.
- **Action Milestone Null Output:** For milestones primarily performing state-changing actions with no data artifact to pass to subsequent steps, the 'value' field should be set to null, as the primary outcome is the side effect.
- **Robust Overwrite Handling:** When creating or modifying resources that might already exist, utilize 'overwrite' or similar parameters in API calls to ensure idempotent behavior and prevent failures due to pre-existing targets.
## Common Pitfalls
- Failing to filter out the output target resource from the input list of items to be processed.
- Not utilizing combined API calls for mutation and cleanup when available, leading to potential inconsistencies if one step fails after another succeeds.
- Modifying resource names or identifiers when the instruction requires verbatim preservation.
- Not handling pre-existing target resources, causing the operation to fail if the target already exists.
- Returning data from a purely action-oriented milestone when a null value is more appropriate.
- Failing to iterate through and process all items identified in the initial collection.
