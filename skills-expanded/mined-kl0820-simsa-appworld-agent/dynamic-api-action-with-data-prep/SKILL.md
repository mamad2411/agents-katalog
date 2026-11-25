---
name: dynamic-api-action-with-data-prep
description: This skill describes how to perform a final action using a dynamically discovered API, after preparing and enriching data from multiple sources, potentially involving pagination.
---
## Overview
This skill addresses scenarios where the exact API method or its parameters for a final action are uncertain, requiring dynamic discovery. It also covers the common need to gather and enrich data from multiple API calls before performing the final action, often involving iterating through paginated results.
## When to Apply
- Perform an action on an item after finding the 'best' one based on some criteria.
- The exact API for the final action is not explicitly known or might vary.
- Data required for the final action needs to be aggregated or enriched from multiple API calls.
- Need to find an item in a paginated list.
## Procedure
1. Obtain necessary authentication credentials (e.g., access token) for the target service.
2. Locate the primary target entity by iterating through a paginated list of entities and matching a specific criterion.
3. Retrieve a collection of sub-entities associated with the primary target.
4. For each sub-entity, enrich its data by making additional API calls if necessary to obtain required attributes (e.g., usage counts).
5. Identify the 'best' sub-entity based on a comparison of the enriched attributes.
6. Dynamically discover the correct API method for the final action by attempting a list of candidate method names.
7. Invoke the discovered API method with the identified 'best' sub-entity, trying various parameter combinations until successful.
8. Construct a structured output detailing the action performed and its results.
## Key Patterns
- **Credential Retrieval:** Securely obtain and use authentication tokens or credentials for API access, often involving a login step or fetching from a credential store.
- **Paginated Search:** Iterate through paginated API results (e.g., using page_index or next_page_token) to find a specific item or collect all items.
- **Data Enrichment (N+1 Query):** For each item in a collection, make an additional API call to retrieve more detailed or missing information that is not available in the initial list response.
- **Dynamic API Discovery:** Attempt to find the correct API method by iterating through a list of potential names using reflection (e.g., getattr) when the exact method name is uncertain.
- **Robust API Invocation:** Try multiple parameter combinations when calling a dynamically discovered API to handle variations in API signatures or required arguments.
- **Max Value Selection:** Iterate through a collection of items to find the one with the highest value for a specific attribute.
## Common Pitfalls
- Not handling pagination correctly, leading to incomplete data or missed target entities.
- Failing to account for missing or null values when extracting data from API responses, causing errors or incorrect comparisons.
- Hardcoding API method names or parameters when they might vary across different versions or implementations of a service.
- Not handling errors gracefully during dynamic API discovery or invocation, leading to unhandled exceptions.
- Making unnecessary N+1 queries when the required data is already available in the initial response, impacting performance.
