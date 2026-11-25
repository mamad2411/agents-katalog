---
name: multi-step-data-flow-with-external-action
description: Describes the strategy for chaining multiple API calls to retrieve information from various sources, process it, and then use the processed information to perform a final external action.
---
## Overview
This skill addresses tasks that require gathering disparate pieces of information from different systems, often sequentially, and then combining or transforming that information to achieve a specific goal, typically culminating in an external action like sending a message or updating a record. The challenge lies in correctly identifying the necessary data from each step and passing it to subsequent steps.
## When to Apply
- The instruction implies a sequence of data retrieval and processing steps.
- The task requires interacting with multiple distinct data sources or services.
- The final step involves a 'send', 'reply', 'create', or 'update' action using previously gathered data.
- Information from an earlier step is explicitly needed for a later step (e.g., 'using the contact from the previous task').
## Procedure
1. Identify and retrieve a primary target entity (e.g., a contact) using a search API, extracting a key identifier (e.g., phone number).
2. Using the key identifier from the previous step, search for related items (e.g., messages) in another system, applying filters to narrow down to the most relevant item (e.g., latest, incoming). Extract specific content from this item.
3. Using the extracted content as a criterion, search a third data source (e.g., notes). This often involves an initial search for item IDs, followed by individual fetches for full content of each item.
4. Filter and aggregate the items from the third data source that match the criterion, transforming them into the desired format (e.g., a list of strings).
5. Construct the final payload or message using the aggregated data and the key identifier obtained in the first step.
6. Perform the final external action (e.g., sending a message) using the constructed payload and identifier.
## Key Patterns
- **Sequential Data Chaining:** The output or extracted value from one milestone is explicitly used as an input parameter or criterion for an API call in a subsequent milestone, often via `prior_variable_values`.
- **Search and Filter for Specificity:** After an initial broad search API call, iterate through the results to find the *exact* matching item based on specific criteria (e.g., case-insensitive name match, latest timestamp, specific sender/receiver).
- **Pagination Loop for Exhaustive Search:** When an API returns paginated results, implement a loop that increments the `page_index` until an empty page or a page with fewer than `page_limit` items is returned, ensuring all relevant data is collected.
- **Metadata-then-Content Fetch:** Some APIs (e.g., `search_notes`) return only metadata (like IDs and titles) in a list. To get the full content, a subsequent API call (e.g., `show_note`) must be made for each individual item using its ID.
- **Payload Construction:** Before performing a final action, data extracted from multiple sources or processed in various ways must be combined and formatted into a specific structure (e.g., a comma-separated string) required by the target API.
- **Mutation Milestone:** A milestone whose primary objective is to cause a side effect (e.g., sending a message, updating a record) rather than returning a specific data value. The `result` for such milestones is often `None` or a confirmation of the action.
## Common Pitfalls
- Failing to correctly extract the necessary identifier or content from an API response for use in a subsequent step.
- Not handling pagination, leading to incomplete data retrieval if the desired item is not on the first page.
- Incorrectly filtering search results, leading to the selection of the wrong entity or item.
- Assuming a search API returns full content when it only provides metadata, necessitating additional fetch calls.
- Not distinguishing between incoming and outgoing messages or other directional data when filtering.
- Improperly formatting the final payload for the action API, leading to errors or incorrect output.
- Not accounting for edge cases like empty search results or no matching items after filtering.
