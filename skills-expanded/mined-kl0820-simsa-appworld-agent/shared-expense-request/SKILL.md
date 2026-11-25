---
name: shared-expense-request
description: Applies when a user needs to split a shared expense among multiple parties and request payment.
---
## Overview
This skill addresses tasks requiring the calculation of individual shares from a total amount, followed by performing an action for each participant. It involves gathering the total amount from one source, identifying participants from another, performing an intermediate calculation, and then iterating to execute an action for each participant.
## When to Apply
- Instructions mentioning splitting an amount 'equally among X and me'.
- Instructions requiring an action (e.g., 'make requests', 'send notifications') to multiple individuals.
- Instructions specifying that the total amount is found in a file or document.
- Instructions specifying that participants are found in a contact list or similar directory.
## Procedure
1. Identify and read a source file or document to extract a numeric total amount. This involves listing potential files, filtering them based on contextual criteria (e.g., date, keywords), reading the content of the selected file, and parsing the content to extract the numeric value. Store this as the 'total shared amount'.
2. Retrieve a list of participants from a contact or directory service. This involves calling an API to search for entities based on a relationship or other criteria, handling pagination to ensure all relevant entities are retrieved, and extracting identifying information (e.g., ID, name, contact details) for each participant. Store this as the 'participants list'.
3. Calculate the individual share for each participant. This involves retrieving the 'total shared amount' and the 'participants list' from previous steps, determining the total number of individuals involved in the split (participants + the user), and dividing the 'total shared amount' by this total count to get the 'individual share amount'. Store this calculated value.
4. Perform a specific action for each participant using their identifying information and the calculated individual share. This involves iterating through the 'participants list', and for each participant, calling an external service API (e.g., a payment request API) using their contact details and the 'individual share amount', along with any required descriptive notes. Collect and store the results of each action (e.g., request IDs) for confirmation.
## Key Patterns
- **Dynamic Data Extraction from File:** Identify a target file by listing and filtering based on contextual cues, then read its content and parse a specific numeric value using contextual labels or patterns within the text.
- **Paginated Entity Retrieval:** Retrieve a complete list of entities (e.g., contacts, items) from an API that supports pagination by repeatedly calling the API with incrementing page indices until no more results are returned, accumulating results across calls.
- **Intermediate Derived Value Calculation:** Perform arithmetic or logical operations on variables obtained from previous milestones to derive new values required for subsequent actions, without involving external API calls.
- **Iterative Action on a Collection:** Loop through a collection of entities obtained from a prior step, performing a standardized API call or action for each entity using its specific attributes and a common derived value.
- **Contextual Filtering for Entity Selection:** Select the correct data source or entity from multiple candidates by applying filtering logic based on contextual information (e.g., temporal criteria like 'last month', relational criteria like 'roommate', or keyword matching).
## Common Pitfalls
- Failing to correctly parse the numeric total amount from the file content, especially with varying formats or currency symbols.
- Not handling pagination when retrieving a list of entities, leading to an incomplete list of participants.
- Incorrectly calculating the total number of individuals for the split (e.g., forgetting to include the user themselves).
- Hardcoding values or API parameters instead of dynamically using variables from prior steps.
- Not using the most specific API parameters available (e.g., using a generic search instead of a dedicated 'relationship' filter for contacts).
