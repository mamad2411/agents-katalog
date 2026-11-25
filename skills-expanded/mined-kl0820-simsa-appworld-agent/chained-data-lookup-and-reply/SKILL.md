---
name: chained-data-lookup-and-reply
description: This skill applies when a task requires retrieving information from multiple distinct sources, potentially involving iterative searches or parsing, to construct a final response.
---
## Overview
Many tasks require combining data from several distinct API calls or data sources. This often involves an initial search to identify a target entity, using that entity's identifier to retrieve related information, and then processing or transforming that information before performing a final action or constructing a response.
## When to Apply
- Retrieve information from multiple systems.
- Combine data from different sources.
- Find an entity and then use its details for a subsequent action.
- Respond to a request using data from a separate storage system.
- Iterate through search results to find a specific item.
- Parse semi-structured text content.
## Procedure
1. Identify the primary target entity using a search function, potentially requiring iterative or broad searches if the initial attempt is too specific.
2. Extract necessary identifiers or attributes from the identified primary target.
3. Using an identifier from the primary target, search for related contextual information or requests.
4. Filter and select the most relevant contextual information, extracting its content.
5. Using keywords or context from the extracted request, search a secondary data source for relevant data entries.
6. Retrieve the full content of the identified data entry.
7. Parse and transform the content of the data entry into the desired structured format.
8. Construct the final response message or payload using the transformed data.
9. Perform the final action (e.g., send a message, update a record) using the primary target's identifier and the constructed response.
## Key Patterns
- **Iterative Search with Pagination:** When an initial search yields no results, broaden the search query and iterate through paginated results until the target is found or all pages are exhausted.
- **List Filtering and Selection:** After retrieving a list of potential items, iterate through them to apply specific criteria (e.g., attribute matching, recency) to select the single most relevant item.
- **Chained Data Dependency:** Information extracted from an earlier API call (e.g., an identifier) is crucial input for subsequent API calls to retrieve related or more detailed data.
- **Semi-structured Content Parsing:** When retrieving free-form text content, apply string manipulation (e.g., splitting by delimiters, checking keywords, stripping whitespace) to extract structured data.
- **Robust API Response Handling:** Anticipate and handle different API response shapes, such as error dictionaries versus expected data lists, to prevent runtime errors and ensure graceful fallback.
## Common Pitfalls
- Not handling pagination or broad searches when initial specific searches fail.
- Failing to filter results correctly, e.g., picking the wrong contact or message.
- Not extracting the correct identifier from an initial API call for subsequent calls.
- Assuming a single API call provides all necessary data.
- Incorrectly parsing semi-structured text, leading to missing or malformed data.
- Not handling empty or error responses from APIs gracefully.
- Forgetting to format the final output as specified (e.g., comma-separated).
