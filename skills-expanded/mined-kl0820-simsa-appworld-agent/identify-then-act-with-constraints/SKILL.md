---
name: identify-then-act-with-constraints
description: Applies when an action needs to be performed on entities that meet specific criteria, requiring an initial data retrieval and filtering step.
---
## Overview
Many tasks require performing an action on a subset of entities. This pattern addresses the need to first identify and filter these target entities based on multiple constraints before executing the action. It ensures that the action is only applied to the correct, pre-qualified targets.
## When to Apply
- An action is specified for a subset of entities.
- The subset is defined by multiple criteria or attributes.
- The criteria require reading data about potential target entities.
## Procedure
1. Retrieve a collection of candidate entities.
2. For each candidate entity, acquire all necessary attributes to evaluate the specified conditions.
3. Filter the collection, retaining only those entities that satisfy all conditions.
4. Execute the primary action on each of the filtered entities.
## Key Patterns
- **Read-then-Act:** The process of identifying and filtering target entities based on criteria is completed before any modifying action is initiated.
- **Pre-filtering with Multiple Constraints:** All conditions and constraints are applied during the initial data acquisition and filtering phase to precisely define the set of entities for the subsequent action.
- **Data Dependency:** The action step is entirely dependent on the output of the identification and filtering step, which provides the specific targets.
## Common Pitfalls
- Interleaving read and write operations when a clear separation is more efficient.
- Not gathering all required data points in the initial read phase to fully evaluate all constraints.
- Applying constraints incorrectly or partially, leading to actions on unqualified entities.
- Proceeding with the action without verifying if any entities met the criteria.
