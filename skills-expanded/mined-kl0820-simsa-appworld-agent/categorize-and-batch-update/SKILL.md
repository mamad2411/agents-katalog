---
name: categorize-and-batch-update
description: Applies when a task requires identifying specific items from a list, categorizing them, and then performing different actions on the identified items versus the remaining ones.
---
## Overview
This skill addresses tasks that involve reading a collection of entities, distinguishing a subset based on specific criteria, and then applying distinct modifications to the identified subset and the remaining entities. It typically involves an initial read operation, followed by filtering and categorization, and then one or more update operations, potentially in a batch.
## When to Apply
- Task requires identifying a specific item or group of items from a larger collection.
- Task requires performing different actions on different subsets of items.
- Task involves reading a list of entities and then modifying some or all of them.
- Task implies a 'find and then act' pattern.
## Procedure
1. Retrieve the full list of entities using a listing API, handling pagination if necessary.
2. Identify the target entity/entities from the retrieved list based on specified criteria (e.g., label, ID).
3. Categorize the remaining entities as 'other' entities.
4. Store the identified target entity's key attributes (e.g., ID, current state) and the list of 'other' entities' key attributes for subsequent steps.
5. Perform the required modification on the target entity, potentially involving data transformation based on its current state.
6. Iterate through the 'other' entities and perform the required modification on each, typically a batch update.
7. Construct a final summary of all actions performed.
## Key Patterns
- **Paginated List Retrieval:** When an API returns a list, assume it might be paginated. Implement a loop to fetch all pages until an empty or partial page indicates the end of the collection.
- **State Preservation Across Milestones:** Crucial data identified or transformed in an earlier milestone (e.g., an entity's ID, its current value, or a list of related entities) must be explicitly stored and passed to subsequent milestones via `prior_variable_values`.
- **Conditional Filtering and Categorization:** Process a retrieved list by applying conditions (e.g., string matching, ID comparison) to identify specific items and separate them from others, creating distinct groups for different subsequent actions.
- **Data Transformation for Update:** Before calling an update API, often the data needs to be transformed from its current state (e.g., parsing a string, performing calculations) into the desired new state or format.
- **Batch Update Iteration:** When an action needs to be applied to multiple items, iterate through a pre-identified list of those items, calling the update API for each one individually.
## Common Pitfalls
- Not handling pagination when retrieving lists, leading to incomplete data.
- Failing to correctly identify or filter the target items from the general collection.
- Not passing necessary data (like IDs or current values) from one milestone to the next.
- Incorrectly applying transformations (e.g., time calculations) before an update.
- Forgetting to iterate and apply actions to *all* items in a batch update, or applying actions to the wrong items.
