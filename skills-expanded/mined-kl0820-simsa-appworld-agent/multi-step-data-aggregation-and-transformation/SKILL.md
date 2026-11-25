---
name: multi-step-data-aggregation-and-transformation
description: When a task requires aggregating data from multiple sources or steps and transforming it for a final calculation.
---
## Overview
This skill addresses tasks that involve a multi-stage data processing pipeline: first, retrieving an initial set of high-level entities, then enriching each entity with detailed information through subsequent calls, and finally performing aggregations and transformations to derive a specific answer.
## When to Apply
- When data needs to be retrieved in multiple stages, where initial retrieval provides identifiers for subsequent detailed retrieval.
- When a calculation requires data that is not directly available from a single API call but needs to be derived from multiple calls and aggregations.
- When a task involves finding an extremum (e.g., shortest, longest, highest, lowest) from a collection of processed items.
- When the final output requires specific unit conversion and rounding.
## Procedure
1. Retrieve an initial list of high-level entities, potentially using pagination to ensure all available items are collected.
2. For each entity in the initial list, make a secondary API call to retrieve detailed information.
3. From the detailed information for each entity, extract and aggregate relevant data points.
4. Store the processed data for each entity, including the aggregated values, for subsequent steps.
5. Identify the entity that meets a specific criterion (e.g., minimum or maximum of an aggregated value) from the collection of processed entities.
6. Perform final transformations (e.g., unit conversion, rounding) on the identified entity's aggregated value.
7. Format and return the final result according to the task's requirements.
## Key Patterns
- **Pagination Loop:** Iteratively call an API with an index or offset parameter until no more data is returned, accumulating all results into a single collection.
- **Detail Enrichment Loop:** Iterate through a list of high-level items obtained from an initial API call, and for each item, make a separate API call to retrieve more granular or specific details.
- **Data Aggregation:** Extract specific numerical values from detailed responses and combine them (e.g., summing, averaging) to create a single aggregated value for each entity.
- **Extremum Selection:** From a collection of processed entities, identify the single entity that possesses the minimum or maximum value for a particular attribute.
- **Unit Conversion and Rounding:** Transform a numerical value from one unit to another (e.g., seconds to minutes) and adjust its precision by rounding to the nearest whole number or specified decimal place.
- **Prior Milestone Variable Usage:** Access and utilize the structured data output from a preceding milestone as the primary input for the current processing step, avoiding redundant API calls.
## Common Pitfalls
- Failing to implement correct pagination logic, leading to incomplete data retrieval.
- Not handling cases where detailed API calls return errors, empty data, or malformed responses.
- Incorrectly extracting or aggregating data points from complex nested structures.
- Errors in the logic for identifying the extremum (e.g., minimum or maximum) from a collection.
- Mistakes in unit conversion factors or rounding rules, leading to inaccurate final results.
- Not guarding against empty collections when attempting to find an extremum, which can cause runtime errors.
