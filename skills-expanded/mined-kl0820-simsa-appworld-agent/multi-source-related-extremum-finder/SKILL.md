---
name: multi-source-related-extremum-finder
description: Identifies the item with an extreme attribute value (e.g., newest, smallest) by consolidating data from multiple distinct collections of the same entity type or related entities within a single application, returning an attribute of that item.
---
## Overview
This pattern addresses tasks where the desired output is derived from comparing data points that originate from several different locations or types of collections within the same system. It involves systematically gathering all relevant data from each source before performing a consolidated comparison to identify the extreme value.
## When to Apply
- Instruction asks for an extreme value (e.g., 'newest', 'oldest', 'largest', 'smallest').
- The extreme value needs to be identified from data residing in multiple distinct collections or types of libraries within a single application.
- The final output is a specific attribute of the item with the extreme value, not just the value itself.
## Procedure
1. Identify all distinct data sources within the target application that could contain the relevant items.
2. For each identified source, create a milestone to read all items and extract the attribute needed for comparison (e.g., date, size, count) and the attribute needed for the final output (e.g., title, name).
3. Create a final milestone to combine all collected items, perform the comparison based on the identified attribute, and extract the requested output attribute from the item that satisfies the extreme condition.
## Key Patterns
- **Parallel Data Acquisition:** When data required for a final computation is distributed across several distinct, independently queryable collections within the same application, acquire data from each source in parallel or sequentially in separate milestones before consolidation.
- **Separate Acquisition from Computation:** Isolate the steps of reading and collecting raw data from the step of processing, comparing, or computing the final result, especially when multiple acquisition paths feed into a single computation.
- **Consolidated Extreme Value Search:** When searching for an extreme value across multiple datasets, collect all relevant data points into a single pool before performing the comparison to ensure global extremum identification.
## Common Pitfalls
- Attempting to compare items incrementally without first gathering all potential candidates from all sources.
- Failing to identify all relevant data sources that might contain the extreme value.
- Not extracting all necessary attributes (comparison attribute and output attribute) during the initial data acquisition steps.
- Performing comparisons within each source individually and then trying to combine local extremes, which might miss the global extreme.
