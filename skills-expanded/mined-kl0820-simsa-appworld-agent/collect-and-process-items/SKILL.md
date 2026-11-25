---
name: collect-and-process-items
description: Collects a list of items, potentially paginated, and processes each item to extract, transform, or aggregate information, often requiring additional detail fetches.
---
## Overview
This skill addresses tasks requiring the collection of multiple entities from an API, where the initial API call might only provide summary information or be paginated. It involves iterating through the collected items, possibly making further API calls for detailed information on each, and then transforming or aggregating this data into a desired format for subsequent use.
## When to Apply
- Retrieve all X and process their Y
- List all items and calculate a property for each
- Find an item based on a complex condition that requires fetching sub-details
- Aggregate information across multiple entities
- Read content from multiple sources and combine/process it
## Procedure
1. Collect all primary entities: Use a pagination loop (if the API supports it) to retrieve all items from the initial listing API.
2. Iterate through collected entities: Loop over each entity obtained in the previous step.
3. Retrieve detailed information (if necessary): If the initial entity object lacks required details, make a separate API call using the entity's identifier to fetch its complete information.
4. Extract and transform data: From the detailed (or initial) entity information, extract relevant fields, perform calculations, apply transformations (e.g., unit conversion, string parsing), or apply filtering conditions.
5. Aggregate or filter: Combine data points or apply conditions to select specific entities or compute summary statistics.
6. Construct structured output: Create a new data structure (e.g., a dictionary) for the processed entity, containing the extracted, transformed, or aggregated data.
7. Accumulate results: Add the structured output for the current entity to a list that will be the final result of the milestone.
## Key Patterns
- **Pagination Loop:** Iteratively call a list-returning API with an incrementing page parameter until an empty response indicates all items have been retrieved, accumulating results into a single list.
- **N+1 Detail Fetching:** For each item in a collected list, make a subsequent API call to retrieve its full details, often using an identifier obtained from the initial list.
- **Data Transformation:** Converting data from one format or unit to another (e.g., seconds to minutes, string parsing to integer) or extracting specific values from structured text content.
- **Structured Output Generation:** Building a list of dictionaries or objects where each entry represents a processed item with specific, derived fields, suitable for subsequent milestones.
- **Filtering by Metadata/Content:** Selecting specific items from a collection based on conditions applied to their attributes or parsed content, often involving case-insensitive comparisons or keyword matching.
## Common Pitfalls
- Failing to implement pagination, resulting in incomplete data.
- Not handling cases where detail-fetching APIs return errors or null/empty values for specific identifiers.
- Errors in parsing complex string content or converting data types (e.g., from string to integer/float).
- Inefficiently fetching details (e.g., making too many individual API calls when a bulk endpoint might exist, if not explicitly forbidden).
- Incorrectly accumulating or structuring the final output, leading to malformed data for subsequent steps.
