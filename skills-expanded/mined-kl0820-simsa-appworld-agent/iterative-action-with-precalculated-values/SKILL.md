---
name: iterative-action-with-precalculated-values
description: Performs a specific action for multiple entities, where the action's parameters are derived from a combination of sourced entity data and a pre-calculated value.
---
## Overview
This skill addresses tasks requiring an action to be performed on a list of targets, where a common value for the action needs to be computed beforehand. It involves retrieving a list of target entities, extracting a relevant value from a separate source, calculating a per-entity value, and then iterating through the entities to execute the action.
## When to Apply
- When an action needs to be performed for multiple entities.
- When a common value for the action needs to be calculated based on external data.
- When target entities need to be retrieved from a list or contact source.
- When a value needs to be extracted from a file or document.
## Procedure
1. Retrieve a list of target entities, potentially involving pagination and filtering based on specific criteria.
2. Identify and extract a primary numerical value from a specified data source, which may involve searching, filtering by temporal or other attributes, and parsing content.
3. Calculate a per-entity value by combining the primary numerical value with the count of target entities, applying any necessary rounding or adjustments.
4. Iterate through the retrieved target entities, performing the specified action for each, using their unique identifier and the calculated per-entity value, along with any fixed descriptive text.
## Key Patterns
- **Paginated Entity Retrieval:** When retrieving a list of entities, ensure all available entities are collected by repeatedly querying with incrementing page indices until an empty result is returned.
- **Contextual File Search and Parsing:** Locate a specific file by searching a file system with keywords and temporal filters, then parse its content to extract a required numerical value.
- **Derived Value Calculation:** Compute a per-entity value by dividing a total amount by the total number of participants (including the user if applicable) and applying rounding as specified.
- **Iterative Action Execution:** Perform the same API call for each item in a list of entities, using entity-specific data (e.g., email) and a common pre-calculated value.
## Common Pitfalls
- Not handling pagination correctly, leading to an incomplete list of target entities.
- Failing to account for the current user when calculating shared amounts, leading to incorrect per-person values.
- Incorrectly parsing the numerical value from the content, especially with varying formats or missing markers.
- Not handling cases where no target entities or no source value can be found.
- Using hardcoded values instead of dynamically calculating or retrieving them from prior steps.
