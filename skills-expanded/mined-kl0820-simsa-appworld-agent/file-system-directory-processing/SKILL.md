---
name: file-system-directory-processing
description: Describes the process of identifying specific sub-directories within a file system, performing an action on each, and then optionally cleaning up the original directories.
---
## Overview
This skill addresses tasks requiring systematic interaction with file system directories. It involves an initial discovery phase to identify target directories, followed by an iterative application of a primary operation (e.g., compression, transformation) to each identified target. Finally, it may include a cleanup phase to remove the original target directories while preserving processed outputs.
## When to Apply
- Process items within a specific directory structure.
- Perform an action for each sub-directory.
- Compress or archive multiple directories.
- Delete directories after processing their contents.
- Identify directories based on their location or name.
## Procedure
1. List the contents of a specified root directory, filtering for directory entries only.
2. From the listed directory entries, extract their bare names and filter out any special or output directories.
3. Store the list of identified target directory names for subsequent steps.
4. Iterate through the stored list of target directory names.
5. For each target directory name, construct the full source path to the directory and the full destination path for the processed output.
6. Apply the primary file system operation (e.g., compress, move, transform) to the source directory, saving the result to the destination path, ensuring that the original source directory is not deleted at this stage.
7. After all primary operations are complete, iterate again through the original list of target directory names.
8. For each target directory name, construct the full path to the original directory.
9. Apply the deletion operation to each original target directory, ensuring only these specific directories are removed and not any parent or output directories.
## Key Patterns
- **Root Directory Identification and Filtering:** The initial listing of a root directory's contents often requires careful filtering to distinguish between container directories and the actual items to be processed. This includes extracting the bare name from a path string and explicitly excluding specific directory names (e.g., output directories) that should not be processed or deleted.
- **Iterative Processing with Prior Variables:** Once a definitive list of target entities (e.g., directory names) is established in an earlier step, subsequent steps should iterate over this exact list. This ensures consistency and avoids redundant discovery or processing of an outdated set of targets, using each item to dynamically construct paths for API calls.
- **Staged Operations with Deletion Control:** When a task involves multiple sequential file system operations (e.g., compress then delete), it is crucial to control deletion behavior in each stage. The processing step should explicitly prevent deletion of source directories if a separate, later cleanup step is intended, to avoid premature data loss.
- **Dynamic Path Construction:** For each item in an iteration, source and target paths must be dynamically constructed by combining a base path with the current item's identifier. This pattern is consistently applied for both processing and cleanup operations to ensure correct targeting of file system entities.
## Common Pitfalls
- Incorrectly identifying the root directory for listing, leading to missing or extraneous entries.
- Failing to filter out non-target entries (e.g., files when only directories are needed) or special directories (e.g., output directories) from the initial list.
- Accidentally deleting parent directories or processed output directories instead of only the intended target sub-directories.
- Not preserving the exact names or casing of target entities, leading to path mismatches in subsequent API calls.
- Attempting to delete source directories during the processing step before their contents have been successfully processed or moved.
- Hardcoding paths instead of dynamically constructing them from identified targets, making the solution inflexible.
