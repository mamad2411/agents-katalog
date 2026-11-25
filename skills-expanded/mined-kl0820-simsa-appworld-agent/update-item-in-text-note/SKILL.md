---
name: update-item-in-text-note
description: Describes how to find a specific text-based note, extract its content, modify a particular item within that content, and then update the note with the changes.
---
## Overview
This skill addresses tasks requiring modification of a specific entry within a larger text block stored in a note-like structure. It involves a multi-step process: first locating the correct note, then retrieving its full content, performing a precise string-based update on a target item, and finally persisting the modified content back to the system. This pattern is common for managing lists, statuses, or simple data entries within free-form text fields.
## When to Apply
- Modify a specific item in a note.
- Mark an item as done/undone in a list.
- Update a status within a text field.
- Change a single line or phrase in a document.
## Procedure
1. Search for the target note using available search parameters (e.g., title, tags).
2. If search results are paginated, iterate through pages until the exact target note is found or all pages are exhausted.
3. Retrieve the full content of the identified note using its unique identifier.
4. Identify the specific item or line within the note's content that needs modification.
5. Perform a targeted string replacement or manipulation on the identified item, ensuring other content remains unchanged.
6. Update the note with the modified content using its unique identifier.
## Key Patterns
- **Search and Detail Retrieval:** Locating a specific record often involves a two-step process: first, using a search API to find its identifier based on partial information, and then using a detail API with that identifier to retrieve its full data.
- **Pagination for Search:** When search results might span multiple pages, implement a loop to fetch successive pages until the desired item is found or no more results are available.
- **Targeted String Replacement:** To modify a specific item within a larger text block without affecting other content, use precise string replacement functions, often matching the exact string to be replaced.
- **Cross-Milestone State Transfer:** Information (like an identifier or content) retrieved in an earlier step is stored and reused in subsequent steps to ensure continuity and avoid redundant API calls.
## Common Pitfalls
- Failing to handle pagination when searching for the target note, leading to not finding the note if it's on a later page.
- Using overly broad string replacement that unintentionally modifies other parts of the note's content.
- Not correctly identifying the unique identifier for the note, leading to updates on the wrong record or failed API calls.
- Forgetting to retrieve the full content before attempting to modify it, or modifying an outdated version of the content.
