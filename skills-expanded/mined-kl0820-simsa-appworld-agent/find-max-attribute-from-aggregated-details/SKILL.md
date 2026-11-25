---
name: find-max-attribute-from-aggregated-details
description: Finds the item with the maximum value for a specific attribute by aggregating identifiers from a paginated list of primary entities and then fetching details for each unique identifier.
---
## Overview
This skill addresses tasks requiring the identification of an extreme value (max/min) among a collection of detailed items. The items themselves are not directly available but must be discovered by first listing primary entities, extracting their associated identifiers, and then fetching individual details for each unique identifier to perform the comparison.
## When to Apply
- Identify the item with the highest/lowest value of a specific property.
- Aggregate data from multiple sources before performing a comparison.
- Process items that are linked via IDs from a primary list.
- Handle paginated API responses for initial data collection.
## Procedure
1. Fetch all primary entities using a paginated API, accumulating results until an empty page is returned.
2. Extract unique detail identifiers from the accumulated primary entities.
3. Initialize a variable to track the extreme comparison value (e.g., maximum or minimum) and another to store the associated display attribute.
4. Iterate through each unique detail identifier.
5. Call the detail fetching API with the current identifier.
6. If the detail fetching API returns a valid response (not an error), extract the comparison attribute and the display attribute.
7. Compare the extracted comparison attribute with the tracked extreme value. If it's a new extreme, update the tracked values.
8. After iterating through all unique detail identifiers, the stored display attribute is the result.
9. Handle the case where no detail identifiers were found or no valid details were processed, returning a default or null value.
## Key Patterns
- **Pagination Loop:** Iterate through API calls with an incrementing page parameter until an empty result set indicates the end of available data, accumulating results from each page.
- **Unique Identifier Aggregation:** Collect identifiers from multiple source objects into a set to ensure each unique item is processed exactly once, preventing redundant API calls and processing.
- **Max/Min Tracking:** Maintain a running maximum or minimum value for a specific attribute, along with an associated identifier or display value, by comparing each new item's attribute against the current extreme.
- **Error Handling for Individual Details:** When fetching details for multiple items, gracefully handle individual errors or missing data for a specific item without failing the entire process, allowing the loop to continue.
## Common Pitfalls
- Not handling pagination correctly, leading to incomplete data.
- Processing duplicate items when identifiers are not unique across sources, leading to redundant API calls or incorrect results.
- Failing to initialize the max/min tracking variables appropriately (e.g., with a value that can never be surpassed/undershot, or with `None` and handling the first valid item).
- Not handling cases where no items are found or all detail fetches fail, leading to an empty or erroneous result.
- Ignoring errors from detail fetching APIs, which might lead to incorrect comparisons or crashes.
- Confusing the comparison attribute with the display attribute for the final output.
