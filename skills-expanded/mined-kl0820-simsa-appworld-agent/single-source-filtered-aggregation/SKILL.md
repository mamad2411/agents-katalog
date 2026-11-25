---
name: single-source-filtered-aggregation
description: Aggregates data from a single source after applying multiple filtering conditions, emphasizing efficient single-tool encapsulation when possible.
---
## Overview
This pattern addresses tasks that involve processing a collection of items from a singular data repository. It requires applying multiple selection criteria to identify relevant items, extracting specific attributes, and then performing a summary computation. A key consideration is that the entire process, from data retrieval to final computation, can often be efficiently encapsulated within a single operational step of a single application or tool.

## When to Apply
- The instruction asks for a summary or total of items.
- The items are located within a single, identifiable data source.
- Multiple conditions must be met for an item to be included in the summary.
- Specific data points need to be extracted from each qualifying item for computation.
- All data access, filtering, and computation can be performed efficiently by a single application or tool, allowing for optimized execution.

## Procedure
1. Identify the single data source, all filtering criteria, and the relevant data attribute(s) for aggregation.
2. Access the specified collection of items from the single data source.
3. Apply all specified filtering conditions to the items. This can be done sequentially or simultaneously, depending on the tool's capabilities.
4. For each item that satisfies all conditions, extract the relevant data attribute(s) required for the final computation.
5. Perform the requested aggregation (e.g., sum, count, average) on all extracted data attributes.
6. Return the aggregated result.
   *Consider encapsulating steps 2-5 into a single operational step or milestone if the chosen tool or application supports it, to optimize performance and simplify the plan.*

## Key Patterns
- **Sequential/Multi-Constraint Filtering:** All filtering conditions must be applied to each item before it is considered for data extraction and aggregation. These can be applied sequentially or simultaneously for efficiency.
- **Pre-computation Data Extraction:** The specific data points needed for the final aggregation are extracted only from items that have passed all filtering criteria, minimizing unnecessary data processing.
- **Single Source Iteration:** The entire process operates on a single, pre-identified collection of data, avoiding the need for joins or cross-source lookups.
- **Single Tool Encapsulation:** When all read, filter, and compute operations can be handled by a single tool's capabilities, combine them into one milestone to minimize inter-tool communication overhead and simplify the plan.
- **Direct Aggregation:** Perform the final aggregation or computation directly on the filtered dataset as part of the same operational step, rather than retrieving raw filtered data and then computing.

## Common Pitfalls
- Failing to apply all filtering conditions, leading to an incorrect set of items for aggregation.
- Extracting data before applying all filters, resulting in unnecessary data processing or errors if the data is not present in non-qualifying items.
- Incorrectly identifying the data attribute to be aggregated from the qualifying items.
- Overlooking the need to handle potential errors or missing data during item processing or data extraction.
- Breaking down the task into separate milestones for reading, filtering, and computing, even when a single tool can handle all steps.
- Retrieving raw data without applying filters, leading to unnecessary data transfer and processing.
- Applying filters sequentially in separate steps, rather than combining them for efficiency when a tool supports multi-constraint filtering.
- Failing to recognize that all operations can be performed within a single tool, leading to over-decomposition.