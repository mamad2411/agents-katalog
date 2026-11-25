---
name: multi-recipient-shared-cost-request
description: This skill applies when a cost needs to be shared among multiple recipients, requiring individual requests or payments.
---
## Overview
This pattern addresses tasks involving a shared cost among multiple entities, where the total amount must be retrieved, the individual share calculated, and then an specific action (like a request or payment) initiated for each relevant entity. It prioritizes gathering all necessary data and performing calculations before executing any external actions.
## When to Apply
- A total amount needs to be retrieved from a source.
- The total amount must be divided among multiple parties.
- An action (e.g., request, payment) needs to be performed for each party.
- Specific identifiers or contact details are required for each target party.
- A specific note or description must accompany the action.
## Procedure
1. Identify and retrieve the primary value or total amount from its specified source, applying any temporal or filtering constraints.
2. Identify and retrieve the list of target entities and their necessary contact information or identifiers from their respective sources.
3. Calculate the individual share for each target entity, based on the retrieved total amount, the count of all contributing parties (including the initiator if applicable), and any specified rounding rules.
4. Iterate through the identified target entities and perform the specified action for each, using their retrieved contact information, the calculated individual share, and any required descriptive text.
## Key Patterns
- **Pre-computation of Shares:** All parameters required for calculating individual shares (total amount, number of participants, rounding rules) are explicitly identified and computed *before* initiating any actions. This includes identifying the precise scope and count of all contributing parties, including the initiator if they are part of the shared cost.
- **Identity Resolution Before Action:** All target entities and their necessary identifiers (e.g., email, phone number, account ID) are resolved and gathered from their respective sources *before* any actions are initiated against them. This ensures the correct recipients are targeted with the appropriate contact method.
- **Data Dependency Ordering:** Milestones are strictly ordered such that all data required for a subsequent step (e.g., total amount for calculation, recipient details for action) is acquired in a preceding step. This prevents attempting operations with missing or incomplete information.
- **Constraint-Guided Data Retrieval:** Any constraints on the data (e.g., 'last month', 'specific type', 'exact match') are explicitly extracted from the instruction and applied during the initial data retrieval step to ensure accuracy and relevance of the primary value and target entities.
## Common Pitfalls
- Attempting to perform actions before all necessary data (total amount, recipient identities, calculation parameters) is fully gathered and validated.
- Incorrectly identifying the scope of participants for the share calculation (e.g., forgetting to include the initiator if they are part of the shared cost, or including entities not meant to receive a request).
- Failing to explicitly extract and apply specific constraints (e.g., temporal filters, exact descriptive text, required data formats) during data retrieval or action execution.
- Not explicitly extracting and applying rounding rules or other calculation specifics, leading to incorrect share amounts.
- Using an incorrect or incomplete identifier for the target entities when performing the action (e.g., using a display name instead of a required email or account ID for a payment request).
