---
name: read-extract-act-on-derived-entities
description: Performs an action on a set of entities that are derived or extracted from a primary collection of source items.
---
## Overview
This pattern addresses tasks where the target entities for an action are not directly specified but must be identified by processing a collection of source items. It involves a distinct phase of data collection, extraction, and processing, followed by an iterative action phase on the derived entities. This separation ensures data integrity, efficient processing, and that all necessary targets are identified and prepared before any mutations occur.

## When to Apply
- An action needs to be performed on a set of entities.
- These entities are not directly provided but must be extracted or derived from a larger collection of primary items.
- The action target is a property of a source item or an entity associated with a primary item.
- The action must apply to all such derived entities.
- The source collection might contain multiple instances of the same derived entity, requiring deduplication.

## Procedure
1. Identify and collect all relevant primary items from the specified source.
2. From each primary item, extract the associated secondary entities.
3. Consolidate and deduplicate the extracted entities to form a unique target set.
4. Iterate through the unique target set and perform the specified action on each entity.

## Key Patterns
- **Read-Process-Act Separation:** Separate the milestone for gathering and processing all necessary data from the milestone that performs the final action. This is crucial when the action depends on a complete, processed set of derived data.
- **Derived Entity Dependency:** The action milestone is entirely dependent on the output of the data extraction and consolidation milestone. The target of an action is an entity associated with a primary item, not the primary item itself.
- **Deduplication Before Action:** Always deduplicate the list of extracted entities before performing an iterative action to avoid redundant operations, ensure idempotence, and prevent potential errors.

## Common Pitfalls
- Attempting to perform the action directly while reading or incrementally before the complete set of derived entities is known, leading to complex state management, redundant actions, incomplete results, or missed targets.
- Failing to deduplicate extracted entities, resulting in repeated actions on the same target or errors.
- Not clearly separating the data collection phase from the action phase, making error handling or partial success difficult.
- Attempting to perform the action on primary items instead of the derived entities.
- Not fully collecting all primary items before extracting derived entities, leading to an incomplete target set.