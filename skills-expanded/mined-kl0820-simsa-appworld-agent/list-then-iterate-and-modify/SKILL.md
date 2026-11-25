---
name: list-then-iterate-and-modify
description: When a task requires processing a collection of items by first listing them and then performing a sequence of actions on each, potentially modifying or removing them.
---
## Overview
This strategy addresses tasks where a set of entities needs to be identified from a source, and then each identified entity requires a specific sequence of operations. It separates the discovery phase from the iterative action phase, ensuring all targets are known before any modifications begin.
## When to Apply
- Process a collection of items.
- Actions need to be performed for 'each' item.
- Items need to be identified or listed before processing.
- The processing involves multiple steps per item (e.g., transform and then delete).
## Procedure
1. Identify and list all target entities from a specified source location, extracting a unique identifier for each.
2. For each identified entity, perform a sequence of specified actions, utilizing its unique identifier for dynamic naming or targeting, and continue until all entities from the initial list have been processed.
## Key Patterns
- **Separate Listing from Action:** The initial step is dedicated solely to enumerating the items to be processed, ensuring a complete and stable list before any modifications occur.
- **Iterative Processing with Dynamic Naming:** Subsequent steps iterate over the pre-listed items, performing actions where output paths or identifiers are dynamically constructed using the unique identifier extracted during the listing phase.
- **Exhaustive Iteration with Deletion as Completion:** The iteration continues until all items from the initial list have been processed, often involving the deletion of the source item as the final step for each iteration, serving as a natural stopping condition for the loop.
## Common Pitfalls
- Attempting to modify items while still listing them, leading to incomplete or inconsistent lists.
- Failing to extract a consistent and unique identifier for each item, causing issues in subsequent dynamic operations.
- Not ensuring that all items from the initial list are processed, potentially leaving some untouched.
- Incorrectly constructing dynamic paths or names, leading to errors in saving or targeting.
