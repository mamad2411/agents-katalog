---
name: file-system-organize-by-attribute
description: Organizes file system entries into new locations based on attributes extracted from each entry.
---
## Overview
This skill addresses tasks requiring the rearrangement of files or directories within a file system. It involves an initial phase of listing relevant entries and retrieving their attributes, followed by a classification step based on these attributes, and finally, performing file system mutations (e.g., moving, copying) to achieve the desired organization.
## When to Apply
- Instructions to organize, arrange, or sort files/directories.
- Instructions to move or copy files/directories based on their properties (e.g., date, size, type).
- Instructions involving creating new directories to house existing files.
## Procedure
1. Identify the source location for file system entries.
2. List all relevant entries (files or directories) from the source location, potentially recursively.
3. For each listed entry, retrieve specific attributes (e.g., creation date, size, type) using a detail-fetching API.
4. Accumulate the entry paths and their retrieved attributes into a structured list.
5. Identify target destination locations or patterns for new locations.
6. Create any necessary new destination directories, ensuring idempotency if possible.
7. Iterate through the accumulated list of entries and their attributes.
8. Apply conditional logic based on the attributes to determine the specific destination for each entry.
9. Construct the full destination path for each entry, preserving original names if required.
10. Perform the specified file system mutation (e.g., move, copy) for each entry to its determined destination.
11. The final output is typically null, as the primary outcome is the side effect on the file system.
## Key Patterns
- **Two-Phase Information Gathering:** First, obtain a list of identifiers (e.g., paths, IDs) for target entities. Second, iterate through these identifiers to fetch detailed attributes for each using a separate API call.
- **Conditional Routing of Actions:** Use if/elif/else statements to classify entities based on their attributes and direct them to different target locations or apply different actions.
- **Attribute-Based Path Construction:** Extract relevant parts of an original path (e.g., filename) and combine them with newly determined directory names to form a new, complete destination path.
- **Idempotent Directory Creation:** When creating new directories, use an 'allow_if_exists' parameter or similar mechanism to prevent errors if the directory already exists, making the operation safely repeatable.
## Common Pitfalls
- Not handling recursive listing when required, leading to incomplete data.
- Failing to parse or correctly extract attributes (e.g., date components) from raw data.
- Incorrectly constructing destination paths, leading to files being moved to unintended locations or overwriting existing files.
- Not making directory creation idempotent, causing errors on re-execution.
- Forgetting to preserve original filenames when moving/copying, if that's the requirement.
- Assuming 'this year' refers to the current year at execution time rather than the year specified in the task context.
