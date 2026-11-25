---
name: paginated-nested-aggregation
description: Processes paginated API responses, aggregates data from nested structures, and identifies the most frequent item.
---
## Overview
This skill addresses tasks requiring the aggregation of data from multiple pages of an API response, where the relevant information is nested within each primary item. It involves iterating through paginated results, accumulating all data, then processing the accumulated data to count occurrences of specific sub-elements, and finally identifying the most frequent one.
## When to Apply
- Instruction requires processing a large collection of items that are returned in pages.
- Instruction requires counting occurrences of sub-items within a collection.
- Instruction asks to find the 'most frequent', 'most popular', or 'top' item based on occurrences.
- API returns a list of objects, where each object contains a list of related sub-objects.
## Procedure
1. Initialize an empty list to accumulate all primary items and a frequency counter (e.g., a dictionary or collections.Counter).
2. Enter a loop to fetch data using a paginated API, incrementing the page index with each iteration.
3. Accumulate the primary items from each page into the main list.
4. Break the pagination loop when an empty page is returned or a page contains fewer items than the specified page limit, indicating the end of the collection.
5. Iterate through the accumulated primary items.
6. For each primary item, iterate through its relevant nested sub-collection.
7. Increment the count for each sub-item's identifier in the frequency counter.
8. After processing all items, check if any data was accumulated; if not, return a null/None result.
9. Otherwise, find the item with the highest count in the frequency counter.
10. Extract the desired identifier (e.g., name, ID) of the most frequent item.
## Key Patterns
- **Pagination Loop with Accumulation:** A 'while True' loop is used to repeatedly call the paginated API. Results from each page are appended to a master list. The loop terminates when an API response is empty or contains fewer items than the page limit, indicating no more data is available.
- **Nested Data Iteration and Frequency Counting:** After accumulating all primary items, a nested loop structure is used: an outer loop iterates through each primary item, and an inner loop iterates through a specific sub-collection within that primary item. A frequency map (e.g., `collections.Counter`) is used to tally occurrences of a specific attribute from the sub-items.
- **Max Item Extraction from Frequency Map:** To find the most frequent item, the `max()` function is applied to the frequency map's items, using a `lambda` function as the `key` to compare based on the count (value) rather than the item identifier (key). The identifier of the maximum item is then extracted.
- **Robust Data Access:** When accessing nested data, use dictionary's `get()` method with a default empty list (e.g., `item.get('key', [])`) to prevent errors if a key might be missing, ensuring the code doesn't crash on malformed or incomplete data.
## Common Pitfalls
- Forgetting to initialize the accumulator list for all items.
- Incorrectly setting pagination termination conditions, leading to infinite loops or incomplete data retrieval.
- Not handling the edge case where the initial API call or subsequent pages return no data.
- Failing to iterate through all relevant sub-items within each primary item.
- Incorrectly accessing nested data, assuming keys always exist without using safe access methods like `dict.get()`.
- Extracting the count of the most frequent item instead of the item's identifier itself.
- Not considering potential performance implications for very large datasets if the accumulation list becomes excessively large.
