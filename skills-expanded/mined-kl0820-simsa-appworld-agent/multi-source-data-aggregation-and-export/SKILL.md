---
name: multi-source-data-aggregation-and-export
description: Describes how to gather data from multiple paginated API sources, consolidate it into a canonical format, deduplicate, and export to a structured file.
---
## Overview
This skill addresses tasks requiring the collection of similar data entities from various API endpoints, often involving pagination and nested detail calls. It outlines a robust procedure for accumulating this data into a consistent intermediate structure, performing necessary transformations and deduplication, and finally exporting the aggregated information to a structured file format, potentially followed by a dependent final action.
## When to Apply
- Instruction requires collecting similar data entities from several distinct API endpoints.
- Data needs to be paginated from one or more sources to retrieve all items.
- A 'list-then-detail' pattern is required to get full entity information for items obtained from a listing API.
- The final output requires deduplication across collected data from multiple sources.
- The final output is a structured file (e.g., CSV, JSON) with specific formatting requirements.
- A final action is specified that must only occur after a prior data processing or export step is confirmed complete.
## Procedure
1. Initialize an empty list to accumulate all records in a canonical intermediate data structure.
2. For each distinct data source:
3.   Paginate the primary listing API for that source, accumulating identifiers or summary data.
4.   For each item obtained from the listing, if necessary, call a detail API to retrieve complete information.
5.   Extract relevant fields from the detail response and transform them into the predefined canonical intermediate data structure (e.g., a dictionary with specific keys and value types).
6.   Append each structured record to the accumulating list.
7. Combine all accumulated lists from different sources into a single master list.
8. Deduplicate the master list: construct a unique key for each record (e.g., a tuple of immutable field values) and add records to a new list only if their key has not been seen before, preserving the order of first appearance.
9. Transform the deduplicated records into the final output format (e.g., CSV rows, JSON array elements), applying any specified formatting or joining rules.
10. Write the formatted data to the specified file path using a robust file writing mechanism that handles headers and proper quoting.
11. If a final action is required, execute it only after confirming the successful completion of the file write operation.
## Key Patterns
- **Pagination Loop:** To retrieve all items from an API that returns results in pages, repeatedly call the API with an incrementing page index and a fixed page limit until an empty or partial page is returned, indicating the end of the collection.
- **List-Then-Detail API Calls:** When a listing API provides only summary information or identifiers, iterate through the items from the listing API and make a subsequent, more detailed API call for each item's identifier to retrieve its full attributes.
- **Canonical Intermediate Data Structure:** Define a consistent dictionary or object structure for each individual record (e.g., {'field_a': string, 'field_b': list_of_strings}) early in the process. All data extracted from different sources must be transformed into this exact structure to facilitate subsequent aggregation, deduplication, and uniform processing.
- **Deduplication Key Construction:** For deduplication, create a unique, hashable key for each record by combining its identifying fields (e.g., a tuple of the record's title and a tuple of its artist names). Use an ordered set of these keys to track seen items while preserving the order of first appearance in the final unique list.
- **Robust Structured File Generation:** When generating structured text files like CSV, use standard library modules (e.g., Python's `csv` module with `io.StringIO`) to correctly handle headers, field delimiters, and automatic quoting of fields containing special characters (like commas or newlines), ensuring data integrity and proper parsing by external tools.
- **Precondition-Dependent Final Action:** When a task specifies a final, irreversible action (e.g., account deletion) that is contingent on a prior step (e.g., data backup), the planner must ensure the final action milestone is only scheduled and executed after the successful completion of the prerequisite step has been confirmed, typically by checking a prior milestone's output or side-effect marker.
## Common Pitfalls
- Forgetting to paginate, leading to incomplete data collection.
- Not handling empty results from API calls, causing errors or incomplete data.
- Inconsistent data structures across different sources, making aggregation and deduplication difficult.
- Incorrectly constructing deduplication keys, leading to either missed duplicates or accidental removal of unique items.
- Manually concatenating strings for CSV output, which can lead to malformed CSVs if fields contain delimiters or quotes.
- Executing a final, irreversible action without explicit confirmation that all preceding critical steps have successfully completed.
