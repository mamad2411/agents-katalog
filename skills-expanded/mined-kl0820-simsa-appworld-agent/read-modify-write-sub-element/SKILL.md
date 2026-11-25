---
name: read-modify-write-sub-element
description: Modifies a specific sub-element within a larger entity, requiring retrieval of the parent, modification of the sub-element, and persistence of the updated parent while preserving other content.
---
## Overview
To precisely modify a specific sub-element within a larger entity, the agent must first locate the target entity using its identifier (e.g., name, title). Once identified, its current content must be retrieved to accurately pinpoint the sub-element. The requested modification is then applied to this specific sub-element, ensuring all other content of the entity remains unchanged. Finally, the updated parent entity is persisted. This process is crucial when direct sub-element modification APIs are not available or when atomicity of the entire entity's state is required.

## When to Apply
- Modify a specific item within a named document, note, or list.
- Update a sub-component or a particular entry of an existing record.
- Change the status or property of an element inside a container or named record.

## Procedure
1.  **Identify Target Entity:** Resolve the unique identifier (e.g., name, title, primary ID) of the parent entity that contains the sub-element to be modified.
2.  **Retrieve Entity Content:** Read and retrieve the full current content of the identified parent entity.
3.  **Locate and Modify Sub-Element:** Within the retrieved content, identify the specific sub-element that needs modification and apply the required change. Ensure that only the targeted sub-element is altered and all other parts of the entity's content are preserved.
4.  **Persist Updated Entity:** Update or write back the entire parent entity with the modified content.

## Key Patterns
-   **Read-Modify-Write Atomicity:** To precisely update a sub-element, the entire entity's content must often be read, the specific change applied, and then the entire entity written back. This ensures the integrity of the entity and prevents inadvertent alteration or loss of other data.
-   **Data Dependency Chaining:** The modification step is directly dependent on the output of the retrieval step, requiring the full content of the parent entity to be passed downstream for sub-element identification and modification.
-   **Identify by Identifier:** Before acting on an entity, its internal identifier (e.g., ID) must be resolved, often from a human-readable name or title.

## Common Pitfalls
-   Attempting to modify a sub-element without first reading the parent entity, leading to errors, partial updates, or data loss.
-   Failing to correctly identify the parent entity or resolve its unique identifier before attempting to locate the sub-element.
-   Overwriting the entire parent entity instead of just updating the specific sub-element, potentially losing other unrelated data.
-   Incorrectly identifying the specific sub-element within the parent's content.
-   Assuming a direct update API exists for sub-elements when only full entity updates are available, necessitating the Read-Modify-Write pattern.