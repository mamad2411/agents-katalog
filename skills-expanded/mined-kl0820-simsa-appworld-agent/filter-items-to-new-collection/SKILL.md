---
name: filter-items-to-new-collection
description: When a task involves identifying a subset of items from a source and placing them into a newly created, named collection.
---
## Overview
This strategy handles tasks that require selecting specific items from a larger set based on multiple conditions, and then organizing these selected items into a new, distinct collection. It ensures the collection is established before items are added, managing the flow of filtered data to its final destination.
## When to Apply
- Instruction specifies filtering items based on multiple attributes.
- Instruction requires creating a new named collection.
- Instruction requires adding the filtered items to the newly created collection.
## Procedure
1. Retrieve and filter source items based on all specified conditions.
2. Create a new collection with the exact specified name.
3. Add all the filtered items to the newly created collection.
## Key Patterns
- **Creation Precedes Population:** A target container must be successfully created and identified before any items can be added to it.
- **Conjunctive Filtering:** Multiple independent criteria are applied simultaneously to narrow down the initial set of items.
- **Intermediate Data Flow:** The output of an initial filtering step serves as the direct input for a subsequent action step.
## Common Pitfalls
- Attempting to populate a collection before it has been successfully created.
- Missing one or more filtering conditions, resulting in an over-inclusive or under-inclusive set of items.
- Failing to use the exact specified name for the new collection.
- Not ensuring that all items meeting the criteria are transferred.
