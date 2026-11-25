---
name: split-payment-request-rounded-share
description: Requests payments from multiple recipients, splitting a document-derived amount, rounding each share to the nearest whole number, and using a verbatim description.
---
## Overview
This skill addresses tasks requiring the distribution of a shared cost among multiple individuals. It involves identifying the recipients, extracting a total amount from a specified source, calculating an equal share for each participant, and then initiating individual payment requests.
## When to Apply
- Request payments from multiple individuals.
- An amount needs to be split equally among a group.
- The total amount is found in a document or file.
- A specific description is required for each request.
## Procedure
1. Identify all relevant recipients from a contact directory using a specified relationship or query, ensuring all pages of results are processed.
2. Extract the necessary contact identifiers (e.g., email addresses) for each identified recipient.
3. Determine a time-based filter (e.g., 'last month') if the source document is time-sensitive.
4. Search a data store (e.g., file system) for a specific document using keywords and the derived time-based filter.
5. Read the content of the identified document.
6. Parse a specific numeric value (e.g., total amount) from the document content using a predefined textual marker.
7. Retrieve the list of recipients and the parsed total amount from prior steps.
8. Calculate the total number of participants by adding the current user to the count of identified recipients.
9. Compute each participant's equal share by dividing the total amount by the total number of participants, rounding the result to the nearest whole number.
10. Define the exact description string for the payment requests.
11. Iterate through each identified recipient.
12. For each recipient, initiate a payment request using their contact identifier, the calculated share, and the predefined description.
13. Accumulate the results of each payment request for auditing or confirmation.
## Key Patterns
- **Pagination Loop:** When retrieving a list of entities, always check for pagination and implement a loop to fetch all available pages until an empty result set is returned, ensuring comprehensive data collection.
- **Time-Based Document Filtering:** When a task specifies a time frame (e.g., 'last month'), dynamically calculate the corresponding time token (e.g., 'YYYY-MM') and use it as a substring filter during document search to precisely identify the correct file.
- **Marker-Based Data Extraction:** To extract a specific numeric value from a document's text content, identify a unique preceding textual marker, split the content based on this marker, and then parse the subsequent string into the required data type.
- **Self-Inclusion in Calculation:** When a task specifies sharing 'among X and me', ensure the count for division includes the current user in addition to the identified group members.
- **Verbatim String Usage:** If a task specifies an exact string for a field (e.g., a description), use that string precisely, including punctuation and casing, without any modification or dynamic generation.
- **Iterative Action Execution:** When an action needs to be performed for each item in a collection (e.g., sending requests to multiple recipients), iterate through the collection and execute the API call for each item, accumulating individual results.
- **Inter-Milestone Variable Passing:** Data generated in one milestone (e.g., a list of entities, a calculated value) must be explicitly stored and then retrieved by subsequent milestones to ensure a continuous data flow and avoid redundant operations.
## Common Pitfalls
- Failing to paginate when retrieving lists of entities, leading to incomplete data.
- Incorrectly deriving or applying time-based filters for document searches, resulting in the wrong document being processed.
- Using an incorrect or ambiguous textual marker for data extraction, leading to parsing errors or incorrect values.
- Forgetting to include the current user in the total count when calculating equal shares, leading to incorrect individual amounts.
- Not rounding the calculated share to the nearest whole number as specified, resulting in fractional amounts where integers are expected.
- Modifying the exact description string provided in the instruction, leading to non-compliance with task requirements.
- Failing to iterate through all identified recipients, resulting in incomplete execution of the required action.
- Not handling cases where no recipients are found or the total amount cannot be parsed, which can lead to downstream errors.
