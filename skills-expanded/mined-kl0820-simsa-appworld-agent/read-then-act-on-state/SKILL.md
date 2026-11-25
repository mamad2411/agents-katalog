---
name: read-then-act-on-state
description: When a task requires performing conditional actions on items based on their current state or attributes, first read the state of all relevant items, then perform the actions.
---
## Overview
Many tasks involve modifying a collection of entities where the modification depends on specific attributes of each entity. This pattern ensures all necessary information is gathered upfront before any irreversible changes are made, allowing for a clear separation of concerns and robust error handling.
## When to Apply
- Arrange items by organizing them based on attributes.
- Move items into sub-directories named after their respective categories.
- Perform actions on items based on their creation date/time.
- Categorize and process items based on specific criteria.
## Procedure
1. Identify the collection of items to be processed.
2. Identify the attributes of each item that determine the action to be taken.
3. Read all relevant items and extract their necessary attributes.
4. For each item, determine the appropriate action based on its extracted attributes.
5. Execute the determined actions, ensuring any required target structures (e.g., subdirectories) are in place.
## Key Patterns
- **Read-Before-Write:** All necessary state information is gathered in a dedicated read step before any modification actions are initiated, preventing partial or incorrect updates.
- **Data-Driven Action:** The specific action taken for each item is dynamically determined by its attributes, which are retrieved in an earlier step.
- **Pre-computation of Targets:** Any target structures (e.g., destination directories) required by the actions are identified or created before the items are moved or modified.
## Common Pitfalls
- Attempting to perform actions and read state concurrently, leading to race conditions or inconsistent data.
- Not gathering all necessary attributes in the initial read, requiring subsequent, inefficient reads.
- Failing to create target structures before attempting to move or place items into them.
- Modifying items without first confirming all conditions are met, leading to irreversible errors.
