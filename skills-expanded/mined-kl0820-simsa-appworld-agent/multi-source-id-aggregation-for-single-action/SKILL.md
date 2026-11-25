---
name: multi-source-id-aggregation-for-single-action
description: Aggregates unique identifiers from multiple paginated sources, performing detailed lookups and content parsing, to enable a single, final action based on the collected IDs.
---
## Overview
This pattern addresses tasks requiring information from several distinct data sources, where initial searches might yield only summary data. It involves iteratively retrieving full datasets, dynamically filtering them based on criteria derived from prior steps, potentially parsing complex content, and compiling a unique list of entities before performing a final action.

## When to Apply
- Task requires combining information from different systems or APIs.
- Initial API calls provide only summary data, necessitating follow-up calls for full details.
- Data sources are paginated and an exhaustive search is required.
- Filtering criteria are dynamic and depend on input from previous steps.
- Content within retrieved items needs parsing to extract relevant sub-elements.
- A final action (e.g., sending a message, updating a record) is required based on the aggregated data, often on a collection of unique identifiers.

## Procedure
1. Identify the initial target or context using a search and extract its primary identifier and any relevant contextual criteria.
2. Retrieve an initial collection of high-level entities from a primary data source, handling pagination to ensure exhaustive retrieval.
3. Iterate through the collected high-level entities.
4. For each high-level entity, perform a secondary lookup or nested API call to retrieve its full details or related sub-entities.
5. Apply specified filtering conditions to the detailed items or sub-entities, potentially involving content parsing, case-insensitive matching across multiple fields, or other complex logic.
6. Aggregate the relevant data, specifically collecting unique identifiers if the final action requires them, potentially using a set data structure.
7. Format the aggregated data into the required output structure or string for the final action.
8. Perform a final action using the formatted data or aggregated unique identifiers.

## Key Patterns
- **Exhaustive Pagination:** Iteratively call a listing API with incrementing page indices until an empty or partial page indicates no more data, ensuring all available items are retrieved.
- **Multi-Step Detail Retrieval / Nested Data Retrieval:** Use a search or list API to obtain identifiers or summary information, then make subsequent 'show' or 'get' API calls for each item to retrieve its complete details or sub-entities.
- **Dynamic Filtering and Content Parsing:** Apply filtering criteria derived from previous steps, potentially involving complex string matching (e.g., case-insensitive substring search) across multiple fields and parsing of item content to extract sub-elements.
- **Unique Identifier Aggregation:** Use a set data structure to efficiently collect and ensure uniqueness of identifiers across multiple iterations, especially when a bulk action is intended.
- **Cross-Milestone Data Dependency / Prior Milestone Variable Access:** Utilize outputs (identifiers, criteria, aggregated data) from preceding milestones as inputs for subsequent steps, often accessed via `prior_variable_values`.
- **Output Formatting for Action:** Transform a structured list of results into a specific string format (e.g., comma-separated) required for a final action or submission.
- **Direct Action on Pre-validated Data:** Perform a mutation API call on a list of identifiers without re-validating their existence or properties, assuming prior steps ensured data quality.

## Common Pitfalls
- Not handling pagination exhaustively, leading to incomplete data retrieval or infinite loops.
- Assuming summary data from a list API is sufficient without performing necessary detail lookups.
- Failing to correctly derive or apply dynamic filtering criteria from prior steps, or not accounting for variations in content structure when parsing.
- Not correctly passing and accessing data between milestones, breaking the task flow.
- Forgetting to use a set for aggregation when unique identifiers are required, leading to redundant processing or incorrect results.
- Incorrectly formatting the final output for the intended action or submission.
- Not handling empty results, API response failures, or unexpected structures gracefully at each step of the data aggregation process.
- Attempting to re-validate data that was already processed and validated in previous steps before performing an action, adding unnecessary complexity.