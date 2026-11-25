---
name: collection-conditional-split-action
description: Manages a collection by retrieving paginated items, identifying specific ones for targeted actions, and applying different conditional or bulk updates to the remaining items, including data transformation and state preservation.
---
## Overview
This skill addresses tasks requiring interaction with a collection of entities that must be retrieved in pages. It covers identifying specific entities within the collection, performing targeted data transformations and updates on them, and then applying different, often bulk, modifications to the remaining items based on conditions or exclusion criteria. This ensures precise control over different subsets of a collection and requires careful data retrieval, filtering, and iterative application of update operations.

## When to Apply
- Retrieve all items from a paginated API.
- Identify specific item(s) within a collection based on attributes.
- Modify an an item's attribute based on its current value, potentially involving data transformation.
- Perform a targeted action on identified items.
- Perform a different, often bulk, update on the remaining items in the collection.
- Apply different actions to different subsets of a collection.
- Perform a bulk update on a collection of items, excluding certain ones.
- Ensure specific attributes are maintained during an update operation to prevent unintended data loss.

## Procedure
1. **Retrieve All Items:** Retrieve all items from the paginated source API, accumulating them into a single list.
2. **Identify and Separate:** Identify the primary target item(s) based on specified criteria (e.g., text matching on a label, ID match). Separate these identified items from the remaining items, storing both the target item(s) and the collection of other items for subsequent steps.
3. **Perform Targeted Action (on identified items):**
    a. Retrieve the specific target item's details (from the separated list).
    b. If data transformation is required, parse relevant attribute(s), perform the transformation (e.g., time calculation), and format the new value.
    c. Call the update API for the specific item, passing its identifier and the transformed attributes. Ensure all necessary attributes (even unchanged ones) are explicitly provided to maintain state and prevent unintended modifications.
4. **Perform Bulk Action (on remaining items):**
    a. Retrieve the collection of other items (the ones not identified as primary targets).
    b. Iterate through each item in this collection.
    c. Apply the specified bulk modification to each item using the appropriate API. This may involve checking exclusion criteria (e.g., its ID does not match a previously identified item's ID) or applying a general update to all remaining items.
    d. *Consider re-retrieving the full list of items from the source before this step if there's a possibility of external changes or if the initial retrieval was not guaranteed to be the most current data.*
5. **Collect Identifiers:** Collect identifiers of all modified items for reporting or further processing.

## Key Patterns
- **Pagination Loop:** Iteratively call a list-retrieval API with page_index and page_limit parameters, accumulating results until an empty or partial page indicates the end of the collection.
- **Conditional Item Identification:** Filter a list of items based on attribute values, often involving case-insensitive string matching, keyword presence checks, or ID comparisons, to find the desired item(s).
- **Inter-Milestone Data Transfer / Prior Milestone Data Access:** Crucial data identified in an early step (e.g., specific item ID, list of other items) must be explicitly stored and passed to subsequent steps (e.g., using `prior_variable_values`) for continuity.
- **Attribute Transformation and Formatting:** Parse an attribute (e.g., a time string), perform a calculation (e.g., adding an hour), and re-format it into the required string representation for an update API.
- **State Preservation in Updates:** Explicitly pass all relevant attributes (even those not changing) to an update API to prevent unintended modifications or defaults, as some APIs may reset unspecified fields.
- **Conditional Bulk Update / Bulk Update Iteration:** Iterate through a collection of items and apply an update action to only those items that meet a specific condition (e.g., not matching an exclusion identifier), or apply a uniform action to all items in the subset.

## Common Pitfalls
- **Incomplete Data Retrieval:** Failing to correctly implement pagination, leading to incomplete data retrieval or infinite loops.
- **Incorrect Item Identification:** Using too broad or too narrow criteria, or not handling case-sensitivity, leading to incorrect identification of target items.
- **Data Transfer Errors:** Forgetting to explicitly store and retrieve necessary data from previous steps, leading to re-fetching or missing information.
- **Data Transformation Errors:** Not handling edge cases in data transformation (e.g., time rollovers, invalid input formats, incorrect parsing/reformatting).
- **Unintended State Changes:** Forgetting to explicitly pass all necessary parameters to an update API, causing unintended changes to other attributes or resetting fields to defaults.
- **Incorrect Action Application:** Accidentally applying a bulk action to the primary target item, or vice-versa, or incorrectly applying exclusion logic during bulk operations.
- **Empty Collection Handling:** Not handling empty collections gracefully, leading to errors if a list is unexpectedly empty.
- **Stale Data:** Failing to re-retrieve the full collection in subsequent steps when the data might have changed externally, leading to updates based on outdated information.