---
name: paginated-data-enrichment-and-conditional-mutation-with-caching
description: Fetches paginated data, enriches items with details (using caching), and then conditionally performs state-changing mutations, potentially across hierarchical structures.
---
## Overview
Many APIs provide paginated lists of primary entities, but lack full details for each. To perform actions based on these details, a secondary call per entity is often required. This skill outlines how to efficiently retrieve, enrich, filter, and then conditionally modify these entities across multiple steps, often involving hierarchical structures.
## When to Apply
- Retrieve all X and their Y details.
- Filter/remove/update X based on a Y property.
- Process items across multiple collections or libraries.
- Task involves pagination and detail fetching for entities.
- Perform a mutation on a subset of entities identified by a condition.
## Procedure
1. Initialize an empty collection for all primary entities.
2. Iteratively fetch pages of primary entities using a paginated API until no more pages are returned.
3. Accumulate all primary entities from each page into the collection.
4. Initialize a cache for detailed entity properties, potentially pre-populating it from prior milestone outputs.
5. For each primary entity, if its required detail is not in the cache, fetch the full details using a secondary API call.
6. Extract the relevant property from the detailed entity and store it in the cache.
7. Process each primary entity, using its cached details, to determine if it meets a specified condition.
8. Accumulate entities that meet the condition, or structure the output hierarchically with the condition flag.
9. For each accumulated entity (or entity flagged within a hierarchical structure), perform the specified mutation using a dedicated API.
10. Record the results of the mutations for reporting.
## Key Patterns
- **Pagination Loop:** To retrieve all items from a paginated API, repeatedly call the API, incrementing the page index, until an empty page or an explicit end-of-data signal is received.
- **N+1 Detail Fetching:** When a primary listing API provides insufficient details, a secondary API call is made for each item to retrieve additional, necessary properties.
- **Cross-Milestone Caching and Deduplication:** To avoid redundant API calls and improve efficiency, build a cache (e.g., a dictionary mapping entity ID to its details) from previously processed data or prior milestone outputs. Before fetching details for an entity, check if it's already in the cache.
- **Conditional Mutation:** Perform a state-changing operation (e.g., delete, update) only on entities that satisfy a specific, pre-determined condition, often identified by a boolean flag computed in a prior step.
- **Hierarchical Data Processing:** When dealing with nested structures (e.g., collections containing items), iterate through the parent entities and then through their child entities, applying processing and conditions at the appropriate level.
## Common Pitfalls
- Forgetting to paginate, leading to incomplete data retrieval.
- Not handling API errors or empty responses during pagination or detail fetching, causing crashes.
- Redundantly fetching details for the same entity multiple times across different processing steps or milestones when a cache could be used.
- Incorrectly parsing or transforming data (e.g., date strings to years) leading to incorrect conditions.
- Failing to accumulate or report which entities were affected by mutation operations.
- Applying mutation operations without first verifying the condition, leading to unintended changes.
