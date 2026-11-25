---
name: iterative-file-system-action
description: Processes multiple file system entries by iterating through a list and performing an action on each.
---
## Overview
This skill addresses tasks requiring operations on a collection of file system objects (e.g., directories, files). It typically involves an initial step to identify and list the target items, followed by an iterative step to perform a specific action on each identified item, often involving dynamic path construction and combined API calls.
## When to Apply
- For each X...
- Compress them and save them in Y for each Z...
- Then delete all X sub-directories.
- Repeat until all X are processed.
## Procedure
1. Identify Source Entries: Use a listing API to retrieve a collection of potential source entries (e.g., files, directories) from a specified base path.
2. Filter and Extract Identifiers: Process the retrieved entries to filter out irrelevant items (e.g., destination paths, non-target types) and extract key identifiers (e.g., name, full path) for each relevant source entry. Store these in a structured list.
3. Iterate and Perform Action: Loop through the structured list of source entries obtained from the previous step.
4. Construct Destination/Action Parameters: For each source entry, dynamically construct any necessary destination paths or API parameters using its extracted identifiers.
5. Execute File System Action: Call the appropriate file system API to perform the required action (e.g., compress, move, delete), passing the source path, dynamically constructed destination/parameters, and any necessary flags (e.g., delete_source, overwrite).
6. Track Progress (Optional): Maintain a record of successfully processed items for summary or reporting.
## Key Patterns
- **Iterate Prior Results:** The output of an initial listing and filtering step (a list of structured items) serves as the input for a subsequent iterative action step, decoupling identification from action.
- **Dynamic Path and Parameter Construction:** Destination paths or API parameters are not static but are built programmatically for each item in the loop, often incorporating identifiers extracted from the source item.
- **Combined File System Operations:** Leverage API parameters (e.g., delete_source, overwrite) to perform multiple related file system actions efficiently and atomically within a single API call.
- **Source List Filtering:** Explicitly exclude entries from the initial listing that are not valid targets for processing, such as the designated output location or entries that do not match the required criteria.
## Common Pitfalls
- Incorrectly Filtering Source Entries: Failing to exclude destination paths or other irrelevant entries from the initial list, leading to errors or unintended modifications.
- Static or Incorrect Path Construction: Hardcoding destination paths or failing to correctly use extracted identifiers to dynamically build unique and correct paths for each processed item.
- Missing Essential API Flags: Overlooking flags like 'overwrite' for existing destinations or 'delete_source' when the instruction requires removal of the original item, leading to incomplete or failed operations.
- Inadequate Error Handling for Iterative Actions: Not anticipating or handling potential API errors that might occur during the processing of individual items in a loop, which could halt the entire operation or leave the system in an inconsistent state.
