---
name: read-filter-create-populate
description: Applies when a task requires identifying specific items based on multiple criteria, creating a new container for them, and then populating that container with the identified items.
---
## Overview
This skill addresses tasks that involve a multi-stage process: first, gathering and refining a set of entities based on various constraints; second, establishing a new destination entity with specific properties; and finally, transferring the refined set of entities into the newly created destination. It emphasizes precise constraint application at each stage, ensuring all requirements are met through careful API interaction.
## When to Apply
- Identify items based on multiple filtering criteria.
- Create a new entity with a specific name or properties.
- Populate the newly created entity with the identified items.
- The task involves a sequence of reading, creating, and then modifying operations.
## Procedure
1. Identify and retrieve all potential items, then filter them based on all specified criteria (e.g., type, attributes, relationships, timeframes). Crucially, consult relevant API documentation or available options to identify the precise field names, parameter values, and methods required to accurately implement these constraints, thereby avoiding over-inclusion or under-inclusion of items.
2. Create the new destination entity, ensuring its properties (e.g., name, visibility, type) exactly match the task's requirements. Consult relevant API documentation or available options to identify the precise field names, parameter values, and methods required to accurately implement these creation parameters.
3. Add the previously identified and filtered items to the newly created destination entity. Verify that the addition operation correctly handles multiple items and maintains any specified order or properties.
## Key Patterns
- **Read-Filter-Create-Populate Sequence:** Decompose tasks into a clear sequence: first, read and filter source items; second, create the target container; third, populate the target container with the filtered items. This ensures data dependencies are met and operations are atomic.
- **Precise Constraint Translation:** For selection, filtering, or creation, translate all specified constraints (e.g., 'recommended', 'R&B', 'this year', 'new', 'exact name') into the precise API calls, field names, and parameter values. Consult API documentation to avoid over-inclusion, under-inclusion, or incorrect entity creation.
- **Intermediate Data Dependency:** The final action (populating) depends on the output of both the initial filtering step (the items) and the creation step (the destination container). Ensure these intermediate results are correctly passed downstream.
## Common Pitfalls
- Failing to apply all filtering criteria, leading to over-inclusion or under-inclusion of items.
- Creating the destination entity with incorrect properties or an incorrect name.
- Attempting to add items before the destination entity is created.
- Not correctly handling the 'new' constraint for the destination entity, potentially modifying an existing one.
- Incorrectly interpreting temporal constraints (e.g., 'this year') without converting them to concrete values.
