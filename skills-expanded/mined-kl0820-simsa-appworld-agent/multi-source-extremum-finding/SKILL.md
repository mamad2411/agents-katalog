---
name: multi-source-extremum-finding
description: This skill applies when the task requires finding an extreme value (e.g., newest, oldest, highest, lowest) from data aggregated across multiple distinct data sources.
---
## Overview
The structural problem addressed is that the desired extreme value (e.g., newest item) is not available from a single API call or data source. It requires fetching data from several distinct sources, potentially enriching each item with additional details, combining them into a unified dataset, and then performing a comparison or aggregation operation on the combined data to find the specific item that meets the criteria.
## When to Apply
- Find the [extreme property] item from [multiple distinct data sources].
- Compare [property] across [multiple distinct data sources].
- Identify the [max/min] value of [property] from [multiple distinct data sources].
- Combine data from [source A], [source B], and [source C] to find X.
## Procedure
1. Identify all distinct data sources that might contain the relevant items.
2. For each identified data source:
3. Retrieve all items from the source, handling pagination if the API returns paginated results.
4. For each retrieved item, extract its unique identifier, the property to be compared (e.g., date, value), and any other properties required for the final output.
5. If the comparison property is not directly available, perform additional API calls or transformations to obtain it for each item.
6. Accumulate these processed items into a temporary list for the current source.
7. Combine all temporary lists from different sources into a single, master list of items.
8. Deduplicate items in the master list based on their unique identifier to ensure each distinct item is represented only once.
9. Convert the comparison property of each item into a comparable data type (e.g., string date to datetime object).
10. Find the item in the master list that has the extreme value (maximum or minimum) for the comparison property.
11. Extract and return the required output property from the identified extreme item.
## Key Patterns
- **Iterative Data Retrieval (Pagination):** Many APIs return data in pages. A `while True` loop with `page_index` and `page_limit` is a common pattern to retrieve all data, stopping when a page is empty or incomplete, or when the number of items returned is less than the page limit.
- **Multi-Step Data Enrichment:** The initial API call for an item might not contain all necessary fields for comparison or final output. A subsequent API call per item (e.g., fetching details for each song ID) is often required to fetch missing details.
- **Cross-Source Data Aggregation and Deduplication:** Data from multiple distinct sources must be collected and then deduplicated (e.g., using a set of unique identifiers) to form a comprehensive, unique dataset before final processing to avoid redundant entries or skewed results.
- **Robust Data Comparison:** When comparing values like dates or numbers, ensure they are converted to appropriate data types (e.g., `datetime` objects from ISO strings, or numeric types) to guarantee accurate and meaningful comparisons, rather than relying on lexicographical string comparison.
## Common Pitfalls
- Missing pagination for any data source, leading to incomplete results.
- Failing to perform necessary data enrichment steps for items where critical comparison properties are not directly available.
- Incorrectly comparing values (e.g., lexicographical comparison of dates instead of parsing them into comparable objects).
- Not handling cases where a source or the combined dataset might be empty, leading to errors.
- Overlooking the need to deduplicate items that might appear in multiple distinct sources, leading to incorrect counts or skewed extreme value identification.
- Assuming a single API call can retrieve all necessary information across different types of libraries or collections.
