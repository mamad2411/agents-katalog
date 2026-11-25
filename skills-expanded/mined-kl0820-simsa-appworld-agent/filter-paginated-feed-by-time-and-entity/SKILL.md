---
name: filter-paginated-feed-by-time-and-entity
description: Filters a paginated feed of items by time-based criteria and involvement with a set of pre-identified entities.
---
## Overview
This skill addresses the common problem of sifting through a potentially large, paginated stream of data to find specific items that meet both temporal and relational conditions. It involves iterating through pages, applying date-based filters, and matching against a set of known entities using multiple identifiers.
## When to Apply
- Instruction asks to retrieve items from a 'feed' or 'stream'.
- Instruction specifies a time window (e.g., 'yesterday or today', 'last week').
- Instruction specifies involvement with a set of entities identified in a prior step.
- The API for retrieving items is paginated.
## Procedure
1. Retrieve the list of relevant entities from a prior milestone's output.
2. Pre-process the entities to create efficient lookup structures (e.g., sets of identifiers like emails, names).
3. Determine the time window for filtering (e.g., today, yesterday, last N days).
4. Initialize an empty list to accumulate all relevant items.
5. Loop through pages of the feed API:
6. Call the feed API with the current page index and a page limit.
7. If the response is empty or indicates no more data, break the loop.
8. For each item in the current page:
9. Parse the item's timestamp into a comparable date/time object.
10. Check if the item's date/time falls within the defined time window.
11. If it does, check if the item involves any of the pre-processed entities, using the lookup structures. This may involve checking multiple fields (e.g., sender/receiver, email/name).
12. If both time and entity criteria are met, add the item to the accumulator.
13. Construct the final result as a list of selected fields from the accumulated items.
## Key Patterns
- **Prior Variable Lookup:** Accessing and utilizing data produced by a previous milestone.
- **Efficient Entity Matching:** Creating hash sets of entity identifiers (e.g., emails, names) for O(1) average-case lookup during filtering.
- **Date Range Filtering:** Parsing timestamps from items and comparing them against a dynamically determined time window.
- **Paginated Data Accumulation:** Iteratively calling a paginated API and collecting all results until no more pages are available.
- **Multi-field Entity Involvement Check:** Checking multiple fields within an item (e.g., sender, receiver) and multiple identifiers for an entity (e.g., email, name) to determine involvement.
## Common Pitfalls
- Not handling pagination correctly, leading to incomplete data.
- Inefficient entity matching (e.g., linear scan through a list of entities for each item).
- Incorrectly parsing or comparing timestamps, leading to wrong date filtering.
- Missing edge cases for entity involvement (e.g., only checking sender, not receiver; only checking email, not name).
- Failing to handle empty results gracefully.
- Not normalizing string fields (e.g., stripping whitespace, lowercasing) before comparison.
