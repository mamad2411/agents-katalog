---
name: bulk-delete-by-sender-identifier
description: Deletes multiple items of a specific type from a communication log or similar collection, identified by a sender's identifier.
---
## Overview
This skill addresses the common pattern of identifying and deleting multiple related items from a collection based on a specific sender or source identifier. It typically involves an initial search to gather all potential items, followed by client-side filtering to ensure precise matching, and then iterating through the filtered results to perform individual deletion actions.
## When to Apply
- Instruction specifies deleting 'all X from Y' where Y is a sender/source identifier.
- Task requires cleaning up communication logs or similar collections based on a specific contact or number.
- The goal is to remove multiple items of one or more types originating from a particular entity.
## Procedure
1. Obtain the primary identifier of the sender (e.g., phone number, email address) from the task instruction or a prior step.
2. For each distinct type of item specified for deletion (e.g., text messages, voice messages):
3.   Identify the appropriate API for searching items of this type.
4.   Initiate a paginated search using the sender's primary identifier as a query parameter, if the API supports it.
5.   Accumulate all results from all pages, ensuring to handle potential API errors (e.g., non-list responses) by treating them as empty results for that page.
6.   Iterate through the accumulated items and apply a client-side filter to precisely match the sender's primary identifier (e.g., `item['sender']['identifier_field'] == primary_identifier`). This is critical if the API's search parameter is broad or includes items where the target is not the sender.
7.   From the filtered items, extract their unique deletion identifiers (e.g., `text_message_id`, `voice_message_id`).
8.   Identify the appropriate API for deleting a single item of this type.
9.   Iterate through the collected deletion identifiers and call the single-item deletion API for each, performing the side effect.
10.   Collect the identifiers of all items for which the deletion API was called.
11. Construct and output a summary that includes the count of deleted items for each type and the list of their identifiers.
## Key Patterns
- **Pagination Loop with Accumulation:** When an API returns results in pages, repeatedly call the API with an incrementing page parameter (e.g., `page_index`) and a fixed page size (e.g., `page_limit`) until an empty or short page indicates the end of results. Accumulate all items from all pages into a single list for subsequent processing.
- **Client-Side Exact Match Filtering:** If an API's search parameter might return items that only partially match the target (e.g., a conversation with a number includes both sent and received messages), always perform an explicit client-side filter on a specific field (e.g., `sender.phone_number`) to ensure exact matching of the sender as required by the task.
- **Iterative Deletion of Collected Identifiers:** To perform a bulk deletion, first collect all unique identifiers of the items to be deleted into a list. Then, iterate through this list, calling a single-item deletion API for each identifier.
- **Robust API Response Handling:** When an API is expected to return a list of items, explicitly check if the response is indeed a list (e.g., `isinstance(result, list)`). A non-list response (e.g., a dictionary with an error message) indicates a failure and should be handled gracefully, typically by treating it as an empty result set for that page or call.
## Common Pitfalls
- Not handling pagination, leading to incomplete results and thus incomplete deletion.
- Relying solely on broad API search parameters without client-side filtering, leading to over-deletion of unintended items.
- Failing to check API response types, leading to runtime errors when attempting to iterate over non-list results (e.g., error dictionaries).
- Attempting to delete items without first collecting all identifiers, which can be inefficient or problematic if the underlying data changes during the process.
- Using an intermediate, resolved identifier (e.g., a contact ID) for deletion when the target deletion API expects the original, primary identifier (e.g., a phone number string).
