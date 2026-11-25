---
name: multi-step-content-modification
description: Applies when a task requires finding an entity, retrieving its detailed content, performing line-by-line modifications on that content, and then updating the entity.
---
## Overview
This skill addresses tasks that involve a sequence of operations: first, identifying a target entity through a search mechanism; second, fetching its complete data, particularly its textual content; third, programmatically altering specific parts of this content, often line by line; and finally, persisting these changes back to the system. It's common for checklist-like structures or notes where specific items need to be toggled or edited.
## When to Apply
- Instructions to find an entity by a partial identifier (e.g., title, name).
- Instructions to read or retrieve the full content of an identified entity.
- Instructions to modify specific lines or items within a larger block of text content.
- Instructions to mark an item as done/not done, complete/incomplete, or similar status changes within a list.
- Instructions to update an entity with new or modified content.
## Procedure
1. Use a search API to locate the target entity based on a provided query.
2. From the search results, identify the most relevant entity, typically by matching a specific field (e.g., title) and extract its unique identifier.
3. Utilize the unique identifier to call a retrieval API and fetch the full details of the entity, including its textual content.
4. Access the textual content obtained from the previous step.
5. Split the content into individual lines or segments.
6. Iterate through these lines/segments to find the specific line(s) that need modification, based on a keyword or pattern.
7. Apply the required transformation to the identified line(s) (e.g., replacing a status marker, editing text).
8. Reassemble the modified lines/segments back into a single block of content.
9. Call an update API, passing the entity's unique identifier and the newly constructed content, to persist the changes.
## Key Patterns
- **Search-then-Retrieve:** An initial search API call returns a list of summary objects, from which a specific entity's ID is extracted to make a subsequent call to a detail-retrieval API for its full content.
- **Prior Milestone Data Access:** Data (e.g., entity ID, content) identified and stored in a previous milestone is explicitly retrieved and used as input for subsequent steps.
- **Line-by-Line Content Processing:** Textual content is split into lines, processed iteratively to find and modify specific lines based on content, and then rejoined.
- **Conditional String Replacement:** Within a line of text, specific substrings (e.g., status markers like '[x]') are conditionally replaced with others (e.g., '[ ]') while preserving the rest of the line's content.
## Common Pitfalls
- Failing to handle cases where the search query yields no results or multiple ambiguous results.
- Incorrectly parsing or splitting the content, leading to loss of formatting or data.
- Modifying the wrong line or failing to correctly identify the target line within the content.
- Not preserving the original content of lines that are not targeted for modification.
- Forgetting to reassemble the content correctly before calling the update API.
- Not handling case sensitivity or variations in status markers (e.g., '[x]' vs '[X]').
- Attempting to update without the correct unique identifier for the entity.
