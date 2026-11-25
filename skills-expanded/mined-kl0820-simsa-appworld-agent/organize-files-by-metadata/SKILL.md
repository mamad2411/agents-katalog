---
name: organize-files-by-metadata
description: Organizes files into subdirectories based on their metadata, such as creation date, type, or size, creating new directories as needed.
---
## Overview
This skill addresses tasks that involve a multi-stage process: first, listing files and extracting their detailed metadata for classification; second, creating target subdirectories based on these classifications; and finally, moving the files into their respective new locations. It demonstrates a common pattern of data-driven organization and manipulation of file systems.

## When to Apply
- Instructions to organize files into subdirectories or other containers.
- Classification criteria based on file metadata (e.g., creation date, size, type, tags).
- Need to create new destination directories before moving files.
- Task involves processing multiple files from a source location into multiple destination locations.
- Maintaining original file names during relocation.

## Procedure
1.  Identify the source directory containing the files to be organized.
2.  List all relevant files within the source location.
3.  For each file, retrieve its detailed metadata using a detail API.
4.  Parse and extract relevant components from the metadata (e.g., year, month from a timestamp; file extension for type) to facilitate categorization.
5.  Apply classification rules based on the extracted metadata to assign each file to a specific category. Store the original file path, its name, and its assigned category along with any other relevant extracted metadata in a structured format for subsequent processing.
6.  Identify the unique categories determined in the previous step (or from task instructions).
7.  For each distinct category:
    a.  Construct a target subdirectory path within a specified parent container.
    b.  Ensure the target subdirectory exists, creating it if necessary. Use an API that allows creation only if it doesn't exist, or explicitly check and create, to ensure idempotency.
    c.  Filter the structured file data to identify files belonging to the current category.
    d.  For each file in the filtered set, construct its new destination path by appending its original name to the target subdirectory path.
    e.  Move the file from its original location to the new destination.
    f.  Record the original and new paths of the moved files.

## Key Patterns
-   **List-Detail-Classify / Metadata Enrichment:** Initial listing APIs often provide only basic file paths. A subsequent call to a detail API for each file is required to fetch richer metadata (e.g., creation date, size, permissions) necessary for categorization or filtering. This enriched data, including any derived attributes (e.g., year, month from a timestamp), must be explicitly included in the output of the current processing step for subsequent steps to use.
-   **Data-Driven Resource Creation / Idempotent Directory Creation:** Create new resources (e.g., directories) based on categories derived from prior classification or a predefined list. When creating resources, use API parameters (e.g., 'allow_if_exists') that prevent errors if the resource already exists, making the operation safe for re-runs.
-   **Conditional Filtering and Action:** Files are processed in groups based on specific criteria derived from their metadata. This involves filtering a master list of files and then applying a common action (e.g., moving) to all files within that filtered group. The filtering logic can be inclusive (e.g., 'attribute == value') or exclusive (e.g., 'not (attribute == value1 or attribute == value2)').
-   **Dependent Actions:** Subsequent steps (e.g., moving items) rely directly on the output and state established by prior steps (e.g., item classification, container creation).
-   **Preserving Original Identifiers / Path Derivation for Relocation:** When moving or copying files, ensure that their original names or unique identifiers are maintained in the new location or context. The original file name must be extracted from the source path and appended to the new destination directory path to maintain file identity and prevent accidental renaming.

## Common Pitfalls
-   Not handling empty listings gracefully, leading to errors when no items are found.
-   Failing to retrieve sufficient metadata for categorization, relying only on basic listing results.
-   Failing to correctly parse and compare metadata (e.g., date formats, string comparisons) or extract relevant components.
-   Incorrectly constructing destination paths, leading to files being moved to the wrong place or overwritten, or loss of original file names.
-   Not making container creation idempotent, causing errors on re-runs if containers already exist.
-   Forgetting to reuse variables from prior milestones, leading to redundant API calls or re-computation of classifications.
-   Modifying the list of files being iterated over for filtering, leading to skipped or double-processed items. Always filter from the original, complete list of files.