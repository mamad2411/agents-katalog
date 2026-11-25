---
name: conditional-record-upsert
description: When a task requires conditionally updating or creating records based on their existence and specific criteria, often involving fetching details and handling paginated responses.
---
## Overview
This skill addresses scenarios where an agent needs to modify or create data records. It involves first determining if a record already exists for a given entity and user, potentially by fetching and filtering paginated lists of related records. Based on this existence check, the agent either updates an existing record using its identifier or creates a new one.
## When to Apply
- Update X if it exists, otherwise create X.
- Modify records based on a condition.
- Set a property for items, creating it if missing.
- Iterate through a collection and perform an action on each item, which might involve checking for existing related data.
## Procedure
1. Retrieve the primary collection of items to be processed (e.g., from a prior milestone or an initial API call).
2. Obtain any necessary user-specific context (e.g., user identifier).
3. Iterate through each item in the primary collection.
4. For each item, attempt to retrieve existing related records that belong to the current user, handling pagination if the retrieval API returns paginated results.
5. If an existing record is found:
6. Extract its unique identifier.
7. Call the appropriate API to update the record using its identifier and the new value.
8. If no existing record is found:
9. Call the appropriate API to create a new record with the required values.
10. Track the count of successful operations for summary reporting.
## Key Patterns
- **Pagination Loop:** Iteratively call an API with page_index and page_limit parameters until an empty or partial page is returned, aggregating all results into a single collection.
- **Conditional Upsert Logic:** Implement branching execution based on whether a related record exists for a given entity and user, leading to either an update operation (if found) or a create operation (if not found).
- **Filtering Paginated Results for User-Specific Data:** When an API returns a paginated list of records that may belong to various users, iterate through the paginated results and filter to find the specific record associated with the current user's identifier.
- **N+1 Detail Fetch:** After retrieving a list of primary entities, make individual API calls for each entity to fetch additional details that are not available in the initial list response.
- **Cross-API Data Filtering/Joining:** Combine data from multiple API calls (e.g., a list of all items and a list of liked items) to identify a specific subset of items based on criteria that span across these different data sources.
## Common Pitfalls
- Not handling pagination correctly, leading to incomplete data retrieval.
- Failing to correctly identify the user's specific record among multiple records (e.g., reviews by different users) when filtering.
- Incorrectly assuming a record's existence and attempting an update when a create is needed, or vice-versa.
- Not passing the correct unique identifier (e.g., a specific review ID vs. a general item ID) to update or delete APIs.
- Overlooking the need to fetch additional details for items if the initial list API does not provide all necessary fields for subsequent operations.
