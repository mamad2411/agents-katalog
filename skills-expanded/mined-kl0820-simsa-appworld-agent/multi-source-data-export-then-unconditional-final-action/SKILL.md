---
name: multi-source-data-export-then-unconditional-final-action
description: Collects, deduplicates, and exports multi-source API data to a file, then performs a mandated final action directly, trusting prior milestone success.
---
## Overview
This skill addresses tasks that involve a multi-stage process: first, gathering data from various API endpoints, often requiring pagination and detail calls for nested entities, and then consolidating and deduplicating this data. Second, transforming the collected data into a specific file format (e.g., CSV) and writing it to the file system. Finally, performing a subsequent, often critical or destructive, action that depends on the successful completion of the data export.

## When to Apply
- Instructions to gather data from multiple distinct sources.
- Requirements to handle paginated API responses.
- Tasks involving deduplication of collected records to create a unique list of items.
- Instructions to format and export data to a structured file (e.g., CSV) with specific headers and formatting.
- A final, often irreversible or state-changing, action is specified after data processing and export.
- Performing an action after a backup or export is complete.

## Procedure
1.  Initialize a central data structure (e.g., a dictionary or set) to store aggregated and unique items.
2.  Define a helper function to standardize the process of extracting identifiers, transforming data fields, and adding items to the central data structure, handling potential API errors or empty responses gracefully.
3.  For each primary data source:
    a.  Implement a pagination loop to retrieve all top-level items or records.
    b.  If top-level items only contain identifiers or references to sub-entities, collect these.
    c.  For each collected identifier or reference, make a detail API call to retrieve the full item or sub-entity data.
    d.  Use the helper function to add the extracted and transformed item data to the central data structure.
4.  After processing all sources, retrieve the consolidated data from the central data structure.
5.  Deduplicate the aggregated data by constructing a unique, hashable key for each record (e.g., a tuple of identifying fields) and storing only unique records in a new collection (if not already handled by the initial data structure).
6.  Read the consolidated and deduplicated data (potentially from a prior milestone variable).
7.  Transform the data into the required output file format (e.g., CSV rows), including headers, proper field formatting, and escaping for delimiters and special characters.
8.  Write the formatted content to the specified file path using a file system API, ensuring correct encoding and overwrite behavior.
9.  Perform the final, state-changing action as instructed, directly calling the relevant API without adding redundant conditional checks, trusting the successful completion of prior milestones.

## Key Patterns
-   **Multi-Source Paginated Data Collection:** Systematically iterate through multiple distinct API endpoints, each potentially requiring pagination, to gather a comprehensive dataset. This often involves a two-step process for complex entities: first listing IDs or references, then making individual detail calls for each to retrieve complete item data.
-   **Complex Object Deduplication:** To deduplicate a list of dictionaries or complex objects, construct a hashable key (e.g., a tuple of relevant scalar fields and immutable representations of nested lists/dictionaries) for each object and use a set to track seen keys, ensuring each unique item is processed only once.
-   **Structured File Content Generation:** Manually construct the content for a structured file (e.g., CSV) by iterating through the collected data, formatting each row according to specifications, and ensuring proper escaping for delimiters and special characters.
-   **Reading Prior Milestone Variables:** Access intermediate results from previous milestones using `prior_variable_values['variable_name']` to ensure continuity and build upon prior computations.
-   **Unconditional Final Action:** When a task explicitly mandates a final, often destructive or irreversible, action after all preceding steps are complete, execute the corresponding API call directly without additional conditional checks, relying on the success status of preceding milestones.

## Common Pitfalls
-   Failing to handle pagination correctly, leading to incomplete data retrieval or infinite loops.
-   Not collecting all necessary sub-entity IDs or references before making detail calls, or missing detail calls entirely.
-   Incorrectly constructing hashable keys for deduplication, leading to either over-deduplication (losing unique items) or under-deduplication (redundant entries).
-   Improperly formatting or escaping fields when generating structured file content (e.g., CSV), leading to parsing errors.
-   Forgetting to read intermediate results from prior milestones, breaking the task flow.
-   Adding unnecessary conditional checks before executing an explicitly requested final action, complicating the code and potentially obscuring the core task.
-   Not confirming the successful completion of prerequisite steps before performing a destructive action.