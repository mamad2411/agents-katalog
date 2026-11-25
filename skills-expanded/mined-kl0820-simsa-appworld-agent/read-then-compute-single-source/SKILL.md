---
name: read-then-compute-single-source
description: Separates the comprehensive retrieval of all necessary data from a single source from the subsequent computation, analysis, or selection of that data to produce a final answer.
---
## Overview
This strategy applies when a task involves retrieving a full set of items or records from a single application or data source, followed by an analytical step to derive a specific result from that collected data. It ensures that all necessary information is available before any processing logic is applied, preventing partial or iterative data fetches during the processing phase. The subsequent step then focuses solely on transforming this collected data to fulfill the task's specific requirements.

## When to Apply
- The task requires identifying a specific entity based on a comparative property within a collection (e.g., 'shortest', 'longest', 'most', 'least').
- A computation or aggregation needs to be performed across a set of items from a single application or data source.
- The final answer is derived by processing a complete dataset rather than a direct lookup.
- The final output depends on comparing or analyzing a complete set of entities.
- The instruction specifies a unit conversion or rounding after an aggregation.

## Procedure
1. Identify the single data source from which all necessary information must be retrieved.
2. Create a milestone to retrieve all relevant entities and their associated attributes from this source, ensuring no data required for downstream computation is missed.
3. Create a subsequent milestone to perform all necessary computations, aggregations, filtering, unit conversions, and formatting using the data collected in the previous step, and then return the final result.

## Key Patterns
- **Read-Process Decoupling / Separation of Concerns:** Separate the milestone responsible for acquiring all necessary data from the milestone that performs the analytical or selection logic. The act of retrieving data is distinct from the act of processing or computing with that data, allowing each phase to be independently verifiable and focused.
- **Sequential Data Flow / Data Acquisition First:** Order milestones such that data acquisition precedes data processing, ensuring the processing step has all required inputs from the previous step. All raw data required for the task's computation is gathered in a single, comprehensive initial step before any processing begins.
- **Complete Set for Aggregation:** For tasks involving comparisons or aggregations (e.g., finding minimum/maximum), it's crucial to acquire the entire set of candidates before attempting the comparison.

## Common Pitfalls
- Attempting to perform computations or selections on an incomplete dataset, or before all relevant items have been retrieved, leading to incomplete or incorrect results.
- Over-combining data retrieval and complex processing into a single, opaque milestone, making it harder to debug or verify intermediate steps.
- Failing to explicitly define the complete dataset as the output of the read step and the input for the processing step.
- Failing to retrieve all necessary attributes of an entity during the initial data acquisition, requiring a re-fetch later.
- Not considering the need for unit conversion or specific formatting until the very end, potentially complicating the computation step.