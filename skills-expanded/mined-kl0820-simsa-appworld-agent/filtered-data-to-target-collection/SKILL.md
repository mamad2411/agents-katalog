---
name: filtered-data-to-target-collection
description: Describes the process of collecting data from multiple API calls, enriching and filtering it based on specific criteria, and then using the filtered data to populate a newly created target collection via further API calls.
---
## Overview
This skill addresses tasks requiring the creation of a new collection and populating it with items that meet specific criteria. The initial data often comes from a paginated source, lacks necessary detail for filtering, and requires subsequent API calls for enrichment. The process involves sequential data retrieval, transformation, and then iterative mutation of a newly created target.
## When to Apply
- Instructions to create a new collection (e.g., playlist, album, report) and populate it.
- Instructions to filter items based on criteria not available in a primary listing API.
- Instructions involving paginated data sources.
- Instructions requiring data from a previous step to be used in a subsequent step.
## Procedure
1. Collect all primary records: Use a pagination loop to retrieve all items from the initial listing API.
2. Enrich records with details: For each primary record, call a detail API using its unique identifier to fetch additional attributes required for filtering. Handle potential API call failures or missing data.
3. Filter and transform records: Apply the specified criteria to the enriched records and store the subset that meets all conditions.
4. Create the target collection: Call the API to create the new collection, providing necessary initial parameters. Extract and store the unique identifier of the newly created collection.
5. Populate the target collection: Iterate through the filtered records from step 3. For each record, call the appropriate API to add it to the target collection using its identifier and the target collection's identifier.
## Key Patterns
- **Pagination Loop:** Iteratively call a listing API with incrementing page parameters until an empty result or error indicates no more data.
- **Per-Item Detail Lookup:** After collecting initial records, iterate through them to call a separate detail API for each item to retrieve attributes not present in the initial listing.
- **Cross-Milestone Variable Passing:** Access and utilize identifiers and filtered data generated and stored in previous milestones via `prior_variable_values`.
- **Idempotent Processing / Duplicate Handling:** Use a set to track processed item identifiers to avoid redundant detail lookups or processing of duplicate items, especially when API calls are expensive.
- **Robust API Response Handling:** Check the type and structure of API responses (e.g., `isinstance(result, dict)`, checking for specific keys like 'message') to gracefully handle success, empty results, or errors.
## Common Pitfalls
- Forgetting to implement pagination, leading to incomplete data collection.
- Failing to perform detail lookups when filtering criteria depend on attributes not available in the initial listing API.
- Incorrectly parsing or comparing date/time strings or other complex data types for filtering.
- Not extracting and correctly passing the unique identifier of the newly created target collection to the population step.
- Ignoring API error responses or empty results, leading to unexpected behavior or crashes.
- Making redundant API calls for duplicate items without tracking already processed identifiers.
