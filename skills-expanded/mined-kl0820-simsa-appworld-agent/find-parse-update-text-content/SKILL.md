---
name: find-parse-update-text-content
description: When the task requires finding a record, parsing its text content, modifying a specific part, and then updating the record.
---
## Overview
This skill addresses tasks that involve locating a specific record, extracting its textual content, performing targeted modifications to that content (e.g., changing a status, updating a specific line), and then persisting the updated content back to the record. It typically involves a search-and-retrieve phase followed by a parse-and-update phase.
## When to Apply
- Find X by Y and modify its Z.
- Update a specific detail within a record's text field.
- Change the status of an item listed in a note/document.
## Procedure
1. Use a search or list API to locate the target record.
2. Select the most relevant record from the search results based on specific criteria.
3. Extract the unique identifier of the selected record.
4. Retrieve the full details of the record, including its textual content, using its identifier.
5. Parse the textual content to identify its constituent parts.
6. Identify the specific segment within the content that requires modification.
7. Apply the necessary changes to the identified content segment.
8. Reassemble the content with the applied modifications.
9. Update the record with the modified textual content using its identifier.
10. Produce a null value as the output for mutation operations.
## Key Patterns
- **Search-then-Get:** First use a listing/search API to find an item's identifier, then use a 'get' API with that identifier to retrieve its full details.
- **Content Line-by-Line Processing:** When modifying text content, it's often processed line by line to isolate and modify specific entries while preserving the rest.
- **Structured Output for Chaining:** When data is needed by subsequent milestones, structure the output as a dictionary containing all necessary identifiers and extracted content.
- **Mutation Output:** For operations that modify state, the output value is typically null or a simple status message.
## Common Pitfalls
- Not handling multiple search results correctly (e.g., not selecting the best match).
- Failing to reconstruct the content correctly after modification, leading to data loss or corruption.
- Incorrectly parsing the content, leading to modifications in unintended places.
- Not passing all necessary identifiers and content from the retrieval phase to the update phase.
- Expecting a data return from a mutation operation.
