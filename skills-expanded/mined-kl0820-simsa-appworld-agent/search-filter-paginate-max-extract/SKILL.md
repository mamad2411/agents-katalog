---
name: search-filter-paginate-max-extract
description: Finds a primary entity by a query, retrieves all its associated secondary entities via pagination, and extracts an attribute from the secondary entity with the highest value for a specified metric.
---
## Overview
This skill addresses tasks requiring the identification of a specific primary entity from a search, followed by the comprehensive retrieval of all its related secondary entities. It then involves processing this collection to pinpoint the secondary entity that maximizes a particular metric, ultimately extracting a specific piece of information from it. This pattern is crucial for tasks that involve aggregation and selection across related data sets.
## When to Apply
- The instruction requires finding a specific primary entity using a descriptive string.
- The primary entity has a collection of associated secondary entities that must all be retrieved.
- The goal is to identify a secondary entity based on the maximum (or minimum) value of one of its attributes.
- The final output is a specific attribute of the identified secondary entity.
## Procedure
1. Initiate a search for the primary entity using the provided query string.
2. From the search results, filter to precisely identify the target primary entity based on a specific attribute (e.g., exact name match). Extract its unique identifier.
3. If the target primary entity is not found, terminate the process and indicate no result.
4. Using the extracted identifier, repeatedly call the API to retrieve all associated secondary entities. Implement pagination to ensure all available items are collected into a single list.
5. If no secondary entities are found after collection, terminate the process and indicate no result.
6. From the collected list of secondary entities, identify the single entity that possesses the maximum value for a specified metric attribute.
7. Extract the desired output attribute from this identified secondary entity.
8. Format and return the extracted attribute as the final result.
## Key Patterns
- **Search and Exact Filter:** When a search API returns multiple potential matches, a subsequent filtering step is often required to pinpoint the exact target entity based on a precise attribute match (e.g., case-insensitive name equality).
- **Dependent ID Retrieval:** Information (like an identifier) obtained from one API call is frequently a required parameter for a subsequent API call to retrieve related or more detailed data.
- **Full Collection Pagination:** To ensure all related items are processed, an API that returns lists of items must be called iteratively with pagination parameters (e.g., page_index, page_limit) until a page returns fewer items than the limit or an empty list, indicating the end of the collection.
- **Max Value Object Selection:** To find an object within a list that has the highest (or lowest) value for a specific attribute, iterate through the list and compare values, or use built-in functions designed for this purpose.
- **Graceful Empty Result Handling:** At multiple stages (initial search, related entity retrieval, max value identification), it's crucial to check if any results were found and handle empty lists or null values gracefully to prevent errors and provide meaningful output.
## Common Pitfalls
- Failing to implement complete pagination, leading to an incomplete set of secondary entities and potentially an incorrect maximum value.
- Not performing an exact match filter on search results, leading to processing data for the wrong primary entity.
- Ignoring edge cases where no primary entity is found, or no secondary entities are associated with the primary entity.
- Incorrectly extracting the identifier from the primary entity or the final attribute from the selected secondary entity.
- Assuming a single API call will return all necessary data without considering pagination or dependent calls.
