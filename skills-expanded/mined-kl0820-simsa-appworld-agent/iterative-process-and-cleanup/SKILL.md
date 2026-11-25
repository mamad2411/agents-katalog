---
name: iterative-process-and-cleanup
description: Applies when a task requires identifying a set of items, performing an action on each, and then performing a subsequent cleanup action on the original items.
---
## Overview
This skill addresses tasks that involve a multi-stage process: first, identifying a collection of target entities; second, performing a primary operation on each entity, often generating new artifacts; and third, performing a cleanup operation on the *original* entities. It emphasizes careful sequencing and avoiding premature cleanup.
## When to Apply
- Identify a set of items (e.g., files, directories, resources) under a specific path.
- Perform an operation on each identified item, potentially creating new artifacts.
- Subsequently clean up or remove the original items.
- The cleanup operation must *not* affect the newly generated artifacts or parent structures.
- The task explicitly separates the primary operation from the cleanup.
## Procedure
1. Identify Targets: Use a listing API to find entities under a specified parent path. Filter these entities based on type (e.g., directories only) and specific names (e.g., exclude a known output directory). Extract both the full path and a unique identifier (e.g., basename) for each target. Store this as a list of structured records.
2. Perform Primary Action: Iterate through the structured records from the identification step. For each record, construct a target path for the new artifact using the unique identifier. Call the relevant action API (e.g., compress, copy) on the original entity's path, saving the output to the constructed target path. Crucially, ensure any parameters that would combine this action with a cleanup (e.g., 'delete_source=True') are *not* used, preserving the original entity. Accumulate results, including the original identifier and the path to the new artifact.
3. Perform Cleanup Action: Iterate through the *original* structured records from the identification step (not the results of the primary action). For each record, call the relevant cleanup API (e.g., delete) on the original entity's path. Ensure this action targets *only* the original entities and does not inadvertently affect parent directories or the newly created artifacts. Accumulate results, including the original identifier and the path of the cleaned-up entity.
## Key Patterns
- **Sequential Processing:** Operations are strictly ordered, with the output of one stage serving as input for the next, or a prior stage's output being reused later in the sequence.
- **Basename Extraction:** Extracting the final path component (basename) from a full path to serve as a unique identifier for naming new artifacts or referencing entities.
- **Dynamic Path Construction:** Building output paths by combining a predefined base path with extracted identifiers from the source entities.
- **Source of Truth:** When multiple steps operate on a set of items, always refer back to the *initial* list of identified items for subsequent cleanup or further processing, rather than an intermediate list of generated artifacts.
## Common Pitfalls
- Combining primary action and cleanup: Using API parameters (e.g., 'delete_source=True') that perform cleanup prematurely, violating the task's explicit sequence. The procedure's sequential steps take precedence over any API shortcuts.
- Incorrectly identifying cleanup targets: Deleting parent directories or newly generated artifacts instead of only the original source items.
- Not filtering initial list: Failing to exclude specific entries (e.g., known output directories) from the initial identification step, leading to incorrect processing or cleanup.
- Using the wrong prior variable: Using the output of an intermediate step (e.g., list of generated artifacts) as the source for a cleanup step that should target the *original* items.
