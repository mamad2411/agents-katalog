---
name: find-retrieve-modify-update
description: Locates a target entity by searching its metadata, retrieves its full content, and then performs a targeted modification on that content.
---
## Overview
This skill addresses tasks requiring a two-stage interaction with an external system: first, identifying a specific record or entity using a search or list operation, and second, retrieving its detailed content for modification. The modification involves precise string manipulation within the retrieved content, followed by an update operation to persist the changes.
## When to Apply
- When an instruction requires finding an item by its descriptive attribute (e.g., title, name).
- When the full content of an identified item needs to be retrieved for further processing.
- When a specific part of a text field within a record needs to be altered.
- When changes made to an item's content must be saved back to the system.
## Procedure
1. Call a search or list API with a query to find potential target entities.
2. Iterate through the results to identify the exact target entity based on a specific attribute match (e.g., title, name).
3. Extract the unique identifier of the identified target entity.
4. Call a retrieve API using the extracted identifier to obtain the full content of the target entity.
5. Read the entity's identifier and its full content from the prior milestone's output.
6. Locate the specific substring within the content that needs to be modified.
7. Perform a targeted string replacement or other content manipulation to generate the updated content.
8. Call an update API with the entity's identifier and the newly generated content to persist the changes.
9. Set the output value to null as this is a mutation operation with no specific data to return.
## Key Patterns
- **Search-then-Retrieve Pattern:** When a search or list API provides only metadata or identifiers, a separate retrieve API call is often necessary to fetch the complete details or full content of the identified entity.
- **Targeted String Replacement:** For modifying specific parts of a text field, use precise string matching and replacement to avoid unintended changes to other content within the same field.
- **Mutation Output Handling:** For operations that primarily cause a side effect (e.g., updating a record) and do not produce specific data for subsequent steps, explicitly set the output value to null.
- **Inter-Milestone Variable Passing:** Information (like entity identifiers and retrieved content) obtained in one milestone is frequently required as input for subsequent milestones.
## Common Pitfalls
- Failing to handle cases where the initial search yields no results or multiple ambiguous matches.
- Attempting to modify content directly from a search result when the search API only returns partial data, necessitating a separate retrieve call.
- Using a broad or untargeted string replacement that could inadvertently alter unintended parts of the content.
- Forgetting to invoke the final update API call after local content modifications, leading to unsaved changes.
- Not explicitly setting the output value to null for mutation operations, which can lead to confusion about the expected return type for subsequent steps.
