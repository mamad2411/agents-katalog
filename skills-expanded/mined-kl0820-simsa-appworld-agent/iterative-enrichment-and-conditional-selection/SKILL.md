---
name: iterative-enrichment-and-conditional-selection
description: When a task requires selecting an item from a list based on complex criteria that necessitate multiple API calls per item and potentially fallback logic.
---
## Overview
This skill addresses scenarios where an initial API call provides a list of entities with insufficient detail for selection. It involves iteratively fetching full details for each entity, aggregating specific attributes, and then applying a multi-stage conditional selection process to identify the most suitable item. The selection often depends on a value derived from a prior step.
## When to Apply
- Select an item from a collection based on a calculated property.
- Find an item that meets a minimum threshold, potentially with a fallback.
- Process a list of items where each item requires further detail retrieval to make a decision.
- Perform an action using an item selected after complex data aggregation.
- When a list API provides only summary data, and detail APIs are needed for each item.
## Procedure
1. Retrieve any necessary input parameters or criteria, often from the output of a preceding task.
2. Initialize an empty collection to store enriched entities.
3. Iteratively call the primary API to fetch lists of entities, handling pagination until all available entities are collected.
4. For each entity obtained from the primary API, make a secondary API call to retrieve its complete details.
5. From the detailed entity information, calculate or aggregate the specific metric required for selection.
6. Store the entity along with its calculated metric in the collection.
7. Apply the primary selection logic: iterate through the enriched entities and select the first one that satisfies the main criteria (e.g., meets a minimum threshold).
8. If no entity satisfies the primary criteria, apply fallback selection logic: select the entity that best fits a secondary criterion (e.g., the one with the maximum value of the metric).
9. Perform the final action using the identifier of the selected entity.
## Key Patterns
- **Prior Milestone Variable Access:** Accessing and utilizing structured data (e.g., numerical values) passed from a previous milestone's output.
- **Pagination Loop:** Implementing a loop to repeatedly call a list-fetching API with incrementing page indices until all available items have been retrieved.
- **Iterative Data Enrichment:** For each item obtained from a summary list, making a subsequent API call to retrieve more comprehensive details necessary for decision-making.
- **Data Aggregation for Selection:** Summing or otherwise combining specific attributes from detailed entity data to compute a single metric used for comparison and selection.
- **Multi-stage Conditional Selection:** Employing a prioritized selection strategy where a strict condition is attempted first, followed by a 'best effort' or 'closest match' condition if the strict one is not met.
## Common Pitfalls
- Failing to implement pagination, leading to an incomplete dataset for selection.
- Neglecting to make necessary follow-up API calls to gather sufficient detail for each item, resulting in an inability to apply selection criteria.
- Incorrectly implementing the fallback selection logic, leading to an suboptimal or incorrect choice when the primary condition isn't met.
- Not handling potential errors or empty results from API calls during pagination or detail retrieval.
- Forgetting to convert units or normalize data consistently before comparison.
