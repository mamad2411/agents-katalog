---
name: derived-entity-action
description: Applies when an action needs to be performed on a set of entities that are identified through a multi-step filtering and aggregation process from initial data.
---
## Overview
This skill addresses tasks where the target entities for a final action are not directly queryable but must be derived. It outlines a multi-milestone strategy to progressively retrieve, filter, and aggregate data from various sources or through multiple steps. The goal is to narrow down a broad initial dataset to a specific, actionable set of entities.
## When to Apply
- Perform an action on entities that are related to other entities which are themselves filtered by a characteristic and sourced from a collection.
- Identify X based on Y from Z, then perform an action on X.
- The target entities for an action are not directly queryable but must be derived from a larger dataset through filtering and aggregation.
- The task involves multiple levels of data retrieval, filtering, and aggregation to identify the final targets for an action.
## Procedure
1. Retrieve initial collections of primary entities, handling pagination if necessary, and extract relevant identifiers.
2. Consolidate and deduplicate all identifiers for a related sub-entity across the initial collections.
3. For each unique sub-entity identifier, retrieve its detailed attributes using a specific API.
4. Filter these detailed sub-entities based on specified criteria.
5. From the filtered sub-entities, extract and deduplicate a secondary set of related entities (the ultimate targets for the action).
6. Iterate through the final, deduplicated set of secondary entities and perform the required action on each.
## Key Patterns
- **Pagination Loop:** Iteratively call an API with an incrementing page parameter until no more results are returned (e.g., a page returns fewer items than the limit or is empty), accumulating results from each page.
- **Multi-level Deduplication:** Use a set to efficiently store and check for uniqueness of identifiers at multiple stages of data processing (e.g., for sub-entities and then for related entities) to avoid redundant processing or API calls.
- **Conditional Detail Retrieval:** Retrieve detailed information for individual items only after an initial bulk retrieval and deduplication step, and potentially after an initial filtering, to minimize API calls.
- **Reading Prior Milestone Variables:** Access the `prior_variable_values` dictionary to retrieve and utilize data produced and stored by previous milestones, ensuring continuity and data flow across the task.
- **Action Iteration:** Iterate over a final, curated list of entities to perform a specific, singular action on each, often recording the outcome of each individual action.
## Common Pitfalls
- Failing to handle pagination for APIs that return results in pages, leading to incomplete data retrieval.
- Not deduplicating entities at appropriate stages, resulting in redundant API calls, processing, or incorrect aggregation.
- Making detail API calls for all items before any filtering or deduplication, leading to excessive and unnecessary API usage.
- Ignoring or not properly handling error responses from APIs during detail retrieval or action execution.
- Not gracefully handling empty lists or collections at intermediate steps, which can cause runtime errors.
- Confusing entity identifiers with full entity objects when performing deduplication or aggregation.
