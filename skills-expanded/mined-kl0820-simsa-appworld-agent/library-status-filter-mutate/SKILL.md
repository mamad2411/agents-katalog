---
name: library-status-filter-mutate
description: Filters and mutates items in a library or collection based on their status, which is determined by joining against bulk status indicators.
---
## Overview
This skill addresses tasks requiring the cleanup or modification of a user's library or collection. It involves first reading the entire library and its associated statuses (e.g., liked, downloaded) by making bulk API calls, then filtering items based on these statuses, and finally performing a mutation (like removal) on the filtered subset. The key is to efficiently gather all status information upfront to avoid N+1 API calls.
## When to Apply
- Modify items in a user's library or collection based on specific criteria.
- Determine the status of items (e.g., liked, downloaded, private) across an entire library.
- Remove or update items that do not meet certain conditions.
- The status of an item depends on a property of its sub-items (e.g., an album is downloaded if all its songs are downloaded).
## Procedure
1. Paginate the primary 'show library' API to retrieve all items in the target collection, extracting relevant identifiers and metadata.
2. Paginate any 'show status' APIs (e.g., 'show liked items', 'show downloaded items') to retrieve all identifiers corresponding to each status type.
3. Store the collected status identifiers in efficient lookup structures (e.g., sets).
4. Iterate through the items from the primary library. For each item, determine its status by checking its identifier(s) against the pre-computed status lookup structures. Apply any complex logical conditions for status determination (e.g., 'all sub-items have status X').
5. Construct an intermediate result: a list of dictionaries, where each dictionary represents an item from the library, augmented with its determined statuses.
6. In a subsequent step (or the same if combined), read the intermediate result (or the current list of items with statuses).
7. Filter these items based on the desired criteria for mutation (e.g., 'neither liked nor downloaded').
8. For each item that meets the mutation criteria, call the appropriate 'remove' or 'update' API using its identifier.
9. Collect the identifiers of all mutated items for reporting.
10. Output the list of mutated item identifiers or a confirmation of the mutation.
## Key Patterns
- **Bulk Status Pre-computation:** Instead of querying the status of each item individually, make bulk API calls to retrieve all status indicators (e.g., all liked IDs, all downloaded IDs) and store them in efficient lookup structures (like sets) for quick membership checks.
- **Join by Membership:** After pre-computing bulk statuses, iterate through the main library items and 'join' their status by checking if their identifier exists in the pre-computed status sets, avoiding N individual API calls.
- **Complex Status Aggregation:** When an item's status depends on the status of its constituent sub-items (e.g., an album's downloaded status depends on all its songs being downloaded), use aggregation functions (like 'all()') over the sub-item identifiers against the global sub-item status set.
- **Prior Variable Leverage for Mutation:** For mutation tasks, explicitly read and utilize the rich, pre-processed data (items with their statuses) from a preceding milestone's output, rather than re-fetching or re-computing statuses.
- **Paginated Collection Retrieval:** Always use pagination loops when retrieving collections from APIs to ensure all items are fetched, incrementing 'page_index' until an empty result page is returned.
## Common Pitfalls
- Making individual API calls for each item's status instead of bulk fetching and using sets.
- Forgetting to paginate when retrieving large collections, leading to incomplete data.
- Not leveraging the output of prior milestones, leading to redundant API calls and computation.
- Incorrectly implementing complex status logic (e.g., using 'any()' instead of 'all()' for 'all sub-items' conditions).
- Failing to collect identifiers of mutated items for reporting, making the mutation untraceable.
