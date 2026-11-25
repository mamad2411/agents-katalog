---
name: find-best-item-and-act
description: When the instruction requires identifying the best item within a collection based on a specific metric and then performing an action on it.
---
## Overview
This skill addresses tasks where an agent needs to navigate a hierarchy of resources, first identifying a specific collection, then iterating through its members to find one that meets a 'best' criterion (e.g., highest, lowest, most recent), and finally invoking an API to act upon that selected item. It often involves multiple API calls for discovery, detail retrieval, and the final action.
## When to Apply
- Play the most listened to song from my playlist.
- Find the largest file in a folder and delete it.
- Identify the oldest unread message in an inbox and mark it as read.
- Select the highest-rated product from a category and add it to cart.
## Procedure
1. Obtain any necessary authentication credentials.
2. List available collections, paginate if necessary, and filter to identify the target collection by a distinguishing attribute. Extract its unique identifier.
3. Retrieve the members of the target collection, paginating fully to ensure all members are considered.
4. For each member, determine the value of the relevant metric. This may involve direct extraction or calling a separate API for each member's details.
5. Compare the metric values across all members to identify the 'best' member according to the task's criterion. Extract its unique identifier and any required display attributes.
6. Perform the specified action on the identified 'best' member using its unique identifier.
7. Indicate that a side effect occurred by setting the output 'value' to 'null'.
## Key Patterns
- **Hierarchical Traversal:** Navigate from a high-level collection to its individual members, often requiring an identifier from the collection to retrieve its contents.
- **Metric Aggregation:** Collect a specific metric for multiple items, potentially requiring individual API calls for each item if the metric is not available in the initial list.
- **Best Item Selection:** Apply a comparison logic (e.g., maximum, minimum, most recent) across aggregated metrics to pick a single item that satisfies the 'best' criterion.
- **Side-Effect Action:** The final step is an API call that changes state in the external system, and the executor's 'value' field should be set to 'null' to reflect this.
## Common Pitfalls
- Not fully paginating when listing collections or their members, leading to an incomplete dataset for comparison.
- Failing to handle cases where the required metric is not directly available and needs a separate detail API call for each item.
- Incorrectly applying the 'best' criterion (e.g., finding minimum instead of maximum, or vice-versa).
- Forgetting to extract the unique identifier needed for subsequent API calls after filtering or selection.
- Not setting the 'value' field to 'null' for actions that primarily have side effects.
