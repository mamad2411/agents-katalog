---
name: aggregate-filtered-collection-data
description: Aggregates a specific value from multiple items in a collection after filtering them based on their content and metadata.
---
## Overview
This pattern addresses tasks that involve processing a collection of items to extract and aggregate specific information. It systematically lists items, retrieves their detailed content, applies multiple filtering criteria based on both content and metadata, extracts specific numerical data from the filtered items, and finally aggregates this data to produce a single summary value.

## When to Apply
- When a task requires processing multiple items from a specified collection or container (e.g., directory, list).
- When items need to be filtered based on their content or associated metadata.
- When a specific numerical value needs to be extracted from each qualifying item.
- When an aggregation (e.g., sum, count, average) of these extracted values is required.
- When the final output is a single summary value.

## Procedure
1. Call a listing API or method to retrieve a collection of item identifiers or entries from the specified location.
2. Initialize an accumulator variable (e.g., sum, count) to its appropriate default value (e.g., 0 for sum, empty list for average).
3. Iterate through each item identifier or entry obtained from the listing.
4. For each item, call a detail API or method to retrieve its full content and associated metadata.
5. Apply the first set of filtering criteria to the item's content or metadata (e.g., string search, category check). If it doesn't match, skip to the next item.
6. Apply any subsequent filtering criteria to the item's content or metadata (e.g., date range check, numerical threshold). If it doesn't match, skip to the next item.
7. From the content of the filtered item, extract the specific numerical data point required for aggregation.
8. Add the extracted data point to the accumulator variable.
9. After iterating through all items, format the final value of the accumulator variable into the required output structure, handling cases where no items met the filtering criteria (e.g., returning the initialized default value).

## Key Patterns
- **Iterative Detail Retrieval:** After obtaining a list of identifiers from a listing API, iterate through each identifier to call a detail API to fetch comprehensive information for each individual item.
- **Multi-Criteria Filtering:** Apply sequential filtering steps, where an item must satisfy all preceding criteria before being subjected to subsequent checks, combining content-based and metadata-based conditions.
- **Robust Data Extraction:** Extract specific numerical or structured data from potentially unstructured or semi-structured content, handling variations in format (e.g., currency symbols, date formats) and converting to the appropriate data type.
- **Graceful API Failure Handling:** When iterating over API results, explicitly check for and handle individual API call failures (e.g., by skipping the item or treating the result as empty) to prevent process interruption.
- **Default Aggregation Value:** Ensure the aggregation operation returns a sensible default value (e.g., zero for a sum, an empty list, or a specific message) when no items meet the filtering criteria or the collection is empty.

## Common Pitfalls
- Not handling API call failures for either the listing or detail APIs, leading to crashes or incomplete processing.
- Incorrectly parsing dates or numerical values from content, especially with varying formats or missing data, or not using metadata as a fallback.
- Applying filtering criteria in an inefficient order or not combining them logically (e.g., AND vs. OR).
- Failing to initialize the accumulator variable correctly or not handling the edge case where no items match the filtering criteria.
- Overlooking case-insensitivity or partial matches when searching for keywords or categories in content or metadata.