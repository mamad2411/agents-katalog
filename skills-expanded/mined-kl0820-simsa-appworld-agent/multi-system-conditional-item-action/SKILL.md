---
name: multi-system-conditional-item-action
description: Use this skill when a task requires integrating data from multiple systems to establish criteria, then conditionally selecting a single item from one system that meets those criteria to perform a final action on that specific item.
---
## Overview
The structural problem involves integrating information from disparate systems, often requiring sequential data retrieval and transformation, to fulfill a complex request. It entails identifying relevant data in one system, extracting specific values, and then using those values to filter or select items in another system before taking a final action.
## When to Apply
- Combine information from multiple data sources to achieve a goal.
- Find an item in one system based on criteria derived from another system.
- Perform an action in a target system using data processed from one or more source systems.
- Ensure a resource meets a specific duration, size, or quantity requirement determined by external data.
## Procedure
1. Search for relevant records in the first system, handling pagination to retrieve all potential matches.
2. Filter the retrieved records based on a specific field's content to identify the primary data source.
3. Extract a unique identifier from the identified primary data source.
4. Retrieve the full content of the primary data source using its identifier.
5. Parse the content to extract a specific, dynamically determined value (e.g., based on current date/time or other context).
6. Retrieve all relevant items from a secondary system, handling pagination.
7. For each item from the secondary system, retrieve associated sub-items or details.
8. Aggregate a specific property (e.g., duration, count) for each item based on its sub-items/details.
9. Store the processed items with their aggregated properties.
10. Compare the dynamically extracted value from the first system with the aggregated properties of items from the secondary system.
11. Select the first item from the secondary system that meets the comparison criteria.
12. Perform a final action in the secondary system using the identifier of the selected item.
## Key Patterns
- **Pagination Loop:** Iteratively call an API with an incrementing page index until an empty or partial page is returned, accumulating results into a single list.
- **Multi-step Data Retrieval & Transformation:** Information from an initial API call (e.g., search results) is used to make a subsequent, more specific API call (e.g., get content), and the result of that is combined with another system's data for a final decision.
- **Content Parsing for Structured Data:** When an API returns unstructured or semi-structured text content, parse it using delimiters (e.g., newlines, specific keywords) to extract specific values.
- **Aggregation of Sub-item Properties:** To determine a property of a parent item (e.g., total duration of a playlist), iterate through its child items (e.g., songs) and sum or aggregate their individual properties.
- **Conditional Selection for Action:** After processing data from multiple sources, iterate through a list of candidates and select the *first* one that satisfies a specific condition derived from previously extracted data, then use its identifier for a final action.
## Common Pitfalls
- Forgetting to implement pagination when an API might return partial results.
- Incorrectly parsing structured text content due to wrong delimiters, case sensitivity, or unexpected formatting.
- Not handling empty search results or cases where no matching data is found gracefully.
- Failing to convert units (e.g., seconds to minutes) when combining or comparing data from different sources.
- Not adhering to the 'first match' or 'best match' criteria when selecting an item, leading to an incorrect choice.
- Ignoring the need to combine data from different systems, treating each system's data in isolation.
