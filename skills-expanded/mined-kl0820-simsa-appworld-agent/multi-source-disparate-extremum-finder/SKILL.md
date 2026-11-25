---
name: multi-source-disparate-extremum-finder
description: Finds the item with an extreme attribute value (e.g., oldest, largest) by querying multiple conceptually unrelated and independent data sources within a single application, returning an attribute of that item.
---
## Overview
This strategy addresses tasks that involve querying for an extreme value (e.g., oldest, newest, largest, smallest) where the relevant data is distributed across several distinct collections or libraries within the same application. It separates the data collection from the aggregation and comparison logic, ensuring all necessary information is gathered before processing.
## When to Apply
- The task specifies multiple distinct data sources within a single application.
- The task requires identifying an extremum (e.g., oldest, newest, highest, lowest) of an attribute across these sources.
- The final output is a specific attribute of the item identified as the extremum.
- The data sources are independent and can be queried in parallel or sequentially without interdependencies.
## Procedure
1. For each distinct data source specified, create a milestone to read all relevant items and their required attributes.
2. Create a final milestone to combine the results from all previous read milestones.
3. Within this final milestone, identify the item that satisfies the extremum condition based on the specified attribute.
4. Extract and return the requested attribute from the identified extremum item.
## Key Patterns
- **Parallel Data Collection:** When multiple distinct data sources contribute to a single aggregate result, collect data from each source in separate, independent milestones before any aggregation or comparison.
- **Consolidation and Extremum Finding:** After collecting data from all relevant sources, consolidate the data into a single set. Then, apply the extremum-finding logic (e.g., min/max on a specific attribute) to this combined set.
- **Attribute Projection:** Only retrieve the attributes necessary for comparison and the final output from each source during collection. Avoid fetching unnecessary data.
## Common Pitfalls
- Attempting to find the extremum within each source individually and then comparing those local extrema, potentially missing the global extremum if the comparison logic is flawed or incomplete.
- Failing to collect all necessary attributes (e.g., the comparison attribute and the return attribute) during the initial read steps, leading to a need for re-fetching data.
- Processing data from one source before all sources have been read, leading to an incomplete or incorrect result.
- Confusing distinct data sources with different filtering criteria on a single source.
