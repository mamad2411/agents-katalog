---
name: find-and-update-content-item
description: This skill applies when the task requires locating a specific record by a partial identifier, retrieving its full content, modifying a specific part of that content, and then persisting the updated content.
---
## Overview
Many systems store structured data within free-form text fields. This pattern addresses the common need to programmatically locate such a record, extract its text, perform a precise, targeted modification to a specific line or item within that text, and then save the updated text back to the record. It involves a search-and-retrieve phase followed by a modify-and-update phase.
## When to Apply
- Find X and update Y within its content.
- Locate a record by its name and modify a specific detail in its description.
- Mark an item as done in a list stored in a note.
- Change a specific setting within a configuration file stored as text.
## Procedure
1. Call a search API with a query derived from the target's partial identifier.
2. Iterate through the search results to find the exact target record, potentially handling pagination.
3. Extract the unique identifier of the target record.
4. Call a retrieval API using the extracted unique identifier to get the full details of the record.
5. Extract the specific content field that needs modification.
6. Perform a precise string replacement or manipulation on the extracted content to update only the desired item, leaving other parts untouched.
7. Call an update API using the unique identifier and the modified content.
8. Confirm the update operation was successful.
## Key Patterns
- **Targeted Search and Selection:** The initial search might return multiple results or partial matches. The plan must include logic to iterate and select the exact target based on a specific field (e.g., title, name), potentially with a fallback strategy.
- **Identifier Chaining:** An identifier obtained from a search or list API call is crucial for subsequent detailed retrieval and update operations.
- **Precise Content Manipulation:** When modifying text content, the change must be surgical, affecting only the specified item or line, not altering formatting or other unrelated items. This often involves `replace()` with exact string matching.
- **Mutation Milestone:** The final step is a mutation, meaning the primary output is the side effect of the API call, and the `value` returned to the user is typically `null`.
## Common Pitfalls
- Not handling pagination during the initial search, leading to missing the target record if it's on a later page.
- Incorrectly identifying the target record due to loose matching criteria or not iterating through all search results.
- Performing a broad or incorrect string replacement that inadvertently modifies unintended parts of the content.
- Failing to extract and reuse the unique identifier between retrieval and update steps.
- Not confirming the existence of the item to be modified within the content before attempting replacement.
