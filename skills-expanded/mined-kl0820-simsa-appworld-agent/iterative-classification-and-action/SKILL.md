---
name: iterative-classification-and-action
description: Applies when items need to be categorized based on their attributes and then organized into corresponding target structures.
---
## Overview
This skill addresses tasks requiring the systematic classification of multiple items based on their properties, followed by their organization into distinct, category-specific locations. It involves an initial data gathering and classification phase, a preparation phase for target structures, and a final action phase to move or copy items.
## When to Apply
- Categorize items based on their attributes.
- Organize items into different destinations.
- Process multiple items in a directory or list.
- Create target directories or containers based on categories.
- Move or copy items to specific locations after classification.
## Procedure
1. List initial items from a source location.
2. For each item, retrieve detailed attributes.
3. Apply conditional logic to classify each item based on its attributes.
4. Accumulate classified items with their original details and assigned categories.
5. Identify unique categories from the classification.
6. Create target containers (e.g., directories) for each unique category, ensuring idempotence.
7. Iterate through the accumulated classified items.
8. For each item, construct a destination path using its assigned category and original name.
9. Perform the organizing action (e.g., move, copy) to the constructed destination.
10. Accumulate results of the organizing actions.
## Key Patterns
- **Iterative Detail Retrieval:** List initial items and then make individual API calls for each item to fetch more detailed attributes.
- **Conditional Classification:** Use if/elif/else statements on extracted attributes (e.g., date components, metadata) to assign categories.
- **Structured Data Accumulation for Chaining:** Build a list of dictionaries, where each dictionary represents an item with its original data and newly derived classifications. This output serves as the primary input for subsequent steps/milestones.
- **Idempotent Container Creation:** Create target containers (e.g., directories) with an 'allow_if_exists' flag or similar mechanism to ensure re-run safety and prevent errors if the container already exists.
- **Dynamic Destination Path Construction:** Build destination paths by combining a base path, a category derived from classification, and the original item identifier (e.g., name).
## Common Pitfalls
- Not handling empty initial listings or missing item details gracefully.
- Incorrectly parsing or comparing attribute values (e.g., date/time strings, numerical ranges).
- Failing to use 'allow_if_exists' or similar idempotent options when creating target containers, leading to errors on re-runs.
- Incorrectly constructing destination paths, leading to items being moved to wrong locations or overwritten.
- Not preserving original item identifiers (e.g., names) when moving/copying, leading to loss of identity.
- Failing to accumulate sufficient information in intermediate steps for subsequent milestones to operate effectively.
