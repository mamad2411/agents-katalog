---
name: conditional-data-modification-workflow
description: A multi-step process for conditionally modifying data records, often involving initial data aggregation and subsequent branching logic for updates or creations.
---
## Overview
This skill addresses tasks requiring modification of existing data based on its current state. It typically involves an initial phase of collecting relevant data, often through paginated API calls and filtering, followed by an iterative process where each item's state is evaluated to determine whether to create, update, or skip an action. A key aspect is handling the distinction between creating new records and updating existing ones, which may require re-fetching identifiers.
## When to Apply
- Modify existing records based on their current values.
- Iterate through a collection of items and perform different actions based on each item's properties.
- Update or create records conditionally.
- Process data retrieved from paginated endpoints.
## Procedure
1. Retrieve initial data, potentially from multiple paginated sources, and aggregate relevant identifiers.
2. Filter or intersect the aggregated data to identify the target items for modification.
3. For each target item, retrieve its current state, including any specific identifiers needed for future updates.
4. Iterate through the target items.
5. For each item, apply conditional logic based on its current state:
6. If a condition is met to skip modification, record it as skipped.
7. If a condition is met to create a new record, call the creation API.
8. If a condition is met to update an existing record, ensure the necessary identifier is available (re-fetch if needed) and call the update API.
9. Accumulate results (e.g., lists of updated/skipped items) for a final summary.
## Key Patterns
- **Pagination Loop:** Iteratively call an API with an incrementing page index until an empty result indicates the end of data, aggregating results from all pages.
- **Conditional Action Dispatch:** Use branching logic (if/elif/else) to perform different API calls (create, update, skip) based on an item's attributes or current state.
- **Identifier Re-fetch for Update:** When an update operation requires a specific identifier (e.g., a review ID) that is not available from prior data retrieval steps, perform an additional lookup API call to obtain it before calling the update API.
- **Set-based Filtering/Intersection:** Use sets for efficient identification of common elements or for filtering across multiple data sources.
## Common Pitfalls
- Confusing create and update API calls, leading to errors or unintended behavior.
- Forgetting to handle pagination for APIs that return large datasets, resulting in incomplete data processing.
- Not re-fetching necessary identifiers for update operations, assuming they are always available from prior steps.
- Incorrectly applying conditional logic, leading to unintended modifications or skips.
- Failing to handle null or empty values gracefully when checking conditions, causing runtime errors.
