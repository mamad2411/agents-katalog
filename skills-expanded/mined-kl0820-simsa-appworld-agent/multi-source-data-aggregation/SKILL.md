---
name: multi-source-data-aggregation
description: Aggregates data from multiple API endpoints, processes it (e.g., deduplication), and then performs a final action or writes to a destination.
---
## Overview
This skill addresses tasks requiring data collection from several distinct API sources, often involving nested calls or pagination. The collected data is then typically consolidated and processed, such as deduplication, before being formatted and written to a final destination or used to trigger a subsequent action.
## When to Apply
- Collect data from multiple distinct sources.
- Deduplicate collected items.
- Write processed data to a file.
- Perform a final action contingent on prior steps.
- Extract specific fields from API responses.
## Procedure
1. Initialize an empty data structure to accumulate items.
2. For each primary data source:
3. Iteratively fetch data, handling pagination if necessary.
4. If the primary data provides only identifiers, make secondary API calls for each identifier to retrieve full details.
5. From each retrieved item, extract specified fields.
6. Add the extracted data to the accumulator.
7. Consolidate the accumulated data from all sources.
8. Process the consolidated data (e.g., deduplicate based on a composite key).
9. Format the processed data according to the target output specification (e.g., CSV string with specific headers and delimiters).
10. Write the formatted data to the specified destination using a file system API.
11. Perform a final, state-changing action using an API, contingent on the successful completion of prior steps.
## Key Patterns
- **Paginated Data Collection:** Iteratively call a listing API with a page index/offset until an empty or partial page indicates the end of results.
- **Nested Detail Fetch:** Collect identifiers from a listing API, then make individual detail calls for each identifier to retrieve complete item data.
- **Composite Deduplication Key:** To ensure uniqueness across multiple fields, construct a hashable key (e.g., a tuple) from relevant item attributes and use a set to track seen items.
- **In-Memory CSV Generation:** Use Python's `csv` module with `io.StringIO` to build CSV content in memory before writing it as a single string to a file API.
- **Sequential Dependent Actions:** Execute a final, often state-changing, API call only after all preceding data collection and processing steps have successfully completed.
## Common Pitfalls
- Failing to handle pagination for listing APIs, leading to incomplete data collection.
- Missing nested API calls when initial list responses only provide identifiers instead of full item details.
- Incorrectly deduplicating items by not considering all relevant fields or by altering data (e.g., sorting lists) that should be treated as-is for uniqueness.
- Generating CSV content manually without using a proper CSV library, leading to incorrect escaping or formatting.
- Executing a final, irreversible action without ensuring all prerequisite data collection and processing steps have successfully completed.
- Not initializing data accumulators before starting collection loops.
