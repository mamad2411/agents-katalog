---
name: retrieve-filter-and-perform-conditional-action
description: Retrieves data from one or more sources, filters and combines it based on specific criteria, and then performs a conditional action on the resulting subset of entities.
---
## Overview
This skill addresses multi-step tasks involving data retrieval from one or more sources, processing through filtering and selection, and then executing a specific action using the derived information. It emphasizes chaining API calls, robust filtering, careful data extraction, handling both single and multiple filtered results, and combining information from disparate sources.

## When to Apply
- Perform an action for some entities, but not others.
- Identify entities that meet certain criteria from multiple data sources.
- Combine information from different systems before taking an action.
- Filter out items that have already been processed or handled.
- Retrieve X from Y (potentially multiple Ys).
- Identify a primary target entity from a collection.
- Read Z using X.
- Filter a collection of items based on criteria (including those from a previously identified entity).
- Select one or more specific items from a filtered list (e.g., latest, earliest, highest value, or all matching).
- Perform an action (e.g., reply, send, update, delete) using data derived from previous retrieval and filtering steps.
- Process data from multiple sources.

## Procedure
1.  **Obtain necessary access tokens or credentials** for all involved APIs.
2.  **Retrieve primary data sets:** Call search or list APIs to find initial entities or collections, handling pagination. If identifying a specific target, use generic queries if direct identification is not possible.
3.  **Process initial search results & identify primary target (if applicable):** Guard against empty or error responses. Implement pagination to ensure all potential matches are retrieved. Filter the retrieved entities to precisely identify the target based on specific attributes (e.g., exact name match, unique identifier).
4.  **Extract and enrich primary entity attributes:** Store all relevant attributes of the identified target entity in a structured format for subsequent use.
5.  **Retrieve secondary or related data sets:** Use identifiers from primary entities (or other relevant data) to call list APIs for related items or main collections from one or more sources. Apply any available server-side filters and handle pagination.
6.  **Combine and join data:** Extract relevant identifiers and data points from all retrieved data sets. Combine or join the extracted data using common identifiers (e.g., an email address or a unique ID) to create a unified view of entities and their associated information.
7.  **Filter the combined data:** Apply filtering logic based on specific criteria (e.g., sender, recency, content match, attributes from primary entities). This may involve layered filtering (API-level then in-memory).
8.  **Select relevant item(s):** From the filtered list, select one or more specific items based on defined ordering or selection rules (e.g., latest timestamp, highest value, or all items that match the criteria).
9.  **Extract required content or identifiers:** From the selected item(s), extract necessary data. If summary information was retrieved, call a detail API for each relevant item to get full content. If content is unstructured text, apply text content parsing (string manipulation, splitting, type conversion) based on known patterns.
10. **Prepare the final message or payload:** Combine data from previous steps and format it as required for the action.
11. **Call the final action/mutation API** with the prepared payload and any necessary identifiers.
12. **Handle the response:** For mutation actions, the milestone's output value should typically be 'None' or an empty dictionary, as the primary outcome is the side effect.

## Key Patterns
-   **Paginated Data Retrieval:** When an API returns results in pages, repeatedly call the API with incrementing page indices until an empty page is returned, accumulating all results.
-   **Cross-Source Data Join:** Combine data from different API responses or parsed content using a common identifier (e.g., an email address or a name) to enrich entities or establish relationships.
-   **Conditional Action Execution:** Perform an API action only on entities that satisfy a specific set of conditions derived from combined and filtered data, avoiding redundant or incorrect operations.
-   **Text Content Parsing:** Extract structured data from unstructured text content (e.g., a note body) by applying string manipulation, splitting, and type conversion rules based on known patterns.
-   **Chained Data Retrieval:** Data dependencies between API calls are common; ensure that unique identifiers or necessary parameters extracted from one API response are correctly passed as arguments to subsequent API calls.
-   **Filtering and Selection:** When an API returns a list of potential matches, apply specific filtering criteria (e.g., exact match, substring, recency, sender, attributes from other entities) to select the single correct item or a subset of relevant items. This often involves iterating and conditional checks.
-   **Detail Fetching:** If a search or list API provides only summary information, and detailed content is required for filtering or processing, a subsequent API call to a 'show' or 'get details' endpoint for each relevant item is necessary.
-   **Constructing Action Payloads:** For action-oriented milestones, the final payload (e.g., a message body) is often constructed by combining and formatting data extracted from multiple prior steps, ensuring it meets the target API's requirements.
-   **Mutation Milestone Output:** For milestones that perform a mutation or side effect (e.g., sending a message, updating a record), the 'construct' step should typically produce 'None' or an empty dictionary as its value, as the primary outcome is the side effect of the API call, not a data return.
-   **Entity Enrichment:** When an entity is identified or selected, extract and store all relevant attributes (not just a minimal ID) in a structured format (e.g., dictionary) to maximize its utility for future steps without needing to re-query.
-   **Cross-Milestone Data Flow:** Outputs from earlier milestones (e.g., an identified entity's unique identifier or specific attributes) are critical inputs for subsequent milestones, enabling chained operations.
-   **Layered Filtering:** Combine API-level filtering (if available) with in-memory filtering to efficiently narrow down large datasets to the specific items required. Always perform exact matching on critical identifiers after initial broad searches.

## Common Pitfalls
-   Forgetting to handle pagination, leading to incomplete data.
-   Incorrectly joining data from different sources due to mismatched identifiers or data types.
-   Failing to account for edge cases in filtering logic (e.g., no items to filter, all items filtered out).
-   Not handling potential API errors or empty responses gracefully during data retrieval.
-   Performing actions on entities that should have been excluded by filtering.
-   Incorrectly parsing structured data from text, leading to malformed values or missed entries.
-   Not handling empty search results or API errors gracefully.
-   Failing to extract all necessary fields from an API response, leading to missing data in subsequent steps, or extracting only a minimal identifier instead of all relevant attributes.
-   Incorrectly identifying the unique identifier or join key between different API calls.
-   Applying filtering criteria too broadly or too narrowly, resulting in incorrect item selection, or incorrectly filtering due to case sensitivity, partial matches, or variations in data formats.
-   Forgetting to format data correctly for the final action API (e.g., list to comma-separated string).
-   Confusing input variables from 'prior_variable_values' with intermediate variables constructed within the current milestone.
-   Assuming a search API provides full details, leading to missed 'show_detail' calls.
-   Not distinguishing between incoming and outgoing messages when filtering.
-   Assuming a search or list API will always return a single result, rather than a list that may require further selection.
-   Returning data for a mutation milestone, which can confuse downstream agents about the primary outcome.
-   Not handling scenarios where a search or filter operation yields no results, leading to errors when attempting to access non-existent data.
-   Forgetting to obtain or correctly use access tokens/credentials for each API call.