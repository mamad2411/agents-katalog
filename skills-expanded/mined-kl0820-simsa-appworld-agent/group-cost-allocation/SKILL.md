---
name: group-cost-allocation
description: When a cost needs to be distributed among a defined group, and requests or notifications are to be sent to each member.
---
## Overview
This skill addresses tasks where a single expense needs to be shared among a specific set of individuals. It involves identifying the total cost, determining the participants, calculating individual shares, and then performing an action (e.g., sending a request) to each participant.
## When to Apply
- An expense needs to be shared among multiple parties.
- The total amount of the expense is available from a specific source.
- The individuals involved in the sharing need to be identified from a contact or identity source.
- An action (e.g., sending a request, notification, or payment) needs to be performed for each individual based on their share.
## Procedure
1. Identify and extract the total amount of the expense from its designated source.
2. Identify and retrieve the list of target individuals who will share the expense from their respective source.
3. Calculate the individual share for each target individual, ensuring all participants (including the agent if applicable) are accounted for in the divisor.
4. For each identified target individual, perform the specified action using their calculated share and any required fixed details.
## Key Patterns
- **Source-of-Truth Extraction:** A critical value (e.g., total amount) is extracted from its primary source before any calculations or actions that depend on it.
- **Group Resolution Before Action:** The specific individuals who are part of the target group are identified and resolved from a contact or identity source before any actions are performed on them.
- **Inclusive Participant Count:** When calculating individual shares, the total number of participants (including the agent if they are part of the sharing) is correctly accounted for in the divisor to ensure accurate distribution.
- **Iterative Action on Group:** The same action is performed for each member of a previously resolved group, using a common calculated value and any fixed parameters.
## Common Pitfalls
- Not correctly identifying all participants in the share calculation, leading to incorrect individual amounts.
- Attempting to perform actions before all necessary data (e.g., total amount, recipient list) has been fully acquired and processed.
- Failing to resolve group members from their source before attempting to act on them, resulting in actions targeting incorrect or non-existent entities.
- Incorrectly applying fixed descriptions or messages, or failing to include them when required by the action.
