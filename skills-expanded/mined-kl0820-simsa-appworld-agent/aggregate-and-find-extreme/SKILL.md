---
name: aggregate-and-find-extreme
description: Applies when the task requires aggregating data from multiple API calls and then identifying an item based on an extreme (min/max) aggregated value.
---
## Overview
This skill addresses tasks that involve collecting a potentially large dataset through paginated API calls, processing each item to extract relevant nested information, and then performing an aggregation (like counting occurrences). Finally, it identifies the item that corresponds to the minimum or maximum value of the aggregated data.
## When to Apply
- Instructions asking to find the 'least' or 'most' of something based on counts or sums.
- Tasks requiring processing all available items from a collection that might be paginated.
- When data needs to be grouped or tallied before a final selection.
## Procedure
1. Initialize an empty collection to store aggregated data (e.g., a counter or dictionary).
2. Iteratively call the primary API method, incrementing the page index, until an empty page is returned, indicating no more results.
3. For each item received from the API, extract the relevant nested data points.
4. Update the aggregated data collection based on the extracted data points (e.g., increment counts for each unique entity).
5. After processing all items, check if the aggregated data collection is empty. If so, the result is null.
6. Otherwise, identify the entity with the minimum or maximum aggregated value from the collection.
7. Set the final result to the identifier of this extreme entity.
8. Format the final result into the required output structure.
## Key Patterns
- **Pagination Loop:** Iterate through API calls using a page index parameter, accumulating results until an empty response signals the end of the collection.
- **Nested Data Extraction and Aggregation:** Process each item from the accumulated data, extract values from nested structures (e.g., lists of dictionaries within an item), and use these values to update a counter or dictionary for aggregation.
- **Extreme Value Identification:** After aggregation, use a min() or max() function with a custom key (e.g., a lambda function) to find the item corresponding to the lowest or highest aggregated value.
## Common Pitfalls
- Forgetting to handle the case where no data is returned by the API, leading to errors when trying to find min/max.
- Incorrectly extracting nested data, leading to incomplete or erroneous aggregation.
- Not correctly handling the pagination termination condition, leading to infinite loops or missed data.
- Confusing the key and value when identifying the extreme element from the aggregated data.
