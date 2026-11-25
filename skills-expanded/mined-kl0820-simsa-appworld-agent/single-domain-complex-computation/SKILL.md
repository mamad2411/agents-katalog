---
name: single-domain-complex-computation
description: When a task requires a complex computation involving multiple data retrieval, aggregation, and selection steps entirely within a single domain, it can be handled as a single milestone.
---
## Overview
Tasks that involve fetching hierarchical data, performing iterative aggregations, comparative selections, and final transformations, all confined to one application or data source, are often most efficiently executed as a single, comprehensive step. This approach minimizes inter-milestone communication overhead and leverages the sub-agent's capacity for complex, integrated logic.
## When to Apply
- The instruction implies a single application or data source.
- The task requires reading a collection of items and their sub-items.
- The task involves aggregating properties across sub-items.
- The task requires selecting a specific item based on a computed property.
- The final output is a transformed value derived from the selected item.
## Procedure
1. Identify the primary data source or domain for the entire task.
2. Formulate a single milestone that explicitly lists all necessary steps:
3. a. Retrieve all relevant top-level entities.
4. b. For each top-level entity, retrieve its associated sub-entities.
5. c. Compute an aggregate property for each top-level entity based on its sub-entities.
6. d. Identify the specific top-level entity that meets a comparative condition (e.g., "longest", "largest").
7. e. Apply any required transformations (e.g., unit conversion, rounding) to the aggregate property of the identified entity.
8. f. Return the final transformed value.
## Key Patterns
- **Monolithic Execution:** All data retrieval, processing, and final computation steps are grouped into a single milestone when they are tightly coupled and operate within a single domain, avoiding unnecessary intermediate state.
- **Nested Collection Processing:** The process involves iterating through a primary collection, and for each item, iterating through its nested sub-collection to extract and aggregate properties.
- **Comparative Selection:** After computing properties for individual entities, a selection is made across the collection based on a comparative criterion (e.g., "maximum", "minimum").
- **Final Value Transformation:** The selected or computed value undergoes one or more final transformations (e.g., unit conversion, rounding) before being presented as the answer.
## Common Pitfalls
- Over-decomposing the task into separate milestones for each sub-step (e.g., "read all items", "read sub-items", "compute aggregate", "select longest"), which can lead to inefficient execution and complex data passing.
- Failing to recognize that the entire sequence of operations can be handled by a single, capable sub-agent interaction.
- Creating intermediate milestones for data that is only transiently needed for the next immediate computation.
