---
name: find-entity-by-extreme-count
description: This skill applies when the task requires identifying an entity associated with the minimum or maximum count of related items within a collection.
---
## Overview
This pattern addresses tasks that involve analyzing a collection of items to determine which entity has the fewest or most associated instances. It requires retrieving all relevant items, aggregating them by a common attribute, and then identifying the entity corresponding to the extreme (min/max) count.
## When to Apply
- The task asks to identify an entity based on a quantitative extreme (e.g., 'least', 'most', 'fewest', 'highest count').
- The quantitative extreme is derived from counting occurrences of related items.
- The entity to be identified is a grouping key for the items.
## Procedure
1. Retrieve the complete collection of items relevant to the analysis.
2. For each item, identify its associated grouping attribute.
3. Aggregate the items by their grouping attribute, counting the occurrences for each unique attribute value.
4. Identify the grouping attribute that corresponds to the minimum (or maximum) count.
5. Extract and return the specific identifier or name of the identified grouping attribute.
## Key Patterns
- **Aggregation by Key:** Items are grouped by a common attribute, and a count is performed for each group to quantify its associated items.
- **Extreme Value Identification:** After aggregation, the entity corresponding to the minimum or maximum count is selected as the target.
- **Data Dependency Chain:** Each step's output (e.g., raw items, grouped counts) serves as the direct input for the subsequent step, ensuring a clear flow from data retrieval to final result.
## Common Pitfalls
- Failing to retrieve all relevant items before aggregation, leading to incomplete counts.
- Incorrectly identifying the grouping attribute, resulting in skewed or irrelevant counts.
- Confusing the item count with other metrics, or failing to correctly identify the minimum/maximum.
- Not extracting the specific requested attribute (e.g., returning the count instead of the entity's name).
