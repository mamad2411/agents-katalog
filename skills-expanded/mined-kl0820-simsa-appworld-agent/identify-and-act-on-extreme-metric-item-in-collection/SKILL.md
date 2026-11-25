---
name: identify-and-act-on-extreme-metric-item-in-collection
description: This skill applies when the task requires identifying an item within a collection based on an extreme metric and then performing an action on that identified item.
---
## Overview
This pattern addresses tasks that involve finding a specific resource within a larger collection by first searching for the collection, then iterating through its members to find one that satisfies a certain extreme condition (e.g., maximum or minimum value of an attribute), and finally executing an action on that identified member. It often involves pagination to ensure all members of the collection are considered.
## When to Apply
- Find the item with the highest/lowest X in a collection Y.
- Perform an action on the most/least popular Z from a group.
- Identify a specific resource based on a quantitative attribute and then interact with it.
## Procedure
1. Search for the primary resource collection using a descriptive query.
2. From the search results, identify and select the target collection, applying specific criteria if necessary (e.g., exact name match, or default to the first result).
3. Retrieve all members of the selected collection, handling pagination if the API returns results in pages, and accumulate them into a single list.
4. From the accumulated list of members, identify the single member that exhibits the extreme value (maximum or minimum) for the specified metric.
5. Extract the unique identifier of the identified extreme member.
6. Perform the required action on the identified member using its unique identifier.
7. Construct a summary of the action performed, including relevant details of the identified member.
## Key Patterns
- **Search and Selection:** Initial search results for a collection may require further filtering or selection logic to pinpoint the exact target collection, often prioritizing exact matches or falling back to the first result.
- **Paginated Collection Retrieval:** When retrieving members of a collection, APIs often return results in pages. A loop is required to fetch all pages until an incomplete or empty page signals the end of the collection.
- **Extreme Value Identification:** After collecting all members, use a function (e.g., max() or min() with a key argument) to efficiently find the item with the highest or lowest value for a specific attribute.
- **Inter-Milestone Data Flow:** The output of an earlier milestone (the identified extreme item and its identifier) serves as the direct input for a subsequent action milestone.
## Common Pitfalls
- Failing to handle cases where the initial search yields no results or the target collection cannot be found.
- Incorrectly implementing pagination, leading to incomplete retrieval of collection members or infinite loops.
- Mistakes in the logic for identifying the extreme value, such as using the wrong attribute or incorrect comparison.
- Not correctly extracting the unique identifier from the identified item for the subsequent action.
- Assuming the prior milestone's output structure without validation, leading to errors when accessing its fields.
