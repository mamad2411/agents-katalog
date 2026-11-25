---
name: chained-data-processing-and-mutation
description: Applies when a task requires processing data through multiple stages, often involving initial aggregation, filtering, and then performing an action based on the refined data.
---
## Overview
This pattern addresses tasks where the final action target is not directly available but must be computed from other data. It involves a sequence of data retrieval, filtering, and aggregation steps, with each milestone building upon the refined output of the previous one, culminating in a final action or mutation.
## When to Apply
- Perform an action on entities derived from a filtered subset of aggregated data.
- Task involves multiple data retrieval, filtering, and aggregation steps before a final action.
- The final action target is not directly available but must be computed from other data.
## Procedure
1. Milestone 1: Initial Data Collection and Aggregation. Identify the primary data source and use a summary API to retrieve a list of primary entities. Implement pagination to ensure all available data is collected. Extract relevant identifiers and summary attributes from each entity, structuring the output to include all necessary identifiers for subsequent milestones.
2. Milestone 2: Detailed Data Fetching, Filtering, and Secondary Entity Aggregation. Load the aggregated identifiers from the previous milestone. Deduplicate these identifiers to avoid redundant API calls. For each unique identifier, call a detail API to retrieve full attributes. Apply filtering criteria based on specific detailed attributes. From the filtered detailed entities, extract and aggregate secondary entities. Deduplicate these secondary entities and structure the output to include all necessary identifiers and attributes for the next milestone.
3. Milestone 3: Action/Mutation. Load the refined list of secondary entities from the previous milestone. Iterate through each entity and call the appropriate action or mutation API using its identifier. For mutation milestones, set the final output 'value' to null and 'answer' to null, as the primary outcome is the side effect.
## Key Patterns
- **Pagination Loop:** When an API returns a paginated list, implement a loop that increments the page index and accumulates results until an empty or partial page indicates the end of the collection.
- **Optimized Detail Fetching:** After initial aggregation, deduplicate identifiers before making detail API calls to avoid redundant fetches for the same entity, improving efficiency.
- **Chained Data Flow with Anticipation:** Each milestone's output must explicitly include all identifiers and attributes required by subsequent milestones, even if not directly used within the current milestone, to ensure a seamless data flow.
- **Filtering on Detailed Attributes:** Filtering logic should be applied only after fetching detailed information for each entity, as summary data often lacks the specific attributes needed for accurate filtering.
## Common Pitfalls
- Failing to implement pagination, leading to incomplete data collection from list-returning APIs.
- Not deduplicating identifiers before making detail API calls, resulting in unnecessary and redundant requests.
- Failing to pass all necessary identifiers and attributes from one milestone's output to the next, breaking the data chain.
- Attempting to apply filtering criteria based on summary data when the required attributes are only available through detailed API calls.
- Not handling API errors (e.g., 'message' in response) or legitimate empty results gracefully, leading to crashes or incorrect assumptions.
- Returning data in the 'value' field for a mutation milestone when the instruction implies a side effect is the primary outcome, and 'value=None' is appropriate.
