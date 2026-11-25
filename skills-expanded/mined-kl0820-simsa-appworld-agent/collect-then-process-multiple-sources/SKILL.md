---
name: collect-then-process-multiple-sources
description: When a task requires finding an extreme value or specific item across multiple data sources, this skill separates data collection from analysis.
---
## Overview
Many tasks require identifying a specific item based on a criterion (e.g., oldest, newest, largest, smallest) from a collection of items. When these items are spread across several distinct sources or endpoints, it's efficient to first gather all relevant data into a unified set. This allows for a single, consolidated analysis step to determine the final answer.
## When to Apply
- Find the [extreme value] from [multiple sources].
- Identify the [specific item] based on a [criterion] across [various collections].
- Aggregate data from disparate locations before performing a calculation or selection.
## Procedure
1. Identify all distinct data sources that need to be queried.
2. For each source, collect all relevant items and their necessary attributes.
3. Consolidate the collected items and attributes into a single dataset.
4. Apply the specified criterion to the consolidated dataset to identify the target item.
5. Extract and return the requested attribute of the target item.
## Key Patterns
- **Data Aggregation Before Analysis:** When a selection or calculation depends on data from multiple distinct sources, collect all necessary data into a single, unified set *before* performing the selection or calculation. This prevents partial results or incorrect comparisons.
- **Two-Phase Operation (Read then Process):** Separate the act of reading/collecting all potential candidates from the act of processing/filtering/selecting the final answer. This allows for independent verification of data collection and simplifies the processing logic.
## Common Pitfalls
- Attempting to compare or select items *before* all data from all sources has been collected.
- Forgetting to collect necessary attributes during the initial collection phase, leading to a need for re-querying.
- Failing to consolidate data from different sources into a consistent format for comparison.
