---
name: single-pass-collection-extremum-aggregation
description: Applies when a task requires finding an extremum within a collection based on an aggregated property of its sub-elements, followed by a final transformation.
---
## Overview
This pattern addresses tasks that involve iterating through a collection, performing calculations on nested data for each item, identifying an item with an extreme aggregated value, and then applying a final transformation to that value. The key is that all these steps are tightly coupled and can be efficiently handled within a single operational unit, thus not requiring further decomposition by the planner.
## When to Apply
- Find the [extremum property] of my [collection type] based on [aggregated metric].
- What is the [extremum property] of [collection type] after [calculation]?
- Determine the [extremum] item from a list by [complex metric].
## Procedure
1. Identify the primary collection of entities that needs to be iterated over.
2. For each entity in the primary collection, identify the related sub-entities and their properties that contribute to the desired metric.
3. Determine the aggregation function required to compute a single metric for each primary entity from its sub-entities (e.g., sum, average, count).
4. Identify the comparison criterion to find the 'best' (e.g., longest, shortest, largest, smallest) primary entity based on its aggregated metric.
5. Specify any final transformations (e.g., unit conversion, rounding, formatting) to be applied to the metric of the identified 'best' entity.
6. Formulate a single milestone that encapsulates the entire process: listing the primary collection, performing nested aggregation, identifying the extremum, and applying final transformations.
## Key Patterns
- **Nested Data Aggregation:** The requirement to compute a summary statistic (e.g., sum, average, count) from properties of child objects for each parent object in a collection.
- **Extremum Selection:** Identifying a single item from a collection that possesses the maximum or minimum value for a specific calculated metric.
- **Terminal Value Transformation:** Applying one or more final operations (e.g., unit conversion, rounding, formatting) to the selected extremum's value before returning it.
## Common Pitfalls
- Incorrectly defining the aggregation logic for sub-elements.
- Failing to handle empty collections or items with no sub-elements.
- Errors in unit conversion or rounding logic.
- Overlooking edge cases for extremum selection (e.g., multiple items having the same maximum value).
