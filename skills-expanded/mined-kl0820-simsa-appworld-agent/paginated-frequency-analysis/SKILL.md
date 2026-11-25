---
name: paginated-frequency-analysis
description: Identifies the most frequent sub-entity within a paginated list of items, aggregating data across all pages and handling nested entities.
---
## Overview
This pattern addresses tasks that involve fetching data from a paginated API, processing the collected records to count occurrences of specific sub-entities, and then identifying the entity with the highest frequency. It ensures all relevant data is retrieved across all pages before aggregation, especially when items contain nested sub-entities.

## When to Apply
- The task asks to find the 'most popular', 'most frequent', 'most recommended', or 'top' item from a collection.
- Find the most X Y
- Identify the top Z based on frequency
- Count occurrences of A in B
- Process all pages of a list
- The data source is known to be paginated.
- The items to be counted are nested within the primary records.

## Procedure
1. Initialize an empty collection to store all retrieved records and a frequency counter (e.g., a dictionary or map).
2. Repeatedly call the paginated API, incrementing the page offset/index with each call, until an empty page or an explicit end-of-data signal is received.
3. For each successful API response, add its records to the accumulated collection.
4. If the accumulated collection is empty after pagination, return a null result or indicate no entities were found.
5. Iterate through each item in the accumulated collection.
6. For each item, extract the relevant sub-entities (which may be a list of entities nested within the item).
7. Increment the count for each extracted sub-entity in the frequency counter.
8. Identify the sub-entity with the highest count from the frequency counter.
9. Handle edge cases such as multiple entities having the same maximum count (e.g., by picking the first encountered) or no entities being found.
10. Format and return the identifier of the most frequent entity as the final result.

## Key Patterns
- **Pagination Loop:** Continuously call the API with an incrementing page parameter until an empty result set or explicit end-of-data signal is received, accumulating all results.
- **Nested Entity Frequency Counting/Aggregation:** When items contain lists of sub-entities, iterate through both the main items and their sub-entity lists to accurately tally frequencies of individual sub-entities.
- **Max Frequency Identification:** After aggregating counts, iterate through the frequency map to find the key associated with the maximum value, handling potential ties or empty results.

## Common Pitfalls
- Not handling pagination correctly, leading to incomplete data and incorrect frequency counts.
- Failing to iterate through nested lists of entities, resulting in undercounting or incorrect aggregation.
- Incorrectly handling edge cases like no data returned or ties in frequency counts.
- Using an identifier that is not unique across all entities (e.g., using only 'name' when 'id' is also available and more robust for disambiguation).
- Incorrectly identifying the most frequent item, e.g., just counting total items instead of unique sub-entities.