---
name: split-payment-request-exact-share
description: Requests payments from multiple recipients, splitting a document-derived amount into exact, potentially fractional, shares, and using a verbatim description.
---
## Overview
This pattern addresses tasks that involve gathering recipient information from one source, extracting a total amount from another, calculating a per-recipient share, and then iterating to perform a transactional action for each recipient. It often requires combining data from multiple prior steps before the final action.
## When to Apply
- Make requests to multiple entities (e.g., roommates, friends, team members).
- Share an amount equally or proportionally among a group.
- Use a specific, verbatim note or description for all requests.
- Recipient information is stored in a contact list or directory.
- The total amount to be shared is found within a file or document in a file system.
## Procedure
1. Identify and accumulate all target recipients from a contact source, extracting a unique identifier (e.g., email) for each.
2. Search a file system for a specific document based on criteria (e.g., date, substring).
3. Read the content of the identified document.
4. Parse a specific numerical value (the total amount) from the document's content.
5. Calculate the per-recipient share by dividing the total amount by the number of recipients (plus one if the user is also included in the split).
6. For each identified recipient, call a transactional API using their unique identifier, the calculated per-recipient share, and the specified verbatim description.
## Key Patterns
- **Pagination Loop:** When searching for multiple entities, repeatedly call the search API with an incrementing page index until an empty list of results is returned, accumulating all results across pages.
- **Dynamic Date Filtering:** To find documents from a relative period (e.g., 'last month'), dynamically compute the relevant date string (e.g., 'YYYY-MM') and use it to filter file paths.
- **Content Parsing by Marker:** Extract a specific value from file content by splitting the string on a known literal marker, then parsing the relevant segment and converting its type.
- **Implicit Self-Inclusion in Calculation:** When a task specifies sharing 'among X and me', ensure the divisor for the equal split includes the current user (number of recipients + 1).
- **Iterative Transactional Call:** After identifying all recipients and calculating the amount, loop through each recipient and make an individual API call for the transactional action.
- **Verbatim String Pass-through:** If the instruction provides an exact string for an API parameter (e.g., a description), use that string literally without modification.
## Common Pitfalls
- Failing to paginate contact searches, leading to an incomplete list of recipients.
- Incorrectly calculating relative dates (e.g., 'last month') or failing to use them for filtering.
- Errors in parsing the numerical value from file content due to unexpected format or missing markers.
- Off-by-one errors in calculating the per-recipient share, such as forgetting to include the user in the divisor when specified.
- Not iterating through all identified recipients to perform the transactional action.
- Modifying the verbatim description string provided in the instruction.
