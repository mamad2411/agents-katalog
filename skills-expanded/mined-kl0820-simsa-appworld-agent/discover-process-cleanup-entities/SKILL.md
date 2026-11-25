---
name: discover-process-cleanup-entities
description: When a task requires identifying multiple entities, performing an action on each, and then cleaning up the original entities.
---
## Overview
This pattern addresses tasks that involve a three-stage process: first, discovering a set of target entities based on specific criteria; second, performing a primary operation on each of these entities; and third, performing a cleanup or secondary operation on the original entities, often involving their removal. This ensures that all targets are correctly identified before any modifications, and cleanup only occurs after the primary action is complete for all targets.
## When to Apply
- Process items within a source location and then remove the originals.
- Identify multiple entities based on a pattern, act on them, then delete the source entities.
- A task involves a discovery phase, an action phase, and a cleanup phase on the discovered items.
## Procedure
1. Identify all target entities within a specified source location, applying any necessary exclusion criteria.
2. For each identified target entity, perform the primary action, potentially creating new artifacts in a separate destination.
3. After all primary actions are completed, delete the original target entities from the source location.
## Key Patterns
- **Discovery First:** All target entities must be identified and listed before any modification or action is taken on them, to ensure a complete and consistent set.
- **Action Before Cleanup:** Destructive operations on source entities must be deferred until after all primary actions have successfully completed for all targets.
- **Exclusion Filtering:** When identifying targets, explicitly filter out any entities that match the general pattern but should not be processed or are destination locations.
## Common Pitfalls
- Deleting source entities before ensuring all primary actions are complete.
- Processing entities that should have been excluded.
- Failing to identify all target entities in the initial discovery phase.
- Mixing discovery, action, and cleanup into a single, monolithic step, leading to potential race conditions or incomplete processing.
