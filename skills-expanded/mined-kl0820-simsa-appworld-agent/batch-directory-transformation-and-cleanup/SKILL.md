---
name: batch-directory-transformation-and-cleanup
description: Iterates through a collection of directories, applies a transformation to each, and then performs a cleanup action on the original directories.
---
## Overview
This pattern addresses tasks requiring sequential operations on a set of file system entities. It typically involves identifying target entities, performing a primary action (like compression or conversion) that generates new output, and then a secondary action (like deletion) on the original entities. The key is managing the state and ensuring the correct entities are acted upon at each stage, often passing structured data between milestones.
## When to Apply
- For each X in Y, do Z.
- Compress them and save them in A, and then delete B.
- Organized in sub-directories for each <entity>.
- Create new files based on existing ones, then remove the originals.
## Procedure
1. Identify and Filter Source Entities: List entities (e.g., directories) from a specified base path, filter out any irrelevant or output-specific entities, and extract a unique identifier and full path for each valid source entity. Store these as structured records.
2. Perform Primary Transformation: Iterate through the identified source entities. For each, construct a target output path/name using its unique identifier and apply the primary transformation API (e.g., compress, convert). Accumulate results, including the identifier and the path to the newly created transformed entity.
3. Perform Cleanup Action: Iterate through the original source entities (identified in step 1). For each, call the cleanup API (e.g., delete) using its original path. Accumulate records of the cleaned-up entities.
## Key Patterns
- **Multi-stage Data Flow:** The structured output (e.g., list of dictionaries) from an earlier milestone, containing identified entities and their properties, serves as the direct input for subsequent processing steps, ensuring continuity and correct targeting.
- **Dynamic Output Path Construction:** Output file paths or names are constructed dynamically by combining a base output directory, a unique identifier extracted from the input entity, and a specified file extension.
- **Separation of Transformation and Cleanup:** When a task specifies a transformation followed by a cleanup action on the original source, these operations are performed in distinct steps or milestones, even if an API offers a combined option, to ensure proper sequencing and control.
- **Basename Extraction for Identifier:** A unique identifier for an entity (e.g., a name) is often derived by extracting the basename or the last path component of its directory or file path.
- **Exclusion Filtering:** Initial listing of entities often requires filtering out specific items (e.g., a designated output directory) to prevent unintended processing or recursion.
## Common Pitfalls
- Deleting source entities prematurely before the transformation is complete or successful.
- Incorrectly constructing output paths, leading to files being saved in the wrong location or with incorrect names.
- Failing to filter out output directories or other irrelevant entities during the initial listing, potentially leading to infinite loops or errors.
- Confusing the source paths with the newly created target paths in subsequent steps.
- Not handling the case where the initial listing yields no entities, leading to errors in subsequent loops.
- Overwriting existing files without explicit instruction or confirmation.
