---
name: chained-information-retrieval-and-response
description: This skill applies when a task requires sequentially retrieving information from multiple sources and then using the aggregated information to perform a final action.
---
## Overview
Many tasks require gathering disparate pieces of information from various APIs before a final action can be taken. This pattern addresses how to chain multiple API calls, where the output of one call (e.g., an identifier or specific data) becomes the input for the next, culminating in a final action that uses all collected data.
## When to Apply
- The task involves obtaining an identifier from one source to query another.
- Information from a previous step is explicitly mentioned as a prerequisite for a current step.
- A search operation returns metadata, and a subsequent call is needed to fetch full content.
- The final action requires data that must be aggregated or processed from multiple prior steps.
- Instructions include phrases like 'read X from Y to obtain Z', 'using Z from previous step, read A from B', or 'reply with Y using Z from previous steps'.
## Procedure
1. Identify the primary entity using a search API. Filter the results to find the specific entity and extract its unique identifier and relevant attributes.
2. Using the identifier from the previous step, search for related transactional or contextual information. Filter these results based on specific criteria (e.g., sender, recency, content) and extract the key data point needed for the next step.
3. With the key data point from the previous step, search a knowledge base or repository. This may involve an initial search for metadata followed by a call to retrieve the full content. Parse and transform the content into the final structured data required for the task's objective.
4. Utilize all gathered and processed information to perform the final, state-changing action, constructing the message or payload as required.
## Key Patterns
- **Chained Information Retrieval:** The output of one API call (e.g., an identifier or specific data point) is directly used as an input parameter for a subsequent API call.
- **Search and In-Memory Filtering:** An API is called to retrieve a list of potential items, which is then programmatically filtered and selected based on specific criteria (e.g., matching a name, sender ID, or recency) within the agent's execution environment.
- **Metadata-Content Split:** An initial API call provides a list of item metadata (e.g., titles, IDs), requiring a second, targeted API call using an item's ID to retrieve its full content.
- **Prior Variable Consumption:** Explicitly reading and utilizing variables stored from previous successful milestone executions as inputs for the current milestone.
- **Robust Response Handling:** Implementing checks for API response shapes (e.g., 'isinstance(result, dict) and "message" in result') to differentiate between successful list results and error/empty dictionary responses.
- **Content Parsing and Transformation:** Extracting raw text content from an API response and programmatically parsing, cleaning, and transforming it into a structured format (e.g., a list of items).
- **Output String Aggregation:** Combining multiple pieces of structured data (e.g., a list of strings) into a single, formatted string suitable for a final output or message.
## Common Pitfalls
- Not handling API responses that indicate no results or an error (e.g., an empty list or an error dictionary) before attempting to process them.
- Failing to correctly identify and extract the unique identifier or critical data point from an API's successful response for use in subsequent calls.
- Incorrectly applying filtering logic to a list of search results, leading to the selection of the wrong item or no item.
- Overlooking the necessity of a second API call to retrieve full content when an initial search API only returns metadata.
- Errors in parsing unstructured text content into the required structured data format.
- Incorrectly formatting the final output string, such as using the wrong delimiter or not handling edge cases (e.g., an empty list).
