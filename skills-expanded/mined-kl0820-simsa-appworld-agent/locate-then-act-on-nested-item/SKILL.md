---
name: locate-then-act-on-nested-item
description: Applies when an action needs to be performed on a specific item nested within a container identified by a unique attribute.
---
## Overview
Many applications organize data hierarchically, where an action targets a specific sub-element. To perform such an action, the system must first locate the parent container using its identifying attribute, then access its contents to find the target sub-element, and finally execute the desired operation.
## When to Apply
- An action is specified for an item.
- The item is described as being "in" or "within" a named container.
- The container is identified by a unique attribute (e.g., title, name).
## Procedure
1. Locate the target container using its unique identifier.
2. Read the contents of the located container to find the specific item.
3. Perform the specified action on the identified item within the container.
## Key Patterns
- **Read-before-Write Dependency:** The action (write) on the nested item is dependent on successfully reading and locating both the container and the item itself.
- **Hierarchical Targeting:** The target of the action is not a top-level entity but an element nested within another identified entity.
- **Identifier Resolution:** The container is resolved by a human-readable identifier (e.g., title) before its internal ID or content can be accessed.
## Common Pitfalls
- Attempting to act on the item without first locating its parent container.
- Failing to read the container's contents to find the specific item before attempting the action.
- Assuming the item can be directly addressed without resolving its container.
- Not preserving the exact text or state of the item when updating.
