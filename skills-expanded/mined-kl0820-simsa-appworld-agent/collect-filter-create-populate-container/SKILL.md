---
name: collect-filter-create-populate-container
description: Collects and filters items from a source, creates a new container, and populates it with the filtered items, often requiring data enrichment.
---
## Overview
This skill addresses tasks that involve a multi-stage process: first, acquiring a collection of raw data, potentially requiring enrichment for complete information. Second, applying specific filtering logic to select relevant items based on multiple criteria. Third, creating a new entity or container. Finally, populating that newly created container with the previously filtered items. This process often involves chaining operations, handling data enrichment, and performing bulk actions.

## When to Apply
- Identify, find, or list items based on multiple criteria.
- Create a new collection, container, playlist, or group.
- Add, populate, or insert items into a newly created container.
- Filter items where initial listing APIs lack sufficient detail, requiring subsequent detail lookups.
- Examples: "Add all X from Y to a new Z playlist," "Create a new [type of collection] with [specific items]," "Filter items based on [criteria] and store them."

## Procedure
1. Paginate through an initial listing API to collect a comprehensive list of primary item identifiers.
2. For each primary item identifier, call a detail or secondary API to fetch comprehensive attributes and enrich the data, if necessary for filtering or display.
3. Apply filtering criteria to the enriched items, selecting only those that match all specified conditions.
4. Extract and store relevant identifiers and attributes from the filtered items for subsequent use.
5. Call a creation API to instantiate a new container entity with a specified name or title.
6. Extract and store the unique identifier of the newly created container.
7. Retrieve the stored identifier of the container and the list of filtered items (e.g., from previous milestones).
8. Iterate through the filtered items. For each item, call an 'add' API, using the container's identifier and the item's identifier, to populate the container.

## Key Patterns
- **Pagination Loop:** Iteratively call a list-fetching API with an incrementing page parameter until an empty result set indicates no more data, ensuring comprehensive data collection.
- **Data Enrichment via Secondary Call:** When initial list items lack necessary filtering or display attributes, perform a secondary API call for each item to retrieve full details.
- **Multi-Criteria Filtering:** Filtering often requires combining conditions across different attributes, sometimes after data transformation (e.g., parsing dates or case-insensitive comparison).
- **Chained Identifiers:** Store and retrieve key identifiers (like the container ID) and filtered data structures from prior milestones to chain operations across multiple steps.
- **Bulk Item Addition:** After identifying a collection of items and a target container, a loop is used to add each item individually to the container via a dedicated API.
- **Mutation Milestone Output:** For actions that primarily cause side effects (e.g., adding items), the milestone's output value can be null, with success indicated by the absence of errors.

## Common Pitfalls
- Failing to handle pagination correctly, leading to incomplete data collection.
- Not identifying the need for data enrichment when initial API responses lack required filtering attributes.
- Not performing detail lookups when filtering criteria are not available in the initial list.
- Incorrectly parsing, comparing, or converting data types (e.g., dates, case-sensitivity) before applying filters.
- Failing to extract and pass the newly created container's ID to subsequent steps.
- Attempting to add items to a container before it has been successfully created.
- Assuming a single API call can add multiple items, when an iterative approach is required.
- Failing to iterate through all filtered items when populating the container.