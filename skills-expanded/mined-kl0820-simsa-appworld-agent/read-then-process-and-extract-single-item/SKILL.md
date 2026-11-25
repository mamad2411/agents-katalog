---
name: read-then-process-and-extract-single-item
description: Applies when a task requires identifying a single item based on a specific criterion from a collection of items, and then extracting a particular attribute from that identified item.
---
## Overview
This skill addresses tasks that involve querying a collection of entities to find one that meets a specific condition, and then returning a particular piece of information about that entity. It separates the initial data retrieval and enrichment from the subsequent processing and extraction steps, ensuring all necessary information is available before making a selection.
## When to Apply
- Identify a single item from a collection based on a criterion.
- Return a specific attribute of the identified item.
- The criterion for selection requires reading an attribute for all items in the collection.
## Procedure
1. Retrieve all relevant entities from the specified source, ensuring all attributes necessary for subsequent processing and extraction are included.
2. From the retrieved entities, identify the single entity that satisfies the specified selection criterion and extract its requested attribute.
## Key Patterns
- **Data Dependency Ordering:** The step that processes and extracts information must always follow the step that retrieves all necessary data, as it depends on the complete dataset.
- **Enrichment Before Selection:** All attributes required for the selection criterion and the final output must be retrieved during the initial data collection phase, even if not directly part of the selection criterion itself.
## Common Pitfalls
- Attempting to filter or select items before all necessary attributes for the criterion have been retrieved.
- Failing to retrieve all attributes required for the final output during the initial data collection.
- Combining data retrieval and complex processing/selection into a single, monolithic step, making it harder to debug or reuse.
