---
name: file-system-transformation-workflow
description: This skill applies when a task requires a sequence of file system operations, including identifying target entities, transforming them, and then cleaning up the original sources.
---
## Overview
This pattern addresses tasks that involve a multi-stage process on file system entities. It typically starts by identifying a set of source directories or files, then applies a specific transformation (e.g., compression, moving, copying) to each, often creating new entities. Finally, it may involve a cleanup phase where the original source entities are removed, ensuring that intermediate or output directories are not inadvertently affected.
## When to Apply
- List/read directories or files based on specific criteria.
- Process each identified entity (e.g., sub-directory, file).
- Perform a transformation (e.g., compress, copy, move) on these entities.
- Save transformed entities to a new location with a specific naming convention.
- Delete the original source entities after transformation.
- Ensure certain directories or files are excluded from processing or deletion.
## Procedure
1. Identify Source Entities: Call a listing API to retrieve potential source entities (directories or files) from a specified base path.
2. Filter and Extract Identifiers: Process the raw listing to extract unique identifiers (e.g., base names) for each relevant source entity. Apply any necessary filtering rules (e.g., excluding specific names or types).
3. Iterate and Transform: Loop through the extracted identifiers. For each identifier, construct the full source path and the desired destination path for the transformed entity. Call the appropriate transformation API (e.g., compress, copy, move), ensuring parameters like 'overwrite' are set as needed and that original sources are NOT deleted at this stage. Accumulate details of the transformed entities.
4. Clean Up Original Sources: Loop through the original source identifiers again. For each, construct its full path and call the deletion API. Ensure that only the original source entities are deleted and that transformed outputs or other critical directories remain untouched.
## Key Patterns
- **Dynamic Path Construction:** Building full file system paths by combining base paths, extracted identifiers, and specific suffixes/prefixes.
- **Iterative Processing of Identified Entities:** Applying a sequence of operations (transformation, deletion) by looping over a list of entities derived from an initial listing.
- **Staged Operations:** Separating transformation and deletion into distinct steps to prevent data loss and ensure transformations complete successfully before sources are removed.
- **Exclusion Filtering:** Explicitly identifying and skipping specific entities (e.g., output directories) during the initial listing or subsequent processing steps.
- **Cross-Milestone Variable Usage:** Relying on variables populated in earlier milestones (e.g., a list of entity identifiers) to drive subsequent iterative operations.
- **Idempotent Operations:** Using API parameters (e.g., 'overwrite=True') to ensure that re-running a step does not cause errors due to existing files.
## Common Pitfalls
- Incorrectly constructing source or destination paths, leading to operations on wrong files/directories or creation in unintended locations.
- Deleting source entities prematurely before their transformation is confirmed or completed.
- Failing to exclude output or temporary directories from the initial listing or subsequent deletion, leading to accidental data loss.
- Not handling cases where the initial listing might be empty, causing subsequent loops to fail or be inefficient.
- Overwriting existing files without explicit instruction or confirmation, or failing to use 'overwrite' when it's intended.
- Misinterpreting the scope of deletion (e.g., deleting a parent directory instead of just its contents).
