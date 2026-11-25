---
name: multi-source-conditional-action
description: Combines data from multiple sources, filters based on conditions and exclusions, and then performs an action on the filtered subset.
---
## Overview
This skill addresses tasks that involve gathering disparate information from multiple data sources (e.g., entity details, user-generated content, transaction histories). It then processes this information to identify specific entities that meet certain criteria, often by joining data across sources and applying filters, and finally executes an API action on the identified subset, potentially excluding items based on pre-conditions.

## When to Apply
- The task requires gathering information from multiple distinct data sources or systems/APIs.
- A specific action needs to be performed only on a subset of entities based on conditions derived from other data sources.
- Data needs to be joined or correlated across different APIs using common identifiers.
- The task involves reading user-generated content (e.g., notes) and parsing it into structured data.
- The task specifies filtering by relative dates (e.g., 'yesterday', 'last week').
- You need to identify items to exclude based on data from a third source.
- You need to map identifiers across different data sources.

## Procedure
1.  Acquire any necessary credentials for the first data source.
2.  Retrieve a primary set of entities from the first source, handling pagination and accumulating results. Extract relevant identifiers and attributes (e.g., 'first_name', 'email') from each entity for later use.
3.  Acquire any necessary credentials for the second data source.
4.  Retrieve related contextual data from the second source, applying filters (e.g., date, query) and paginating. Search for specific contextual records. Read the full content of identified records and parse it to extract structured data (e.g., key-value pairs).
5.  Acquire any necessary credentials for the third data source (if applicable).
6.  Retrieve exclusion/inclusion criteria data or exclusion candidates from the third source, applying filters (e.g., date, description) and paginating. Filter locally if necessary to identify entities that should be excluded. Extract unique identifiers (e.g., 'email') from these exclusion entities, normalizing them for comparison.
7.  Create lookup structures (e.g., identifier-to-attribute maps) from the initial entity data to facilitate joining.
8.  Map identifiers from the primary entity set to the structured data extracted from the contextual record. Filter the mapped entities by excluding those whose identifiers match the exclusion set.
9.  Iterate through the primary set of entities (or the mapped and filtered set).
10. For each entity, use the lookup structures to find corresponding attributes and check against the exclusion/inclusion criteria.
11. If an entity meets the criteria and is not excluded, perform the specified API action using its extracted attributes (e.g., 'user_email', 'amount', 'description').
12. Collect details of each performed action, including any generated identifiers (e.g., 'payment_request_id'), and report the outcome.

## Key Patterns
-   **Multi-Source Data Join / Cross-Source Data Joining:** Combine data from different API responses (e.g., contacts, notes, transactions) by creating intermediate lookup structures (e.g., identifier-to-attribute map) and using common identifiers (e.g., name, email) to correlate records. Build lookup structures (e.g., dictionaries mapping a common key like `first_name` to a target value like `email`) from one data source to efficiently retrieve corresponding information when iterating through another data source.
-   **Conditional Action Execution / Exclusion Set Construction:** Perform an API action only on a subset of entities after applying filtering logic derived from other data sources (e.g., 'if not already processed'). This often involves iterating through a primary list and checking against an exclusion set. When certain entities need to be excluded from a final action, retrieve and process the exclusion criteria into an efficient lookup structure (e.g., a set of unique identifiers, normalized to lowercase for comparison) to quickly check for membership during the final processing step.
-   **API Response Pagination and Accumulation / Pagination Loop:** When an API returns paginated results, repeatedly call the API with incrementing page indices (or similar parameter) and a fixed page limit, accumulating all results into a single list until an empty page is returned or a page with fewer than `page_limit` items is returned. The `page_limit` should be set to the maximum allowed by the API.
-   **Relative Date Calculation / Date-Based Filtering:** Calculate date parameters (e.g., `min_created_at`) relative to the task's execution time (e.g., 'yesterday', 'last week') to filter API calls. Calculate a dynamic date cutoff (e.g., 'start of yesterday' from `task_datetime_dt`) and filter API results or locally retrieved data based on a `created_at` or similar timestamp field. Ensure the correct date format for API calls or comparison (e.g., 'YYYY-MM-DD').
-   **User Content Parsing / Structured Content Parsing:** Extract structured data from unstructured or semi-structured user-provided text (e.g., note content) by applying string manipulation, splitting, and type conversion rules. Define clear delimiters (e.g., newlines, specific characters like '=>', '$') and parsing rules (e.g., splitting, stripping, type conversion to `int`) to extract structured key-value pairs or lists of data. Specify the exact field path for the content (e.g., `result['content']`).
-   **Credential Acquisition:** Explicitly call a credential API (e.g., `access_token_from`) before making calls to a service that requires it.
-   **Local vs. API Filtering:** Understand if an API's `query` parameter performs exact filtering or relevance ranking. If ranking, retrieve broadly and apply precise filters (e.g., exact string match, date range) locally after data retrieval. If exact filtering is supported, use API parameters directly.
-   **Intermediate Data Structure Definition:** Clearly define the exact structure (e.g., list of dicts, dict of dicts), field names (e.g., 'first_name', 'email'), and data types (e.g., `string`, `int`) for intermediate results passed between milestones to ensure seamless data flow and correct interpretation by subsequent steps.

## Common Pitfalls
-   Failing to paginate and thus missing data when an API returns partial results.
-   Incorrectly joining data across sources due to mismatched identifiers or case sensitivity; always normalize (e.g., to lowercase) for comparison.
-   Not converting exclusion/inclusion lists into efficient lookup structures (e.g., sets) for performance, leading to inefficient O(N*M) lookups.
-   Failing to handle relative date calculations correctly, leading to incorrect time window filtering or incorrect date formatting for API calls.
-   Assuming API responses are always dicts with a 'success' key, instead of checking the actual schema (e.g., direct list return).
-   Not handling empty results from intermediate steps gracefully, leading to downstream errors.
-   Performing actions on entities that should have been excluded based on prior data.
-   Confusing API query parameters (for ranking) with exact filtering, leading to over-retrieval or missed data.
-   Errors in parsing structured content due to incorrect delimiters, type conversions, or missing data.
-   Incorrectly extracting data from API responses by using the wrong field paths (e.g., `response['data'][0]['field']` vs `response['field']`).