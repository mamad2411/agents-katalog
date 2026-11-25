---
name: populate-new-container-with-filtered-items
description: When a task requires populating a newly created container with items filtered from a source.
---
## Overview
This pattern addresses tasks where a new collection or container must be created, and then populated with a subset of items from an existing source. The challenge lies in correctly identifying and filtering the source items, creating the destination, and then linking the filtered items to the new destination.
## When to Apply
- Create a new container and add items to it.
- Filter items from a source based on multiple criteria.
- The target container does not exist initially.
- Items must meet specific conditions before being added.
## Procedure
1. Identify and retrieve the initial set of items from the source.
2. Apply all specified filtering criteria to the retrieved items to obtain the final set of items to be acted upon.
3. Create the new target container with its specified name or properties.
4. Add the filtered set of items to the newly created container.
## Key Patterns
- **Pre-computation of Filtered Set:** All filtering and selection of source items should be completed in a single, initial step to define the exact set of items before any modification actions are taken.
- **Container Pre-creation:** The target container must be created and its identity established before any items can be added to it. This ensures the destination exists when the population step occurs.
- **Data Dependency Ordering:** The step that identifies the items to be moved must precede the step that creates the destination container, and both must precede the step that populates the container.
## Common Pitfalls
- Attempting to add items to a container that has not yet been created.
- Mixing filtering logic with the action of adding items, leading to inefficient or incorrect item selection.
- Not clearly defining the exact set of items to be moved before starting the modification process.
- Failing to correctly interpret dynamic date/time constraints (e.g., 'this year' or 'last year') at the planning stage.
