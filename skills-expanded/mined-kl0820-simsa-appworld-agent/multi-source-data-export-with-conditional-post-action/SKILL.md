---
name: multi-source-data-export-with-conditional-post-action
description: Collects, deduplicates, and exports multi-source API data to a file, then performs a dependent action only if the export is confirmed successful.
---
## Overview
This skill addresses tasks where required data is spread across several API endpoints, often necessitating pagination and/or multiple levels of API calls to gather complete records. The collected data then needs to be consolidated, deduplicated, formatted according to specific output requirements, and finally written to a file. A common follow-up is a dependent action that should only occur after the export is confirmed.
## When to Apply
- Export a unique list of items from multiple sources (e.g., 'library', 'albums', 'playlists')
- Combine data from various API endpoints into a single output
- Create a file with specific headers and custom field formatting
- Deduplicate records across different data sets before final output
- Perform a subsequent action only after a critical data export is complete
## Procedure
1. Initialize an empty list to accumulate all records.
2. For each distinct data source:
3.   Implement a pagination loop to retrieve all available items from the source's listing API.
4.   If the listing API provides only summary information or IDs, make a subsequent detail API call for each item to fetch complete record details.
5.   Extract the required fields from each record and append the structured data (e.g., as dictionaries) to the accumulated list.
6. Concatenate all accumulated lists from different sources into a single combined list.
7. Deduplicate the combined list by creating a composite key for each record (e.g., a tuple of relevant field values) and using a set to track seen keys, building a new list of unique records.
8. Prepare the output content:
9.   Construct the header row based on the specified output format.
10.   For each unique record, apply any required data transformations or formatting (e.g., joining multiple sub-fields with a specific delimiter).
11.   Format each record into a line suitable for the target file type (e.g., CSV with proper escaping/quoting).
12. Combine headers and formatted records into the final file content string.
13. Write the content to the specified file path using the file system API, ensuring any overwrite requirements are met.
14. If a dependent action is required, execute it only after the file write operation is confirmed successful.
## Key Patterns
- **Pagination Loop:** Use a `while True` loop with a `page_index` and `page_limit` to iterate through API results. Break the loop when the returned page is empty or contains fewer items than the `page_limit`, indicating the end of the collection.
- **Two-Level Data Retrieval:** When a listing API provides only identifiers or summary data, iterate through its results and make a subsequent detail API call for each item to retrieve the full set of required attributes.
- **Deduplication with Composite Key:** To deduplicate records across multiple sources, create a unique, hashable key for each record (e.g., a tuple of its primary identifying fields, ensuring any list-like fields within the key are converted to tuples) and store these keys in a `set` to efficiently check for uniqueness before adding the record to a final list.
- **Custom Delimited Field Formatting:** When a field needs to contain multiple sub-values separated by a specific character (e.g., artists separated by '|'), use a string `join` method on the list of sub-values with the specified delimiter.
- **CSV Field Escaping:** For CSV output, manually implement or use a utility to escape field values that contain commas, double quotes, or newlines by enclosing them in double quotes and doubling any internal double quotes, to ensure correct parsing.
- **Conditional Post-Export Action:** If a task requires a destructive or irreversible action (e.g., account termination) to occur after a critical data export, ensure the export milestone explicitly confirms success before proceeding with the dependent action.
## Common Pitfalls
- Failing to handle pagination correctly, leading to incomplete data retrieval or infinite loops.
- Not making necessary detail API calls when summary responses lack required fields.
- Incorrectly defining the deduplication key (e.g., using mutable types like lists directly in a set, or omitting critical identifying fields), resulting in improper deduplication.
- Neglecting to properly escape/quote fields for CSV output, leading to malformed files that are difficult to parse.
- Performing a destructive action before confirming the successful completion of a prerequisite data export.
- Overlooking edge cases like empty lists from API calls or records with missing optional fields.
