---
name: filter-extract-aggregate-from-collection
description: Applies when a task requires filtering items from a collection based on multiple criteria, extracting specific data from the filtered items, and then performing an aggregation on that data.
---
## Overview
This pattern addresses tasks that involve processing a collection of entities to derive a single aggregated value. It separates the concerns of identifying relevant data and extracting necessary attributes from the final computation, ensuring that filtering and extraction are completed before aggregation.
## When to Apply
- A collection of items needs to be processed.
- Specific items must be selected based on multiple conditions.
- A particular attribute needs to be extracted from the selected items.
- A final summary or total needs to be computed from the extracted attributes.
## Procedure
1. Access the specified collection of items, apply all filtering criteria to identify relevant items, and extract the necessary data points from each identified item.
2. Perform the required aggregation operation (e.g., sum, count, average) on the collection of extracted data points.
3. Return the aggregated result.
## Key Patterns
- **Sequential Filtering and Extraction:** All filtering criteria and data extraction must be completed in a single logical step before any aggregation can occur, ensuring the aggregation operates on the correct, pre-processed dataset.
- **Data Dependency Ordering:** Aggregation steps are strictly dependent on the successful completion of data identification and extraction steps. The output of the extraction phase serves as the direct input for the aggregation phase.
## Common Pitfalls
- Attempting to aggregate data before all filtering criteria have been applied.
- Failing to extract the correct attribute from the filtered items, leading to incorrect aggregation.
- Not handling cases where no items match the filtering criteria.
- Mixing filtering logic with aggregation logic, making the process less modular and harder to debug.
