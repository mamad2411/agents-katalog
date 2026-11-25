---
name: iterative-payment-request
description: This skill applies when a task requires making multiple similar payment requests to different recipients based on calculated amounts and a common description.
---
## Overview
This pattern addresses tasks that involve performing a transactional action for multiple entities, where the action's parameters (like amount) might need to be calculated from other data sources. It typically involves gathering recipient information, calculating individual amounts, and then iterating to perform the action for each recipient.
## When to Apply
- Make payment requests to multiple recipients.
- Share an amount equally among a group.
- Perform a transactional action for each item in a list.
- Use a specific description for all requests.
## Procedure
1. Retrieve the list of target entities (e.g., contacts, users) from their respective source, ensuring all relevant identifiers (e.g., email, ID) are collected.
2. If the source is paginated, implement a loop to fetch all pages and accumulate the complete list of entities.
3. De-duplicate the collected entities based on their unique identifier.
4. Retrieve the total amount from its designated source, which may involve parsing or extracting data from a file or external system.
5. Calculate the individual share amount by dividing the total amount by the number of target entities plus any additional participants (e.g., the current user).
6. Round or format the individual share amount as required for the transactional API.
7. Define the common description or message for the transaction.
8. Iterate through each unique target entity.
9. For each entity, call the transactional API using their identifier, the calculated individual amount, and the common description.
## Key Patterns
- **Pagination Loop:** Repeatedly call a list-fetching API with an incrementing offset or page index until an empty result indicates exhaustion, accumulating all results into a single collection.
- **Dynamic Date Filtering:** Programmatically construct a date string (e.g., for 'last month' or 'next week') to filter a list of items based on their names, timestamps, or metadata.
- **Multi-Source Data Aggregation:** Combine data points obtained from distinct API calls or data sources (e.g., recipient list from one API, amount from another) to form the complete input for a subsequent step.
- **Self-Inclusive Division:** When calculating an equal share for a group, ensure the initiator of the action is correctly included in the divisor if they are also part of the sharing group.
- **Iterative Transaction Execution:** Perform a state-changing API call repeatedly within a loop, once for each item in a pre-processed list of targets, using a common set of parameters and an item-specific identifier.
## Common Pitfalls
- Forgetting to handle pagination when retrieving lists of items, leading to incomplete data.
- Incorrectly parsing or extracting numerical data from unstructured text content.
- Off-by-one errors when calculating shares, especially when the initiator is part of the group.
- Not using the exact required string for descriptions or notes in transactional APIs.
- Failing to de-duplicate recipients if the source data might contain redundant entries.
- Not handling cases where no recipients are found or the total amount cannot be extracted.
