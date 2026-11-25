---
name: single-app-atomic-value-derivation
description: When a task requires reading data from a single application, performing an aggregation, computation, or comparison, and returning a single derived value or extracted attribute.
---
## Overview
This pattern applies to tasks that are self-contained within one application and involve a straightforward data retrieval followed by an aggregation, computation, or comparison to produce a single answer. The key is recognizing when decomposition into separate milestones is unnecessary or counterproductive, as all operations can be efficiently performed within the context of a single application's capabilities or a single, tightly coupled sequence of operations.

## When to Apply
- The task specifies a single application.
- The task asks for a computed, aggregated, or compared value (e.g., "total Y", "average Z").
- The task asks to identify an entity based on a comparison and extract an attribute from it (e.g., "What is the [attribute] of the [most/least] [entity]?", "Find the [entity] with the [highest/lowest] [metric]").
- The task implies a direct read-and-process operation without external dependencies or subsequent actions.

## Procedure
1. Identify the specific data source within the target application or formulate a single query to retrieve all necessary entities and their attributes.
2. Retrieve the necessary data or entities.
3. Perform the specified aggregation, computation, or comparison on the retrieved data to derive the single result or identify the single target entity.
4. If an entity was identified, extract the specified attribute from it. Otherwise, return the single, computed result.

## Key Patterns
- **Atomic Operation Scope:** The entire sequence of data retrieval, processing (aggregation, computation, comparison), and result extraction is treated as a single, indivisible operation within the planner's scope.
- **Single Application Context:** All data and operations are confined to a single application, simplifying data flow and credential management.
- **Implicit Data Dependency Resolution:** The planner implicitly understands the data dependencies (e.g., needing a metric to find a maximum, needing an attribute to return) and bundles them into one step.

## Common Pitfalls
- Unnecessary or over-decomposition into separate "read", "compute", "aggregate", or "extract" milestones when the operations are trivial, tightly coupled, and directly follow the read within a single application.
- Failing to recognize that the task requires a computation or comparison rather than a direct lookup.
- Introducing external dependencies or steps when the task is entirely self-contained within one application.
- Creating intermediate milestones for data processing that can be handled as part of the initial data retrieval or immediate post-processing.