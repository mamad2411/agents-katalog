---
name: build-unified-list-from-multiple-sources-then-act
description: Gathers, consolidates, and deduplicates data from multiple disparate sources, potentially using complex retrieval patterns, to construct a unified dataset, then filters this dataset and performs an iterative action on each item.
---
## Overview
This skill addresses tasks requiring the integration of information from disparate data sources, often involving initial searches, detailed retrievals, and subsequent filtering or transformation, culminating in an iterative action based on the consolidated data. It handles common challenges like pagination, data deduplication, and dynamic criteria derivation from the task context.
## When to Apply
- Task requires combining information from multiple distinct data sources.
- Data needs to be filtered or transformed based on criteria derived from the instruction or other data.
- An action needs to be performed iteratively for a subset of consolidated data.
- Data retrieval involves pagination.
- Specific parsing rules for structured text content are implied or explicitly stated.
## Procedure
1. Retrieve initial data from the first source, handling pagination and deduplication if necessary.
2. Retrieve supplementary data from a second source, potentially involving a two-step search-then-fetch process.
3. Parse structured content from one of the retrieved sources using identified delimiters or patterns.
4. Retrieve additional filtering data from a third source, applying dynamic date or keyword criteria.
5. Consolidate and join the retrieved datasets using common keys or derived mappings.
6. Apply exclusion or inclusion filtering to the consolidated data based on criteria from the third source.
7. Iterate through the final filtered dataset and perform the specified action for each item.
## Key Patterns
- **Pagination Loop:** Iteratively call an API with incrementing page indices until an empty result set is returned, accumulating all results into a single list.
- **Multi-Query Data Retrieval:** Querying the same conceptual data type with multiple related parameters (e.g., different relationship types or keywords) and consolidating/deduplicating the results to ensure comprehensive coverage.
- **Two-Step Data Retrieval:** First, search for an identifier (e.g., a note ID) using broad criteria, then use that identifier to fetch detailed content or attributes in a subsequent API call.
- **Dynamic Date Calculation:** Calculating date boundaries (e.g., 'yesterday', 'last week') relative to the `task_datetime_dt` variable for use as API query parameters or filtering criteria.
- **Structured Content Parsing:** Analyzing content examples or plan instructions to identify delimiters and structural patterns (e.g., newlines, specific substrings, character prefixes) for extracting structured data from free-form text.
- **Data Joining/Mapping:** Creating lookup dictionaries (e.g., `attribute_A -> attribute_B`) to link data points from different sources based on common attributes, enabling cross-referencing and consolidation.
- **Set-Based Filtering/Exclusion:** Using sets to efficiently identify and exclude items that are present in a 'blacklist' or 'already processed' list, optimizing filtering operations on consolidated data.
## Common Pitfalls
- Failing to handle pagination, leading to incomplete data retrieval from APIs that return results in pages.
- Incorrectly deriving dynamic criteria (e.g., date ranges, query strings) from the task instruction or context.
- Not accounting for potential data duplication when combining results from multiple queries or sources, leading to redundant processing.
- Errors in parsing structured text due to incorrect delimiter identification, pattern matching, or type conversion.
- Ignoring the need to join or map data from different sources before applying final filters or actions, resulting in disjointed data.
- Not effectively utilizing prior milestone outputs, leading to redundant API calls or missing necessary data for subsequent steps.
