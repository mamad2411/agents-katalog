---
name: conditional-item-mutation
description: Applies conditional updates or creations to a collection of items based on their current state, often requiring prior data and additional lookups.
---
## Overview
This skill addresses scenarios where a list of items needs to be processed, and for each item, a specific action (create or update) is chosen based on its existing attributes. It often involves retrieving additional context (like user credentials) and performing multiple API calls per item to achieve the desired state.
## When to Apply
- Process a list of items from a previous step.
- Perform different actions (e.g., create, update) based on an item's current status.
- Modify existing records or create new ones if they don't exist.
- Ensure a specific state for a collection of entities.
- Update an attribute of an entity that might require first retrieving its specific identifier.
## Procedure
1. Load the list of target items from the previous milestone's output.
2. If required, retrieve any necessary user-specific credentials or identifiers (e.g., user email) that will be used to identify specific records.
3. Iterate through each target item in the loaded list.
4. For each item, evaluate its current state or attributes to determine the appropriate action.
5. Based on the evaluation:
6. a. If a new record needs to be created for the item, call the appropriate creation API with the required parameters.
7. b. If an existing record needs to be updated for the item:
8. i. First, retrieve the specific identifier of the existing record (e.g., a review ID) using a lookup API, potentially filtering by the user-specific credentials obtained earlier.
9. ii. Then, call the appropriate update API with the retrieved record identifier and the new attribute values.
10. Track the count of successfully processed items for summary purposes.
11. Return null as the value, indicating a mutation milestone, along with a summary of the actions taken.
## Key Patterns
- **Conditional Action Dispatch:** Choosing between different API calls (e.g., create vs. update) based on an item's attribute value.
- **Dependent Lookup for Update:** Before updating an item, performing a lookup to retrieve its specific identifier (e.g., review_id) that is not available in the initial item data.
- **Credential/Context Injection:** Using a global or user-specific credential (like user_email) to filter or identify specific records.
- **Mutation Milestone Output:** Explicitly returning null for the value field in the final JSON for mutation milestones, as the primary outcome is a side effect.
## Common Pitfalls
- Not handling both creation and update paths for items based on their initial state.
- Failing to retrieve the specific identifier needed for an update operation when it's not directly available in the input.
- Not using user-specific credentials to filter results when looking up existing records, leading to incorrect updates.
- Incorrectly assuming all necessary data for an update is present in the initial item list from the prior milestone.
- Forgetting to return null for the value field in the final JSON for mutation milestones.
