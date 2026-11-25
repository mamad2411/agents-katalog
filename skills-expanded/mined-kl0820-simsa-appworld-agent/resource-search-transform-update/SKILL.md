---
name: resource-search-transform-update
description: This skill describes the process of locating a resource, retrieving its full details, programmatically transforming its content, and then persisting the changes.
---
## Overview
This skill addresses tasks that require a multi-step interaction with a resource. It involves an initial search to identify the target, a subsequent call to retrieve its complete data, an in-memory modification of that data, and finally, an update operation to save the changes back to the system. This pattern is common when the initial search results are insufficient for direct modification.
## When to Apply
- When an item needs to be located by a partial identifier or search query.
- When the initial search results do not contain all necessary details for modification.
- When content within a resource needs to be programmatically altered.
- When changes to a resource need to be saved back to the system.
## Procedure
1. Search for the target resource using available search parameters.
2. Iterate through search results, potentially across multiple pages, to identify the specific resource based on a unique identifier or matching criteria.
3. Extract the unique identifier of the identified resource.
4. Use the unique identifier to retrieve the full details of the resource.
5. Access the relevant content from the retrieved details.
6. Perform the necessary programmatic transformation on the content.
7. Use the unique identifier and the transformed content to update the resource.
## Key Patterns
- **Search and Detail Retrieval Chain:** An initial search API call provides basic identifiers, which are then used in a subsequent detail retrieval API call to get the full resource data.
- **Content-Based Transformation:** The core logic involves modifying a specific part of the retrieved content string based on a defined rule or pattern.
- **Inter-Milestone Data Flow:** Crucial identifiers and content retrieved in an earlier milestone are passed as variables to subsequent milestones for further processing and updates.
- **Conditional Pagination:** Search results are iterated through, and pagination is handled by incrementing a page index until the target is found or no more results are available.
## Common Pitfalls
- Failing to access and reuse data (e.g., identifiers, content) retrieved in previous milestones, leading to redundant API calls or hardcoding values that should be dynamically retrieved.
- Not handling pagination correctly when searching for a resource, potentially missing the target if it's not on the first page.
- Performing string transformations that are too broad or too narrow, leading to unintended changes or failure to modify the correct part of the content.
- Attempting to update a resource without its unique identifier, or with an incorrect identifier.
- Not verifying that the search results actually contain the target resource before attempting to retrieve its details or update it.
