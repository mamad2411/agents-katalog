---
name: search-and-extract-from-content
description: Locates a specific document or record via search and extracts structured information from its textual content.
---
## Overview
This skill addresses scenarios where specific information needs to be extracted from the content of a document or record, which itself must first be located through a search. It involves searching, potentially paginating results, filtering to identify the target, retrieving its full content, and then parsing that content.
## When to Apply
- Find a specific document and extract details from its text content
- Locate a record by a query and parse its body for structured data
- Retrieve information embedded within a text field of a searched item
## Procedure
1. Call a search API with a query to find relevant items.
2. If the search results are paginated, iterate through all pages to collect all matching items.
3. Filter the collected items based on a specific attribute (e.g., title, tags) to identify the target item.
4. Use the identifier of the target item to call a detail API to retrieve its full content.
5. Parse the retrieved content string to extract the required information, potentially involving identifying sections, matching patterns, and converting data types.
## Key Patterns
- **Paginated Search:** Iteratively call a search API with pagination parameters (e.g., page_index, page_limit) until an empty page is returned, accumulating all results.
- **Conditional Item Selection:** From a list of search results, select the single item that best matches a specific criterion (e.g., a keyword in its title, a specific tag), often requiring case-insensitive comparison.
- **Content Parsing:** Apply string manipulation, regular expressions, or structured parsing (e.g., splitting by delimiters, identifying key-value pairs) to extract specific data from a text block. The parsing logic must be robust to variations in content format.
## Common Pitfalls
- Not handling pagination, leading to incomplete search results.
- Incorrectly parsing content due to unexpected formats, missing data, or incorrect pattern matching.
- Failing to account for case-insensitivity or partial matches when filtering items.
