---
name: single-source-single-value-extraction
description: When a task requires extracting a single, processed value from a single data source, it can be handled in one milestone.
---
## Overview
Tasks that involve querying a single application or data source to derive a specific, singular piece of information often do not require complex multi-step decomposition. If the processing (e.g., filtering, aggregation, transformation) needed to obtain the final value is straightforward and can be performed directly on the data from that single source, the entire operation can be encapsulated within a single milestone.
## When to Apply
- Identify the X of Y from Z.
- What is the A of B in C?
- Find the D that is E in F.
## Procedure
1. Access the specified data source.
2. Perform the necessary processing (e.g., filtering, aggregation, computation) on the data from that source.
3. Extract and return the single requested value.
## Key Patterns
- **Direct Single-Value Derivation:** If the task's objective is to produce a single, specific value that can be directly derived from a single data source through simple processing, the entire derivation process can be contained within one milestone, avoiding unnecessary intermediate steps.
## Common Pitfalls
- Over-decomposing a task into separate read and process steps when the processing is trivial and local to the data source.
- Treating a single-value extraction as requiring iteration or complex state management when it does not.
- Failing to identify that the task's output is a single, derived value, leading to retrieval of raw, un-processed data.
